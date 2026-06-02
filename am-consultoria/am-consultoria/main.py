
import tkinter as tk
from tkinter import ttk, messagebox
from database import criar_tabelas
from ui.dashboard import DashboardView
from ui.clientes_view import ClientesView
from ui.visitas_view import VisitasView
from ui.pendencias_view import PendenciasView
from ui.contratos_view import ContratosView


class AMConsultoriaApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("AM Consultoria - Central Inteligente")
        self.geometry("1100x700")
        self.configure(bg="#f5f5f5")

        criar_tabelas()

        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.colors = {
            "primary": "#000000",
            "secondary": "#1d1d1f",
            "bg": "#f5f5f7",
            "white": "#ffffff",
            "text": "#1d1d1f",
            "accent": "#0071e3",
            "danger": "#ff3b30"
        }

        self.setup_styles()
        self.setup_layout()
        
        self.show_view("Dashboard")

    def setup_styles(self):
        self.style.configure("Sidebar.TFrame", background=self.colors["white"])
        self.style.configure("Content.TFrame", background=self.colors["bg"])
        
        self.style.configure("Menu.TButton", 
                            background=self.colors["white"], 
                            foreground=self.colors["text"], 
                            font=("Segoe UI", 11),
                            borderwidth=0,
                            padding=12)
        self.style.map("Menu.TButton",
                      background=[('active', "#e8e8ed"), ('selected', "#e8e8ed")],
                      foreground=[('active', self.colors["accent"])])

        self.style.configure("Header.TLabel", 
                            background=self.colors["bg"], 
                            foreground=self.colors["primary"],
                            font=("Segoe UI", 24, "bold"))
        
        self.style.configure("Action.TButton",
                            background=self.colors["accent"],
                            foreground="white",
                            font=("Segoe UI", 10, "bold"))
        
        self.style.configure("Danger.TButton",
                            background=self.colors["danger"],
                            foreground="white",
                            font=("Segoe UI", 10, "bold"))

    def setup_layout(self):
        self.sidebar = tk.Frame(self, bg=self.colors["white"], width=220, highlightbackground="#d2d2d7", highlightthickness=1)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        logo_label = tk.Label(self.sidebar, text="AM", font=("Segoe UI", 28, "bold"), 
                             bg=self.colors["white"], fg=self.colors["primary"], pady=30)
        logo_label.pack()
        
        sub_label = tk.Label(self.sidebar, text="CONSULTORIA", font=("Segoe UI", 8, "bold"), 
                            bg=self.colors["white"], fg="#86868b")
        sub_label.pack(pady=(0, 40))

        menus = [
            ("Dashboard", self.show_dashboard),
            ("Clientes", self.show_clientes),
            ("Visitas", self.show_visitas),
            ("Pendências", self.show_pendencias),
            ("Contratos", self.show_contratos)
        ]

        for text, command in menus:
            btn = ttk.Button(self.sidebar, text=text, style="Menu.TButton", command=command)
            btn.pack(fill="x", padx=10, pady=2)
        
        tk.Frame(self.sidebar, bg="#d2d2d7", height=1).pack(fill="x", pady=20, padx=20)
        
        btn_sair = ttk.Button(self.sidebar, text="Sair", style="Menu.TButton", command=self.quit)
        btn_sair.pack(fill="x", padx=10, pady=2, side="bottom")

        self.content_area = ttk.Frame(self, style="Content.TFrame")
        self.content_area.pack(side="right", expand=True, fill="both", padx=40, pady=40)

    def clear_content(self):
        for widget in self.content_area.winfo_children():
            widget.destroy()

    def show_view(self, view_name):
        self.clear_content()
        if view_name == "Dashboard":
            view = DashboardView(self.content_area, self)
        elif view_name == "Clientes":
            view = ClientesView(self.content_area, self)
        elif view_name == "Visitas":
            view = VisitasView(self.content_area, self)
        elif view_name == "Pendências":
            view = PendenciasView(self.content_area, self)
        elif view_name == "Contratos":
            view = ContratosView(self.content_area, self)
        
        view.pack(expand=True, fill="both")

    def show_dashboard(self): self.show_view("Dashboard")
    def show_clientes(self): self.show_view("Clientes")
    def show_visitas(self): self.show_view("Visitas")
    def show_pendencias(self): self.show_view("Pendências")
    def show_contratos(self): self.show_view("Contratos")


if __name__ == "__main__":
    app = AMConsultoriaApp()
    app.mainloop()
