import sqlite3

from app.schemas.question import (
    CreateQuestionRequest,
    QuestionBankResponse,
    QuestionBankSummary,
    QuestionOptionResponse,
    QuestionPublicResponse,
    QuestionResponse,
    UpdateQuestionRequest,
)


class QuestionNotFoundError(Exception):
    pass


class InvalidQuestionError(Exception):
    pass


def _row_to_question_response(
    row: sqlite3.Row,
    include_answer: bool = True,
) -> QuestionResponse | QuestionPublicResponse:
    options = [
        QuestionOptionResponse(letter="A", text=row["opcion_a"]),
        QuestionOptionResponse(letter="B", text=row["opcion_b"]),
        QuestionOptionResponse(letter="C", text=row["opcion_c"]),
        QuestionOptionResponse(letter="D", text=row["opcion_d"]),
    ]

    if not include_answer:
        return QuestionPublicResponse(
            id=row["id"],
            text=row["texto"],
            options=options,
            order=row["orden"],
        )

    return QuestionResponse(
        id=row["id"],
        text=row["texto"],
        options=options,
        correct_answer=row["respuesta_correcta"],
        explanation=row["explicacion"],
        order=row["orden"],
        active=bool(row["activa"]),
    )


def _normalize_question_order(connection: sqlite3.Connection) -> None:
    rows = connection.execute(
        "SELECT id FROM preguntas ORDER BY orden ASC, id ASC"
    ).fetchall()
    for index, row in enumerate(rows, start=1):
        connection.execute(
            "UPDATE preguntas SET orden = ? WHERE id = ?",
            (index, row["id"]),
        )


def _get_question_row(connection: sqlite3.Connection, question_id: int) -> sqlite3.Row:
    row = connection.execute(
        "SELECT * FROM preguntas WHERE id = ?",
        (question_id,),
    ).fetchone()
    if row is None:
        raise QuestionNotFoundError("Pregunta no encontrada")
    return row


def get_active_questions(connection: sqlite3.Connection) -> list[QuestionResponse]:
    rows = connection.execute(
        """
        SELECT * FROM preguntas
        WHERE activa = 1
        ORDER BY orden ASC
        """
    ).fetchall()
    return [_row_to_question_response(row) for row in rows]  # type: ignore[misc]


def get_all_questions(connection: sqlite3.Connection) -> list[QuestionResponse]:
    rows = connection.execute(
        "SELECT * FROM preguntas ORDER BY orden ASC, id ASC"
    ).fetchall()
    return [_row_to_question_response(row) for row in rows]  # type: ignore[misc]


def get_question_bank(connection: sqlite3.Connection) -> QuestionBankResponse:
    questions = get_all_questions(connection)
    active_count = sum(1 for question in questions if question.active)
    return QuestionBankResponse(
        summary=QuestionBankSummary(
            active_count=active_count,
            total_count=len(questions),
        ),
        questions=questions,
    )


def count_active_questions(connection: sqlite3.Connection) -> int:
    result = connection.execute(
        "SELECT COUNT(*) FROM preguntas WHERE activa = 1"
    ).fetchone()
    return int(result[0])


def get_question_by_id(connection: sqlite3.Connection, question_id: int) -> QuestionResponse:
    row = _get_question_row(connection, question_id)
    return _row_to_question_response(row)  # type: ignore[return-value]


def get_question_by_order(connection: sqlite3.Connection, order: int) -> QuestionResponse | None:
    row = connection.execute(
        """
        SELECT * FROM preguntas
        WHERE activa = 1 AND orden = ?
        """,
        (order,),
    ).fetchone()
    if row is None:
        return None
    return _row_to_question_response(row)  # type: ignore[return-value]


def get_public_question_by_order(
    connection: sqlite3.Connection,
    order: int,
) -> QuestionPublicResponse | None:
    row = connection.execute(
        """
        SELECT * FROM preguntas
        WHERE activa = 1 AND orden = ?
        """,
        (order,),
    ).fetchone()
    if row is None:
        return None
    return _row_to_question_response(row, include_answer=False)  # type: ignore[return-value]


