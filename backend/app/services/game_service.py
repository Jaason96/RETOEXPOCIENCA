from datetime import datetime, timezone

import sqlite3

from app.constants import MAX_PLAYERS, MIN_PLAYERS
from app.database import PLAYER_COLORS, get_connection
from app.models.game_status import GameStatus
from app.schemas.game import CreateGameRequest, GameDetailResponse
from app.services.game_question_service import GameQuestionError, snapshot_question_set_for_game
from app.services.game_runtime_service import build_game_detail


class GameNotFoundError(Exception):
    pass


class InvalidGameRequestError(Exception):
    pass


def _normalize_player_name(name: str) -> str:
    return name.strip()


def _validate_create_request(request: CreateGameRequest) -> None:
    player_count = len(request.players)

    if player_count < MIN_PLAYERS or player_count > MAX_PLAYERS:
        raise InvalidGameRequestError(
            f"La partida debe tener entre {MIN_PLAYERS} y {MAX_PLAYERS} jugadores"
        )

    numbers = sorted(player.number for player in request.players)
    expected_numbers = list(range(1, player_count + 1))

    if numbers != expected_numbers:
        raise InvalidGameRequestError(
            "Los números de jugador deben ser consecutivos desde 1 hasta la cantidad seleccionada"
        )

    for player in request.players:
        if player.number < 1 or player.number > MAX_PLAYERS:
            raise InvalidGameRequestError(
                f"Los números de jugador deben estar entre 1 y {MAX_PLAYERS}"
            )

        normalized_name = _normalize_player_name(player.name)
        if not normalized_name:
            raise InvalidGameRequestError("Todos los jugadores deben tener un nombre")
        if len(normalized_name) > 20:
            raise InvalidGameRequestError("Los nombres no pueden superar 20 caracteres")


def create_game(request: CreateGameRequest) -> GameDetailResponse:
    _validate_create_request(request)

    with get_connection() as connection:
        created_at = datetime.now(timezone.utc).isoformat()
        cursor = connection.execute(
            """
            INSERT INTO partidas (
                fecha_creacion, estado, pregunta_actual, finalizada,
                failed_player_ids
            ) VALUES (?, ?, ?, 0, '[]')
            """,
            (created_at, GameStatus.BUZZ_OPEN.value, 1),
        )
        game_id = int(cursor.lastrowid)

        for player in request.players:
            connection.execute(
                """
                INSERT INTO jugadores (
                    partida_id, numero_jugador, nombre, color, puntuacion, activo
                ) VALUES (?, ?, ?, ?, 0, 1)
                """,
                (
                    game_id,
                    player.number,
                    _normalize_player_name(player.name),
                    PLAYER_COLORS[player.number],
                ),
            )

        try:
            snapshot_question_set_for_game(connection, game_id, request.question_set_id)
        except GameQuestionError as error:
            connection.execute("DELETE FROM partidas WHERE id = ?", (game_id,))
            raise InvalidGameRequestError(str(error)) from error

        game = build_game_detail(connection, game_id)
        if game is None:
            raise GameNotFoundError("No se pudo crear la partida")
        return game


def fetch_game(game_id: int) -> GameDetailResponse:
    with get_connection() as connection:
        game = build_game_detail(connection, game_id)
        if game is None:
            raise GameNotFoundError("Partida no encontrada")
        return game
