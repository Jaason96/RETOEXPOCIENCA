import sqlite3
from datetime import datetime, timezone

from app.schemas.question_set import (
    CreateQuestionSetRequest,
    QuestionSetDetailResponse,
    QuestionSetItemResponse,
    QuestionSetSummary,
    UpdateQuestionSetRequest,
)


class QuestionSetNotFoundError(Exception):
    pass


class InvalidQuestionSetError(Exception):
    pass


def _get_set_row(connection: sqlite3.Connection, question_set_id: int) -> sqlite3.Row:
    row = connection.execute(
        "SELECT * FROM listas_preguntas WHERE id = ?",
        (question_set_id,),
    ).fetchone()
    if row is None:
        raise QuestionSetNotFoundError("Lista de preguntas no encontrada")
    return row


def _count_set_items(connection: sqlite3.Connection, question_set_id: int) -> tuple[int, int]:
    rows = connection.execute(
        """
        SELECT p.activa
        FROM lista_preguntas_items lpi
        JOIN preguntas p ON p.id = lpi.pregunta_id
        WHERE lpi.lista_id = ?
        """,
        (question_set_id,),
    ).fetchall()
    total_count = len(rows)
    active_count = sum(1 for row in rows if row["activa"])
    return total_count, active_count


def _build_set_summary(connection: sqlite3.Connection, row: sqlite3.Row) -> QuestionSetSummary:
    total_count, active_count = _count_set_items(connection, row["id"])
    return QuestionSetSummary(
        id=row["id"],
        name=row["nombre"],
        description=row["descripcion"],
        active=bool(row["activa"]),
        created_at=row["fecha_creacion"],
        question_count=total_count,
        active_question_count=active_count,
    )


def _get_set_items(connection: sqlite3.Connection, question_set_id: int) -> list[QuestionSetItemResponse]:
    rows = connection.execute(
        """
        SELECT lpi.id, lpi.pregunta_id, lpi.question_order, p.texto, p.activa
        FROM lista_preguntas_items lpi
        JOIN preguntas p ON p.id = lpi.pregunta_id
        WHERE lpi.lista_id = ?
        ORDER BY lpi.question_order ASC
        """,
        (question_set_id,),
    ).fetchall()
    return [
        QuestionSetItemResponse(
            id=row["id"],
            question_id=row["pregunta_id"],
            question_order=row["question_order"],
            text=row["texto"],
            active=bool(row["activa"]),
        )
        for row in rows
    ]


def _validate_question_ids(connection: sqlite3.Connection, question_ids: list[int]) -> None:
    for question_id in question_ids:
        row = connection.execute(
            "SELECT id, activa FROM preguntas WHERE id = ?",
            (question_id,),
        ).fetchone()
        if row is None:
            raise InvalidQuestionSetError(f"La pregunta {question_id} no existe")
        if not row["activa"]:
            raise InvalidQuestionSetError(
                "Solo se pueden agregar preguntas activas del banco a una lista nueva"
            )


def _replace_set_items(
    connection: sqlite3.Connection,
    question_set_id: int,
    question_ids: list[int],
) -> None:
    connection.execute(
        "DELETE FROM lista_preguntas_items WHERE lista_id = ?",
        (question_set_id,),
    )
    connection.executemany(
        """
        INSERT INTO lista_preguntas_items (lista_id, pregunta_id, question_order)
        VALUES (?, ?, ?)
        """,
        [(question_set_id, question_id, index) for index, question_id in enumerate(question_ids, start=1)],
    )


def get_all_question_sets(connection: sqlite3.Connection) -> list[QuestionSetSummary]:
    rows = connection.execute(
        "SELECT * FROM listas_preguntas ORDER BY id ASC"
    ).fetchall()
    return [_build_set_summary(connection, row) for row in rows]


def get_question_set_detail(
    connection: sqlite3.Connection,
    question_set_id: int,
) -> QuestionSetDetailResponse:
    row = _get_set_row(connection, question_set_id)
    summary = _build_set_summary(connection, row)
    return QuestionSetDetailResponse(
        **summary.model_dump(),
        items=_get_set_items(connection, question_set_id),
    )


