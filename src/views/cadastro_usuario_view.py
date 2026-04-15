import re
import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image

from controllers.usuario_controller import cadastrar_usuario


def abrir_cadastro_usuario():
    ctk.set_appearance_mode("light")

    app = ctk.CTk()
    app.title("BemStock - Cadastro de Usuário")
    app.configure(fg_color="#F5E6F3")

    try:
        app.state("zoomed")
    except Exception:
        app.attributes("-zoomed", True)

    app.resizable(True, True)

    senha_visivel = False
    confirmar_visivel = False
    dropdown_aberto = False
    dropdown_menu = None

    cor_input = "#f8f8f8"
    cor_borda = "#d0d0d0"
    cor_foco = "#C084FC"
    cor_texto = "#1a1a1a"
    cor_placeholder = "#666666"
    cor_erro = "#dc2626"
    cor_hover = "#f0f0f0"

    nivel_var = ctk.StringVar(value="Selecione o nível de acesso")

    def validar_email(email):
        padrao = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"
        return re.match(padrao, email) is not None

    def aplicar_foco(widget):
        widget.configure(border_color=cor_foco)

    def remover_foco(widget):
        widget.configure(border_color=cor_borda)

    def registrar_foco(widget):
        widget.bind("<FocusIn>", lambda event: aplicar_foco(widget))
        widget.bind("<FocusOut>", lambda event: remover_foco(widget))

    def limpar_erros_visuais():
        entry_nome.configure(border_color=cor_borda)
        entry_email.configure(border_color=cor_borda)
        entry_senha.configure(border_color=cor_borda)
        entry_confirmar.configure(border_color=cor_borda)
        frame_select.configure(border_color=cor_borda)

    def marcar_erro(widget):
        widget.configure(border_color=cor_erro)

    def alternar_senha():
        nonlocal senha_visivel
        senha_visivel = not senha_visivel
        entry_senha.configure(show="" if senha_visivel else "●")
        botao_senha.configure(text="🙈" if senha_visivel else "👁")

    def alternar_confirmar():
        nonlocal confirmar_visivel
        confirmar_visivel = not confirmar_visivel
        entry_confirmar.configure(show="" if confirmar_visivel else "●")
        botao_confirmar.configure(text="🙈" if confirmar_visivel else "👁")

    def fechar_dropdown():
        nonlocal dropdown_aberto, dropdown_menu

        if dropdown_menu is not None:
            try:
                dropdown_menu.destroy()
            except Exception:
                pass
            dropdown_menu = None

        dropdown_aberto = False
        botao_seta.configure(text="▼")
        frame_select.configure(border_color=cor_borda)

    def selecionar_opcao(opcao):
        nivel_var.set(opcao)
        label_select.configure(text=opcao, text_color=cor_texto)
        fechar_dropdown()

    def abrir_dropdown():
        nonlocal dropdown_aberto, dropdown_menu

        if dropdown_aberto:
            return

        app.update_idletasks()

        x = frame_select.winfo_rootx()
        y = frame_select.winfo_rooty() + frame_select.winfo_height() + 4
        largura_dropdown = frame_select.winfo_width()

        opcoes = [
            "Administrador",
            "Responsável pelo Estoque"
        ]
        altura_dropdown = (len(opcoes) * 34) + 8

        dropdown_menu = tk.Toplevel(app)
        dropdown_menu.overrideredirect(True)
        dropdown_menu.attributes("-topmost", True)
        dropdown_menu.geometry(f"{largura_dropdown}x{altura_dropdown}+{x}+{y}")
        dropdown_menu.configure(bg=cor_borda)

        container = tk.Frame(
            dropdown_menu,
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
                fg=cor_texto,
                padx=10,
                pady=8,
                font=("Segoe UI", 11)
            )
            item.pack(fill="x")

            item.bind("<Enter>", lambda e, w=item: w.configure(bg=cor_hover))
            item.bind("<Leave>", lambda e, w=item: w.configure(bg="#ffffff"))
            item.bind("<Button-1>", lambda e, texto=opcao: selecionar_opcao(texto))

        dropdown_aberto = True
        botao_seta.configure(text="▲")
        frame_select.configure(border_color=cor_foco)

    def toggle_dropdown(event=None):
        if dropdown_aberto:
            fechar_dropdown()
        else:
            abrir_dropdown()
        return "break"

    def clique_global(event):
        nonlocal dropdown_aberto

        if not dropdown_aberto or dropdown_menu is None:
            return

        widget = event.widget

        if widget in (frame_select, label_select, botao_seta):
            return

        parent = widget
        while parent is not None:
            if str(parent) == str(dropdown_menu):
                return
            try:
                parent = parent.master
            except Exception:
                parent = None

        fechar_dropdown()

    def voltar():
        fechar_dropdown()
        app.destroy()
        from views.login_view import abrir_login
        abrir_login()

    def limpar():
        entry_nome.delete(0, "end")
        entry_email.delete(0, "end")
        entry_senha.delete(0, "end")
        entry_confirmar.delete(0, "end")
        nivel_var.set("Selecione o nível de acesso")
        label_select.configure(
            text="Selecione o nível de acesso",
            text_color=cor_placeholder
        )
        fechar_dropdown()
        limpar_erros_visuais()
        entry_nome.focus()

    def cadastrar(event=None):
        limpar_erros_visuais()
        fechar_dropdown()

        nome = entry_nome.get().strip()
        email = entry_email.get().strip().lower()
        senha = entry_senha.get()
        confirmar = entry_confirmar.get()
        nivel_exibicao = nivel_var.get()

        if not nome:
            marcar_erro(entry_nome)
            messagebox.showerror("Erro", "Preencha o nome completo.")
            entry_nome.focus()
            return

        if not email:
            marcar_erro(entry_email)
            messagebox.showerror("Erro", "Preencha o e-mail.")
            entry_email.focus()
            return

        if not validar_email(email):
            marcar_erro(entry_email)
            messagebox.showerror("Erro", "Digite um e-mail válido.")
            entry_email.focus()
            return

        if not senha:
            marcar_erro(entry_senha)
            messagebox.showerror("Erro", "Preencha a senha.")
            entry_senha.focus()
            return

        if len(senha) < 6:
            marcar_erro(entry_senha)
            messagebox.showerror("Erro", "A senha deve ter no mínimo 6 caracteres.")
            entry_senha.focus()
            return

        if not confirmar:
            marcar_erro(entry_confirmar)
            messagebox.showerror("Erro", "Confirme a senha.")
            entry_confirmar.focus()
            return

        if senha != confirmar:
            marcar_erro(entry_senha)
            marcar_erro(entry_confirmar)
            messagebox.showerror("Erro", "As senhas não coincidem.")
            entry_confirmar.focus()
            return

        if nivel_exibicao == "Selecione o nível de acesso":
            marcar_erro(frame_select)
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
            limpar()
        else:
            messagebox.showerror(
                "Erro",
                mensagem if mensagem else "Não foi possível cadastrar o usuário."
            )

    app.bind("<Return>", cadastrar)
    app.bind("<Button-1>", clique_global)

    frame_principal = ctk.CTkFrame(
        app,
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
        text_color=cor_texto
    )
    label_titulo.pack(pady=(0, 5))

    label_subtitulo = ctk.CTkLabel(
        frame_principal,
        text="Sistema BemStock - Lar Bem",
        font=("Segoe UI", 13),
        text_color=cor_placeholder
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
        text_color=cor_texto,
        anchor="w"
    ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 5))

    entry_nome = ctk.CTkEntry(
        frame_form,
        width=560,
        height=40,
        placeholder_text="Digite o nome completo",
        corner_radius=6,
        border_width=1,
        border_color=cor_borda,
        fg_color=cor_input,
        text_color=cor_texto,
        placeholder_text_color=cor_placeholder,
        font=("Segoe UI", 14)
    )
    entry_nome.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 15))
    registrar_foco(entry_nome)

    ctk.CTkLabel(
        frame_form,
        text="E-mail*",
        font=("Segoe UI", 13, "bold"),
        text_color=cor_texto,
        anchor="w"
    ).grid(row=2, column=0, columnspan=2, sticky="w", pady=(0, 5))

    entry_email = ctk.CTkEntry(
        frame_form,
        width=560,
        height=40,
        placeholder_text="Digite o e-mail",
        corner_radius=6,
        border_width=1,
        border_color=cor_borda,
        fg_color=cor_input,
        text_color=cor_texto,
        placeholder_text_color=cor_placeholder,
        font=("Segoe UI", 14)
    )
    entry_email.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 15))
    registrar_foco(entry_email)

    ctk.CTkLabel(
        frame_form,
        text="Senha*",
        font=("Segoe UI", 13, "bold"),
        text_color=cor_texto,
        anchor="w"
    ).grid(row=4, column=0, sticky="w", pady=(0, 5), padx=(0, 7))

    ctk.CTkLabel(
        frame_form,
        text="Confirmar Senha*",
        font=("Segoe UI", 13, "bold"),
        text_color=cor_texto,
        anchor="w"
    ).grid(row=4, column=1, sticky="w", pady=(0, 5), padx=(7, 0))

    frame_senha = ctk.CTkFrame(frame_form, fg_color="transparent")
    frame_senha.grid(row=5, column=0, sticky="ew", pady=(0, 15), padx=(0, 7))
    frame_senha.grid_columnconfigure(0, weight=1)

    entry_senha = ctk.CTkEntry(
        frame_senha,
        height=40,
        placeholder_text="Mínimo 6 caracteres",
        show="●",
        corner_radius=6,
        border_width=1,
        border_color=cor_borda,
        fg_color=cor_input,
        text_color=cor_texto,
        placeholder_text_color=cor_placeholder,
        font=("Segoe UI", 14)
    )
    entry_senha.grid(row=0, column=0, sticky="ew")
    registrar_foco(entry_senha)

    botao_senha = ctk.CTkButton(
        frame_senha,
        text="👁",
        width=40,
        height=40,
        corner_radius=6,
        fg_color=cor_input,
        hover_color=cor_hover,
        text_color=cor_texto,
        border_width=1,
        border_color=cor_borda,
        command=alternar_senha
    )
    botao_senha.grid(row=0, column=1, padx=(8, 0))

    frame_confirmar = ctk.CTkFrame(frame_form, fg_color="transparent")
    frame_confirmar.grid(row=5, column=1, sticky="ew", pady=(0, 15), padx=(7, 0))
    frame_confirmar.grid_columnconfigure(0, weight=1)

    entry_confirmar = ctk.CTkEntry(
        frame_confirmar,
        height=40,
        placeholder_text="Digite a senha novamente",
        show="●",
        corner_radius=6,
        border_width=1,
        border_color=cor_borda,
        fg_color=cor_input,
        text_color=cor_texto,
        placeholder_text_color=cor_placeholder,
        font=("Segoe UI", 14)
    )
    entry_confirmar.grid(row=0, column=0, sticky="ew")
    registrar_foco(entry_confirmar)

    botao_confirmar = ctk.CTkButton(
        frame_confirmar,
        text="👁",
        width=40,
        height=40,
        corner_radius=6,
        fg_color=cor_input,
        hover_color=cor_hover,
        text_color=cor_texto,
        border_width=1,
        border_color=cor_borda,
        command=alternar_confirmar
    )
    botao_confirmar.grid(row=0, column=1, padx=(8, 0))

    ctk.CTkLabel(
        frame_form,
        text="Nível de Acesso*",
        font=("Segoe UI", 13, "bold"),
        text_color=cor_texto,
        anchor="w"
    ).grid(row=6, column=0, columnspan=2, sticky="w", pady=(0, 5))

    frame_select = ctk.CTkFrame(
        frame_form,
        height=40,
        corner_radius=6,
        border_width=1,
        border_color=cor_borda,
        fg_color=cor_input
    )
    frame_select.grid(row=7, column=0, columnspan=2, sticky="ew", pady=(0, 20))
    frame_select.grid_propagate(False)
    frame_select.grid_columnconfigure(0, weight=1)
    frame_select.grid_columnconfigure(1, weight=0)

    label_select = ctk.CTkLabel(
        frame_select,
        text="Selecione o nível de acesso",
        font=("Segoe UI", 14),
        text_color=cor_placeholder,
        anchor="w",
        fg_color="transparent"
    )
    label_select.grid(row=0, column=0, sticky="ew", padx=(12, 0), pady=1)

    botao_seta = ctk.CTkLabel(
        frame_select,
        text="▼",
        font=("Segoe UI", 12),
        text_color=cor_texto,
        fg_color="transparent",
        width=30
    )
    botao_seta.grid(row=0, column=1, padx=(0, 10), pady=1)

    frame_select.bind("<Button-1>", toggle_dropdown)
    label_select.bind("<Button-1>", toggle_dropdown)
    botao_seta.bind("<Button-1>", toggle_dropdown)

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
        command=voltar
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
        command=cadastrar
    )
    btn_cadastrar.grid(row=0, column=1, padx=(7, 0))

    entry_nome.focus()
    app.mainloop()