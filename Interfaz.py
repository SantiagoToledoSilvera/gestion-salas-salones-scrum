def mostrar_salas(lista_salas):

    print("\n--- Lista de salas ---")

    for s in lista_salas:

        print("ID:", s.id_sala, "| Nombre:", s.nombre)

def pedir_datos_reserva():

    try:

        print("\n--- Datos de la reserva ---")

        id_sala = int(input("ID sala: "))
        dia = input("Día: ")
        hora_inicio = int(input("Hora inicio: "))
        hora_fin = int(input("Hora fin: "))
        persona = input("Nombre: ")
        descripcion = input("Descripción: ")

        return id_sala, dia, hora_inicio, hora_fin, persona, descripcion

    except ValueError:

        print("❌ Error: Los datos de ID y horas deben ser números")
        
        return None
    
def mostrar_reservas(lista_reservas, dia):

    print("\n--- Reservas del día", dia, "---")

    if not lista_reservas:

        print("No hay reservas para este día")

    for r in lista_reservas:

        print(r.persona, "| Sala:", r.id_sala, "| Horario:", r.hora_inicio, "-", r.hora_fin)