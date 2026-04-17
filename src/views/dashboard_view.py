import customtkinter as ctk
from tkinter import messagebox
from PIL import Image

from controllers.produto_controller import listar_produtos
from controllers.movimentacao_controller import listar_historico


class DashboardView(ctk.CTkFrame):
    def __init__(self, master, usuario):
        super().__init__(master, fg_color="#F5E6F3")
        self.master = master
        self.usuario = usuario

        self.cor_fundo = "#F5E6F3"
        self.cor_sidebar = "#ffffff"
        self.cor_card = "#ffffff"
        self.cor_borda = "#e0e0e0"
        self.cor_texto = "#1a1a1a"
        self.cor_texto_secundario = "#666666"
        self.cor_roxo = "#a855f7"
        self.cor_roxo_hover = "#9333ea"
        self.cor_hover_secundario = "#f5f5f5"
        self.cor_card_info = "#f8f8f8"

        self.nome_usuario = self.usuario.get("nome", "Usuário")
        self.perfil_usuario = self.usuario.get("perfil", "N/A")

        self.criar_interface()

    def sair(self):
        confirmar = messagebox.askyesno("Sair", "Deseja realmente sair do sistema?")
        if confirmar:
            self.master.usuario_logado = None
            self.master.mostrar_login()

    def abrir_produtos(self):
        self.master.mostrar_produto(self.usuario)

    def abrir_movimentacoes(self):
        self.master.mostrar_movimentacao(self.usuario)

    def abrir_usuarios(self):
        messagebox.showinfo("Usuários", "Tela de usuários ainda será conectada.")

    def abrir_relatorios(self):
        messagebox.showinfo("Relatórios", "Tela de relatórios ainda será conectada.")

    def obter_indicadores(self):
        try:
            produtos = listar_produtos()
            historico = listar_historico()

            total_produtos = len(produtos)
            total_movimentacoes = len(historico)

            total_alimentos = len([p for p in produtos if p["categoria"] == "Alimentos"])
            total_limpeza = len([p for p in produtos if p["categoria"] == "Limpeza"])
            total_higiene = len([p for p in produtos if p["categoria"] == "Higiene Pessoal"])

        except Exception:
            total_produtos = 0
            total_movimentacoes = 0
            total_alimentos = 0
            total_limpeza = 0
            total_higiene = 0

        return {
            "total_produtos": total_produtos,
            "total_movimentacoes": total_movimentacoes,
            "total_alimentos": total_alimentos,
            "total_limpeza": total_limpeza,
            "total_higiene": total_higiene
        }

    def criar_card_resumo(self, master, coluna, titulo, valor, subtitulo):
        card = ctk.CTkFrame(
            master,
            height=130,
            corner_radius=15,
            fg_color=self.cor_card,
            border_width=1,
            border_color=self.cor_borda
        )
        card.grid(row=0, column=coluna, sticky="nsew", padx=10)
        card.pack_propagate(False)

        ctk.CTkLabel(
            card,
            text=titulo,
            font=("Segoe UI", 13, "bold"),
            text_color=self.cor_texto_secundario
        ).pack(anchor="w", padx=20, pady=(18, 8))

        ctk.CTkLabel(
            card,
            text=str(valor),
            font=("Segoe UI", 30, "bold"),
            text_color=self.cor_roxo
        ).pack(anchor="w", padx=20)

        ctk.CTkLabel(
            card,
            text=subtitulo,
            font=("Segoe UI", 12),
            text_color=self.cor_texto_secundario
        ).pack(anchor="w", padx=20, pady=(5, 0))

    def criar_interface(self):
        indicadores = self.obter_indicadores()

        frame_sidebar = ctk.CTkFrame(
            self,
            width=260,
            corner_radius=0,
            fg_color=self.cor_sidebar,
            border_width=1,
            border_color=self.cor_borda
        )
        frame_sidebar.pack(side="left", fill="y")
        frame_sidebar.pack_propagate(False)

        frame_conteudo = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        frame_conteudo.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        frame_logo = ctk.CTkFrame(
            frame_sidebar,
            fg_color="transparent"
        )
        frame_logo.pack(pady=(25, 20), padx=20, fill="x")
        frame_logo.grid_columnconfigure(1, weight=1)

        try:
            logo_img = ctk.CTkImage(
                light_image=Image.open("assets/logo.png"),
                size=(42, 42)
            )
            label_logo = ctk.CTkLabel(
                frame_logo,
                image=logo_img,
                text=""
            )
            label_logo.image = logo_img
            label_logo.grid(row=0, column=0, rowspan=2, padx=(0, 10))
        except Exception:
            label_logo = ctk.CTkLabel(
                frame_logo,
                text="LB",
                font=("Segoe UI", 16, "bold"),
                text_color="#ec4899",
                width=42,
                height=42
            )
            label_logo.grid(row=0, column=0, rowspan=2, padx=(0, 10))

        ctk.CTkLabel(
            frame_logo,
            text="BemStock",
            font=("Segoe UI", 18, "bold"),
            text_color=self.cor_roxo
        ).grid(row=0, column=1, sticky="w")

        ctk.CTkLabel(
            frame_logo,
            text="Sistema de Estoque",
            font=("Segoe UI", 12),
            text_color=self.cor_texto_secundario
        ).grid(row=1, column=1, sticky="w")

        ctk.CTkLabel(
            frame_sidebar,
            text=f"Usuário: {self.nome_usuario}",
            font=("Segoe UI", 14, "bold"),
            text_color=self.cor_texto
        ).pack(anchor="w", padx=20, pady=(0, 5))

        ctk.CTkLabel(
            frame_sidebar,
            text=f"Perfil: {self.perfil_usuario}",
            font=("Segoe UI", 13),
            text_color=self.cor_texto_secundario
        ).pack(anchor="w", padx=20, pady=(0, 25))

        ctk.CTkButton(
            frame_sidebar,
            text="Dashboard",
            height=42,
            corner_radius=8,
            fg_color=self.cor_roxo,
            hover_color=self.cor_roxo_hover,
            text_color="#ffffff",
            font=("Segoe UI", 14, "bold")
        ).pack(fill="x", padx=20, pady=6)

        ctk.CTkButton(
            frame_sidebar,
            text="Produtos",
            height=42,
            corner_radius=8,
            fg_color="#ffffff",
            hover_color=self.cor_hover_secundario,
            text_color=self.cor_texto,
            border_width=1,
            border_color=self.cor_borda,
            font=("Segoe UI", 14, "bold"),
            command=self.abrir_produtos
        ).pack(fill="x", padx=20, pady=6)

        ctk.CTkButton(
            frame_sidebar,
            text="Movimentações",
            height=42,
            corner_radius=8,
            fg_color="#ffffff",
            hover_color=self.cor_hover_secundario,
            text_color=self.cor_texto,
            border_width=1,
            border_color=self.cor_borda,
            font=("Segoe UI", 14, "bold"),
            command=self.abrir_movimentacoes
        ).pack(fill="x", padx=20, pady=6)

        if self.perfil_usuario == "admin":
            ctk.CTkButton(
                frame_sidebar,
                text="Usuários",
                height=42,
                corner_radius=8,
                fg_color="#ffffff",
                hover_color=self.cor_hover_secundario,
                text_color=self.cor_texto,
                border_width=1,
                border_color=self.cor_borda,
                font=("Segoe UI", 14, "bold"),
                command=self.abrir_usuarios
            ).pack(fill="x", padx=20, pady=6)

        ctk.CTkButton(
            frame_sidebar,
            text="Relatórios",
            height=42,
            corner_radius=8,
            fg_color="#ffffff",
            hover_color=self.cor_hover_secundario,
            text_color=self.cor_texto,
            border_width=1,
            border_color=self.cor_borda,
            font=("Segoe UI", 14, "bold"),
            command=self.abrir_relatorios
        ).pack(fill="x", padx=20, pady=6)

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
            command=self.sair
        ).pack(side="bottom", fill="x", padx=20, pady=25)

        frame_topo = ctk.CTkFrame(
            frame_conteudo,
            height=90,
            corner_radius=15,
            fg_color=self.cor_card,
            border_width=1,
            border_color=self.cor_borda
        )
        frame_topo.pack(fill="x", pady=(0, 20))
        frame_topo.pack_propagate(False)

        ctk.CTkLabel(
            frame_topo,
            text="Dashboard",
            font=("Segoe UI", 28, "bold"),
            text_color=self.cor_texto
        ).pack(anchor="w", padx=25, pady=(18, 0))

        ctk.CTkLabel(
            frame_topo,
            text="Visão geral do sistema BemStock",
            font=("Segoe UI", 13),
            text_color=self.cor_texto_secundario
        ).pack(anchor="w", padx=25, pady=(2, 0))

        frame_cards = ctk.CTkFrame(frame_conteudo, fg_color="transparent")
        frame_cards.pack(fill="x", pady=(0, 20))

        frame_cards.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.criar_card_resumo(
            frame_cards, 0,
            "Produtos cadastrados",
            indicadores["total_produtos"],
            "Total atual no sistema"
        )
        self.criar_card_resumo(
            frame_cards, 1,
            "Movimentações",
            indicadores["total_movimentacoes"],
            "Registros realizados"
        )
        self.criar_card_resumo(
            frame_cards, 2,
            "Alimentos",
            indicadores["total_alimentos"],
            "Produtos dessa categoria"
        )
        self.criar_card_resumo(
            frame_cards, 3,
            "Limpeza + Higiene",
            indicadores["total_limpeza"] + indicadores["total_higiene"],
            "Produtos cadastrados"
        )

        frame_central = ctk.CTkFrame(
            frame_conteudo,
            corner_radius=15,
            fg_color=self.cor_card,
            border_width=1,
            border_color=self.cor_borda
        )
        frame_central.pack(fill="both", expand=True)

        ctk.CTkLabel(
            frame_central,
            text=f"Olá, {self.nome_usuario} 👋",
            font=("Segoe UI", 24, "bold"),
            text_color=self.cor_texto
        ).pack(anchor="w", padx=25, pady=(25, 8))

        ctk.CTkLabel(
            frame_central,
            text="Seja bem-vindo(a) ao painel principal do BemStock.",
            font=("Segoe UI", 14),
            text_color=self.cor_texto_secundario
        ).pack(anchor="w", padx=25)

        frame_acoes = ctk.CTkFrame(frame_central, fg_color="transparent")
        frame_acoes.pack(fill="x", padx=25, pady=(25, 20))
        frame_acoes.grid_columnconfigure((0, 1), weight=1)

        card_atalho_1 = ctk.CTkFrame(
            frame_acoes,
            height=160,
            corner_radius=15,
            fg_color=self.cor_card_info,
            border_width=1,
            border_color=self.cor_borda
        )
        card_atalho_1.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        card_atalho_1.pack_propagate(False)

        ctk.CTkLabel(
            card_atalho_1,
            text="Gerenciar Produtos",
            font=("Segoe UI", 18, "bold"),
            text_color=self.cor_texto
        ).pack(anchor="w", padx=20, pady=(20, 8))

        ctk.CTkLabel(
            card_atalho_1,
            text="Cadastre, edite e acompanhe os produtos do sistema.",
            font=("Segoe UI", 13),
            text_color=self.cor_texto_secundario,
            justify="left"
        ).pack(anchor="w", padx=20)

        ctk.CTkButton(
            card_atalho_1,
            text="Abrir Produtos",
            height=40,
            corner_radius=8,
            fg_color=self.cor_roxo,
            hover_color=self.cor_roxo_hover,
            text_color="#ffffff",
            font=("Segoe UI", 13, "bold"),
            command=self.abrir_produtos
        ).pack(anchor="w", padx=20, pady=(18, 0))

        card_atalho_2 = ctk.CTkFrame(
            frame_acoes,
            height=160,
            corner_radius=15,
            fg_color=self.cor_card_info,
            border_width=1,
            border_color=self.cor_borda
        )
        card_atalho_2.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        card_atalho_2.pack_propagate(False)

        ctk.CTkLabel(
            card_atalho_2,
            text="Registrar Movimentações",
            font=("Segoe UI", 18, "bold"),
            text_color=self.cor_texto
        ).pack(anchor="w", padx=20, pady=(20, 8))

        ctk.CTkLabel(
            card_atalho_2,
            text=(
                f"Total de movimentações: {indicadores['total_movimentacoes']}\n"
                f"Alimentos cadastrados: {indicadores['total_alimentos']}\n"
                f"Limpeza: {indicadores['total_limpeza']} | Higiene: {indicadores['total_higiene']}"
            ),
            font=("Segoe UI", 13),
            text_color=self.cor_texto_secundario,
            justify="left"
        ).pack(anchor="w", padx=20)

        ctk.CTkButton(
            card_atalho_2,
            text="Abrir Movimentações",
            height=40,
            corner_radius=8,
            fg_color=self.cor_roxo,
            hover_color=self.cor_roxo_hover,
            text_color="#ffffff",
            font=("Segoe UI", 13, "bold"),
            command=self.abrir_movimentacoes
        ).pack(anchor="w", padx=20, pady=(18, 0))

        frame_info = ctk.CTkFrame(
            frame_central,
            corner_radius=12,
            fg_color="#fcfcfc",
            border_width=1,
            border_color=self.cor_borda
        )
        frame_info.pack(fill="x", padx=25, pady=(0, 25))

        ctk.CTkLabel(
            frame_info,
            text="Informações do usuário logado",
            font=("Segoe UI", 15, "bold"),
            text_color=self.cor_texto
        ).pack(anchor="w", padx=20, pady=(18, 10))

        ctk.CTkLabel(
            frame_info,
            text=f"Nome: {self.nome_usuario}",
            font=("Segoe UI", 13),
            text_color=self.cor_texto_secundario
        ).pack(anchor="w", padx=20, pady=2)

        ctk.CTkLabel(
            frame_info,
            text=f"Perfil: {self.perfil_usuario}",
            font=("Segoe UI", 13),
            text_color=self.cor_texto_secundario
        ).pack(anchor="w", padx=20, pady=(2, 18))