from datetime import datetime, timezone

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.schemas.game import AnswerResultResponse, GameDetailResponse
from app.services.buzz_timer_service import buzz_timer_service
from app.services.game_runtime_service import (
    GameNotFoundError,
    InvalidGameActionError,
    expire_buzz_timeout,
    finish_game,
    get_game_detail,
    lock_buzzers,
    next_question,
    register_buzz,
    reset_buzzers,
    submit_answer,
)
from app.services.websocket_manager import connection_manager

router = APIRouter(tags=["websocket"])


def _seconds_until_deadline(buzz_deadline: str | None) -> float:
    """Duration to wait before a buzz times out, derived from the server-computed deadline.

    The deadline already encodes the configured response time (game_runtime_service
    reads it from event config when the buzz is registered), so the timer service
    only needs to know how long is left until that instant — it never reads the
    configured seconds itself.
    """
    if buzz_deadline is None:
        return 0.0

    deadline = datetime.fromisoformat(buzz_deadline)
    remaining = (deadline - datetime.now(timezone.utc)).total_seconds()
    return max(0.0, remaining)


async def _send_game_state(game_id: int, game: GameDetailResponse) -> None:
    await connection_manager.broadcast(
        game_id,
        {
            "type": "game_state",
            "payload": game.model_dump(mode="json"),
        },
    )


async def _broadcast_answer_result(
    game_id: int,
    game: GameDetailResponse,
    answer_result: AnswerResultResponse,
) -> None:
    await connection_manager.broadcast(
        game_id,
        {
            "type": "answer_result",
            "payload": answer_result.model_dump(mode="json"),
        },
    )
    await _send_game_state(game_id, game)


async def _handle_buzz_timeout(game_id: int, buzz_player_id: int) -> None:
    """Callback invoked by BuzzTimerService when a player's answer window expires.

    Runs outside any single connection's request loop, so it must broadcast
    on its own instead of relying on the per-message handling below.
    """
    result = expire_buzz_timeout(game_id, buzz_player_id)
    if result is None:
        return

    game, answer_result = result
    await _broadcast_answer_result(game_id, game, answer_result)


@router.websocket("/ws/games/{game_id}")
async def game_websocket(websocket: WebSocket, game_id: int) -> None:
    try:
        initial_game = get_game_detail(game_id)
    except GameNotFoundError:
        await websocket.close(code=4404)
        return

    await connection_manager.connect(game_id, websocket)

    try:
        await websocket.send_json(
            {
                "type": "game_state",
                "payload": initial_game.model_dump(mode="json"),
            }
        )

        while True:
            message = await websocket.receive_json()
            action = message.get("action")

            try:
                if action == "lock_buzzers":
                    game = lock_buzzers(game_id)
                    await _send_game_state(game_id, game)

                elif action == "reset_buzzers":
                    buzz_timer_service.cancel(game_id)
                    game = reset_buzzers(game_id)
                    await _send_game_state(game_id, game)

                elif action == "register_buzz":
                    player_number = int(message.get("player_number", 0))
                    game, buzz_player = register_buzz(game_id, player_number)
                    if buzz_player is not None:
                        await connection_manager.broadcast(
                            game_id,
                            {
                                "type": "buzz_registered",
                                "payload": {
                                    "player_id": buzz_player.id,
                                    "player_number": buzz_player.player_number,
                                    "player_name": buzz_player.name,
                                },
                            },
                        )
                        buzz_timer_service.schedule_timeout(
                            game_id,
                            buzz_player.id,
                            _seconds_until_deadline(game.buzz_deadline),
                            _handle_buzz_timeout,
                        )
                    await _send_game_state(game_id, game)

                elif action == "submit_answer":
                    buzz_timer_service.cancel(game_id)
                    selected_answer = str(message.get("answer", "")).upper()
                    game, answer_result = submit_answer(game_id, selected_answer)
                    await _broadcast_answer_result(game_id, game, answer_result)

                elif action == "next_question":
                    buzz_timer_service.cancel(game_id)
                    game = next_question(game_id)
                    await connection_manager.broadcast(
                        game_id,
                        {
                            "type": "question_changed",
                            "payload": {
                                "current_question_index": game.current_question_index,
                            },
                        },
                    )
                    await _send_game_state(game_id, game)

                elif action == "finish_game":
                    buzz_timer_service.cancel(game_id)
                    game = finish_game(game_id)
                    await connection_manager.broadcast(
                        game_id,
                        {
                            "type": "game_finished",
                            "payload": {"game_id": game.id},
                        },
                    )
                    await _send_game_state(game_id, game)

            except InvalidGameActionError as error:
                await websocket.send_json(
                    {
                        "type": "error",
                        "payload": {"message": str(error)},
                    }
                )
            except GameNotFoundError as error:
                await websocket.send_json(
                    {
                        "type": "error",
                        "payload": {"message": str(error)},
                    }
                )

    except WebSocketDisconnect:
        connection_manager.disconnect(game_id, websocket)
