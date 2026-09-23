import json
import sqlite3
from datetime import datetime, timedelta, timezone

from app.database import get_connection
from app.models.game_status import GameStatus
from app.schemas.game import (
    AnswerFailureReason,
    AnswerResultResponse,
    BuzzPlayerResponse,
    GameDetailResponse,
    PlayerResponse,
)
from app.schemas.question import QuestionOptionResponse, QuestionResponse
from app.services import event_config_service, game_question_service


class GameNotFoundError(Exception):
    pass


class InvalidGameActionError(Exception):
    pass


def _get_correct_answer_points(connection: sqlite3.Connection) -> int:
    return event_config_service.get_event_config(connection).correct_answer_points


def _get_response_time_seconds(connection: sqlite3.Connection) -> int:
    return event_config_service.get_event_config(connection).response_time_seconds


def _parse_failed_player_ids(raw_value: str | None) -> list[int]:
    if not raw_value:
        return []
    try:
        parsed = json.loads(raw_value)
        return [int(player_id) for player_id in parsed]
    except (TypeError, ValueError, json.JSONDecodeError):
        return []


def _serialize_failed_player_ids(player_ids: list[int]) -> str:
    return json.dumps(sorted(set(player_ids)))


def _compute_buzz_deadline(response_time_seconds: int) -> str:
    deadline = datetime.now(timezone.utc) + timedelta(seconds=response_time_seconds)
    return deadline.isoformat()


def _row_to_player(row: sqlite3.Row) -> PlayerResponse:
    return PlayerResponse(
        id=row["id"],
        player_number=row["numero_jugador"],
        name=row["nombre"],
        color=row["color"],
        score=row["puntuacion"],
        active=bool(row["activo"]),
    )


def _get_buzz_player(connection: sqlite3.Connection, buzz_player_id: int | None) -> BuzzPlayerResponse | None:
    if buzz_player_id is None:
        return None

    row = connection.execute(
        "SELECT id, numero_jugador, nombre FROM jugadores WHERE id = ?",
        (buzz_player_id,),
    ).fetchone()

    if row is None:
        return None

    return BuzzPlayerResponse(
        id=row["id"],
        player_number=row["numero_jugador"],
        name=row["nombre"],
    )


def _build_last_answer_result(
    connection: sqlite3.Connection,
    game_row: sqlite3.Row,
    reveal_correct_answer: bool,
) -> AnswerResultResponse | None:
    if game_row["estado"] != GameStatus.ANSWER_RESULT.value:
        return None

    correct_answer_points = _get_correct_answer_points(connection)

    current_question = game_question_service.get_game_question_by_order(
        connection,
        game_row["id"],
        game_row["pregunta_actual"],
    )
    if current_question is None:
        return None

    correct_option = next(
        option for option in current_question.options
        if option.letter == current_question.correct_answer
    )

    if game_row["last_selected_answer"] is None:
        return AnswerResultResponse(
            player_id=0,
            player_name="",
            selected_answer="",
            is_correct=False,
            points_awarded=0,
            correct_answer=current_question.correct_answer,
            correct_answer_text=correct_option.text,
            explanation=current_question.explanation,
        )

    buzz_player = _get_buzz_player(connection, game_row["buzz_player_id"])
    if buzz_player is None:
        return None

    selected_answer = game_row["last_selected_answer"]
    is_correct = selected_answer == current_question.correct_answer

    return AnswerResultResponse(
        player_id=buzz_player.id,
        player_name=buzz_player.name,
        selected_answer=selected_answer,
        is_correct=is_correct,
        points_awarded=correct_answer_points if is_correct else 0,
        correct_answer=current_question.correct_answer,
        correct_answer_text=correct_option.text,
        explanation=current_question.explanation,
    )


