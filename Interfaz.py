import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


def mostrar_salas(tree, lista_salas):

    # Tarea: Mostrar lista de salas
    for item in tree.get_children():
        tree.delete(item)

    for s in lista_salas:
        tree.insert("", "end", values=(s.id_sala, s.nombre))
