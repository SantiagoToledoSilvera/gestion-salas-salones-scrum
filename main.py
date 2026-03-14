from reservas import crear_reserva, reservas_por_dia
from data import reservas


def menu():

    while True:

        print("\nSistema de reservas")

        print("1 Crear reserva")
        print("2 Ver reservas por día")
        print("3 Salir")

        opcion = input("Seleccione opción: ")

        if opcion == "1":

            id_sala = int(input("ID sala: "))
            dia = input("Día: ")
            hora_inicio = int(input("Hora inicio: "))
            hora_fin = int(input("Hora fin: "))
            persona = input("Nombre: ")
            descripcion = input("Descripción: ")

            crear_reserva(id_sala, dia, hora_inicio, hora_fin, persona, descripcion)

        elif opcion == "2":

            dia = input("Ingrese día: ")

            lista = reservas_por_dia(dia)

            for r in lista:

                print(r.persona, r.id_sala, r.hora_inicio, "-", r.hora_fin)

        elif opcion == "3":

            break


menu()