def create_question_set(
    connection: sqlite3.Connection,
    request: CreateQuestionSetRequest,
) -> QuestionSetDetailResponse:
    _validate_question_ids(connection, request.question_ids)

    created_at = datetime.now(timezone.utc).isoformat()
    cursor = connection.execute(
        """
        INSERT INTO listas_preguntas (nombre, descripcion, activa, fecha_creacion)
        VALUES (?, ?, 1, ?)
        """,
        (request.name, request.description, created_at),
    )
    question_set_id = int(cursor.lastrowid)
    _replace_set_items(connection, question_set_id, request.question_ids)
    return get_question_set_detail(connection, question_set_id)


def update_question_set(
    connection: sqlite3.Connection,
    question_set_id: int,
    request: UpdateQuestionSetRequest,
) -> QuestionSetDetailResponse:
    _get_set_row(connection, question_set_id)
    updates = request.model_dump(exclude_unset=True)

    if "name" in updates:
        connection.execute(
            "UPDATE listas_preguntas SET nombre = ? WHERE id = ?",
            (updates["name"], question_set_id),
        )

    if "description" in updates:
        connection.execute(
            "UPDATE listas_preguntas SET descripcion = ? WHERE id = ?",
            (updates["description"], question_set_id),
        )

    if "question_ids" in updates and updates["question_ids"] is not None:
        question_ids = updates["question_ids"]
        existing_items = _get_set_items(connection, question_set_id)
        existing_ids = {item.question_id for item in existing_items}
        new_ids = set(question_ids) - existing_ids

        for question_id in new_ids:
            row = connection.execute(
                "SELECT id, activa FROM preguntas WHERE id = ?",
                (question_id,),
            ).fetchone()
            if row is None:
                raise InvalidQuestionSetError(f"La pregunta {question_id} no existe")
            if not row["activa"]:
                raise InvalidQuestionSetError(
                    "No se pueden agregar preguntas inactivas a la lista"
                )

        _replace_set_items(connection, question_set_id, question_ids)

    return get_question_set_detail(connection, question_set_id)


def duplicate_question_set(
    connection: sqlite3.Connection,
    question_set_id: int,
) -> QuestionSetDetailResponse:
    source = get_question_set_detail(connection, question_set_id)
    created_at = datetime.now(timezone.utc).isoformat()
    cursor = connection.execute(
        """
        INSERT INTO listas_preguntas (nombre, descripcion, activa, fecha_creacion)
        VALUES (?, ?, 1, ?)
        """,
        (f"{source.name} (copia)", source.description, created_at),
    )
    new_set_id = int(cursor.lastrowid)
    question_ids = [item.question_id for item in source.items]
    _replace_set_items(connection, new_set_id, question_ids)
    return get_question_set_detail(connection, new_set_id)


def move_question_in_set(
    connection: sqlite3.Connection,
    question_set_id: int,
    question_id: int,
    direction: str,
) -> QuestionSetDetailResponse:
    _get_set_row(connection, question_set_id)
    items = _get_set_items(connection, question_set_id)
    current_item = next((item for item in items if item.question_id == question_id), None)
    if current_item is None:
        raise InvalidQuestionSetError("La pregunta no pertenece a esta lista")

    current_index = next(
        index for index, item in enumerate(items) if item.question_id == question_id
    )

    if direction == "up":
        if current_index == 0:
            raise InvalidQuestionSetError("La pregunta ya está en la primera posición")
        swap_index = current_index - 1
    else:
        if current_index >= len(items) - 1:
            raise InvalidQuestionSetError("La pregunta ya está en la última posición")
        swap_index = current_index + 1

    reordered_ids = [item.question_id for item in items]
    reordered_ids[current_index], reordered_ids[swap_index] = (
        reordered_ids[swap_index],
        reordered_ids[current_index],
    )
    _replace_set_items(connection, question_set_id, reordered_ids)
    return get_question_set_detail(connection, question_set_id)


def delete_question_set(connection: sqlite3.Connection, question_set_id: int) -> None:
    _get_set_row(connection, question_set_id)
    connection.execute("DELETE FROM listas_preguntas WHERE id = ?", (question_set_id,))


def get_active_questions_for_set(
    connection: sqlite3.Connection,
    question_set_id: int,
) -> list[sqlite3.Row]:
    _get_set_row(connection, question_set_id)
    rows = connection.execute(
        """
        SELECT p.*
        FROM lista_preguntas_items lpi
        JOIN preguntas p ON p.id = lpi.pregunta_id
        WHERE lpi.lista_id = ? AND p.activa = 1
        ORDER BY lpi.question_order ASC
        """,
        (question_set_id,),
    ).fetchall()
    return rows
