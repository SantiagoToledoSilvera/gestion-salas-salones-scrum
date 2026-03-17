import sqlite3

DB_PATH = "nexus.db"


def init_db():
    """Crea las tablas salas y reservas + inserta las 3 salas iniciales si no existen."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS salas (
                id INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS reservas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_sala INTEGER NOT NULL,
                dia TEXT NOT NULL,
                h_inicio INTEGER NOT NULL,
                h_fin INTEGER NOT NULL,
                persona TEXT NOT NULL,
                descripcion TEXT,
                FOREIGN KEY (id_sala) REFERENCES salas(id)
            )
        """)

        # Salas iniciales (INSERT OR IGNORE para no duplicar)
        salas_iniciales = [(1, "Sala A"), (2, "Sala B"), (3, "Sala C")]
        for s_id, nombre in salas_iniciales:
            conn.execute(
                "INSERT OR IGNORE INTO salas (id, nombre) VALUES (?, ?)",
                (s_id, nombre)
            )
        conn.commit()