def build_game_detail(connection: sqlite3.Connection, game_id: int) -> GameDetailResponse | None:
    game_row = connection.execute(
        "SELECT * FROM partidas WHERE id = ?",
        (game_id,),
    ).fetchone()

    if game_row is None:
        return None

    player_rows = connection.execute(
        """
        SELECT * FROM jugadores
        WHERE partida_id = ?
        ORDER BY numero_jugador ASC
        """,
        (game_id,),
    ).fetchall()

    total_questions = game_question_service.count_game_questions(connection, game_id)
    current_question = game_question_service.get_game_question_by_order(
        connection,
        game_id,
        game_row["pregunta_actual"],
    )
    failed_player_ids = _parse_failed_player_ids(game_row["failed_player_ids"])
    reveal_correct_answer = game_row["estado"] == GameStatus.ANSWER_RESULT.value
    buzz_player = _get_buzz_player(connection, game_row["buzz_player_id"])

    return GameDetailResponse(
        id=game_row["id"],
        created_at=game_row["fecha_creacion"],
        status=GameStatus(game_row["estado"]),
        current_question_index=game_row["pregunta_actual"],
        finished=bool(game_row["finalizada"]),
        total_questions=total_questions,
        players=[_row_to_player(row) for row in player_rows],
        current_question=current_question,
        buzz_player=buzz_player,
        buzz_deadline=game_row["buzz_deadline"],
        failed_player_ids=failed_player_ids,
        last_answer_result=_build_last_answer_result(
            connection,
            game_row,
            reveal_correct_answer,
        ),
        reveal_correct_answer=reveal_correct_answer,
    )


def get_game_detail(game_id: int) -> GameDetailResponse:
    with get_connection() as connection:
        game = build_game_detail(connection, game_id)
        if game is None:
            raise GameNotFoundError("Partida no encontrada")
        return game


def _get_player_by_number(
    connection: sqlite3.Connection,
    game_id: int,
    player_number: int,
) -> sqlite3.Row | None:
    return connection.execute(
        """
        SELECT * FROM jugadores
        WHERE partida_id = ? AND numero_jugador = ?
        """,
        (game_id, player_number),
    ).fetchone()


def _get_active_player_ids(connection: sqlite3.Connection, game_id: int) -> list[int]:
    rows = connection.execute(
        "SELECT id FROM jugadores WHERE partida_id = ? AND activo = 1",
        (game_id,),
    ).fetchall()
    return [row["id"] for row in rows]


def lock_buzzers(game_id: int) -> GameDetailResponse:
    with get_connection() as connection:
        game_row = connection.execute(
            "SELECT * FROM partidas WHERE id = ?",
            (game_id,),
        ).fetchone()

        if game_row is None:
            raise GameNotFoundError("Partida no encontrada")

        if GameStatus(game_row["estado"]) != GameStatus.BUZZ_OPEN:
            raise InvalidGameActionError("Solo se pueden bloquear pulsadores cuando están activos")

        connection.execute(
            "UPDATE partidas SET estado = ? WHERE id = ?",
            (GameStatus.BUZZ_LOCKED.value, game_id),
        )

        return build_game_detail(connection, game_id)  # type: ignore[return-value]


def reset_buzzers(game_id: int) -> GameDetailResponse:
    """Clear the current buzz and reopen buzzers without changing scores or failed players."""
    with get_connection() as connection:
        game_row = connection.execute(
            "SELECT * FROM partidas WHERE id = ?",
            (game_id,),
        ).fetchone()

        if game_row is None:
            raise GameNotFoundError("Partida no encontrada")

        if GameStatus(game_row["estado"]) != GameStatus.BUZZ_LOCKED:
            raise InvalidGameActionError("Solo se puede reiniciar el pulsador activo")

        connection.execute(
            """
            UPDATE partidas
            SET estado = ?, buzz_player_id = NULL, last_selected_answer = NULL,
                buzz_deadline = NULL
            WHERE id = ?
            """,
            (GameStatus.BUZZ_OPEN.value, game_id),
        )

        return build_game_detail(connection, game_id)  # type: ignore[return-value]


def _apply_failed_answer(
    connection: sqlite3.Connection,
    game_id: int,
    game_row: sqlite3.Row,
    buzz_player: BuzzPlayerResponse,
    current_question: QuestionResponse,
    correct_option: QuestionOptionResponse,
    selected_answer: str,
    reason: AnswerFailureReason,
) -> AnswerResultResponse:
    """Lock out the active player for this question and reopen or resolve the buzz.

    Shared by a moderator-submitted wrong answer and a server-side timeout,
    so both paths keep exactly the same lockout/reopen behaviour.
    """
    failed_player_ids = _parse_failed_player_ids(game_row["failed_player_ids"])
    failed_player_ids.append(buzz_player.id)
    active_player_ids = _get_active_player_ids(connection, game_id)
    remaining_players = [
        player_id for player_id in active_player_ids
        if player_id not in failed_player_ids
    ]

    next_status = GameStatus.BUZZ_OPEN if remaining_players else GameStatus.ANSWER_RESULT

    connection.execute(
        """
        UPDATE partidas
        SET estado = ?, buzz_player_id = NULL, last_selected_answer = NULL,
            buzz_deadline = NULL, failed_player_ids = ?
        WHERE id = ?
        """,
        (
            next_status.value,
            _serialize_failed_player_ids(failed_player_ids),
            game_id,
        ),
    )

    return AnswerResultResponse(
        player_id=buzz_player.id,
        player_name=buzz_player.name,
        selected_answer=selected_answer,
        is_correct=False,
        points_awarded=0,
        correct_answer=current_question.correct_answer if not remaining_players else None,
        correct_answer_text=correct_option.text if not remaining_players else None,
        explanation=current_question.explanation if not remaining_players else None,
        reason=reason,
    )


