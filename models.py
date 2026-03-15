class Sala:
    def __init__(self, id_sala, nombre):
        self.id_sala = id_sala
        self.nombre = nombre

    def __str__(self):
        return f"{self.nombre} (ID: {self.id_sala})"


class Reserva:
    def __init__(self, id_sala, dia, hora_inicio, hora_fin, persona, descripcion):
        self.id_sala = id_sala
        self.dia = dia
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.persona = persona
        self.descripcion = descripcion

    def __str__(self):
        return (
            f"Sala {self.id_sala} | {self.dia} | "
            f"{self.hora_inicio:02d}:00 - {self.hora_fin:02d}:00 | "
            f"{self.persona} | {self.descripcion}"
        )
