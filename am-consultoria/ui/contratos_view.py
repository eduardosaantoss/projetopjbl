import tkinter as tk
from tkinter import ttk, messagebox
from contratos import listar_contratos, cadastrar_contrato, excluir_contrato
from clientes import listar_clientes

class ContratosView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.setup_ui()

    def setup_ui(self):
        header_frame = ttk.Frame(self, style="Content.TFrame")
        header_frame.pack(fill="x", pady=(0, 25))

        ttk.Label(header_frame, text="Contratos", style="Header.TLabel").pack(side="left")
        
        btn_frame = ttk.Frame(header_frame, style="Content.TFrame")
        btn_frame.pack(side="right")

        ttk.Button(btn_frame, text="+ Novo Contrato", style="Action.TButton", command=self.abrir_cadastro).pack(side="right", padx=5)
        ttk.Button(btn_frame, text="Excluir", style="Danger.TButton", command=self.remover_selecionado).pack(side="right", padx=5)

        # Tabela de Contratos Minimalista
        columns = ("id", "cliente", "tipo", "valor", "inicio", "fim")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=15)
        self.tree.heading("id", text="ID")
        self.tree.heading("cliente", text="Cliente")
        self.tree.heading("tipo", text="Tipo")
        self.tree.heading("valor", text="Valor")
        self.tree.heading("inicio", text="Início")
        self.tree.heading("fim", text="Vencimento")
        
        self.tree.column("id", width=50)
        self.tree.pack(expand=True, fill="both")

        self.atualizar_tabela()

    def atualizar_tabela(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for c in listar_contratos():
            self.tree.insert("", "end", values=(c['id'], c['cliente_nome'], c['tipo_contrato'], f"R$ {c['valor']:.2f}", c['data_inicio'], c['data_fim']))

    def remover_selecionado(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um contrato para excluir.")
            return
        
        item = self.tree.item(selected[0])
        contrato_id = item['values'][0]
        
        if messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir este contrato?"):
            excluir_contrato(contrato_id)
            self.atualizar_tabela()
            messagebox.showinfo("Sucesso", "Contrato excluído com sucesso.")

    def abrir_cadastro(self):
        dialog = tk.Toplevel(self)
        dialog.title("Novo Contrato")
        dialog.geometry("400x550")

        clientes = listar_clientes()
        if not clientes:
            messagebox.showwarning("Aviso", "Cadastre um cliente antes de criar um contrato.")
            dialog.destroy()
            return

        cliente_map = {c['nome']: c['id'] for c in clientes}

        frame = ttk.Frame(dialog, padding=20)
        frame.pack(fill="both")

        ttk.Label(frame, text="Cliente*").pack(anchor="w")
        combo_cli = ttk.Combobox(frame, values=list(cliente_map.keys()), state="readonly")
        combo_cli.pack(fill="x", pady=(0, 10))

        ttk.Label(frame, text="Tipo de Contrato").pack(anchor="w")
        combo_tipo = ttk.Combobox(frame, values=["Mensal", "Projeto", "Por Visita"], state="readonly")
        combo_tipo.pack(fill="x", pady=(0, 10))

        ttk.Label(frame, text="Valor (R$)*").pack(anchor="w")
        entry_valor = ttk.Entry(frame)
        entry_valor.pack(fill="x", pady=(0, 10))

        ttk.Label(frame, text="Data Início (AAAA-MM-DD)").pack(anchor="w")
        entry_ini = ttk.Entry(frame)
        entry_ini.pack(fill="x", pady=(0, 10))

        ttk.Label(frame, text="Data Fim (AAAA-MM-DD)*").pack(anchor="w")
        entry_fim = ttk.Entry(frame)
        entry_fim.pack(fill="x", pady=(0, 10))

        ttk.Label(frame, text="Observações").pack(anchor="w")
        text_obs = tk.Text(frame, height=3)
        text_obs.pack(fill="x", pady=(0, 10))

        def salvar():
            try:
                if not combo_cli.get() or not entry_valor.get() or not entry_fim.get():
                    messagebox.showerror("Erro", "Campos com * são obrigatórios!")
                    return
                
                cadastrar_contrato(
                    cliente_map[combo_cli.get()],
                    combo_tipo.get(),
                    float(entry_valor.get().replace(',', '.')),
                    entry_ini.get(),
                    entry_fim.get(),
                    text_obs.get("1.0", "end-1c")
                )
                messagebox.showinfo("Sucesso", "Contrato cadastrado!")
                dialog.destroy()
                self.atualizar_tabela()
            except ValueError:
                messagebox.showerror("Erro", "Valor inválido. Use apenas números e ponto.")

        ttk.Button(frame, text="Salvar Contrato", command=salvar).pack(pady=10)
