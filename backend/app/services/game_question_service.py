import sqlite3

from app.schemas.question import QuestionOptionResponse, QuestionResponse
from app.services import question_service
from app.services.question_set_service import (
    QuestionSetNotFoundError,
    get_active_questions_for_set,
)


class GameQuestionError(Exception):
    pass


def _snapshot_row_to_question(row: sqlite3.Row) -> QuestionResponse:
    return QuestionResponse(
        id=row["id"],
        text=row["texto"],
        options=[
            QuestionOptionResponse(letter="A", text=row["opcion_a"]),
            QuestionOptionResponse(letter="B", text=row["opcion_b"]),
            QuestionOptionResponse(letter="C", text=row["opcion_c"]),
            QuestionOptionResponse(letter="D", text=row["opcion_d"]),
        ],
        correct_answer=row["respuesta_correcta"],
        explanation=row["explicacion"],
        order=row["question_order"],
        active=True,
    )


def game_has_question_snapshots(connection: sqlite3.Connection, game_id: int) -> bool:
    row = connection.execute(
        "SELECT 1 FROM partida_preguntas WHERE partida_id = ? LIMIT 1",
        (game_id,),
    ).fetchone()
    return row is not None


def snapshot_question_set_for_game(
    connection: sqlite3.Connection,
    game_id: int,
    question_set_id: int,
) -> int:
    try:
        set_row = connection.execute(
            "SELECT id, nombre FROM listas_preguntas WHERE id = ?",
            (question_set_id,),
        ).fetchone()
        if set_row is None:
            raise QuestionSetNotFoundError("Lista de preguntas no encontrada")

        active_rows = get_active_questions_for_set(connection, question_set_id)
        if not active_rows:
            raise GameQuestionError(
                "La lista seleccionada no contiene preguntas activas."
            )

        connection.executemany(
            """
            INSERT INTO partida_preguntas (
                partida_id,
                question_order,
                pregunta_id,
                texto,
                opcion_a,
                opcion_b,
                opcion_c,
                opcion_d,
                respuesta_correcta,
                explicacion
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    game_id,
                    index,
                    row["id"],
                    row["texto"],
                    row["opcion_a"],
                    row["opcion_b"],
                    row["opcion_c"],
                    row["opcion_d"],
                    row["respuesta_correcta"],
                    row["explicacion"],
                )
                for index, row in enumerate(active_rows, start=1)
            ],
        )

        connection.execute(
            """
            UPDATE partidas
            SET lista_preguntas_id = ?, lista_preguntas_nombre = ?
            WHERE id = ?
            """,
            (question_set_id, set_row["nombre"], game_id),
        )
        return len(active_rows)
    except QuestionSetNotFoundError as error:
        raise GameQuestionError(str(error)) from error


def count_game_questions(connection: sqlite3.Connection, game_id: int) -> int:
    if game_has_question_snapshots(connection, game_id):
        result = connection.execute(
            "SELECT COUNT(*) FROM partida_preguntas WHERE partida_id = ?",
            (game_id,),
        ).fetchone()
        return int(result[0])

    return question_service.count_active_questions(connection)


def get_game_question_by_order(
    connection: sqlite3.Connection,
    game_id: int,
    order: int,
) -> QuestionResponse | None:
    if game_has_question_snapshots(connection, game_id):
        row = connection.execute(
            """
            SELECT * FROM partida_preguntas
            WHERE partida_id = ? AND question_order = ?
            """,
            (game_id, order),
        ).fetchone()
        if row is None:
            return None
        return _snapshot_row_to_question(row)

    return question_service.get_question_by_order(connection, order)
