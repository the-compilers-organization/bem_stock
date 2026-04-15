import re
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image

from controllers.login_controller import autenticar_usuario


def abrir_login():
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("BemStock - Login")
    app.configure(fg_color="#F5E6F3")

    try:
        app.state("zoomed")
    except Exception:
        app.attributes("-zoomed", True)

    app.resizable(True, True)

    cor_card = "#ffffff"
    cor_borda = "#d0d0d0"
    cor_foco = "#C084FC"
    cor_erro = "#dc2626"
    cor_texto = "#1a1a1a"
    cor_texto_secundario = "#666666"
    cor_input = "#f8f8f8"
    cor_roxo = "#a855f7"
    cor_roxo_hover = "#9333ea"
    cor_hover_secundario = "#f5f5f5"

    email_var = ctk.StringVar()
    senha_var = ctk.StringVar()
    mostrar_senha_var = ctk.BooleanVar(value=False)

    def aplicar_foco(widget):
        widget.configure(border_color=cor_foco)

    def remover_foco(widget):
        widget.configure(border_color=cor_borda)

    def limpar_erros():
        entry_email.configure(border_color=cor_borda)
        entry_senha.configure(border_color=cor_borda)

    def validar_campos_vazios():
        email = email_var.get().strip()
        senha = senha_var.get()

        if not email:
            entry_email.configure(border_color=cor_erro)
            messagebox.showerror("Erro", "Por favor, digite seu e-mail.")
            entry_email.focus()
            return False

        if not senha:
            entry_senha.configure(border_color=cor_erro)
            messagebox.showerror("Erro", "Por favor, digite sua senha.")
            entry_senha.focus()
            return False

        return True

    def validar_email_local(email):
        padrao = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(padrao, email):
            entry_email.configure(border_color=cor_erro)
            messagebox.showerror("Erro", "E-mail inválido.")
            entry_email.focus()
            return False
        return True

    def toggle_senha():
        entry_senha.configure(show="" if mostrar_senha_var.get() else "●")

    def abrir_cadastro():
        app.destroy()
        from views.cadastro_usuario_view import abrir_cadastro_usuario
        abrir_cadastro_usuario()

    def abrir_sistema_principal(usuario):
        nome = usuario.get("nome", "usuário")
        perfil = usuario.get("perfil", "")
        messagebox.showinfo(
            "Login realizado",
            f"Bem-vindo(a), {nome}!\nPerfil: {perfil}\n\nA tela principal ainda não foi conectada."
        )

    def fazer_login(event=None):
        limpar_erros()

        if not validar_campos_vazios():
            return

        email = email_var.get().strip().lower()
        senha = senha_var.get()

        if not validar_email_local(email):
            return

        btn_entrar.configure(state="disabled", text="Verificando...")
        app.update_idletasks()

        try:
            sucesso, resultado = autenticar_usuario(email, senha)

            if sucesso:
                usuario = resultado
                nome_usuario = usuario.get("nome", "usuário")
                messagebox.showinfo("Sucesso", f"Bem-vindo(a), {nome_usuario}!")
                app.destroy()
                abrir_sistema_principal(usuario)
            else:
                mensagem = resultado
                entry_email.configure(border_color=cor_erro)
                entry_senha.configure(border_color=cor_erro)
                messagebox.showerror("Erro de Login", mensagem)
                btn_entrar.configure(state="normal", text="Entrar")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao realizar login: {str(e)}")
            btn_entrar.configure(state="normal", text="Entrar")

    app.bind("<Return>", fazer_login)

    frame_principal = ctk.CTkFrame(
        app,
        width=640,
        height=600,
        corner_radius=15,
        border_width=1,
        border_color="#e0e0e0",
        fg_color=cor_card
    )
    frame_principal.place(relx=0.5, rely=0.5, anchor="center")

    try:
        logo_img = ctk.CTkImage(
            light_image=Image.open("assets/logo.png"),
            size=(80, 80)
        )
        label_logo = ctk.CTkLabel(frame_principal, image=logo_img, text="")
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
        text="Bem-vindo ao BemStock",
        font=("Segoe UI", 24, "bold"),
        text_color=cor_texto
    )
    label_titulo.pack(pady=(0, 5))

    label_subtitulo = ctk.CTkLabel(
        frame_principal,
        text="Sistema de Gerenciamento de Estoque",
        font=("Segoe UI", 13),
        text_color=cor_texto_secundario
    )
    label_subtitulo.pack(pady=(0, 20))

    frame_form = ctk.CTkFrame(frame_principal, fg_color="transparent")
    frame_form.pack(pady=(0, 20), padx=24, fill="x")

    frame_form.grid_columnconfigure(0, weight=1)

    ctk.CTkLabel(
        frame_form,
        text="E-mail",
        font=("Segoe UI", 13, "bold"),
        text_color=cor_texto,
        anchor="w"
    ).grid(row=0, column=0, sticky="w", pady=(0, 5))

    entry_email = ctk.CTkEntry(
        frame_form,
        width=560,
        height=40,
        textvariable=email_var,
        placeholder_text="Digite seu e-mail",
        corner_radius=6,
        border_width=1,
        border_color=cor_borda,
        fg_color=cor_input,
        text_color=cor_texto,
        placeholder_text_color="#999999",
        font=("Segoe UI", 14)
    )
    entry_email.grid(row=1, column=0, sticky="ew", pady=(0, 16))
    entry_email.bind("<FocusIn>", lambda e: aplicar_foco(entry_email))
    entry_email.bind("<FocusOut>", lambda e: remover_foco(entry_email))
    entry_email.bind("<KeyPress>", lambda e: entry_email.configure(border_color=cor_borda))

    ctk.CTkLabel(
        frame_form,
        text="Senha",
        font=("Segoe UI", 13, "bold"),
        text_color=cor_texto,
        anchor="w"
    ).grid(row=2, column=0, sticky="w", pady=(0, 5))

    entry_senha = ctk.CTkEntry(
        frame_form,
        width=560,
        height=40,
        textvariable=senha_var,
        placeholder_text="Digite sua senha",
        show="●",
        corner_radius=6,
        border_width=1,
        border_color=cor_borda,
        fg_color=cor_input,
        text_color=cor_texto,
        placeholder_text_color="#999999",
        font=("Segoe UI", 14)
    )
    entry_senha.grid(row=3, column=0, sticky="ew", pady=(0, 10))
    entry_senha.bind("<FocusIn>", lambda e: aplicar_foco(entry_senha))
    entry_senha.bind("<FocusOut>", lambda e: remover_foco(entry_senha))
    entry_senha.bind("<KeyPress>", lambda e: entry_senha.configure(border_color=cor_borda))
    entry_senha.bind("<Return>", fazer_login)

    checkbox_mostrar = ctk.CTkCheckBox(
        frame_form,
        text="Mostrar senha",
        variable=mostrar_senha_var,
        font=("Segoe UI", 12),
        text_color=cor_texto_secundario,
        fg_color=cor_roxo,
        hover_color=cor_roxo_hover,
        command=toggle_senha
    )
    checkbox_mostrar.grid(row=4, column=0, sticky="w", pady=(0, 24))

    btn_entrar = ctk.CTkButton(
        frame_form,
        text="Entrar",
        height=45,
        corner_radius=6,
        fg_color=cor_roxo,
        hover_color=cor_roxo_hover,
        text_color="#ffffff",
        font=("Segoe UI", 14, "bold"),
        cursor="hand2",
        command=fazer_login
    )
    btn_entrar.grid(row=5, column=0, sticky="ew", pady=(0, 14))

    btn_cadastrar = ctk.CTkButton(
        frame_form,
        text="Cadastrar novo usuário",
        height=45,
        corner_radius=6,
        border_width=1,
        border_color="#d0d0d0",
        fg_color="#ffffff",
        hover_color=cor_hover_secundario,
        text_color="#1a1a1a",
        font=("Segoe UI", 14, "bold"),
        cursor="hand2",
        command=abrir_cadastro
    )
    btn_cadastrar.grid(row=6, column=0, sticky="ew")

    entry_email.focus()
    app.mainloop()