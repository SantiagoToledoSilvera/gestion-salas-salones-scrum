class Sala:

    def __init__(self, id_sala, nombre):
        self.id_sala = id_sala
        self.nombre = nombre


class Reserva:

    def __init__(self, id_sala, dia, hora_inicio, hora_fin, persona, descripcion):

        self.id_sala = id_sala
        self.dia = dia
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.persona = persona
        self.descripcion = descripcion