def create_question(
    connection: sqlite3.Connection,
    request: CreateQuestionRequest,
) -> QuestionResponse:
    max_order = connection.execute(
        "SELECT COALESCE(MAX(orden), 0) FROM preguntas"
    ).fetchone()[0]
    next_order = int(max_order) + 1

    cursor = connection.execute(
        """
        INSERT INTO preguntas (
            texto, opcion_a, opcion_b, opcion_c, opcion_d,
            respuesta_correcta, explicacion, activa, orden
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            request.text,
            request.option_a,
            request.option_b,
            request.option_c,
            request.option_d,
            request.correct_answer,
            request.explanation,
            1 if request.active else 0,
            next_order,
        ),
    )
    return get_question_by_id(connection, int(cursor.lastrowid))


def update_question(
    connection: sqlite3.Connection,
    question_id: int,
    request: UpdateQuestionRequest,
) -> QuestionResponse:
    current_row = _get_question_row(connection, question_id)
    updates = request.model_dump(exclude_unset=True)

    if not updates:
        return get_question_by_id(connection, question_id)

    field_map = {
        "text": "texto",
        "option_a": "opcion_a",
        "option_b": "opcion_b",
        "option_c": "opcion_c",
        "option_d": "opcion_d",
        "correct_answer": "respuesta_correcta",
        "explanation": "explicacion",
        "active": "activa",
    }

    set_clauses: list[str] = []
    values: list[object] = []

    for field_name, column_name in field_map.items():
        if field_name not in updates:
            continue
        value = updates[field_name]
        if field_name == "active":
            value = 1 if value else 0
        set_clauses.append(f"{column_name} = ?")
        values.append(value)

    values.append(question_id)
    connection.execute(
        f"UPDATE preguntas SET {', '.join(set_clauses)} WHERE id = ?",
        values,
    )
    return get_question_by_id(connection, question_id)


def duplicate_question(connection: sqlite3.Connection, question_id: int) -> QuestionResponse:
    source_row = _get_question_row(connection, question_id)
    insert_order = int(source_row["orden"]) + 1

    connection.execute(
        """
        UPDATE preguntas
        SET orden = orden + 1
        WHERE orden >= ?
        """,
        (insert_order,),
    )

    cursor = connection.execute(
        """
        INSERT INTO preguntas (
            texto, opcion_a, opcion_b, opcion_c, opcion_d,
            respuesta_correcta, explicacion, activa, orden
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            f"{source_row['texto']} (copia)",
            source_row["opcion_a"],
            source_row["opcion_b"],
            source_row["opcion_c"],
            source_row["opcion_d"],
            source_row["respuesta_correcta"],
            source_row["explicacion"],
            source_row["activa"],
            insert_order,
        ),
    )
    _normalize_question_order(connection)
    return get_question_by_id(connection, int(cursor.lastrowid))


def set_question_active(
    connection: sqlite3.Connection,
    question_id: int,
    active: bool,
) -> QuestionResponse:
    _get_question_row(connection, question_id)
    connection.execute(
        "UPDATE preguntas SET activa = ? WHERE id = ?",
        (1 if active else 0, question_id),
    )
    return get_question_by_id(connection, question_id)


def move_question(
    connection: sqlite3.Connection,
    question_id: int,
    direction: str,
) -> QuestionResponse:
    current_row = _get_question_row(connection, question_id)
    current_order = int(current_row["orden"])

    if direction == "up":
        if current_order <= 1:
            raise InvalidQuestionError("La pregunta ya está en la primera posición")
        neighbor = connection.execute(
            """
            SELECT id, orden FROM preguntas
            WHERE orden < ?
            ORDER BY orden DESC, id DESC
            LIMIT 1
            """,
            (current_order,),
        ).fetchone()
    else:
        neighbor = connection.execute(
            """
            SELECT id, orden FROM preguntas
            WHERE orden > ?
            ORDER BY orden ASC, id ASC
            LIMIT 1
            """,
            (current_order,),
        ).fetchone()
        if neighbor is None:
            raise InvalidQuestionError("La pregunta ya está en la última posición")

    if neighbor is None:
        raise InvalidQuestionError("No se puede mover la pregunta en esa dirección")

    connection.execute(
        "UPDATE preguntas SET orden = ? WHERE id = ?",
        (neighbor["orden"], question_id),
    )
    connection.execute(
        "UPDATE preguntas SET orden = ? WHERE id = ?",
        (current_order, neighbor["id"]),
    )
    _normalize_question_order(connection)
    return get_question_by_id(connection, question_id)


def delete_question(connection: sqlite3.Connection, question_id: int) -> None:
    _get_question_row(connection, question_id)
    connection.execute("DELETE FROM preguntas WHERE id = ?", (question_id,))
    _normalize_question_order(connection)
