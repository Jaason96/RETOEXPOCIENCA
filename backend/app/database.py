import sqlite3

from pathlib import Path



from app.seed_data.cartagena_water_bank import (

    PROJECT_QUESTIONS,

    needs_cartagena_water_bank_migration,

    needs_english_water_bank_migration,

    seed_cartagena_water_bank,

    seed_english_water_bank,

)



DATABASE_DIR = Path(__file__).resolve().parent.parent / "data"

DATABASE_PATH = DATABASE_DIR / "reto_cientifico.db"



PLAYER_COLORS = {

    1: "#018EE0",

    2: "#009256",

    3: "#E6A817",

    4: "#D94F4F",

}





def get_connection() -> sqlite3.Connection:

    DATABASE_DIR.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)

    connection.row_factory = sqlite3.Row

    connection.execute("PRAGMA foreign_keys = ON")

    return connection





def init_database() -> None:

    with get_connection() as connection:

        connection.executescript(

            """

            CREATE TABLE IF NOT EXISTS preguntas (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                texto TEXT NOT NULL,

                opcion_a TEXT NOT NULL,

                opcion_b TEXT NOT NULL,

                opcion_c TEXT NOT NULL,

                opcion_d TEXT NOT NULL,

                respuesta_correcta TEXT NOT NULL CHECK (respuesta_correcta IN ('A', 'B', 'C', 'D')),

                explicacion TEXT NOT NULL DEFAULT '',

                activa INTEGER NOT NULL DEFAULT 1,

                orden INTEGER NOT NULL

            );



            CREATE TABLE IF NOT EXISTS partidas (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                fecha_creacion TEXT NOT NULL,

                estado TEXT NOT NULL,

                pregunta_actual INTEGER NOT NULL DEFAULT 1,

                finalizada INTEGER NOT NULL DEFAULT 0

            );



            CREATE TABLE IF NOT EXISTS jugadores (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                partida_id INTEGER NOT NULL,

                numero_jugador INTEGER NOT NULL CHECK (numero_jugador BETWEEN 1 AND 4),

                nombre TEXT NOT NULL,

                color TEXT NOT NULL,

                puntuacion INTEGER NOT NULL DEFAULT 0,

                activo INTEGER NOT NULL DEFAULT 1,

                FOREIGN KEY (partida_id) REFERENCES partidas(id) ON DELETE CASCADE,

                UNIQUE (partida_id, numero_jugador)

            );

            """

        )

        _migrate_partidas_table(connection)

        _migrate_partida_preguntas_table(connection)

        _migrate_question_sets_table(connection)

        _migrate_event_config_table(connection)

        _migrate_event_config_cleanup(connection)

        _migrate_event_config_response_time(connection)

        _migrate_event_config_player_keys(connection)

        _migrate_cartagena_water_question_bank(connection)

        _migrate_english_water_bank(connection)

        _seed_questions_if_empty(connection)

        _seed_default_question_set(connection)

        _seed_event_config(connection)





def _migrate_partidas_table(connection: sqlite3.Connection) -> None:

    from app.migrations import _migrate_partidas_table as migrate



    migrate(connection)





def _migrate_partida_preguntas_table(connection: sqlite3.Connection) -> None:

    from app.migrations import _migrate_partida_preguntas_table as migrate



    migrate(connection)





def _migrate_question_sets_table(connection: sqlite3.Connection) -> None:

    from app.migrations import _migrate_question_sets_table as migrate



    migrate(connection)





def _seed_default_question_set(connection: sqlite3.Connection) -> None:

    from app.migrations import _seed_default_question_set as seed



    seed(connection)





def _migrate_event_config_table(connection: sqlite3.Connection) -> None:

    from app.migrations import _migrate_event_config_table as migrate



    migrate(connection)





def _migrate_event_config_cleanup(connection: sqlite3.Connection) -> None:

    from app.migrations import _migrate_event_config_cleanup as migrate



    migrate(connection)





def _migrate_event_config_response_time(connection: sqlite3.Connection) -> None:

    from app.migrations import _migrate_event_config_response_time as migrate



    migrate(connection)





def _migrate_event_config_player_keys(connection: sqlite3.Connection) -> None:

    from app.migrations import _migrate_event_config_player_keys as migrate



    migrate(connection)





def _seed_event_config(connection: sqlite3.Connection) -> None:

    from app.migrations import _seed_event_config as seed



    seed(connection)





def _migrate_cartagena_water_question_bank(connection: sqlite3.Connection) -> None:

    if not needs_cartagena_water_bank_migration(connection):

        return



    seed_cartagena_water_bank(connection, replace=True)





def _migrate_english_water_bank(connection: sqlite3.Connection) -> None:

    if not needs_english_water_bank_migration(connection):

        return



    seed_english_water_bank(connection)





def _seed_questions_if_empty(connection: sqlite3.Connection) -> None:

    count = connection.execute("SELECT COUNT(*) FROM preguntas").fetchone()[0]

    if count > 0:

        return



    connection.executemany(

        """

        INSERT INTO preguntas (

            texto, opcion_a, opcion_b, opcion_c, opcion_d,

            respuesta_correcta, explicacion, activa, orden

        ) VALUES (

            :texto, :opcion_a, :opcion_b, :opcion_c, :opcion_d,

            :respuesta_correcta, :explicacion, 1, :orden

        )

        """,

        PROJECT_QUESTIONS,

    )

