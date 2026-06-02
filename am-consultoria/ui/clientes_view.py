import tkinter as tk
from tkinter import ttk, messagebox
from clientes import listar_clientes, cadastrar_cliente, buscar_cliente_por_id, listar_contatos, adicionar_contato, excluir_cliente
from visitas import listar_visitas
from pendencias import listar_pendencias
from contratos import listar_contratos

class ClientesView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.setup_ui()

    def setup_ui(self):
        # Header com Pesquisa e Botões
        header_frame = ttk.Frame(self, style="Content.TFrame")
        header_frame.pack(fill="x", pady=(0, 25))

        ttk.Label(header_frame, text="Clientes", style="Header.TLabel").pack(side="left")

        # Container para botões à direita
        btn_frame = ttk.Frame(header_frame, style="Content.TFrame")
        btn_frame.pack(side="right")

        self.btn_add = ttk.Button(btn_frame, text="+ Novo Cliente", style="Action.TButton", command=self.abrir_cadastro)
        self.btn_add.pack(side="right", padx=5)
        
        self.btn_del = ttk.Button(btn_frame, text="Excluir", style="Danger.TButton", command=self.remover_selecionado)
        self.btn_del.pack(side="right", padx=5)

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.atualizar_tabela())
        search_entry = ttk.Entry(header_frame, textvariable=self.search_var, width=25)
        search_entry.pack(side="right", padx=20)
        ttk.Label(header_frame, text="Pesquisar:", background=self.controller.colors["bg"]).pack(side="right")

        # Tabela de Clientes Minimalista
        columns = ("id", "nome", "tipo", "cidade", "contato")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=15)
        self.tree.heading("id", text="ID")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("tipo", text="Tipo")
        self.tree.heading("cidade", text="Cidade")
        self.tree.heading("contato", text="Contato Principal")

        self.tree.column("id", width=50)
        self.tree.column("nome", width=250)
        self.tree.pack(expand=True, fill="both")

        self.tree.bind("<Double-1>", self.abrir_perfil)

        self.atualizar_tabela()

    def atualizar_tabela(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        clientes = listar_clientes(self.search_var.get())
        for c in clientes:
            self.tree.insert("", "end", values=(c['id'], c['nome'], c['tipo_cliente'], c['cidade'], c['contato_principal']))

    def remover_selecionado(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um cliente para excluir.")
            return
        
        item = self.tree.item(selected[0])
        cliente_id = item['values'][0]
        nome = item['values'][1]
        
        if messagebox.askyesno("Confirmar", f"Tem certeza que deseja excluir o cliente '{nome}'?\nIsso apagará todas as visitas, contratos e pendências relacionadas."):
            excluir_cliente(cliente_id)
            self.atualizar_tabela()
            messagebox.showinfo("Sucesso", "Cliente excluído com sucesso.")

    def abrir_cadastro(self):
        dialog = tk.Toplevel(self)
        dialog.title("Cadastrar Novo Cliente")
        dialog.geometry("400x500")
        dialog.padx = 20
        dialog.pady = 20

        fields = [
            ("Nome*", "nome"),
            ("Tipo (Empresa/Individual)", "tipo"),
            ("Cidade", "cidade"),
            ("Contato Principal", "contato"),
            ("Telefone", "tel"),
            ("Email", "email")
        ]
        
        entries = {}
        for label, key in fields:
            frame = ttk.Frame(dialog)
            frame.pack(fill="x", pady=5, padx=20)
            ttk.Label(frame, text=label).pack(anchor="w")
            entry = ttk.Entry(frame)
            entry.pack(fill="x")
            entries[key] = entry

        ttk.Label(dialog, text="Observações:").pack(anchor="w", padx=20)
        obs_text = tk.Text(dialog, height=4)
        obs_text.pack(fill="x", padx=20, pady=5)

        def salvar():
            if not entries['nome'].get():
                messagebox.showerror("Erro", "O nome é obrigatório!")
                return
            
            cadastrar_cliente(
                entries['nome'].get(),
                entries['tipo'].get(),
                entries['cidade'].get(),
                entries['contato'].get(),
                entries['tel'].get(),
                entries['email'].get(),
                obs_text.get("1.0", "end-1c")
            )
            messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
            dialog.destroy()
            self.atualizar_tabela()

        ttk.Button(dialog, text="Salvar Cliente", command=salvar).pack(pady=20)

    def abrir_perfil(self, event):
        selected = self.tree.selection()
        if not selected: return
        
        cliente_id = self.tree.item(selected[0])['values'][0]
        cliente = buscar_cliente_por_id(cliente_id)
        
        profile_win = tk.Toplevel(self)
        profile_win.title(f"Perfil: {cliente['nome']}")
        profile_win.geometry("800x600")

        notebook = ttk.Notebook(profile_win)
        notebook.pack(expand=True, fill="both", padx=10, pady=10)

        # Aba Resumo
        tab_resumo = ttk.Frame(notebook, padding=20)
        notebook.add(tab_resumo, text="Resumo")
        
        resumo_text = f"""
Nome: {cliente['nome']}
Tipo: {cliente['tipo_cliente']}
Cidade: {cliente['cidade']}
Contato Principal: {cliente['contato_principal']}
Telefone: {cliente['telefone']}
Email: {cliente['email']}

Observações Gerais:
{cliente['observacoes']}
"""
        tk.Label(tab_resumo, text=resumo_text, justify="left", font=("Segoe UI", 11), bg="white", relief="flat").pack(anchor="w", fill="both", expand=True)

        # Aba Histórico (Visitas)
        tab_hist = ttk.Frame(notebook)
        notebook.add(tab_hist, text="Histórico")
        visitas_tree = ttk.Treeview(tab_hist, columns=("data", "tipo", "resumo"), show="headings")
        visitas_tree.heading("data", text="Data")
        visitas_tree.heading("tipo", text="Tipo")
        visitas_tree.heading("resumo", text="Resumo")
        visitas_tree.pack(expand=True, fill="both")
        
        for v in listar_visitas(cliente_id):
            visitas_tree.insert("", "end", values=(v['data_visita'], v['tipo_visita'], v['resumo']))

        # Aba Pendências
        tab_pend = ttk.Frame(notebook)
        notebook.add(tab_pend, text="Pendências")
        pend_tree = ttk.Treeview(tab_pend, columns=("desc", "prazo", "prioridade", "status"), show="headings")
        pend_tree.heading("desc", text="Descrição")
        pend_tree.heading("prazo", text="Prazo")
        pend_tree.heading("prioridade", text="Prioridade")
        pend_tree.heading("status", text="Status")
        pend_tree.pack(expand=True, fill="both")
        
        for p in listar_pendencias(cliente_id):
            pend_tree.insert("", "end", values=(p['descricao'], p['prazo'], p['prioridade'], p['status']))

        # Aba Contratos
        tab_cont = ttk.Frame(notebook)
        notebook.add(tab_cont, text="Contratos")
        cont_tree = ttk.Treeview(tab_cont, columns=("tipo", "valor", "fim"), show="headings")
        cont_tree.heading("tipo", text="Tipo")
        cont_tree.heading("valor", text="Valor")
        cont_tree.heading("fim", text="Vencimento")
        cont_tree.pack(expand=True, fill="both")
        
        for con in listar_contratos(cliente_id):
            cont_tree.insert("", "end", values=(con['tipo_contrato'], f"R$ {con['valor']:.2f}", con['data_fim']))

        # Aba Observações Humanas (Contexto Relacional)
        tab_human = ttk.Frame(notebook, padding=20)
        notebook.add(tab_human, text="Obs. Humanas")
        
        tk.Label(tab_human, text="Contexto Relacional e Comportamental:", font=("Segoe UI", 12, "bold")).pack(anchor="w")
        
        # Aqui podemos listar o "Contexto Humano" de todas as visitas
        canvas = tk.Canvas(tab_human)
        scrollbar = ttk.Scrollbar(tab_human, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        for v in listar_visitas(cliente_id):
            f = ttk.LabelFrame(scrollable_frame, text=f"Visita em {v['data_visita']}")
            f.pack(fill="x", pady=5, padx=5)
            ttk.Label(f, text=v['contexto_humano'], wraplength=700).pack(pady=5, padx=5)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
