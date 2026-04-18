import customtkinter as ctk
from tkinter import messagebox

from controllers.usuario_controller import concluir_primeiro_acesso
from controllers.usuario_controller import buscar_usuario_por_id


class PrimeiroAcessoView(ctk.CTkFrame):
    def __init__(self, master, usuario):
        super().__init__(master, fg_color="#F5E6F3")
        self.master = master
        self.usuario = usuario

        self.cor_texto = "#1a1a1a"
        self.cor_texto_secundario = "#666666"
        self.cor_borda = "#d0d0d0"
        self.cor_borda_foco = "#C084FC"
        self.cor_borda_erro = "#ef4444"
        self.cor_input = "#f8f8f8"
        self.cor_roxo = "#a855f7"
        self.cor_roxo_hover = "#9333ea"

        self.campos = {}
        self.labels_erro = {}
        self.mostrar_senha_var = ctk.BooleanVar(value=False)

        self.criar_interface()

    def destacar_foco(self, widget):
        try:
            widget.configure(border_color=self.cor_borda_foco)
        except Exception:
            pass

    def remover_destaque(self, widget):
        try:
            widget.configure(border_color=self.cor_borda)
        except Exception:
            pass

    def marcar_erro(self, chave, mensagem):
        widget = self.campos.get(chave)
        label_erro = self.labels_erro.get(chave)

        if widget is not None:
            try:
                widget.configure(border_color=self.cor_borda_erro)
            except Exception:
                pass

        if label_erro is not None:
            label_erro.configure(text=mensagem)

    def limpar_erro(self, chave):
        widget = self.campos.get(chave)
        label_erro = self.labels_erro.get(chave)

        if widget is not None:
            try:
                widget.configure(border_color=self.cor_borda)
            except Exception:
                pass

        if label_erro is not None:
            label_erro.configure(text="")

    def limpar_todos_erros(self):
        for chave in self.labels_erro.keys():
            self.limpar_erro(chave)

    def ao_entrar_no_campo(self, chave):
        self.limpar_erro(chave)
        widget = self.campos.get(chave)
        if widget is not None:
            self.destacar_foco(widget)

    def ao_sair_do_campo(self, chave):
        widget = self.campos.get(chave)
        if widget is not None:
            self.remover_destaque(widget)

    def obter_valor_campo(self, chave):
        widget = self.campos.get(chave)
        if widget is None:
            return ""

        try:
            return widget.get().strip()
        except Exception:
            return ""

    def toggle_senha(self):
        mostrar = "" if self.mostrar_senha_var.get() else "●"

        if "nova_senha" in self.campos:
            self.campos["nova_senha"].configure(show=mostrar)

        if "confirmar_senha" in self.campos:
            self.campos["confirmar_senha"].configure(show=mostrar)

    def criar_label(self, parent, texto):
        ctk.CTkLabel(
            parent,
            text=texto,
            font=("Segoe UI", 13, "bold"),
            text_color=self.cor_texto,
            anchor="w"
        ).pack(anchor="w", pady=(0, 5))

    def criar_label_erro(self, parent, chave):
        label = ctk.CTkLabel(
            parent,
            text="",
            font=("Segoe UI", 11),
            text_color=self.cor_borda_erro,
            anchor="w"
        )
        label.pack(anchor="w", pady=(0, 10))
        self.labels_erro[chave] = label

    def criar_entry(self, parent, chave, valor="", mostrar=""):
        entry = ctk.CTkEntry(
            parent,
            height=40,
            corner_radius=6,
            border_width=1,
            border_color=self.cor_borda,
            fg_color=self.cor_input,
            text_color=self.cor_texto,
            font=("Segoe UI", 14),
            show=mostrar
        )
        entry.pack(fill="x", pady=(0, 4))

        if valor:
            entry.insert(0, valor)

        entry.bind("<FocusIn>", lambda event, c=chave: self.ao_entrar_no_campo(c))
        entry.bind("<FocusOut>", lambda event, c=chave: self.ao_sair_do_campo(c))
        entry.bind("<KeyPress>", lambda event, c=chave: self.limpar_erro(c))

        self.campos[chave] = entry
        self.criar_label_erro(parent, chave)

    def validar_campos(self):
        self.limpar_todos_erros()
        valido = True

        novo_email = self.obter_valor_campo("novo_email")
        nova_senha = self.obter_valor_campo("nova_senha")
        confirmar_senha = self.obter_valor_campo("confirmar_senha")

        if not novo_email:
            self.marcar_erro("novo_email", "O novo e-mail é obrigatório.")
            valido = False

        if not nova_senha:
            self.marcar_erro("nova_senha", "A nova senha é obrigatória.")
            valido = False

        if not confirmar_senha:
            self.marcar_erro("confirmar_senha", "Confirme a nova senha.")
            valido = False

        if nova_senha and confirmar_senha and nova_senha != confirmar_senha:
            self.marcar_erro("nova_senha", "As senhas não coincidem.")
            self.marcar_erro("confirmar_senha", "As senhas não coincidem.")
            valido = False

        if novo_email.lower() == "teste@bemstock.com":
            self.marcar_erro("novo_email", "Informe um novo e-mail diferente do temporário.")
            valido = False

        if nova_senha == "123456":
            self.marcar_erro("nova_senha", "Informe uma nova senha diferente da temporária.")
            valido = False

        return valido

    def concluir(self):
        if not self.validar_campos():
            return

        novo_email = self.obter_valor_campo("novo_email")
        nova_senha = self.obter_valor_campo("nova_senha")

        sucesso, mensagem = concluir_primeiro_acesso(
            self.usuario["id_usuario"],
            novo_email,
            nova_senha
        )

        if sucesso:
            usuario_atualizado = buscar_usuario_por_id(self.usuario["id_usuario"])

            if usuario_atualizado is None:
                messagebox.showerror("Erro", "Não foi possível recarregar o usuário após a atualização.")
                return

            messagebox.showinfo("Sucesso", "Primeiro acesso concluído com sucesso.")
            self.master.usuario_logado = usuario_atualizado
            self.master.mostrar_dashboard(usuario_atualizado)
        else:
            self.tratar_erro_controller(mensagem)
            messagebox.showerror("Erro", mensagem)

    def tratar_erro_controller(self, mensagem):
        texto = mensagem.lower()

        if "e-mail" in texto or "email" in texto:
            self.marcar_erro("novo_email", mensagem)
        elif "senha" in texto:
            self.marcar_erro("nova_senha", mensagem)
            self.marcar_erro("confirmar_senha", mensagem)

    def criar_interface(self):
        frame_principal = ctk.CTkFrame(self, fg_color="transparent")
        frame_principal.pack(fill="both", expand=True, padx=20, pady=20)

        topo = ctk.CTkFrame(
            frame_principal,
            height=110,
            corner_radius=15,
            fg_color="#ffffff",
            border_width=1,
            border_color="#e0e0e0"
        )
        topo.pack(fill="x", pady=(0, 20))
        topo.pack_propagate(False)

        ctk.CTkLabel(
            topo,
            text="Primeiro Acesso",
            font=("Segoe UI", 28, "bold"),
            text_color=self.cor_texto
        ).pack(anchor="w", padx=25, pady=(18, 0))

        ctk.CTkLabel(
            topo,
            text="Por segurança, altere o e-mail e a senha do administrador temporário para continuar.",
            font=("Segoe UI", 13),
            text_color=self.cor_texto_secundario,
            anchor="w",
            justify="left",
            wraplength=700
        ).pack(anchor="w", padx=25, pady=(4, 0))

        frame_form = ctk.CTkFrame(
            frame_principal,
            fg_color="#ffffff",
            corner_radius=15,
            border_width=1,
            border_color="#e0e0e0"
        )
        frame_form.pack(fill="both", expand=True)

        scroll = ctk.CTkScrollableFrame(
            frame_form,
            fg_color="transparent"
        )
        scroll.pack(fill="both", expand=True, padx=24, pady=(24, 12))

        self.criar_label(scroll, "Usuário temporário")
        self.criar_entry(
            scroll,
            "usuario_temporario",
            valor=self.usuario.get("email", "teste@bemstock.com")
        )
        self.campos["usuario_temporario"].configure(state="disabled")

        self.criar_label(scroll, "Novo e-mail admin*")
        self.criar_entry(scroll, "novo_email", valor="")

        self.criar_label(scroll, "Nova senha*")
        self.criar_entry(scroll, "nova_senha", valor="", mostrar="●")

        self.criar_label(scroll, "Confirmar nova senha*")
        self.criar_entry(scroll, "confirmar_senha", valor="", mostrar="●")

        checkbox_mostrar = ctk.CTkCheckBox(
            scroll,
            text="Mostrar senha",
            variable=self.mostrar_senha_var,
            font=("Segoe UI", 12),
            text_color=self.cor_texto_secundario,
            fg_color=self.cor_roxo,
            hover_color=self.cor_roxo_hover,
            command=self.toggle_senha
        )
        checkbox_mostrar.pack(anchor="w", pady=(0, 12))

        frame_botoes = ctk.CTkFrame(frame_form, fg_color="transparent")
        frame_botoes.pack(fill="x", padx=24, pady=(0, 24))

        btn_confirmar = ctk.CTkButton(
            frame_botoes,
            text="Concluir Primeiro Acesso",
            height=45,
            corner_radius=6,
            fg_color=self.cor_roxo,
            hover_color=self.cor_roxo_hover,
            text_color="#ffffff",
            font=("Segoe UI", 14, "bold"),
            command=self.concluir
        )
        btn_confirmar.pack(fill="x")