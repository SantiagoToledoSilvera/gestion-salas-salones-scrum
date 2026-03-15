import tkinter as tk
from tkinter import ttk, messagebox
from data import salas, reservas

try:
    from tkcalendar import DateEntry
    HAVE_CAL = True
except ImportError:
    HAVE_CAL = False
from reservas import crear_reserva, reservas_por_dia, eliminar_reserva

# ─── Paleta de colores ────────────────────────────────────────────────────────
BG         = "#1E1E2E"   # fondo principal
SURFACE    = "#2A2A3E"   # tarjetas / frames
ACCENT     = "#7C6AF7"   # violeta principal
ACCENT2    = "#A78BFA"   # violeta claro (hover)
SUCCESS    = "#4ADE80"   # verde
DANGER     = "#F87171"   # rojo
TEXT       = "#E2E8F0"   # texto principal
SUBTEXT    = "#94A3B8"   # texto secundario
BORDER     = "#3B3B52"   # bordes
ENTRY_BG   = "#12121E"   # fondo de inputs
HEADER_BG  = "#7C6AF7"   # fondo cabecera tabla

FONT_TITLE  = ("Segoe UI", 22, "bold")
FONT_LABEL  = ("Segoe UI", 10)
FONT_BOLD   = ("Segoe UI", 10, "bold")
FONT_SMALL  = ("Segoe UI", 9)
FONT_HEADER = ("Segoe UI", 10, "bold")


# ─── Helpers ──────────────────────────────────────────────────────────────────

def solo_enteros(accion, valor_nuevo):
    """Validación de entry: sólo dígitos."""
    if accion == "1":
        return valor_nuevo.isdigit()
    return True


def make_entry(parent, **kwargs):
    return tk.Entry(
        parent,
        bg=ENTRY_BG, fg=TEXT, insertbackground=TEXT,
        relief="flat", bd=0,
        font=FONT_LABEL,
        highlightthickness=1,
        highlightbackground=BORDER,
        highlightcolor=ACCENT,
        **kwargs,
    )


def make_label(parent, text, **kwargs):
    return tk.Label(
        parent, text=text,
        bg=SURFACE, fg=SUBTEXT,
        font=FONT_LABEL,
        **kwargs,
    )


def make_btn(parent, text, command, color=ACCENT, hover=ACCENT2, width=18):
    btn = tk.Button(
        parent, text=text, command=command,
        bg=color, fg="white",
        activebackground=hover, activeforeground="white",
        relief="flat", bd=0,
        font=FONT_BOLD,
        cursor="hand2",
        padx=12, pady=8,
        width=width,
    )
    btn.bind("<Enter>", lambda e: btn.config(bg=hover))
    btn.bind("<Leave>", lambda e: btn.config(bg=color))
    return btn


def card(parent, **kwargs):
    return tk.Frame(parent, bg=SURFACE, relief="flat", bd=0, **kwargs)


