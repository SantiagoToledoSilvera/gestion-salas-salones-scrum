def mostrar_salas(lista_salas):

    print("\n--- Lista de salas ---")

    for s in lista_salas:

        print("ID:", s.id_sala, "| Nombre:", s.nombre)

def formulario_reserva(parent, callback_guardar):

    # Tarea: Formulario para crear reserva
    frame = tk.LabelFrame(parent, text=" Nueva Reserva ")
    frame.pack(pady=10, padx=10, fill="x")

    tk.Label(frame, text="ID Sala:").pack()
    ent_id = tk.Entry(frame)
    ent_id.pack()

    tk.Label(frame, text="Día:").pack()
    ent_dia = tk.Entry(frame)
    ent_dia.pack()

    tk.Label(frame, text="Hora Inicio:").pack()
    ent_ini = tk.Entry(frame)
    ent_ini.pack()

    tk.Label(frame, text="Hora Fin:").pack()
    ent_fin = tk.Entry(frame)
    ent_fin.pack()

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
