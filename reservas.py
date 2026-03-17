# reservas.py (refactorizado completo)
import sqlite3
from models import Sala, Reserva
from data import DB_PATH


# ─── Validaciones ────────────────────────────────────────────────────────────
def sala_existe(id_sala: int) -> bool:
    with sqlite3.connect(DB_PATH) as conn:
        resultado = conn.execute("SELECT 1 FROM salas WHERE id = ?", (id_sala,)).fetchone()
        return resultado is not None


def horas_validas(hora_inicio: int, hora_fin: int) -> tuple[bool, str]:
    if not isinstance(hora_inicio, int) or not isinstance(hora_fin, int):
        return False, "Las horas deben ser números enteros."
    if hora_inicio < 0 or hora_inicio > 23:
        return False, "La hora de inicio debe estar entre 0 y 23."
    if hora_fin < 0 or hora_fin > 23:
        return False, "La hora de fin debe estar entre 0 y 23."
    if hora_inicio >= hora_fin:
        return False, "La hora de inicio debe ser menor que la hora de fin."
    return True, ""


# ─── Lógica principal (todo con SQLite) ──────────────────────────────────────
def verificar_conflicto(id_sala: int, dia: str, hora_inicio: int, hora_fin: int) -> bool:
    """Consulta SQL equivalente al algoritmo original de solapamiento."""
    with sqlite3.connect(DB_PATH) as conn:
        resultado = conn.execute("""
            SELECT 1 FROM reservas
            WHERE id_sala = ? AND dia = ?
              AND ? < h_fin AND ? > h_inicio
        """, (id_sala, dia, hora_inicio, hora_fin)).fetchone()
        return resultado is not None


def crear_reserva(
    id_sala: int,
    dia: str,
    hora_inicio: int,
    hora_fin: int,
    persona: str,
    descripcion: str,
) -> tuple[bool, str]:
    if not sala_existe(id_sala):
        return False, f"No existe una sala con ID {id_sala}."

    ok, msg = horas_validas(hora_inicio, hora_fin)
    if not ok:
        return False, msg

    if not persona.strip():
        return False, "El nombre de la persona no puede estar vacío."

    if verificar_conflicto(id_sala, dia, hora_inicio, hora_fin):
        return False, "Conflicto de horario: ya existe una reserva en ese rango."

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            INSERT INTO reservas (id_sala, dia, h_inicio, h_fin, persona, descripcion)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (id_sala, dia, hora_inicio, hora_fin, persona.strip(), descripcion.strip()))
        conn.commit()

    return True, "Reserva creada correctamente."


def reservas_por_dia(dia: str) -> list:
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute("""
            SELECT id_sala, dia, h_inicio, h_fin, persona, descripcion
            FROM reservas WHERE dia = ? ORDER BY h_inicio
        """, (dia,)).fetchall()
        return [Reserva(*row) for row in rows]


def reservas_por_sala(id_sala: int) -> list:
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute("""
            SELECT id_sala, dia, h_inicio, h_fin, persona, descripcion
            FROM reservas WHERE id_sala = ? ORDER BY dia, h_inicio
        """, (id_sala,)).fetchall()
        return [Reserva(*row) for row in rows]


def eliminar_reserva(reserva_id: int) -> tuple[bool, str]:
    """Ahora elimina por ID de la tabla (no por índice de lista)."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute("DELETE FROM reservas WHERE id = ?", (reserva_id,))
        if cursor.rowcount > 0:
            conn.commit()
            return True, "Reserva eliminada correctamente."
        return False, "ID de reserva inválido."


# ─── Helpers para UI (mantienen lógica y vistas intactas) ─────────────────────
def get_salas() -> list:
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute("SELECT id, nombre FROM salas ORDER BY id").fetchall()
        return [Sala(s_id, nombre) for s_id, nombre in rows]


def get_all_reservas() -> list:
    """Retorna [(id_db, Reserva), ...] para poder usar iid en Treeview + eliminación."""
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute("""
            SELECT id, id_sala, dia, h_inicio, h_fin, persona, descripcion
            FROM reservas ORDER BY dia, h_inicio
        """).fetchall()
        return [(row[0], Reserva(row[1], row[2], row[3], row[4], row[5], row[6])) for row in rows]