# ─── Ventana principal ────────────────────────────────────────────────────────

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Reservas de Salas")
        self.geometry("950x680")
        self.configure(bg=BG)
        self.resizable(True, True)
        self._setup_styles()
        self._build_ui()

    # ── estilos ttk ───────────────────────────────────────────────────────────
    def _setup_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background=SURFACE,
            foreground=TEXT,
            fieldbackground=SURFACE,
            rowheight=32,
            font=FONT_SMALL,
            borderwidth=0,
        )
        style.configure(
            "Treeview.Heading",
            background=HEADER_BG,
            foreground="white",
            font=FONT_HEADER,
            relief="flat",
        )
        style.map("Treeview",
                  background=[("selected", ACCENT)],
                  foreground=[("selected", "white")])

        style.configure("TCombobox",
                        fieldbackground=ENTRY_BG,
                        background=ENTRY_BG,
                        foreground=TEXT,
                        arrowcolor=ACCENT)
        style.map("TCombobox",
                  fieldbackground=[("readonly", ENTRY_BG)],
                  selectbackground=[("readonly", ACCENT)])

        style.configure("TNotebook", background=BG, borderwidth=0)
        style.configure("TNotebook.Tab",
                        background=SURFACE,
                        foreground=SUBTEXT,
                        font=FONT_BOLD,
                        padding=[16, 8])
        style.map("TNotebook.Tab",
                  background=[("selected", ACCENT)],
                  foreground=[("selected", "white")])

    # ── layout general ────────────────────────────────────────────────────────
    def _build_ui(self):
        # Header
        header = tk.Frame(self, bg=ACCENT, height=64)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(
            header,
            text="🏢  Sistema de Reservas de Salas",
            bg=ACCENT, fg="white",
            font=FONT_TITLE,
        ).pack(side="left", padx=24)

        # Notebook / pestañas
        self.nb = ttk.Notebook(self)
        self.nb.pack(fill="both", expand=True, padx=16, pady=16)

        self._tab_nueva_reserva()
        self._tab_ver_reservas()

    # ── TAB 1: Nueva Reserva ──────────────────────────────────────────────────
    def _tab_nueva_reserva(self):
        frame = tk.Frame(self.nb, bg=BG)
        self.nb.add(frame, text="  ➕  Nueva Reserva  ")

        wrap = card(frame)
        wrap.pack(padx=40, pady=30, fill="both", expand=True)

        tk.Label(wrap, text="Crear nueva reserva",
                 bg=SURFACE, fg=TEXT, font=("Segoe UI", 14, "bold")).grid(
            row=0, column=0, columnspan=2, pady=(20, 16), padx=24, sticky="w")

        vcmd = (self.register(solo_enteros), "%d", "%P")

        # ── Sala ──────────────────────────────────────────────────────────────
        make_label(wrap, "Sala *").grid(row=1, column=0, sticky="w", padx=(24, 8), pady=6)
        self.cmb_sala = ttk.Combobox(
            wrap,
            values=[f"{s.id_sala} – {s.nombre}" for s in salas],
            state="readonly", width=30,
        )
        self.cmb_sala.grid(row=1, column=1, sticky="w", padx=(0, 24), pady=6)
        self.cmb_sala.current(0)

        # ── Día ───────────────────────────────────────────────────────────────
        make_label(wrap, "Día *").grid(row=2, column=0, sticky="w", padx=(24, 8), pady=6)
        if HAVE_CAL:
            self.ent_dia = DateEntry(
                wrap, width=28, background=ACCENT, foreground="white",
                borderwidth=0, date_pattern="yyyy-mm-dd",
                font=FONT_LABEL,
            )
        else:
            self.ent_dia = make_entry(wrap, width=30)
            self.ent_dia.insert(0, "YYYY-MM-DD")
        self.ent_dia.grid(row=2, column=1, sticky="w", padx=(0, 24), pady=6)

        # ── Horas ─────────────────────────────────────────────────────────────
        make_label(wrap, "Hora inicio (0-23) *").grid(row=3, column=0, sticky="w", padx=(24, 8), pady=6)
        self.ent_h_ini = make_entry(wrap, width=10, validate="key", validatecommand=vcmd)
        self.ent_h_ini.grid(row=3, column=1, sticky="w", padx=(0, 24), pady=6, ipady=4)

        make_label(wrap, "Hora fin (0-23) *").grid(row=4, column=0, sticky="w", padx=(24, 8), pady=6)
        self.ent_h_fin = make_entry(wrap, width=10, validate="key", validatecommand=vcmd)
        self.ent_h_fin.grid(row=4, column=1, sticky="w", padx=(0, 24), pady=6, ipady=4)

        # ── Persona ───────────────────────────────────────────────────────────
        make_label(wrap, "Nombre *").grid(row=5, column=0, sticky="w", padx=(24, 8), pady=6)
        self.ent_persona = make_entry(wrap, width=32)
        self.ent_persona.grid(row=5, column=1, sticky="w", padx=(0, 24), pady=6, ipady=4)

        # ── Descripción ───────────────────────────────────────────────────────
        make_label(wrap, "Descripción").grid(row=6, column=0, sticky="nw", padx=(24, 8), pady=6)
        self.ent_desc = tk.Text(
            wrap, width=32, height=3,
            bg=ENTRY_BG, fg=TEXT, insertbackground=TEXT,
            relief="flat", font=FONT_LABEL,
            highlightthickness=1,
            highlightbackground=BORDER,
            highlightcolor=ACCENT,
        )
        self.ent_desc.grid(row=6, column=1, sticky="w", padx=(0, 24), pady=6)

        # ── Botón ─────────────────────────────────────────────────────────────
        btn_frame = tk.Frame(wrap, bg=SURFACE)
        btn_frame.grid(row=7, column=0, columnspan=2, pady=(16, 24))
        make_btn(btn_frame, "✅  Crear Reserva", self._crear_reserva).pack(side="left", padx=8)
        make_btn(btn_frame, "🗑  Limpiar", self._limpiar_form,
                 color="#475569", hover="#64748B").pack(side="left", padx=8)

    # ── TAB 2: Ver Reservas ───────────────────────────────────────────────────
    def _tab_ver_reservas(self):
        frame = tk.Frame(self.nb, bg=BG)
        self.nb.add(frame, text="  📋  Ver Reservas  ")

        # Filtros
        filter_card = card(frame)
        filter_card.pack(fill="x", padx=40, pady=(20, 8))

        tk.Label(filter_card, text="Filtrar reservas",
                 bg=SURFACE, fg=TEXT, font=("Segoe UI", 13, "bold")).pack(
            anchor="w", padx=20, pady=(14, 6))

        row_f = tk.Frame(filter_card, bg=SURFACE)
        row_f.pack(fill="x", padx=20, pady=(0, 14))

        tk.Label(row_f, text="Día:", bg=SURFACE, fg=SUBTEXT, font=FONT_LABEL).pack(side="left")

        if HAVE_CAL:
            self.ent_filtro_dia = DateEntry(
                row_f, width=18, background=ACCENT, foreground="white",
                borderwidth=0, date_pattern="yyyy-mm-dd", font=FONT_LABEL,
            )
        else:
            self.ent_filtro_dia = make_entry(row_f, width=18)
            self.ent_filtro_dia.insert(0, "YYYY-MM-DD")
        self.ent_filtro_dia.pack(side="left", padx=8)

        make_btn(row_f, "🔍  Buscar", self._buscar_reservas, width=14).pack(side="left", padx=4)
        make_btn(row_f, "📋  Todas", self._ver_todas,
                 color="#475569", hover="#64748B", width=12).pack(side="left", padx=4)
        make_btn(row_f, "🗑  Eliminar sel.", self._eliminar_seleccionada,
                 color="#B91C1C", hover=DANGER, width=14).pack(side="right", padx=(0, 4))

        # Tabla
        table_frame = card(frame)
        table_frame.pack(fill="both", expand=True, padx=40, pady=(0, 20))

        cols = ("Sala", "Día", "Inicio", "Fin", "Persona", "Descripción")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", selectmode="browse")

        for col in cols:
            self.tree.heading(col, text=col)
        self.tree.column("Sala",       width=80,  anchor="center")
        self.tree.column("Día",        width=110, anchor="center")
        self.tree.column("Inicio",     width=70,  anchor="center")
        self.tree.column("Fin",        width=70,  anchor="center")
        self.tree.column("Persona",    width=150, anchor="w")
        self.tree.column("Descripción",width=280, anchor="w")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True, padx=2, pady=2)
        scrollbar.pack(side="right", fill="y", pady=2)

        # Contador
        self.lbl_count = tk.Label(
            frame, text="", bg=BG, fg=SUBTEXT, font=FONT_SMALL)
        self.lbl_count.pack(anchor="e", padx=44, pady=(0, 4))

    # ── Acciones ──────────────────────────────────────────────────────────────

    def _crear_reserva(self):
        # ── Sala ──────────────────────────────────────────────────────────────
        sel = self.cmb_sala.current()
        if sel < 0:
            messagebox.showerror("Error", "Selecciona una sala.", parent=self)
            return
        id_sala = salas[sel].id_sala

        # ── Día ───────────────────────────────────────────────────────────────
        try:
            dia = self.ent_dia.get_date().strftime("%Y-%m-%d")
        except AttributeError:
            dia = self.ent_dia.get().strip()
            if not dia or dia == "YYYY-MM-DD":
                messagebox.showerror("Error", "Ingresa un día válido.", parent=self)
                return

        # ── Horas ─────────────────────────────────────────────────────────────
        h_ini_str = self.ent_h_ini.get().strip()
        h_fin_str = self.ent_h_fin.get().strip()
        if not h_ini_str or not h_fin_str:
            messagebox.showerror("Error", "Las horas de inicio y fin son obligatorias.", parent=self)
            return
        hora_inicio = int(h_ini_str)
        hora_fin    = int(h_fin_str)

        # ── Persona ───────────────────────────────────────────────────────────
        persona = self.ent_persona.get().strip()
        if not persona:
            messagebox.showerror("Error", "El nombre de la persona es obligatorio.", parent=self)
            self.ent_persona.focus_set()
            return

        descripcion = self.ent_desc.get("1.0", "end").strip()

        ok, msg = crear_reserva(id_sala, dia, hora_inicio, hora_fin, persona, descripcion)
        if ok:
            messagebox.showinfo("✅ Éxito", msg, parent=self)
            self._limpiar_form()
            self._ver_todas()
        else:
            messagebox.showerror("❌ Error", msg, parent=self)

    def _limpiar_form(self):
        self.cmb_sala.current(0)
        self.ent_h_ini.delete(0, "end")
        self.ent_h_fin.delete(0, "end")
        self.ent_persona.delete(0, "end")
        self.ent_desc.delete("1.0", "end")

    def _poblar_tabla(self, lista):
        self.tree.delete(*self.tree.get_children())
        for r in lista:
            sala_nombre = next(
                (s.nombre for s in salas if s.id_sala == r.id_sala), f"Sala {r.id_sala}"
            )
            self.tree.insert("", "end", values=(
                sala_nombre,
                r.dia,
                f"{r.hora_inicio:02d}:00",
                f"{r.hora_fin:02d}:00",
                r.persona,
                r.descripcion,
            ))
        n = len(lista)
        self.lbl_count.config(text=f"{n} reserva{'s' if n != 1 else ''} mostrada{'s' if n != 1 else ''}")

    def _buscar_reservas(self):
        try:
            dia = self.ent_filtro_dia.get_date().strftime("%Y-%m-%d")
        except AttributeError:
            dia = self.ent_filtro_dia.get().strip()
        if not dia:
            messagebox.showwarning("Atención", "Ingresa un día para buscar.", parent=self)
            return
        resultado = reservas_por_dia(dia)
        if not resultado:
            messagebox.showinfo("Sin resultados", f"No hay reservas para el día {dia}.", parent=self)
        self._poblar_tabla(resultado)

    def _ver_todas(self):
        self._poblar_tabla(reservas)

    def _eliminar_seleccionada(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Atención", "Selecciona una reserva para eliminar.", parent=self)
            return
        idx = self.tree.index(sel[0])
        confirmado = messagebox.askyesno(
            "Confirmar",
            "¿Estás seguro de que quieres eliminar esta reserva?",
            parent=self,
        )
        if confirmado:
            ok, msg = eliminar_reserva(idx)
            if ok:
                messagebox.showinfo("✅ Eliminada", msg, parent=self)
                self._ver_todas()
            else:
                messagebox.showerror("Error", msg, parent=self)


# ─── Entry point ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = App()
    app.mainloop()
