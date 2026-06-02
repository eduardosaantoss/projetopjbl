
import tkinter as tk
from tkinter import ttk
import sqlite3
from database import get_connection
from datetime import datetime, timedelta
from contratos import calcular_valor_total_contratos
from utils import formatar_data_brasileira


class DashboardView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.colors = controller.colors
        self.setup_ui()

    def setup_ui(self):
        header_frame = ttk.Frame(self, style="Content.TFrame")
        header_frame.pack(fill="x", pady=(0, 40))
        
        ttk.Label(header_frame, text="Dashboard", style="Header.TLabel").pack(anchor="w")
        ttk.Label(header_frame, text="Resumo das atividades e métricas de hoje.", 
                 font=("Segoe UI", 11), foreground="#86868b", background=self.colors["bg"]).pack(anchor="w", pady=(5, 0))

        cards_frame = ttk.Frame(self, style="Content.TFrame")
        cards_frame.pack(fill="x")

        stats = self.get_stats()
        valor_total = calcular_valor_total_contratos()

        self.create_card(cards_frame, "Clientes", stats['total_clientes'], 0, 0)
        self.create_card(cards_frame, "Visitas", stats['total_visitas'], 0, 1)
        self.create_card(cards_frame, "Pendências", stats['pendencias_abertas'], 0, 2)
        self.create_card(cards_frame, "Valor Total Contratos", f"R$ {valor_total:,.2f}", 1, 0, colspan=3)

        alerts_frame = tk.Frame(self, bg=self.colors["white"], padx=25, pady=25, 
                               highlightbackground="#d2d2d7", highlightthickness=1)
        alerts_frame.pack(fill="both", expand=True, pady=30)

        tk.Label(alerts_frame, text="Alertas e Atenção", font=("Segoe UI", 14, "bold"), 
                 bg=self.colors["white"], fg=self.colors["primary"]).pack(anchor="w", pady=(0, 15))

        alertas = self.get_alerts()
        if not alertas:
            tk.Label(alerts_frame, text="Nenhum alerta crítico no momento. Bom trabalho!", 
                      font=("Segoe UI", 11), bg=self.colors["white"], fg="#86868b").pack(anchor="w")
        else:
            for alerta in alertas:
                lbl = tk.Label(alerts_frame, text=f"• {alerta}", font=("Segoe UI", 11), 
                              bg=self.colors["white"], fg=self.colors["danger"], pady=3)
                lbl.pack(anchor="w")

    def create_card(self, parent, title, value, row, col, colspan=1):
        card = tk.Frame(parent, bg=self.colors["white"], highlightbackground="#d2d2d7", 
                        highlightthickness=1, padx=25, pady=25)
        card.grid(row=row, column=col, columnspan=colspan, padx=10, pady=10, sticky="nsew")
        parent.grid_columnconfigure(col, weight=1)

        tk.Label(card, text=title.upper(), font=("Segoe UI", 9, "bold"), 
                 bg=self.colors["white"], fg="#86868b").pack(anchor="w")
        tk.Label(card, text=str(value), font=("Segoe UI", 28, "bold"), 
                 bg=self.colors["white"], fg=self.colors["primary"]).pack(anchor="w", pady=(10, 0))

    def get_stats(self):
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM clientes")
        total_clientes = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM visitas")
        total_visitas = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM pendencias WHERE status = 'aberta'")
        pendencias_abertas = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM contratos WHERE data_fim >= date('now')")
        contratos_ativos = cursor.fetchone()[0]

        conn.close()
        return {
            'total_clientes': total_clientes,
            'total_visitas': total_visitas,
            'pendencias_abertas': pendencias_abertas,
            'contratos_ativos': contratos_ativos
        }

    def get_alerts(self):
        alerts = []
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT c.nome 
            FROM clientes c
            LEFT JOIN (
                SELECT cliente_id, MAX(data_visita) as ultima_visita 
                FROM visitas 
                GROUP BY cliente_id
            ) v ON c.id = v.cliente_id
            WHERE v.ultima_visita IS NULL OR v.ultima_visita < date('now', '-30 days')
        """)
        sem_visita = cursor.fetchall()
        for c in sem_visita:
            alerts.append(f"Cliente '{c['nome']}' está sem visita há mais de 30 dias.")

        cursor.execute("""
            SELECT p.descricao, c.nome 
            FROM pendencias p 
            JOIN clientes c ON p.cliente_id = c.id
            WHERE p.status = 'aberta' AND p.prazo < date('now')
        """)
        atrasadas = cursor.fetchall()
        for p in atrasadas:
            alerts.append(f"Pendência atrasada: '{p['descricao']}' (Cliente: {p['nome']})")

        cursor.execute("""
            SELECT c.nome, con.data_fim 
            FROM contratos con
            JOIN clientes c ON con.cliente_id = c.id
            WHERE con.data_fim BETWEEN date('now') AND date('now', '+7 days')
        """)
        vencendo = cursor.fetchall()
        for con in vencendo:
            alerts.append(f"Contrato de '{con['nome']}' vence em breve ({formatar_data_brasileira(con['data_fim'])}).")

        conn.close()
        return alerts

