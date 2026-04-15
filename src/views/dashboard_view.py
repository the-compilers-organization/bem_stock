import customtkinter as ctk
from tkinter import messagebox


def abrir_dashboard(usuario):
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("BemStock - Dashboard")
    app.configure(fg_color="#F5E6F3")

    try:
        app.state("zoomed")
    except Exception:
        app.attributes("-zoomed", True)

    app.resizable(True, True)

    # =========================
    # CORES
    # =========================
    cor_fundo = "#F5E6F3"
    cor_sidebar = "#ffffff"
    cor_card = "#ffffff"
    cor_borda = "#e0e0e0"
    cor_texto = "#1a1a1a"
    cor_texto_secundario = "#666666"
    cor_roxo = "#a855f7"
    cor_roxo_hover = "#9333ea"
    cor_hover_secundario = "#f5f5f5"
    cor_card_info = "#f8f8f8"

    nome_usuario = usuario.get("nome", "Usuário")
    perfil_usuario = usuario.get("perfil", "N/A")

    # =========================
    # FUNÇÕES
    # =========================
    def sair():
        confirmar = messagebox.askyesno("Sair", "Deseja realmente sair do sistema?")
        if confirmar:
            app.destroy()
            from views.login_view import abrir_login
            abrir_login()

    def abrir_produtos():
        messagebox.showinfo("Produtos", "Tela de produtos ainda será conectada.")

    def abrir_movimentacoes():
        messagebox.showinfo("Movimentações", "Tela de movimentações ainda será conectada.")

    def abrir_usuarios():
        messagebox.showinfo("Usuários", "Tela de usuários ainda será conectada.")

    def abrir_relatorios():
        messagebox.showinfo("Relatórios", "Tela de relatórios ainda será conectada.")

    # =========================
    # LAYOUT PRINCIPAL
    # =========================
    frame_sidebar = ctk.CTkFrame(
        app,
        width=260,
        corner_radius=0,
        fg_color=cor_sidebar,
        border_width=1,
        border_color=cor_borda
    )
    frame_sidebar.pack(side="left", fill="y")
    frame_sidebar.pack_propagate(False)

    frame_conteudo = ctk.CTkFrame(
        app,
        fg_color="transparent"
    )
    frame_conteudo.pack(side="left", fill="both", expand=True, padx=20, pady=20)

    # =========================
    # SIDEBAR
    # =========================
    ctk.CTkLabel(
        frame_sidebar,
        text="BemStock",
        font=("Segoe UI", 24, "bold"),
        text_color=cor_roxo
    ).pack(pady=(30, 8))

    ctk.CTkLabel(
        frame_sidebar,
        text="Sistema de Estoque",
        font=("Segoe UI", 13),
        text_color=cor_texto_secundario
    ).pack(pady=(0, 30))

    ctk.CTkLabel(
        frame_sidebar,
        text=f"Usuário: {nome_usuario}",
        font=("Segoe UI", 14, "bold"),
        text_color=cor_texto
    ).pack(anchor="w", padx=20, pady=(0, 5))

    ctk.CTkLabel(
        frame_sidebar,
        text=f"Perfil: {perfil_usuario}",
        font=("Segoe UI", 13),
        text_color=cor_texto_secundario
    ).pack(anchor="w", padx=20, pady=(0, 25))

    btn_dashboard = ctk.CTkButton(
        frame_sidebar,
        text="Dashboard",
        height=42,
        corner_radius=8,
        fg_color=cor_roxo,
        hover_color=cor_roxo_hover,
        text_color="#ffffff",
        font=("Segoe UI", 14, "bold")
    )
    btn_dashboard.pack(fill="x", padx=20, pady=6)

    btn_produtos = ctk.CTkButton(
        frame_sidebar,
        text="Produtos",
        height=42,
        corner_radius=8,
        fg_color="#ffffff",
        hover_color=cor_hover_secundario,
        text_color=cor_texto,
        border_width=1,
        border_color=cor_borda,
        font=("Segoe UI", 14, "bold"),
        command=abrir_produtos
    )
    btn_produtos.pack(fill="x", padx=20, pady=6)

    btn_movimentacoes = ctk.CTkButton(
        frame_sidebar,
        text="Movimentações",
        height=42,
        corner_radius=8,
        fg_color="#ffffff",
        hover_color=cor_hover_secundario,
        text_color=cor_texto,
        border_width=1,
        border_color=cor_borda,
        font=("Segoe UI", 14, "bold"),
        command=abrir_movimentacoes
    )
    btn_movimentacoes.pack(fill="x", padx=20, pady=6)

    if perfil_usuario == "admin":
        btn_usuarios = ctk.CTkButton(
            frame_sidebar,
            text="Usuários",
            height=42,
            corner_radius=8,
            fg_color="#ffffff",
            hover_color=cor_hover_secundario,
            text_color=cor_texto,
            border_width=1,
            border_color=cor_borda,
            font=("Segoe UI", 14, "bold"),
            command=abrir_usuarios
        )
        btn_usuarios.pack(fill="x", padx=20, pady=6)

    btn_relatorios = ctk.CTkButton(
        frame_sidebar,
        text="Relatórios",
        height=42,
        corner_radius=8,
        fg_color="#ffffff",
        hover_color=cor_hover_secundario,
        text_color=cor_texto,
        border_width=1,
        border_color=cor_borda,
        font=("Segoe UI", 14, "bold"),
        command=abrir_relatorios
    )
    btn_relatorios.pack(fill="x", padx=20, pady=6)

    ctk.CTkButton(
        frame_sidebar,
        text="Sair",
        height=42,
        corner_radius=8,
        fg_color="#ffffff",
        hover_color="#fdecec",
        text_color="#b91c1c",
        border_width=1,
        border_color="#efcaca",
        font=("Segoe UI", 14, "bold"),
        command=sair
    ).pack(side="bottom", fill="x", padx=20, pady=25)

    # =========================
    # TOPO DO CONTEÚDO
    # =========================
    frame_topo = ctk.CTkFrame(
        frame_conteudo,
        height=90,
        corner_radius=15,
        fg_color=cor_card,
        border_width=1,
        border_color=cor_borda
    )
    frame_topo.pack(fill="x", pady=(0, 20))
    frame_topo.pack_propagate(False)

    ctk.CTkLabel(
        frame_topo,
        text="Dashboard",
        font=("Segoe UI", 28, "bold"),
        text_color=cor_texto
    ).pack(anchor="w", padx=25, pady=(18, 0))

    ctk.CTkLabel(
        frame_topo,
        text="Visão geral do sistema BemStock",
        font=("Segoe UI", 13),
        text_color=cor_texto_secundario
    ).pack(anchor="w", padx=25, pady=(2, 0))

    # =========================
    # CARDS DE RESUMO
    # =========================
    frame_cards = ctk.CTkFrame(frame_conteudo, fg_color="transparent")
    frame_cards.pack(fill="x", pady=(0, 20))

    frame_cards.grid_columnconfigure((0, 1, 2), weight=1)

    def criar_card(master, coluna, titulo, valor, subtitulo):
        card = ctk.CTkFrame(
            master,
            height=130,
            corner_radius=15,
            fg_color=cor_card,
            border_width=1,
            border_color=cor_borda
        )
        card.grid(row=0, column=coluna, sticky="nsew", padx=10)
        card.pack_propagate(False)

        ctk.CTkLabel(
            card,
            text=titulo,
            font=("Segoe UI", 13, "bold"),
            text_color=cor_texto_secundario
        ).pack(anchor="w", padx=20, pady=(18, 8))

        ctk.CTkLabel(
            card,
            text=str(valor),
            font=("Segoe UI", 30, "bold"),
            text_color=cor_roxo
        ).pack(anchor="w", padx=20)

        ctk.CTkLabel(
            card,
            text=subtitulo,
            font=("Segoe UI", 12),
            text_color=cor_texto_secundario
        ).pack(anchor="w", padx=20, pady=(5, 0))

    criar_card(frame_cards, 0, "Produtos cadastrados", 0, "Total atual no sistema")
    criar_card(frame_cards, 1, "Movimentações hoje", 0, "Entradas e saídas do dia")
    criar_card(frame_cards, 2, "Usuários ativos", 1, "Acessando o sistema")

    # =========================
    # ÁREA CENTRAL
    # =========================
    frame_central = ctk.CTkFrame(
        frame_conteudo,
        corner_radius=15,
        fg_color=cor_card,
        border_width=1,
        border_color=cor_borda
    )
    frame_central.pack(fill="both", expand=True)

    ctk.CTkLabel(
        frame_central,
        text=f"Olá, {nome_usuario} 👋",
        font=("Segoe UI", 24, "bold"),
        text_color=cor_texto
    ).pack(anchor="w", padx=25, pady=(25, 8))

    ctk.CTkLabel(
        frame_central,
        text="Seja bem-vindo(a) ao painel principal do BemStock.",
        font=("Segoe UI", 14),
        text_color=cor_texto_secundario
    ).pack(anchor="w", padx=25)

    frame_acoes = ctk.CTkFrame(frame_central, fg_color="transparent")
    frame_acoes.pack(fill="x", padx=25, pady=(25, 20))

    frame_acoes.grid_columnconfigure((0, 1), weight=1)

    card_atalho_1 = ctk.CTkFrame(
        frame_acoes,
        height=160,
        corner_radius=15,
        fg_color=cor_card_info,
        border_width=1,
        border_color=cor_borda
    )
    card_atalho_1.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
    card_atalho_1.pack_propagate(False)

    ctk.CTkLabel(
        card_atalho_1,
        text="Gerenciar Produtos",
        font=("Segoe UI", 18, "bold"),
        text_color=cor_texto
    ).pack(anchor="w", padx=20, pady=(20, 8))

    ctk.CTkLabel(
        card_atalho_1,
        text="Cadastre, edite e acompanhe os produtos do estoque.",
        font=("Segoe UI", 13),
        text_color=cor_texto_secundario,
        justify="left"
    ).pack(anchor="w", padx=20)

    ctk.CTkButton(
        card_atalho_1,
        text="Abrir Produtos",
        height=40,
        corner_radius=8,
        fg_color=cor_roxo,
        hover_color=cor_roxo_hover,
        text_color="#ffffff",
        font=("Segoe UI", 13, "bold"),
        command=abrir_produtos
    ).pack(anchor="w", padx=20, pady=(18, 0))

    card_atalho_2 = ctk.CTkFrame(
        frame_acoes,
        height=160,
        corner_radius=15,
        fg_color=cor_card_info,
        border_width=1,
        border_color=cor_borda
    )
    card_atalho_2.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
    card_atalho_2.pack_propagate(False)

    ctk.CTkLabel(
        card_atalho_2,
        text="Registrar Movimentações",
        font=("Segoe UI", 18, "bold"),
        text_color=cor_texto
    ).pack(anchor="w", padx=20, pady=(20, 8))

    ctk.CTkLabel(
        card_atalho_2,
        text="Controle entradas e saídas dos itens do estoque.",
        font=("Segoe UI", 13),
        text_color=cor_texto_secundario,
        justify="left"
    ).pack(anchor="w", padx=20)

    ctk.CTkButton(
        card_atalho_2,
        text="Abrir Movimentações",
        height=40,
        corner_radius=8,
        fg_color=cor_roxo,
        hover_color=cor_roxo_hover,
        text_color="#ffffff",
        font=("Segoe UI", 13, "bold"),
        command=abrir_movimentacoes
    ).pack(anchor="w", padx=20, pady=(18, 0))

    frame_info = ctk.CTkFrame(
        frame_central,
        corner_radius=12,
        fg_color="#fcfcfc",
        border_width=1,
        border_color=cor_borda
    )
    frame_info.pack(fill="x", padx=25, pady=(0, 25))

    ctk.CTkLabel(
        frame_info,
        text="Informações do usuário logado",
        font=("Segoe UI", 15, "bold"),
        text_color=cor_texto
    ).pack(anchor="w", padx=20, pady=(18, 10))

    ctk.CTkLabel(
        frame_info,
        text=f"Nome: {nome_usuario}",
        font=("Segoe UI", 13),
        text_color=cor_texto_secundario
    ).pack(anchor="w", padx=20, pady=2)

    ctk.CTkLabel(
        frame_info,
        text=f"Perfil: {perfil_usuario}",
        font=("Segoe UI", 13),
        text_color=cor_texto_secundario
    ).pack(anchor="w", padx=20, pady=(2, 18))

    app.mainloop()