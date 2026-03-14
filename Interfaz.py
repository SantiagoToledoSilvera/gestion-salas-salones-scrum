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

    tk.Label(frame, text="Responsable:").pack()
    ent_per = tk.Entry(frame)
    ent_per.pack()

    tk.Label(frame, text="Descripción:").pack()
    ent_des = tk.Entry(frame)
    ent_des.pack()

    btn = tk.Button(frame, text="Guardar Reserva", 
                    command=lambda: callback_guardar(ent_id.get(), ent_dia.get(), 
                                                   ent_ini.get(), ent_fin.get(), 
                                                   ent_per.get(), ent_des.get()))
    btn.pack(pady=10)