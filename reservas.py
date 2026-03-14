from models import Reserva
from data import reservas


def verificar_conflicto(id_sala, dia, hora_inicio, hora_fin):

    for r in reservas:

        if r.id_sala == id_sala and r.dia == dia:

            if not (hora_fin <= r.hora_inicio or hora_inicio >= r.hora_fin):

                return True

    return False


def crear_reserva(id_sala, dia, hora_inicio, hora_fin, persona, descripcion):

    if verificar_conflicto(id_sala, dia, hora_inicio, hora_fin):

        print("❌ Conflicto de horario")
        return False

    nueva = Reserva(id_sala, dia, hora_inicio, hora_fin, persona, descripcion)

    reservas.append(nueva)

    print("✅ Reserva creada correctamente")

    return True


def reservas_por_dia(dia):

    resultado = []

    for r in reservas:

        if r.dia == dia:

            resultado.append(r)

    return resultado


def reservas_por_sala(id_sala):

    resultado = []

    for r in reservas:

        if r.id_sala == id_sala:

            resultado.append(r)

    return resultado