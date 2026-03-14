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
    
def mostrar_reservas_dia(tree, lista_reservas):

    # Tarea: Mostrar reservas del día
    for item in tree.get_children():
        tree.delete(item)

    if not lista_reservas:
        messagebox.showinfo("Consulta", "No hay reservas para este día")

    for r in lista_reservas:
        tree.insert("", "end", values=(r.hora_inicio, r.hora_fin, r.id_sala, r.persona))

def mostrar_error(mensaje):

    # Tarea: Mostrar mensajes de error
    messagebox.showerror("Error del Sistema", mensaje)