def register_buzz(game_id: int, player_number: int) -> tuple[GameDetailResponse, BuzzPlayerResponse | None]:
    with get_connection() as connection:
        connection.execute("BEGIN IMMEDIATE")

        game_row = connection.execute(
            "SELECT * FROM partidas WHERE id = ?",
            (game_id,),
        ).fetchone()

        if game_row is None:
            connection.execute("ROLLBACK")
            raise GameNotFoundError("Partida no encontrada")

        if GameStatus(game_row["estado"]) != GameStatus.BUZZ_OPEN:
            connection.execute("ROLLBACK")
            return build_game_detail(connection, game_id), None  # type: ignore[return-value]

        player_row = _get_player_by_number(connection, game_id, player_number)
        if player_row is None or not player_row["activo"]:
            connection.execute("ROLLBACK")
            return build_game_detail(connection, game_id), None  # type: ignore[return-value]

        failed_player_ids = _parse_failed_player_ids(game_row["failed_player_ids"])
        if player_row["id"] in failed_player_ids:
            connection.execute("ROLLBACK")
            return build_game_detail(connection, game_id), None  # type: ignore[return-value]

        if game_row["buzz_player_id"] is not None:
            connection.execute("ROLLBACK")
            return build_game_detail(connection, game_id), None  # type: ignore[return-value]

        response_time_seconds = _get_response_time_seconds(connection)

        connection.execute(
            """
            UPDATE partidas
            SET buzz_player_id = ?, estado = ?, buzz_deadline = ?
            WHERE id = ? AND buzz_player_id IS NULL
            """,
            (
                player_row["id"],
                GameStatus.BUZZ_LOCKED.value,
                _compute_buzz_deadline(response_time_seconds),
                game_id,
            ),
        )

        if connection.total_changes == 0:
            connection.execute("ROLLBACK")
            return build_game_detail(connection, game_id), None  # type: ignore[return-value]

        connection.execute("COMMIT")

        buzz_player = BuzzPlayerResponse(
            id=player_row["id"],
            player_number=player_row["numero_jugador"],
            name=player_row["nombre"],
        )
        return build_game_detail(connection, game_id), buzz_player  # type: ignore[return-value]


def submit_answer(game_id: int, selected_answer: str) -> tuple[GameDetailResponse, AnswerResultResponse]:
    selected_answer = selected_answer.upper()

    if selected_answer not in {"A", "B", "C", "D"}:
        raise InvalidGameActionError("La respuesta debe ser A, B, C o D")

    with get_connection() as connection:
        game_row = connection.execute(
            "SELECT * FROM partidas WHERE id = ?",
            (game_id,),
        ).fetchone()

        if game_row is None:
            raise GameNotFoundError("Partida no encontrada")

        if GameStatus(game_row["estado"]) != GameStatus.BUZZ_LOCKED:
            raise InvalidGameActionError("No hay un pulsador registrado para evaluar")

        if game_row["buzz_player_id"] is None:
            raise InvalidGameActionError("Ningún jugador ha pulsado todavía")

        buzz_player = _get_buzz_player(connection, game_row["buzz_player_id"])
        if buzz_player is None:
            raise InvalidGameActionError("Jugador no encontrado")

        current_question = game_question_service.get_game_question_by_order(
            connection,
            game_id,
            game_row["pregunta_actual"],
        )
        if current_question is None:
            raise InvalidGameActionError("No hay pregunta activa")

        is_correct = selected_answer == current_question.correct_answer
        correct_answer_points = _get_correct_answer_points(connection)
        correct_option = next(
            option for option in current_question.options
            if option.letter == current_question.correct_answer
        )

        if is_correct:
            connection.execute(
                """
                UPDATE jugadores
                SET puntuacion = puntuacion + ?
                WHERE id = ?
                """,
                (correct_answer_points, buzz_player.id),
            )
            connection.execute(
                """
                UPDATE partidas
                SET estado = ?, last_selected_answer = ?, buzz_deadline = NULL
                WHERE id = ?
                """,
                (GameStatus.ANSWER_RESULT.value, selected_answer, game_id),
            )
            answer_result = AnswerResultResponse(
                player_id=buzz_player.id,
                player_name=buzz_player.name,
                selected_answer=selected_answer,
                is_correct=True,
                points_awarded=correct_answer_points,
                correct_answer=current_question.correct_answer,
                correct_answer_text=correct_option.text,
                explanation=current_question.explanation,
            )
        else:
            answer_result = _apply_failed_answer(
                connection,
                game_id,
                game_row,
                buzz_player,
                current_question,
                correct_option,
                selected_answer,
                reason="INCORRECT",
            )

        return build_game_detail(connection, game_id), answer_result  # type: ignore[return-value]


