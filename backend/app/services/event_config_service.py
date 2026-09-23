import sqlite3

from app.schemas.event_config import EventConfigResponse, UpdateEventConfigRequest


class EventConfigNotFoundError(Exception):
    pass


class InvalidEventConfigError(Exception):
    pass


def _row_to_response(row: sqlite3.Row) -> EventConfigResponse:
    return EventConfigResponse(
        correct_answer_points=row["puntos_respuesta_correcta"],
        response_time_seconds=row["tiempo_respuesta_segundos"],
        player_1_key=row["jugador_1_tecla"],
        player_2_key=row["jugador_2_tecla"],
        player_3_key=row["jugador_3_tecla"],
        player_4_key=row["jugador_4_tecla"],
    )


def get_event_config(connection: sqlite3.Connection) -> EventConfigResponse:
    row = connection.execute(
        "SELECT * FROM configuracion_evento ORDER BY id ASC LIMIT 1"
    ).fetchone()
    if row is None:
        raise EventConfigNotFoundError("Configuración del evento no encontrada")
    return _row_to_response(row)


def update_event_config(
    connection: sqlite3.Connection,
    request: UpdateEventConfigRequest,
) -> EventConfigResponse:
    row = connection.execute(
        "SELECT id FROM configuracion_evento ORDER BY id ASC LIMIT 1"
    ).fetchone()
    if row is None:
        raise EventConfigNotFoundError("Configuración del evento no encontrada")

    connection.execute(
        """
        UPDATE configuracion_evento
        SET puntos_respuesta_correcta = ?,
            tiempo_respuesta_segundos = ?,
            jugador_1_tecla = ?,
            jugador_2_tecla = ?,
            jugador_3_tecla = ?,
            jugador_4_tecla = ?
        WHERE id = ?
        """,
        (
            request.correct_answer_points,
            request.response_time_seconds,
            request.player_1_key,
            request.player_2_key,
            request.player_3_key,
            request.player_4_key,
            row["id"],
        ),
    )
    return get_event_config(connection)
