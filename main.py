import tkinter as tk
from tkinter import ttk, messagebox
from data import init_db                     
from reservas import crear_reserva, eliminar_reserva, get_salas, get_all_reservas  # ← ACTUALIZADO


# ─── CONFIGURACIÓN DE IDENTIDAD VISUAL ────────────────────────────────────────
CLR_BG         = "#0D0D12"
CLR_SURFACE    = "#161625"
CLR_ACCENT     = "#7C3AED"
CLR_ACCENT_H   = "#9D67EF"
CLR_DANGER     = "#EF4444"
CLR_TEXT       = "#F1F5F9"
CLR_TEXT_DIM   = "#94A3B8"

class NexusApp(tk.Tk):
    def __init__(self):
        super().__init__()
        init_db()                               # ← LLAMADA OBLIGATORIA AL INICIO
        self.title("Nexus Hub | Workspace Management")
        self.geometry("1100x850")
        self.configure(bg=CLR_BG)
        
        self._setup_styles()
        self._build_layout()
        self.show_view("dashboard")

    def _setup_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        
        style.configure("Treeview",
            background=CLR_SURFACE,
            foreground=CLR_TEXT,
            fieldbackground=CLR_SURFACE,
            rowheight=45,
            borderwidth=0,
            font=("Segoe UI", 10))
        
        style.configure("Treeview.Heading",
            background=CLR_BG,
            foreground=CLR_ACCENT,
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            padding=12)
        
        style.map("Treeview", background=[('selected', CLR_ACCENT)])

    def _build_layout(self):
        # Sidebar
        self.sidebar = tk.Frame(self, bg=CLR_BG, width=240)
        self.sidebar.pack(side="left", fill="y", padx=10, pady=20)
        
        tk.Label(self.sidebar, text="🚀 NEXUS", font=("Segoe UI", 22, "bold"), 
                 bg=CLR_BG, fg=CLR_ACCENT).pack(pady=(20, 40))

        self._nav_btn("📊  Panel", "dashboard")
        self._nav_btn("📅  Nueva Reserva", "registro")
        self._nav_btn("📋  Historial", "historial")

        self.view_port = tk.Frame(self, bg=CLR_BG)
        self.view_port.pack(side="right", fill="both", expand=True, padx=20, pady=20)

    def _nav_btn(self, text, view_name):
        btn = tk.Button(self.sidebar, text=f"  {text}", font=("Segoe UI", 11),
                        bg=CLR_BG, fg=CLR_TEXT_DIM, activebackground=CLR_SURFACE,
                        activeforeground=CLR_ACCENT, bd=0, cursor="hand2",
                        anchor="w", padx=20, pady=12,
                        command=lambda: self.show_view(view_name))
        btn.pack(fill="x", pady=2)

    def show_view(self, view_name):
        for widget in self.view_port.winfo_children():
            widget.destroy()
            
        if view_name == "dashboard": self._render_dashboard()
        elif view_name == "registro": self._render_registro()
        elif view_name == "historial": self._render_historial()

    # ─── VISTAS ───────────────────────────────────────────────────────────────

    def _render_dashboard(self):
        tk.Label(self.view_port, text="Resumen General", font=("Segoe UI", 20, "bold"), 
                 bg=CLR_BG, fg=CLR_TEXT).pack(anchor="w", pady=(0, 20))
        card = tk.Frame(self.view_port, bg=CLR_SURFACE, padx=30, pady=30)
        card.pack(fill="x")
        tk.Label(card, text=f"Reservas activas: {len(get_all_reservas())}",   # ← CAMBIO
                 font=("Segoe UI", 14), bg=CLR_SURFACE, fg=CLR_ACCENT).pack(anchor="w")

    def _render_registro(self):
        tk.Label(self.view_port, text="Registrar Espacio 📅", 
                 font=("Segoe UI", 20, "bold"), bg=CLR_BG, fg=CLR_TEXT).pack(anchor="w", pady=(0, 20))
        
        container = tk.Frame(self.view_port, bg=CLR_SURFACE, padx=40, pady=30)
        container.pack(fill="both", expand=True)

        # Campos
        tk.Label(container, text="SALA", bg=CLR_SURFACE, fg=CLR_TEXT_DIM, font=("Segoe UI", 9, "bold")).pack(anchor="w")
        self.cmb_sala = ttk.Combobox(container, 
                                     values=[f"{s.id_sala} - {s.nombre}" for s in get_salas()],  # ← CAMBIO
                                     state="readonly")
        self.cmb_sala.pack(fill="x", pady=(5, 15))
        self.cmb_sala.current(0)

        tk.Label(container, text="DÍA (AAAA-MM-DD)", bg=CLR_SURFACE, fg=CLR_TEXT_DIM, font=("Segoe UI", 9, "bold")).pack(anchor="w")
        self.ent_dia = self._custom_entry(container)
        self.ent_dia.pack(fill="x", pady=(5, 15))

        h_frame = tk.Frame(container, bg=CLR_SURFACE)
        h_frame.pack(fill="x", pady=10)
        
        tk.Label(h_frame, text="INICIO (H)", bg=CLR_SURFACE, fg=CLR_TEXT_DIM).grid(row=0, column=0, sticky="w")
        self.ent_ini = self._custom_entry(h_frame)
        self.ent_ini.grid(row=1, column=0, sticky="ew", padx=(0, 10))
        
        tk.Label(h_frame, text="FIN (H)", bg=CLR_SURFACE, fg=CLR_TEXT_DIM).grid(row=0, column=1, sticky="w")
        self.ent_fin = self._custom_entry(h_frame)
        self.ent_fin.grid(row=1, column=1, sticky="ew")
        h_frame.columnconfigure((0,1), weight=1)

        tk.Label(container, text="RESPONSABLE", bg=CLR_SURFACE, fg=CLR_TEXT_DIM, font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(10, 0))
        self.ent_per = self._custom_entry(container)
        self.ent_per.pack(fill="x", pady=(5, 15))

        tk.Label(container, text="DESCRIPCIÓN", bg=CLR_SURFACE, fg=CLR_TEXT_DIM, font=("Segoe UI", 9, "bold")).pack(anchor="w")
        self.ent_desc = self._custom_entry(container)
        self.ent_desc.pack(fill="x", pady=(5, 20))

        btn_save = tk.Button(container, text="CREAR RESERVA ✨", bg=CLR_ACCENT, fg="white",
                             font=("Segoe UI", 10, "bold"), bd=0, pady=15, cursor="hand2",
                             command=self._handle_crear)
        btn_save.pack(fill="x")

    def _render_historial(self):
        header = tk.Frame(self.view_port, bg=CLR_BG)
        header.pack(fill="x", pady=(0, 20))
        
        tk.Label(header, text="Historial de Reservas", font=("Segoe UI", 20, "bold"), 
                 bg=CLR_BG, fg=CLR_TEXT).pack(side="left")
        
        btn_del = tk.Button(header, text="🗑️ ELIMINAR SELECCIÓN", bg=CLR_DANGER, fg="white",
                            font=("Segoe UI", 9, "bold"), bd=0, padx=15, pady=8, cursor="hand2",
                            command=self._handle_eliminar)
        btn_del.pack(side="right")

        cols = ("Sala", "Día", "H. Inicio", "H. Fin", "Persona", "Descripción")
        self.tree = ttk.Treeview(self.view_port, columns=cols, show="headings", style="Treeview")
        for col in cols:
            self.tree.heading(col, text=col.upper())
            self.tree.column(col, anchor="center")
        self.tree.pack(fill="both", expand=True)
        self._refresh_table()

    # ─── LÓGICA ───────────────────────────────────────────────────────────────

    def _custom_entry(self, parent):
        return tk.Entry(parent, bg=CLR_BG, fg=CLR_TEXT, insertbackground=CLR_TEXT,
                        relief="flat", font=("Segoe UI", 11), highlightthickness=1,
                        highlightbackground="#2D2D3F", highlightcolor=CLR_ACCENT)

    def _handle_crear(self):
        try:
            id_sala = int(self.cmb_sala.get().split(" - ")[0])
            dia, h_ini, h_fin = self.ent_dia.get(), int(self.ent_ini.get()), int(self.ent_fin.get())
            persona, desc = self.ent_per.get(), self.ent_desc.get()
            
            ok, msg = crear_reserva(id_sala, dia, h_ini, h_fin, persona, desc)
            if ok:
                messagebox.showinfo("Nexus", msg)
                self.show_view("historial")
            else:
                messagebox.showerror("Error", msg)
        except ValueError:
            messagebox.showerror("Error", "Revisa que las horas sean números válidos.")


    def _handle_eliminar(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Atención", "Por favor, selecciona una reserva de la lista.")
            return
            
        reserva_id = int(selected[0])                            # ← ID real de la BD (iid)
        confirm = messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar esta reserva?")
        
        if confirm:
            ok, msg = eliminar_reserva(reserva_id)               # ← ahora recibe ID
            if ok:
                messagebox.showinfo("Eliminado", msg)
                self._refresh_table()
            else:
                messagebox.showerror("Error", msg)
        index = self.tree.index(selected[0])
        confirm = messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar esta reserva?")
        
        if confirm:
            ok, msg = eliminar_reserva(index)
            if ok:
                messagebox.showinfo("Eliminado", msg)
                self._refresh_table()
            else:
                messagebox.showerror("Error", msg)

    def _refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for res_id, r in get_all_reservas():                     # ← NUEVO
            self.tree.insert("", "end", iid=str(res_id),          # ← iid = ID de BD
                             values=(r.id_sala, r.dia, r.hora_inicio, r.hora_fin, r.persona, r.descripcion))

if __name__ == "__main__":
    NexusApp().mainloop()