def expire_buzz_timeout(
    game_id: int,
    expected_buzz_player_id: int,
) -> tuple[GameDetailResponse, AnswerResultResponse] | None:
    """Resolve a buzz that was not answered within the configured response time.

    Returns None when the buzz was already resolved by another action (a
    manual answer, a moderator reset, or a newer buzz) before the scheduled
    timeout fired — the caller should treat that as a no-op.
    """
    with get_connection() as connection:
        connection.execute("BEGIN IMMEDIATE")

        game_row = connection.execute(
            "SELECT * FROM partidas WHERE id = ?",
            (game_id,),
        ).fetchone()

        if (
            game_row is None
            or GameStatus(game_row["estado"]) != GameStatus.BUZZ_LOCKED
            or game_row["buzz_player_id"] != expected_buzz_player_id
        ):
            connection.execute("ROLLBACK")
            return None

        buzz_player = _get_buzz_player(connection, expected_buzz_player_id)
        current_question = game_question_service.get_game_question_by_order(
            connection,
            game_id,
            game_row["pregunta_actual"],
        )

        if buzz_player is None or current_question is None:
            connection.execute("ROLLBACK")
            return None

        correct_option = next(
            option for option in current_question.options
            if option.letter == current_question.correct_answer
        )

        answer_result = _apply_failed_answer(
            connection,
            game_id,
            game_row,
            buzz_player,
            current_question,
            correct_option,
            selected_answer="",
            reason="TIMEOUT",
        )

        connection.execute("COMMIT")

        return build_game_detail(connection, game_id), answer_result  # type: ignore[return-value]


def next_question(game_id: int) -> GameDetailResponse:
    with get_connection() as connection:
        game_row = connection.execute(
            "SELECT * FROM partidas WHERE id = ?",
            (game_id,),
        ).fetchone()

        if game_row is None:
            raise GameNotFoundError("Partida no encontrada")

        if GameStatus(game_row["estado"]) != GameStatus.ANSWER_RESULT:
            raise InvalidGameActionError("Solo se puede avanzar después de mostrar el resultado")

        total_questions = game_question_service.count_game_questions(connection, game_id)
        next_index = game_row["pregunta_actual"] + 1

        if next_index > total_questions:
            raise InvalidGameActionError("Ya no quedan más preguntas")

        connection.execute(
            """
            UPDATE partidas
            SET pregunta_actual = ?, estado = ?, buzz_player_id = NULL,
                failed_player_ids = '[]', last_selected_answer = NULL
            WHERE id = ?
            """,
            (next_index, GameStatus.BUZZ_OPEN.value, game_id),
        )

        return build_game_detail(connection, game_id)  # type: ignore[return-value]


def finish_game(game_id: int) -> GameDetailResponse:
    with get_connection() as connection:
        game_row = connection.execute(
            "SELECT * FROM partidas WHERE id = ?",
            (game_id,),
        ).fetchone()

        if game_row is None:
            raise GameNotFoundError("Partida no encontrada")

        connection.execute(
            """
            UPDATE partidas
            SET estado = ?, finalizada = 1
            WHERE id = ?
            """,
            (GameStatus.FINISHED.value, game_id),
        )

        return build_game_detail(connection, game_id)  # type: ignore[return-value]
