import re
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image

from controllers.login_controller import autenticar_usuario


class LoginView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#F5E6F3")
        self.master = master

        self.cor_card = "#ffffff"
        self.cor_borda = "#d0d0d0"
        self.cor_foco = "#C084FC"
        self.cor_erro = "#dc2626"
        self.cor_texto = "#1a1a1a"
        self.cor_texto_secundario = "#666666"
        self.cor_input = "#f8f8f8"
        self.cor_roxo = "#a855f7"
        self.cor_roxo_hover = "#9333ea"
        self.cor_hover_secundario = "#f5f5f5"

        self.email_var = ctk.StringVar()
        self.senha_var = ctk.StringVar()
        self.mostrar_senha_var = ctk.BooleanVar(value=False)

        self.entry_email = None
        self.entry_senha = None
        self.btn_entrar = None

        self.criar_interface()

    def aplicar_foco(self, widget):
        widget.configure(border_color=self.cor_foco)

    def remover_foco(self, widget):
        widget.configure(border_color=self.cor_borda)

    def limpar_erros(self):
        self.entry_email.configure(border_color=self.cor_borda)
        self.entry_senha.configure(border_color=self.cor_borda)

    def validar_campos_vazios(self):
        email = self.email_var.get().strip()
        senha = self.senha_var.get()

        if not email:
            self.entry_email.configure(border_color=self.cor_erro)
            messagebox.showerror("Erro", "Por favor, digite seu e-mail.")
            self.entry_email.focus()
            return False

        if not senha:
            self.entry_senha.configure(border_color=self.cor_erro)
            messagebox.showerror("Erro", "Por favor, digite sua senha.")
            self.entry_senha.focus()
            return False

        return True

    def validar_email_local(self, email):
        padrao = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(padrao, email):
            self.entry_email.configure(border_color=self.cor_erro)
            messagebox.showerror("Erro", "E-mail inválido.")
            self.entry_email.focus()
            return False
        return True

    def toggle_senha(self):
        self.entry_senha.configure(show="" if self.mostrar_senha_var.get() else "●")

    def abrir_cadastro(self):
        self.master.mostrar_cadastro()

    def fazer_login(self, event=None):
        self.limpar_erros()

        if not self.validar_campos_vazios():
            return

        email = self.email_var.get().strip().lower()
        senha = self.senha_var.get()

        if not self.validar_email_local(email):
            return

        self.btn_entrar.configure(state="disabled", text="Verificando...")
        self.master.update_idletasks()

        try:
            sucesso, resultado = autenticar_usuario(email, senha)

            if sucesso:
                usuario = resultado
                self.master.mostrar_dashboard(usuario)
            else:
                mensagem = resultado
                self.entry_email.configure(border_color=self.cor_erro)
                self.entry_senha.configure(border_color=self.cor_erro)
                messagebox.showerror("Erro de Login", mensagem)
                self.btn_entrar.configure(state="normal", text="Entrar")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao realizar login: {str(e)}")
            self.btn_entrar.configure(state="normal", text="Entrar")

    def criar_interface(self):
        self.master.bind("<Return>", self.fazer_login)

        frame_principal = ctk.CTkFrame(
            self,
            width=640,
            height=600,
            corner_radius=15,
            border_width=1,
            border_color="#e0e0e0",
            fg_color=self.cor_card
        )
        frame_principal.place(relx=0.5, rely=0.5, anchor="center")
        frame_principal.pack_propagate(False)
        frame_principal.grid_propagate(False)

        try:
            logo_img = ctk.CTkImage(
                light_image=Image.open("assets/logo.png"),
                size=(80, 80)
            )
            label_logo = ctk.CTkLabel(
                frame_principal,
                image=logo_img,
                text=""
            )
            label_logo.image = logo_img
            label_logo.pack(pady=(32, 8))
        except Exception:
            label_logo = ctk.CTkLabel(
                frame_principal,
                text="LARBEM",
                font=("Segoe UI", 20, "bold"),
                text_color="#ec4899"
            )
            label_logo.pack(pady=(32, 8))

        label_titulo = ctk.CTkLabel(
            frame_principal,
            text="Bem-vindo ao BemStock",
            font=("Segoe UI", 24, "bold"),
            text_color=self.cor_texto
        )
        label_titulo.pack(pady=(0, 6))

        label_subtitulo = ctk.CTkLabel(
            frame_principal,
            text="Sistema de Gerenciamento de Estoque",
            font=("Segoe UI", 13),
            text_color=self.cor_texto_secundario
        )
        label_subtitulo.pack(pady=(0, 30))

        frame_form = ctk.CTkFrame(
            frame_principal,
            fg_color="transparent"
        )
        frame_form.pack(pady=(0, 20), padx=24, fill="x")
        frame_form.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            frame_form,
            text="E-mail",
            font=("Segoe UI", 13, "bold"),
            text_color=self.cor_texto,
            anchor="w"
        ).grid(row=0, column=0, sticky="w", pady=(0, 5))

        self.entry_email = ctk.CTkEntry(
            frame_form,
            height=40,
            textvariable=self.email_var,
            placeholder_text="Digite seu e-mail",
            corner_radius=6,
            border_width=1,
            border_color=self.cor_borda,
            fg_color=self.cor_input,
            text_color=self.cor_texto,
            placeholder_text_color="#999999",
            font=("Segoe UI", 14)
        )
        self.entry_email.grid(row=1, column=0, sticky="ew", pady=(0, 16))
        self.entry_email.bind("<FocusIn>", lambda e: self.aplicar_foco(self.entry_email))
        self.entry_email.bind("<FocusOut>", lambda e: self.remover_foco(self.entry_email))
        self.entry_email.bind("<KeyPress>", lambda e: self.entry_email.configure(border_color=self.cor_borda))

        ctk.CTkLabel(
            frame_form,
            text="Senha",
            font=("Segoe UI", 13, "bold"),
            text_color=self.cor_texto,
            anchor="w"
        ).grid(row=2, column=0, sticky="w", pady=(0, 5))

        self.entry_senha = ctk.CTkEntry(
            frame_form,
            height=40,
            textvariable=self.senha_var,
            placeholder_text="Digite sua senha",
            show="●",
            corner_radius=6,
            border_width=1,
            border_color=self.cor_borda,
            fg_color=self.cor_input,
            text_color=self.cor_texto,
            placeholder_text_color="#999999",
            font=("Segoe UI", 14)
        )
        self.entry_senha.grid(row=3, column=0, sticky="ew", pady=(0, 10))
        self.entry_senha.bind("<FocusIn>", lambda e: self.aplicar_foco(self.entry_senha))
        self.entry_senha.bind("<FocusOut>", lambda e: self.remover_foco(self.entry_senha))
        self.entry_senha.bind("<KeyPress>", lambda e: self.entry_senha.configure(border_color=self.cor_borda))
        self.entry_senha.bind("<Return>", self.fazer_login)

        checkbox_mostrar = ctk.CTkCheckBox(
            frame_form,
            text="Mostrar senha",
            variable=self.mostrar_senha_var,
            font=("Segoe UI", 12),
            text_color=self.cor_texto_secundario,
            fg_color=self.cor_roxo,
            hover_color=self.cor_roxo_hover,
            command=self.toggle_senha
        )
        checkbox_mostrar.grid(row=4, column=0, sticky="w", pady=(0, 24))

        self.btn_entrar = ctk.CTkButton(
            frame_form,
            text="Entrar",
            height=45,
            corner_radius=6,
            fg_color=self.cor_roxo,
            hover_color=self.cor_roxo_hover,
            text_color="#ffffff",
            font=("Segoe UI", 14, "bold"),
            command=self.fazer_login
        )
        self.btn_entrar.grid(row=5, column=0, sticky="ew", pady=(0, 14))

        btn_cadastrar = ctk.CTkButton(
            frame_form,
            text="Cadastrar novo usuário",
            height=45,
            corner_radius=6,
            border_width=1,
            border_color="#d0d0d0",
            fg_color="#ffffff",
            hover_color=self.cor_hover_secundario,
            text_color="#1a1a1a",
            font=("Segoe UI", 14, "bold"),
            command=self.abrir_cadastro
        )
        btn_cadastrar.grid(row=6, column=0, sticky="ew")

        self.entry_email.focus()