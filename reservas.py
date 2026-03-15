from models import Reserva
from data import reservas, salas


# ─── Validaciones ────────────────────────────────────────────────────────────

def sala_existe(id_sala: int) -> bool:
    return any(s.id_sala == id_sala for s in salas)


def horas_validas(hora_inicio: int, hora_fin: int) -> tuple[bool, str]:
    if not (0 <= hora_inicio <= 23 and 0 <= hora_fin <= 23):
        return False, "Las horas deben estar entre 0 y 23."
    if hora_inicio >= hora_fin:
        return False, "La hora de inicio debe ser menor que la hora de fin."
    return True, ""


# ─── Lógica principal ─────────────────────────────────────────────────────────

def verificar_conflicto(id_sala: int, dia: str, hora_inicio: int, hora_fin: int) -> bool:
    for r in reservas:
        if r.id_sala == id_sala and r.dia == dia:
            if not (hora_fin <= r.hora_inicio or hora_inicio >= r.hora_fin):
                return True
    return False


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

    nueva = Reserva(id_sala, dia, hora_inicio, hora_fin, persona.strip(), descripcion.strip())
    reservas.append(nueva)
    return True, "Reserva creada correctamente."


def reservas_por_dia(dia: str) -> list:
    return [r for r in reservas if r.dia == dia]


def reservas_por_sala(id_sala: int) -> list:
    return [r for r in reservas if r.id_sala == id_sala]


def eliminar_reserva(index: int) -> tuple[bool, str]:
    if 0 <= index < len(reservas):
        reservas.pop(index)
        return True, "Reserva eliminada correctamente."
    return False, "Índice de reserva inválido."
