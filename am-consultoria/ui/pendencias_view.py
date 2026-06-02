import tkinter as tk
from tkinter import ttk, messagebox
from pendencias import listar_pendencias, atualizar_status_pendencia, excluir_pendencia

class PendenciasView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.setup_ui()

    def setup_ui(self):
        header_frame = ttk.Frame(self, style="Content.TFrame")
        header_frame.pack(fill="x", pady=(0, 25))

        ttk.Label(header_frame, text="Pendências", style="Header.TLabel").pack(side="left")
        
        btn_frame = ttk.Frame(header_frame, style="Content.TFrame")
        btn_frame.pack(side="right")

        ttk.Button(btn_frame, text="Marcar Concluída", style="Action.TButton", command=self.concluir_pendencia).pack(side="right", padx=5)
        ttk.Button(btn_frame, text="Excluir", style="Danger.TButton", command=self.remover_selecionado).pack(side="right", padx=5)
        
        self.show_all_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(header_frame, text="Mostrar Concluídas", variable=self.show_all_var, 
                        command=self.atualizar_tabela).pack(side="right", padx=20)

        # Tabela de Pendências Minimalista
        columns = ("id", "cliente", "descricao", "prazo", "prioridade", "status")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=15)
        self.tree.heading("id", text="ID")
        self.tree.heading("cliente", text="Cliente")
        self.tree.heading("descricao", text="Descrição")
        self.tree.heading("prazo", text="Prazo")
        self.tree.heading("prioridade", text="Prioridade")
        self.tree.heading("status", text="Status")
        
        self.tree.column("id", width=50)
        self.tree.column("descricao", width=300)
        self.tree.pack(expand=True, fill="both")

        self.atualizar_tabela()

    def atualizar_tabela(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for p in listar_pendencias(apenas_abertas=not self.show_all_var.get()):
            self.tree.insert("", "end", values=(p['id'], p['cliente_nome'], p['descricao'], p['prazo'], p['prioridade'], p['status']))

    def remover_selecionado(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione uma pendência para excluir.")
            return
        
        item = self.tree.item(selected[0])
        pendencia_id = item['values'][0]
        
        if messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir esta pendência?"):
            excluir_pendencia(pendencia_id)
            self.atualizar_tabela()
            messagebox.showinfo("Sucesso", "Pendência excluída com sucesso.")

    def concluir_pendencia(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione uma pendência para concluir.")
            return
        
        item = self.tree.item(selected[0])
        pendencia_id = item['values'][0]
        status = item['values'][5]
        
        if status == 'concluída':
            messagebox.showinfo("Aviso", "Esta pendência já está concluída.")
            return

        if messagebox.askyesno("Confirmar", "Deseja marcar esta pendência como concluída?"):
            atualizar_status_pendencia(pendencia_id, 'concluída')
            self.atualizar_tabela()
