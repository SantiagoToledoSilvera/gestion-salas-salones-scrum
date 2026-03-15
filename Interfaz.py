import tkinter as tk
from tkinter import messagebox, ttk

# Colores para que combine con el main.py
COLOR_FONDO = "#2A2A3E"
COLOR_TEXTO = "#E2E8F0"
COLOR_ACENTO = "#7C6AF7"

def mostrar_salas(tree, lista_salas):
    """Tarea: Refrescar la tabla de salas"""
    for item in tree.get_children():
        tree.delete(item)

    for s in lista_salas:
        tree.insert("", "end", values=(s.id_sala, s.nombre))

def formulario_reserva(parent, callback_guardar):
    """Tarea: Crear el formulario visual"""
    frame = tk.LabelFrame(parent, text=" Nueva Reserva ", bg=COLOR_FONDO, fg=COLOR_ACENTO, padx=10, pady=10)
    frame.pack(pady=10, padx=10, fill="x")

    # Campos de entrada con estilo
    tk.Label(frame, text="ID Sala:", bg=COLOR_FONDO, fg=COLOR_TEXTO).pack()
    ent_id = tk.Entry(frame)
    ent_id.pack(fill="x", padx=5)

    tk.Label(frame, text="Día (YYYY-MM-DD):", bg=COLOR_FONDO, fg=COLOR_TEXTO).pack()
    ent_dia = tk.Entry(frame)
    ent_dia.pack(fill="x", padx=5)

    tk.Label(frame, text="Hora Inicio:", bg=COLOR_FONDO, fg=COLOR_TEXTO).pack()
    ent_ini = tk.Entry(frame)
    ent_ini.pack(fill="x", padx=5)

    tk.Label(frame, text="Hora Fin:", bg=COLOR_FONDO, fg=COLOR_TEXTO).pack()
    ent_fin = tk.Entry(frame)
    ent_fin.pack(fill="x", padx=5)

    tk.Label(frame, text="Responsable:", bg=COLOR_FONDO, fg=COLOR_TEXTO).pack()
    ent_per = tk.Entry(frame)
    ent_per.pack(fill="x", padx=5)

    tk.Label(frame, text="Descripción:", bg=COLOR_FONDO, fg=COLOR_TEXTO).pack()
    ent_des = tk.Entry(frame)
    ent_des.pack(fill="x", padx=5)

    btn = tk.Button(frame, text="Guardar Reserva", bg=COLOR_ACENTO, fg="white",
                    command=lambda: callback_guardar(ent_id.get(), ent_dia.get(), 
                                                   ent_ini.get(), ent_fin.get(), 
                                                   ent_per.get(), ent_des.get()))
    btn.pack(pady=10)

def mostrar_reservas_dia(tree, lista_reservas):
    """Tarea: Mostrar reservas filtradas (Corregido)"""
    for item in tree.get_children():
        tree.delete(item)

    # CORRECCIÓN: Ahora itera sobre lista_reservas, no sobre salas
    for r in lista_reservas:
        tree.insert("", "end", values=(f"{r.hora_inicio:02d}:00", f"{r.hora_fin:02d}:00", r.id_sala, r.persona))

def mostrar_error(mensaje):
    """Tarea: Mensajes de error visuales"""
    messagebox.showerror("Error del Sistema", mensaje)