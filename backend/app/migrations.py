import sqlite3

from app.constants import DEFAULT_BUZZ_RESPONSE_TIME_SECONDS, DEFAULT_PLAYER_KEY_CODES


def _column_exists(connection: sqlite3.Connection, table: str, column: str) -> bool:
    columns = connection.execute(f"PRAGMA table_info({table})").fetchall()
    return any(row["name"] == column for row in columns)


def _table_exists(connection: sqlite3.Connection, table: str) -> bool:
    row = connection.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table' AND name = ?",
        (table,),
    ).fetchone()
    return row is not None


def _migrate_partidas_table(connection: sqlite3.Connection) -> None:
    if not _column_exists(connection, "partidas", "buzz_player_id"):
        connection.execute(
            "ALTER TABLE partidas ADD COLUMN buzz_player_id INTEGER NULL"
        )

    if not _column_exists(connection, "partidas", "failed_player_ids"):
        connection.execute(
            "ALTER TABLE partidas ADD COLUMN failed_player_ids TEXT NOT NULL DEFAULT '[]'"
        )

    if not _column_exists(connection, "partidas", "last_selected_answer"):
        connection.execute(
            "ALTER TABLE partidas ADD COLUMN last_selected_answer TEXT NULL"
        )

    if not _column_exists(connection, "partidas", "lista_preguntas_id"):
        connection.execute(
            "ALTER TABLE partidas ADD COLUMN lista_preguntas_id INTEGER NULL"
        )

    if not _column_exists(connection, "partidas", "lista_preguntas_nombre"):
        connection.execute(
            "ALTER TABLE partidas ADD COLUMN lista_preguntas_nombre TEXT NULL"
        )

    if not _column_exists(connection, "partidas", "buzz_deadline"):
        connection.execute(
            "ALTER TABLE partidas ADD COLUMN buzz_deadline TEXT NULL"
        )


def _migrate_partida_preguntas_table(connection: sqlite3.Connection) -> None:
    if _table_exists(connection, "partida_preguntas"):
        return

    connection.execute(
        """
        CREATE TABLE partida_preguntas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            partida_id INTEGER NOT NULL,
            question_order INTEGER NOT NULL,
            pregunta_id INTEGER NULL,
            texto TEXT NOT NULL,
            opcion_a TEXT NOT NULL,
            opcion_b TEXT NOT NULL,
            opcion_c TEXT NOT NULL,
            opcion_d TEXT NOT NULL,
            respuesta_correcta TEXT NOT NULL CHECK (respuesta_correcta IN ('A', 'B', 'C', 'D')),
            explicacion TEXT NOT NULL DEFAULT '',
            FOREIGN KEY (partida_id) REFERENCES partidas(id) ON DELETE CASCADE,
            UNIQUE (partida_id, question_order)
        )
        """
    )


def _migrate_question_sets_table(connection: sqlite3.Connection) -> None:
    if not _table_exists(connection, "listas_preguntas"):
        connection.execute(
            """
            CREATE TABLE listas_preguntas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT NOT NULL DEFAULT '',
                activa INTEGER NOT NULL DEFAULT 1,
                fecha_creacion TEXT NOT NULL
            )
            """
        )

    if not _table_exists(connection, "lista_preguntas_items"):
        connection.execute(
            """
            CREATE TABLE lista_preguntas_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lista_id INTEGER NOT NULL,
                pregunta_id INTEGER NOT NULL,
                question_order INTEGER NOT NULL,
                FOREIGN KEY (lista_id) REFERENCES listas_preguntas(id) ON DELETE CASCADE,
                FOREIGN KEY (pregunta_id) REFERENCES preguntas(id) ON DELETE CASCADE,
                UNIQUE (lista_id, pregunta_id),
                UNIQUE (lista_id, question_order)
            )
            """
        )


def _migrate_event_config_table(connection: sqlite3.Connection) -> None:
    if not _table_exists(connection, "configuracion_evento"):
        connection.execute(
            """
            CREATE TABLE configuracion_evento (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_evento TEXT NOT NULL,
                institucion TEXT NOT NULL,
                puntos_respuesta_correcta INTEGER NOT NULL
            )
            """
        )


def _migrate_event_config_response_time(connection: sqlite3.Connection) -> None:
    if not _table_exists(connection, "configuracion_evento"):
        return

    if not _column_exists(connection, "configuracion_evento", "tiempo_respuesta_segundos"):
        connection.execute(
            """
            ALTER TABLE configuracion_evento
            ADD COLUMN tiempo_respuesta_segundos INTEGER NOT NULL DEFAULT 7
            """
        )


def _migrate_event_config_player_keys(connection: sqlite3.Connection) -> None:
    if not _table_exists(connection, "configuracion_evento"):
        return

    for player_number, default_key_code in DEFAULT_PLAYER_KEY_CODES.items():
        column = f"jugador_{player_number}_tecla"
        if not _column_exists(connection, "configuracion_evento", column):
            connection.execute(
                f"""
                ALTER TABLE configuracion_evento
                ADD COLUMN {column} TEXT NOT NULL DEFAULT '{default_key_code}'
                """
            )


def _migrate_event_config_cleanup(connection: sqlite3.Connection) -> None:
    if not _table_exists(connection, "configuracion_evento"):
        return

    if not _column_exists(connection, "configuracion_evento", "tiempo_respuesta"):
        return

    connection.execute(
        """
        CREATE TABLE configuracion_evento_new (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_evento TEXT NOT NULL,
            institucion TEXT NOT NULL,
            puntos_respuesta_correcta INTEGER NOT NULL
        )
        """
    )
    connection.execute(
        """
        INSERT INTO configuracion_evento_new (
            id, nombre_evento, institucion, puntos_respuesta_correcta
        )
        SELECT id, nombre_evento, institucion, puntos_respuesta_correcta
        FROM configuracion_evento
        """
    )
    connection.execute("DROP TABLE configuracion_evento")
    connection.execute(
        "ALTER TABLE configuracion_evento_new RENAME TO configuracion_evento"
    )


def _seed_event_config(connection: sqlite3.Connection) -> None:
    existing = connection.execute("SELECT COUNT(*) FROM configuracion_evento").fetchone()[0]
    if existing > 0:
        return

    connection.execute(
        """
        INSERT INTO configuracion_evento (
            nombre_evento,
            institucion,
            puntos_respuesta_correcta,
            tiempo_respuesta_segundos,
            jugador_1_tecla,
            jugador_2_tecla,
            jugador_3_tecla,
            jugador_4_tecla
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            "Expoproyecto 2026",
            "Colegio La Nueva Esperanza",
            1000,
            DEFAULT_BUZZ_RESPONSE_TIME_SECONDS,
            DEFAULT_PLAYER_KEY_CODES[1],
            DEFAULT_PLAYER_KEY_CODES[2],
            DEFAULT_PLAYER_KEY_CODES[3],
            DEFAULT_PLAYER_KEY_CODES[4],
        ),
    )


def _seed_default_question_set(connection: sqlite3.Connection) -> None:
    from app.seed_data.cartagena_water_bank import seed_question_sets_if_missing

    seed_question_sets_if_missing(connection)


def run_migrations(connection: sqlite3.Connection) -> None:
    _migrate_partidas_table(connection)
    _migrate_partida_preguntas_table(connection)
    _migrate_question_sets_table(connection)
    _migrate_event_config_table(connection)
    _migrate_event_config_cleanup(connection)
    _migrate_event_config_response_time(connection)
    _migrate_event_config_player_keys(connection)
    _seed_default_question_set(connection)
    _seed_event_config(connection)
