import re
import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image

from controllers.usuario_controller import cadastrar_usuario


class CadastroUsuarioView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#F5E6F3")
        self.master = master

        self.senha_visivel = False
        self.confirmar_visivel = False
        self.dropdown_aberto = False
        self.dropdown_menu = None

        self.cor_input = "#f8f8f8"
        self.cor_borda = "#d0d0d0"
        self.cor_foco = "#C084FC"
        self.cor_texto = "#1a1a1a"
        self.cor_placeholder = "#666666"
        self.cor_erro = "#dc2626"
        self.cor_hover = "#f0f0f0"

        self.nivel_var = ctk.StringVar(value="Selecione o nível de acesso")

        self.entry_nome = None
        self.entry_email = None
        self.entry_senha = None
        self.entry_confirmar = None
        self.label_select = None
        self.botao_seta = None
        self.frame_select = None
        self.botao_senha = None
        self.botao_confirmar = None

        self.criar_interface()

    def validar_email(self, email):
        padrao = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"
        return re.match(padrao, email) is not None

    def aplicar_foco(self, widget):
        widget.configure(border_color=self.cor_foco)

    def remover_foco(self, widget):
        widget.configure(border_color=self.cor_borda)

    def registrar_foco(self, widget):
        widget.bind("<FocusIn>", lambda event: self.aplicar_foco(widget))
        widget.bind("<FocusOut>", lambda event: self.remover_foco(widget))

    def limpar_erros_visuais(self):
        self.entry_nome.configure(border_color=self.cor_borda)
        self.entry_email.configure(border_color=self.cor_borda)
        self.entry_senha.configure(border_color=self.cor_borda)
        self.entry_confirmar.configure(border_color=self.cor_borda)
        self.frame_select.configure(border_color=self.cor_borda)

    def marcar_erro(self, widget):
        widget.configure(border_color=self.cor_erro)

    def alternar_senha(self):
        self.senha_visivel = not self.senha_visivel
        self.entry_senha.configure(show="" if self.senha_visivel else "●")
        self.botao_senha.configure(text="🙈" if self.senha_visivel else "👁")

    def alternar_confirmar(self):
        self.confirmar_visivel = not self.confirmar_visivel
        self.entry_confirmar.configure(show="" if self.confirmar_visivel else "●")
        self.botao_confirmar.configure(text="🙈" if self.confirmar_visivel else "👁")

    def fechar_dropdown(self):
        if self.dropdown_menu is not None:
            try:
                self.dropdown_menu.destroy()
            except Exception:
                pass
            self.dropdown_menu = None

        self.dropdown_aberto = False
        self.botao_seta.configure(text="▼")
        self.frame_select.configure(border_color=self.cor_borda)

    def selecionar_opcao(self, opcao):
        self.nivel_var.set(opcao)
        self.label_select.configure(text=opcao, text_color=self.cor_texto)
        self.fechar_dropdown()

    def abrir_dropdown(self):
        if self.dropdown_aberto:
            return

        self.master.update_idletasks()

        x = self.frame_select.winfo_rootx()
        y = self.frame_select.winfo_rooty() + self.frame_select.winfo_height() + 4
        largura_dropdown = self.frame_select.winfo_width()

        opcoes = [
            "Administrador",
            "Responsável pelo Estoque"
        ]
        altura_dropdown = (len(opcoes) * 34) + 8

        self.dropdown_menu = tk.Toplevel(self.master)
        self.dropdown_menu.overrideredirect(True)
        self.dropdown_menu.attributes("-topmost", True)
        self.dropdown_menu.geometry(f"{largura_dropdown}x{altura_dropdown}+{x}+{y}")
        self.dropdown_menu.configure(bg=self.cor_borda)

        container = tk.Frame(
            self.dropdown_menu,
            bg="#ffffff",
            bd=0,
            highlightthickness=0
        )
        container.place(x=1, y=1, width=largura_dropdown - 2, height=altura_dropdown - 2)

        for opcao in opcoes:
            item = tk.Label(
                container,
                text=opcao,
                anchor="w",
                bg="#ffffff",
                fg=self.cor_texto,
                padx=10,
                pady=8,
                font=("Segoe UI", 11)
            )
            item.pack(fill="x")

            item.bind("<Enter>", lambda e, w=item: w.configure(bg=self.cor_hover))
            item.bind("<Leave>", lambda e, w=item: w.configure(bg="#ffffff"))
            item.bind("<Button-1>", lambda e, texto=opcao: self.selecionar_opcao(texto))

        self.dropdown_aberto = True
        self.botao_seta.configure(text="▲")
        self.frame_select.configure(border_color=self.cor_foco)

    def toggle_dropdown(self, event=None):
        if self.dropdown_aberto:
            self.fechar_dropdown()
        else:
            self.abrir_dropdown()
        return "break"

    def clique_global(self, event):
        if not self.dropdown_aberto or self.dropdown_menu is None:
            return

        widget = event.widget

        if widget in (self.frame_select, self.label_select, self.botao_seta):
            return

        parent = widget
        while parent is not None:
            if str(parent) == str(self.dropdown_menu):
                return
            try:
                parent = parent.master
            except Exception:
                parent = None

        self.fechar_dropdown()

    def voltar(self):
        self.fechar_dropdown()
        self.master.mostrar_login()

    def limpar(self):
        self.entry_nome.delete(0, "end")
        self.entry_email.delete(0, "end")
        self.entry_senha.delete(0, "end")
        self.entry_confirmar.delete(0, "end")
        self.nivel_var.set("Selecione o nível de acesso")
        self.label_select.configure(
            text="Selecione o nível de acesso",
            text_color=self.cor_placeholder
        )
        self.fechar_dropdown()
        self.limpar_erros_visuais()
        self.entry_nome.focus()

    def cadastrar(self, event=None):
        self.limpar_erros_visuais()
        self.fechar_dropdown()

        nome = self.entry_nome.get().strip()
        email = self.entry_email.get().strip().lower()
        senha = self.entry_senha.get()
        confirmar = self.entry_confirmar.get()
        nivel_exibicao = self.nivel_var.get()

        if not nome:
            self.marcar_erro(self.entry_nome)
            messagebox.showerror("Erro", "Preencha o nome completo.")
            self.entry_nome.focus()
            return

        if not email:
            self.marcar_erro(self.entry_email)
            messagebox.showerror("Erro", "Preencha o e-mail.")
            self.entry_email.focus()
            return

        if not self.validar_email(email):
            self.marcar_erro(self.entry_email)
            messagebox.showerror("Erro", "Digite um e-mail válido.")
            self.entry_email.focus()
            return

        if not senha:
            self.marcar_erro(self.entry_senha)
            messagebox.showerror("Erro", "Preencha a senha.")
            self.entry_senha.focus()
            return

        if len(senha) < 6:
            self.marcar_erro(self.entry_senha)
            messagebox.showerror("Erro", "A senha deve ter no mínimo 6 caracteres.")
            self.entry_senha.focus()
            return

        if not confirmar:
            self.marcar_erro(self.entry_confirmar)
            messagebox.showerror("Erro", "Confirme a senha.")
            self.entry_confirmar.focus()
            return

        if senha != confirmar:
            self.marcar_erro(self.entry_senha)
            self.marcar_erro(self.entry_confirmar)
            messagebox.showerror("Erro", "As senhas não coincidem.")
            self.entry_confirmar.focus()
            return

        if nivel_exibicao == "Selecione o nível de acesso":
            self.marcar_erro(self.frame_select)
            messagebox.showerror("Erro", "Selecione o nível de acesso.")
            return

        mapa_nivel = {
            "Administrador": "admin",
            "Responsável pelo Estoque": "estoque"
        }
        nivel = mapa_nivel.get(nivel_exibicao)

        sucesso, mensagem = cadastrar_usuario(nome, email, senha, nivel)

        if sucesso:
            messagebox.showinfo(
                "Sucesso",
                mensagem if mensagem else "Usuário cadastrado com sucesso!"
            )
            self.master.mostrar_login()
        else:
            messagebox.showerror(
                "Erro",
                mensagem if mensagem else "Não foi possível cadastrar o usuário."
            )

    def criar_interface(self):
        self.master.bind("<Return>", self.cadastrar)
        self.master.bind("<Button-1>", self.clique_global)

        frame_principal = ctk.CTkFrame(
            self,
            width=640,
            height=600,
            corner_radius=15,
            border_width=1,
            border_color="#e0e0e0",
            fg_color="#ffffff"
        )
        frame_principal.place(relx=0.5, rely=0.5, anchor="center")

        try:
            logo_img = ctk.CTkImage(
                light_image=Image.open("assets/logo.png"),
                size=(80, 80)
            )
            label_logo = ctk.CTkLabel(frame_principal, image=logo_img, text="")
            label_logo.image = logo_img
            label_logo.pack(pady=(20, 8))
        except Exception:
            label_logo = ctk.CTkLabel(
                frame_principal,
                text="LARBEM",
                font=("Segoe UI", 18, "bold"),
                text_color="#ec4899"
            )
            label_logo.pack(pady=(20, 8))

        label_titulo = ctk.CTkLabel(
            frame_principal,
            text="Cadastro de Usuário",
            font=("Segoe UI", 24, "bold"),
            text_color=self.cor_texto
        )
        label_titulo.pack(pady=(0, 5))

        label_subtitulo = ctk.CTkLabel(
            frame_principal,
            text="Sistema BemStock - Lar Bem",
            font=("Segoe UI", 13),
            text_color=self.cor_placeholder
        )
        label_subtitulo.pack(pady=(0, 20))

        frame_form = ctk.CTkFrame(frame_principal, fg_color="transparent")
        frame_form.pack(pady=(0, 20), padx=24, fill="x")

        frame_form.grid_columnconfigure(0, weight=1)
        frame_form.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            frame_form,
            text="Nome Completo*",
            font=("Segoe UI", 13, "bold"),
            text_color=self.cor_texto,
            anchor="w"
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 5))

        self.entry_nome = ctk.CTkEntry(
            frame_form,
            height=40,
            placeholder_text="Digite o nome completo",
            corner_radius=6,
            border_width=1,
            border_color=self.cor_borda,
            fg_color=self.cor_input,
            text_color=self.cor_texto,
            placeholder_text_color=self.cor_placeholder,
            font=("Segoe UI", 14)
        )
        self.entry_nome.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        self.registrar_foco(self.entry_nome)

        ctk.CTkLabel(
            frame_form,
            text="E-mail*",
            font=("Segoe UI", 13, "bold"),
            text_color=self.cor_texto,
            anchor="w"
        ).grid(row=2, column=0, columnspan=2, sticky="w", pady=(0, 5))

        self.entry_email = ctk.CTkEntry(
            frame_form,
            height=40,
            placeholder_text="Digite o e-mail",
            corner_radius=6,
            border_width=1,
            border_color=self.cor_borda,
            fg_color=self.cor_input,
            text_color=self.cor_texto,
            placeholder_text_color=self.cor_placeholder,
            font=("Segoe UI", 14)
        )
        self.entry_email.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        self.registrar_foco(self.entry_email)

        ctk.CTkLabel(
            frame_form,
            text="Senha*",
            font=("Segoe UI", 13, "bold"),
            text_color=self.cor_texto,
            anchor="w"
        ).grid(row=4, column=0, sticky="w", pady=(0, 5), padx=(0, 7))

        ctk.CTkLabel(
            frame_form,
            text="Confirmar Senha*",
            font=("Segoe UI", 13, "bold"),
            text_color=self.cor_texto,
            anchor="w"
        ).grid(row=4, column=1, sticky="w", pady=(0, 5), padx=(7, 0))

        frame_senha = ctk.CTkFrame(frame_form, fg_color="transparent")
        frame_senha.grid(row=5, column=0, sticky="ew", pady=(0, 15), padx=(0, 7))
        frame_senha.grid_columnconfigure(0, weight=1)

        self.entry_senha = ctk.CTkEntry(
            frame_senha,
            height=40,
            placeholder_text="Mínimo 6 caracteres",
            show="●",
            corner_radius=6,
            border_width=1,
            border_color=self.cor_borda,
            fg_color=self.cor_input,
            text_color=self.cor_texto,
            placeholder_text_color=self.cor_placeholder,
            font=("Segoe UI", 14)
        )
        self.entry_senha.grid(row=0, column=0, sticky="ew")
        self.registrar_foco(self.entry_senha)

        self.botao_senha = ctk.CTkButton(
            frame_senha,
            text="👁",
            width=40,
            height=40,
            corner_radius=6,
            fg_color=self.cor_input,
            hover_color=self.cor_hover,
            text_color=self.cor_texto,
            border_width=1,
            border_color=self.cor_borda,
            command=self.alternar_senha
        )
        self.botao_senha.grid(row=0, column=1, padx=(8, 0))

        frame_confirmar = ctk.CTkFrame(frame_form, fg_color="transparent")
        frame_confirmar.grid(row=5, column=1, sticky="ew", pady=(0, 15), padx=(7, 0))
        frame_confirmar.grid_columnconfigure(0, weight=1)

        self.entry_confirmar = ctk.CTkEntry(
            frame_confirmar,
            height=40,
            placeholder_text="Digite a senha novamente",
            show="●",
            corner_radius=6,
            border_width=1,
            border_color=self.cor_borda,
            fg_color=self.cor_input,
            text_color=self.cor_texto,
            placeholder_text_color=self.cor_placeholder,
            font=("Segoe UI", 14)
        )
        self.entry_confirmar.grid(row=0, column=0, sticky="ew")
        self.registrar_foco(self.entry_confirmar)

        self.botao_confirmar = ctk.CTkButton(
            frame_confirmar,
            text="👁",
            width=40,
            height=40,
            corner_radius=6,
            fg_color=self.cor_input,
            hover_color=self.cor_hover,
            text_color=self.cor_texto,
            border_width=1,
            border_color=self.cor_borda,
            command=self.alternar_confirmar
        )
        self.botao_confirmar.grid(row=0, column=1, padx=(8, 0))

        ctk.CTkLabel(
            frame_form,
            text="Nível de Acesso*",
            font=("Segoe UI", 13, "bold"),
            text_color=self.cor_texto,
            anchor="w"
        ).grid(row=6, column=0, columnspan=2, sticky="w", pady=(0, 5))

        self.frame_select = ctk.CTkFrame(
            frame_form,
            height=40,
            corner_radius=6,
            border_width=1,
            border_color=self.cor_borda,
            fg_color=self.cor_input
        )
        self.frame_select.grid(row=7, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        self.frame_select.grid_propagate(False)
        self.frame_select.grid_columnconfigure(0, weight=1)
        self.frame_select.grid_columnconfigure(1, weight=0)

        self.label_select = ctk.CTkLabel(
            self.frame_select,
            text="Selecione o nível de acesso",
            font=("Segoe UI", 14),
            text_color=self.cor_placeholder,
            anchor="w",
            fg_color="transparent"
        )
        self.label_select.grid(row=0, column=0, sticky="ew", padx=(12, 0), pady=1)

        self.botao_seta = ctk.CTkLabel(
            self.frame_select,
            text="▼",
            font=("Segoe UI", 12),
            text_color=self.cor_texto,
            fg_color="transparent",
            width=30
        )
        self.botao_seta.grid(row=0, column=1, padx=(0, 10), pady=1)

        self.frame_select.bind("<Button-1>", self.toggle_dropdown)
        self.label_select.bind("<Button-1>", self.toggle_dropdown)
        self.botao_seta.bind("<Button-1>", self.toggle_dropdown)

        frame_botoes = ctk.CTkFrame(frame_form, fg_color="transparent")
        frame_botoes.grid(row=8, column=0, columnspan=2, pady=(10, 0))

        btn_voltar = ctk.CTkButton(
            frame_botoes,
            text="← Voltar",
            width=272,
            height=45,
            corner_radius=6,
            border_width=1,
            border_color="#d0d0d0",
            fg_color="#ffffff",
            hover_color="#f5f5f5",
            text_color="#1a1a1a",
            font=("Segoe UI", 14, "bold"),
            command=self.voltar
        )
        btn_voltar.grid(row=0, column=0, padx=(0, 7))

        btn_cadastrar = ctk.CTkButton(
            frame_botoes,
            text="Cadastrar Usuário",
            width=272,
            height=45,
            corner_radius=6,
            fg_color="#a855f7",
            hover_color="#9333ea",
            text_color="#ffffff",
            font=("Segoe UI", 14, "bold"),
            command=self.cadastrar
        )
        btn_cadastrar.grid(row=0, column=1, padx=(7, 0))

        self.entry_nome.focus()