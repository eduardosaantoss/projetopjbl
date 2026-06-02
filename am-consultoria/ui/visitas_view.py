
import tkinter as tk
from tkinter import ttk, messagebox
from visitas import registrar_visita, listar_visitas, excluir_visita
from clientes import listar_clientes
from pendencias import criar_pendencia
from utils import formatar_data_brasileira, formatar_data_iso, aplicar_mascara_data, data_hoje_br


class VisitasView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.setup_ui()

    def setup_ui(self):
        header_frame = ttk.Frame(self, style="Content.TFrame")
        header_frame.pack(fill="x", pady=(0, 25))

        ttk.Label(header_frame, text="Visitas", style="Header.TLabel").pack(side="left")
        
        btn_frame = ttk.Frame(header_frame, style="Content.TFrame")
        btn_frame.pack(side="right")

        ttk.Button(btn_frame, text="+ Nova Visita", style="Action.TButton", command=self.abrir_registro).pack(side="right", padx=5)
        ttk.Button(btn_frame, text="Excluir", style="Danger.TButton", command=self.remover_selecionado).pack(side="right", padx=5)

        columns = ("id", "cliente", "data", "tipo", "prioridade")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=15)
        self.tree.heading("id", text="ID")
        self.tree.heading("cliente", text="Cliente")
        self.tree.heading("data", text="Data")
        self.tree.heading("tipo", text="Tipo")
        self.tree.heading("prioridade", text="Prioridade")
        
        self.tree.column("id", width=50)
        self.tree.pack(expand=True, fill="both")

        self.atualizar_tabela()

    def atualizar_tabela(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for v in listar_visitas():
            self.tree.insert("", "end", values=(v['id'], v['cliente_nome'], formatar_data_brasileira(v['data_visita']), v['tipo_visita'], v['prioridade']))

    def remover_selecionado(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione uma visita para excluir.")
            return
        
        item = self.tree.item(selected[0])
        visita_id = item['values'][0]
        
        if messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir esta visita?"):
            excluir_visita(visita_id)
            self.atualizar_tabela()
            messagebox.showinfo("Sucesso", "Visita excluída com sucesso.")

    def abrir_registro(self):
        dialog = tk.Toplevel(self)
        dialog.title("Registrar Nova Visita")
        dialog.geometry("500x650")

        clientes = listar_clientes()
        if not clientes:
            messagebox.showwarning("Aviso", "Cadastre um cliente antes de registrar uma visita.")
            dialog.destroy()
            return

        cliente_map = {c['nome']: c['id'] for c in clientes}
        
        frame_cli = ttk.Frame(dialog, padding=10)
        frame_cli.pack(fill="x")
        ttk.Label(frame_cli, text="Cliente*").pack(anchor="w")
        combo_cli = ttk.Combobox(frame_cli, values=list(cliente_map.keys()), state="readonly")
        combo_cli.pack(fill="x")

        frame_data = ttk.Frame(dialog, padding=10)
        frame_data.pack(fill="x")
        ttk.Label(frame_data, text="Data*").pack(anchor="w")
        entry_data = ttk.Entry(frame_data)
        entry_data.insert(0, data_hoje_br())
        aplicar_mascara_data(entry_data)
        entry_data.pack(fill="x")

        frame_tipo = ttk.Frame(dialog, padding=10)
        frame_tipo.pack(fill="x")
        ttk.Label(frame_tipo, text="Tipo de Visita").pack(anchor="w")
        combo_tipo = ttk.Combobox(frame_tipo, values=["Acompanhamento", "Emergência", "Auditoria", "Supervisão", "Reunião"], state="readonly")
        combo_tipo.pack(fill="x")

        frame_res = ttk.Frame(dialog, padding=10)
        frame_res.pack(fill="x")
        ttk.Label(frame_res, text="Resumo da Visita*").pack(anchor="w")
        entry_resumo = ttk.Entry(frame_res)
        entry_resumo.pack(fill="x")

        frame_hum = ttk.Frame(dialog, padding=10)
        frame_hum.pack(fill="x")
        ttk.Label(frame_hum, text="Contexto Humano (Obrigatório)*").pack(anchor="w")
        text_humano = tk.Text(frame_hum, height=5)
        text_humano.pack(fill="x")

        frame_extra = ttk.Frame(dialog, padding=10)
        frame_extra.pack(fill="x")
        ttk.Label(frame_extra, text="Prioridade").pack(anchor="w", side="left")
        combo_prio = ttk.Combobox(frame_extra, values=["Baixa", "Média", "Alta"], state="readonly", width=10)
        combo_prio.pack(side="left", padx=10)
        
        ttk.Label(frame_extra, text="Responsável").pack(anchor="w", side="left", padx=(20, 0))
        entry_resp = ttk.Entry(frame_extra, width=20)
        entry_resp.pack(side="left")

        def salvar():
            if not combo_cli.get() or not entry_resumo.get() or not text_humano.get("1.0", "end-1c").strip():
                messagebox.showerror("Erro", "Campos com * são obrigatórios!")
                return
            
            cliente_id = cliente_map[combo_cli.get()]
            data_iso = formatar_data_iso(entry_data.get())
            visita_id = registrar_visita(
                cliente_id,
                data_iso,
                combo_tipo.get(),
                entry_resumo.get(),
                text_humano.get("1.0", "end-1c"),
                entry_resp.get(),
                combo_prio.get()
            )
            
            if messagebox.askyesno("Sucesso", "Visita salva! Deseja criar uma pendência agora?"):
                self.abrir_pendencia_rapida(cliente_id, visita_id)
            
            dialog.destroy()
            self.atualizar_tabela()

        ttk.Button(dialog, text="Salvar Visita", command=salvar).pack(pady=20)

    def abrir_pendencia_rapida(self, cliente_id, visita_id):
        dialog = tk.Toplevel(self)
        dialog.title("Nova Pendência")
        dialog.geometry("400x300")

        frame = ttk.Frame(dialog, padding=20)
        frame.pack(fill="both")

        ttk.Label(frame, text="Descrição*").pack(anchor="w")
        desc = ttk.Entry(frame)
        desc.pack(fill="x", pady=(0, 10))

        ttk.Label(frame, text="Prazo (dd/mm/aaaa)").pack(anchor="w")
        prazo = ttk.Entry(frame)
        aplicar_mascara_data(prazo)
        prazo.pack(fill="x", pady=(0, 10))

        ttk.Label(frame, text="Prioridade").pack(anchor="w")
        prio = ttk.Combobox(frame, values=["Baixa", "Média", "Alta"], state="readonly")
        prio.pack(fill="x", pady=(0, 10))

        def salvar_p():
            if not desc.get():
                messagebox.showerror("Erro", "Descrição é obrigatória.")
                return
            prazo_iso = formatar_data_iso(prazo.get())
            criar_pendencia(cliente_id, visita_id, desc.get(), prazo_iso, prio.get())
            messagebox.showinfo("Sucesso", "Pendência criada!")
            dialog.destroy()

        ttk.Button(frame, text="Criar Pendência", command=salvar_p).pack(pady=10)

