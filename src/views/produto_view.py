import customtkinter as ctk
from tkinter import messagebox

from controllers.produto_controller import (
    listar_produtos,
    buscar_produtos_por_nome,
    filtrar_produtos_por_categoria,
    excluir_produto
)


class ProdutoView(ctk.CTkFrame):
    def __init__(self, master, usuario):
        super().__init__(master, fg_color="#F5E6F3")
        self.master = master
        self.usuario = usuario

        self.cor_sidebar = "#ffffff"
        self.cor_borda = "#e0e0e0"
        self.cor_texto = "#1a1a1a"
        self.cor_texto_secundario = "#6b7280"
        self.cor_roxo = "#a855f7"
        self.cor_roxo_hover = "#9333ea"
        self.cor_hover_secundario = "#f5f5f5"
        self.cor_input = "#f8f8f8"

        self.nome_usuario = self.usuario.get("nome", "Usuário")
        self.perfil_usuario = self.usuario.get("perfil", "N/A")

        self.entry_busca = None
        self.combo_categoria = None
        self.lista_container = None

        self.colunas_tabela = [
            ("Produto", 330),
            ("Categoria", 150),
            ("Unidade", 150),
            ("Estoque Atual", 140),
            ("Estoque Mínimo", 150),
            ("Status", 160),
            ("Validade", 190),
            ("Ações", 120),
        ]

        self.criar_interface()
        self.carregar_produtos()

    def abrir_dashboard(self):
        self.master.mostrar_dashboard(self.usuario)

    def abrir_movimentacao(self):
        self.master.mostrar_movimentacao(self.usuario)

    def abrir_usuarios(self):
        messagebox.showinfo("Usuários", "Tela de usuários ainda será conectada.")

    def abrir_relatorios(self):
        messagebox.showinfo("Relatórios", "Tela de relatórios ainda será conectada.")

    def sair(self):
        confirmar = messagebox.askyesno("Sair", "Deseja realmente sair do sistema?")
        if confirmar:
            self.master.usuario_logado = None
            self.master.mostrar_login()

    def abrir_cadastro_produto(self):
        self.master.mostrar_cadastro_produto(self.usuario)

    def abrir_edicao_produto(self, produto):
        self.master.mostrar_cadastro_produto(self.usuario, produto)

    def configurar_colunas_grid(self, frame):
        for i, (_, largura) in enumerate(self.colunas_tabela):
            frame.grid_columnconfigure(i, minsize=largura, weight=0)

    def carregar_produtos(self, produtos=None):
        for widget in self.lista_container.winfo_children():
            widget.destroy()

        if produtos is None:
            produtos = listar_produtos()

        if not produtos:
            ctk.CTkLabel(
                self.lista_container,
                text="Nenhum produto encontrado.",
                font=("Segoe UI", 14),
                text_color=self.cor_texto_secundario
            ).pack(pady=20)
            return

        self.criar_cabecalho_tabela()

        for produto in produtos:
            self.criar_linha_produto(produto)

    def criar_cabecalho_tabela(self):
        cabecalho = ctk.CTkFrame(self.lista_container, fg_color="transparent")
        cabecalho.pack(fill="x", padx=12, pady=(0, 8))

        self.configurar_colunas_grid(cabecalho)

        for i, (titulo, _) in enumerate(self.colunas_tabela):
            label = ctk.CTkLabel(
                cabecalho,
                text=titulo,
                font=("Segoe UI", 13, "bold"),
                text_color=self.cor_texto,
                anchor="w"
            )
            label.grid(row=0, column=i, sticky="w", padx=(0, 10))

    def obter_estilo_status(self, produto):
        status = produto.get("status_estoque", "Normal")

        if status == "Normal":
            return "#22c55e", "#ffffff"
        if status == "Baixo":
            return "#f97316", "#ffffff"
        if status == "Próximo ao Mínimo":
            return "#eab308", "#ffffff"
        if status == "Esgotado":
            return "#e11d48", "#ffffff"

        return "#9ca3af", "#ffffff"

    def obter_estilo_validade(self, produto):
        status_validade = produto.get("status_validade", "normal")

        if status_validade == "vencido":
            return "#ef4444", "#ffffff"
        if status_validade == "proximo":
            return "#f59e0b", "#ffffff"

        return None, self.cor_texto

    def formatar_validade(self, produto):
        validade = produto.get("validade_exibicao") or "-"
        dias = produto.get("dias_para_vencer")

        if validade == "Vencido":
            return "Vencido"

        if dias is not None and produto.get("status_validade") == "proximo":
            return f"{validade} ({dias}d)"

        return validade

    def criar_linha_produto(self, produto):
        linha = ctk.CTkFrame(
            self.lista_container,
            fg_color="#ffffff",
            corner_radius=10,
            border_width=1,
            border_color="#eeeeee"
        )
        linha.pack(fill="x", padx=12, pady=6)

        self.configurar_colunas_grid(linha)

        frame_produto = ctk.CTkFrame(linha, fg_color="transparent")
        frame_produto.grid(row=0, column=0, sticky="w", padx=(12, 10), pady=12)

        ctk.CTkLabel(
            frame_produto,
            text=produto.get("nome", "-"),
            font=("Segoe UI", 13, "bold"),
            text_color=self.cor_texto,
            anchor="w"
        ).pack(anchor="w")

        ctk.CTkLabel(
            frame_produto,
            text=produto.get("descricao") or "-",
            font=("Segoe UI", 12),
            text_color=self.cor_texto_secundario,
            anchor="w"
        ).pack(anchor="w")

        ctk.CTkLabel(
            linha,
            text=produto.get("categoria", "-"),
            font=("Segoe UI", 13),
            text_color=self.cor_texto,
            anchor="w"
        ).grid(row=0, column=1, sticky="w", padx=(0, 10), pady=12)

        ctk.CTkLabel(
            linha,
            text=(produto.get("unidade_medida", "-") or "-").title(),
            font=("Segoe UI", 13),
            text_color=self.cor_texto,
            anchor="w"
        ).grid(row=0, column=2, sticky="w", padx=(0, 10), pady=12)

        ctk.CTkLabel(
            linha,
            text=str(produto.get("estoque_atual", 0)),
            font=("Segoe UI", 13, "bold"),
            text_color=self.cor_texto,
            anchor="w"
        ).grid(row=0, column=3, sticky="w", padx=(0, 10), pady=12)

        ctk.CTkLabel(
            linha,
            text=str(produto.get("estoque_minimo", 0)),
            font=("Segoe UI", 13),
            text_color=self.cor_texto,
            anchor="w"
        ).grid(row=0, column=4, sticky="w", padx=(0, 10), pady=12)

        cor_status, cor_texto_status = self.obter_estilo_status(produto)
        frame_status = ctk.CTkFrame(linha, fg_color="transparent")
        frame_status.grid(row=0, column=5, sticky="w", padx=(0, 10), pady=12)

        ctk.CTkLabel(
            frame_status,
            text=produto.get("status_estoque", "Normal"),
            font=("Segoe UI", 12, "bold"),
            text_color=cor_texto_status,
            fg_color=cor_status,
            corner_radius=16,
            width=125,
            height=28
        ).pack(anchor="w")

        cor_validade, cor_texto_validade = self.obter_estilo_validade(produto)
        frame_validade = ctk.CTkFrame(linha, fg_color="transparent")
        frame_validade.grid(row=0, column=6, sticky="w", padx=(0, 10), pady=12)

        texto_validade = self.formatar_validade(produto)

        if cor_validade:
            ctk.CTkLabel(
                frame_validade,
                text=texto_validade,
                font=("Segoe UI", 12, "bold"),
                text_color=cor_texto_validade,
                fg_color=cor_validade,
                corner_radius=16,
                width=150,
                height=28
            ).pack(anchor="w")
        else:
            ctk.CTkLabel(
                frame_validade,
                text=texto_validade,
                font=("Segoe UI", 13),
                text_color=self.cor_texto,
                anchor="w"
            ).pack(anchor="w")

        frame_acoes = ctk.CTkFrame(linha, fg_color="transparent")
        frame_acoes.grid(row=0, column=7, sticky="w", padx=(0, 10), pady=12)

        btn_editar = ctk.CTkButton(
            frame_acoes,
            text="✎",
            width=34,
            height=34,
            corner_radius=8,
            fg_color="#ffffff",
            hover_color="#f3f4f6",
            text_color="#111111",
            border_width=0,
            font=("Segoe UI", 16),
            command=lambda p=produto: self.abrir_edicao_produto(p)
        )
        btn_editar.pack(side="left", padx=(0, 8))

        btn_excluir = ctk.CTkButton(
            frame_acoes,
            text="🗑",
            width=34,
            height=34,
            corner_radius=8,
            fg_color="#ffffff",
            hover_color="#fef2f2",
            text_color="#dc2626",
            border_width=0,
            font=("Segoe UI", 16),
            command=lambda p=produto: self.confirmar_exclusao(p)
        )
        btn_excluir.pack(side="left")

    def confirmar_exclusao(self, produto):
        confirmar = messagebox.askyesno(
            "Excluir produto",
            f"Deseja realmente excluir o produto '{produto.get('nome', '')}'?"
        )
        if not confirmar:
            return

        sucesso, mensagem = excluir_produto(produto["id_produto"])

        if sucesso:
            messagebox.showinfo("Sucesso", mensagem)
            self.carregar_produtos()
        else:
            messagebox.showerror("Erro", mensagem)

    def aplicar_filtros(self):
        termo = self.entry_busca.get().strip()
        categoria = self.combo_categoria.get().strip()

        try:
            produtos = listar_produtos()

            if termo:
                produtos = buscar_produtos_por_nome(termo)

            if categoria and categoria != "Todas":
                produtos = [
                    p for p in produtos
                    if p.get("categoria") == categoria
                ]

            self.carregar_produtos(produtos)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao aplicar filtros: {str(e)}")

    def limpar_filtros(self):
        self.entry_busca.delete(0, "end")
        self.combo_categoria.set("Todas")
        self.carregar_produtos()

    def criar_interface(self):
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

        frame_conteudo = ctk.CTkFrame(self, fg_color="transparent")
        frame_conteudo.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        frame_logo = ctk.CTkFrame(frame_sidebar, fg_color="transparent")
        frame_logo.pack(pady=(25, 20), padx=20, fill="x")
        frame_logo.grid_columnconfigure(1, weight=1)

        try:
            from PIL import Image
            logo_img = ctk.CTkImage(
                light_image=Image.open("assets/logo.png"),
                size=(42, 42)
            )
            label_logo = ctk.CTkLabel(frame_logo, image=logo_img, text="")
            label_logo.image = logo_img
            label_logo.grid(row=0, column=0, rowspan=2, padx=(0, 10))
        except Exception:
            ctk.CTkLabel(
                frame_logo,
                text="LB",
                font=("Segoe UI", 16, "bold"),
                text_color="#ec4899",
                width=42,
                height=42
            ).grid(row=0, column=0, rowspan=2, padx=(0, 10))

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
            fg_color="#ffffff",
            hover_color=self.cor_hover_secundario,
            text_color=self.cor_texto,
            border_width=1,
            border_color=self.cor_borda,
            font=("Segoe UI", 14, "bold"),
            command=self.abrir_dashboard
        ).pack(fill="x", padx=20, pady=6)

        ctk.CTkButton(
            frame_sidebar,
            text="Produtos",
            height=42,
            corner_radius=8,
            fg_color=self.cor_roxo,
            hover_color=self.cor_roxo_hover,
            text_color="#ffffff",
            font=("Segoe UI", 14, "bold")
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
            command=self.abrir_movimentacao
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

        ctk.CTkLabel(
            frame_conteudo,
            text="Produtos",
            font=("Segoe UI", 28, "bold"),
            text_color=self.cor_texto
        ).pack(anchor="w", pady=(0, 10))

        frame_filtros = ctk.CTkFrame(
            frame_conteudo,
            fg_color="#ffffff",
            border_width=1,
            border_color=self.cor_borda,
            corner_radius=15
        )
        frame_filtros.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(
            frame_filtros,
            text="Filtros",
            font=("Segoe UI", 16, "bold"),
            text_color=self.cor_texto
        ).pack(anchor="w", padx=20, pady=(15, 10))

        linha1 = ctk.CTkFrame(frame_filtros, fg_color="transparent")
        linha1.pack(fill="x", padx=20, pady=(0, 15))

        self.entry_busca = ctk.CTkEntry(
            linha1,
            width=280,
            height=40,
            placeholder_text="Buscar por nome do produto",
            corner_radius=6,
            border_width=1,
            border_color="#d0d0d0",
            fg_color=self.cor_input,
            text_color=self.cor_texto,
            font=("Segoe UI", 14)
        )
        self.entry_busca.pack(side="left", padx=(0, 10))

        self.combo_categoria = ctk.CTkComboBox(
            linha1,
            width=220,
            height=40,
            values=["Todas", "Alimentos", "Limpeza", "Higiene Pessoal"],
            corner_radius=6,
            border_width=1,
            border_color="#d0d0d0",
            fg_color=self.cor_input,
            button_color=self.cor_roxo,
            button_hover_color=self.cor_roxo_hover,
            text_color=self.cor_texto,
            dropdown_fg_color="#ffffff",
            dropdown_text_color=self.cor_texto,
            dropdown_hover_color="#f0f0f0",
            font=("Segoe UI", 14)
        )
        self.combo_categoria.pack(side="left", padx=(0, 10))
        self.combo_categoria.set("Todas")

        ctk.CTkButton(
            linha1,
            text="Filtrar",
            width=100,
            height=40,
            corner_radius=6,
            fg_color=self.cor_roxo,
            hover_color=self.cor_roxo_hover,
            text_color="#ffffff",
            font=("Segoe UI", 13, "bold"),
            command=self.aplicar_filtros
        ).pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            linha1,
            text="Limpar",
            width=100,
            height=40,
            corner_radius=6,
            border_width=1,
            border_color="#d0d0d0",
            fg_color="#ffffff",
            hover_color="#f5f5f5",
            text_color="#1a1a1a",
            font=("Segoe UI", 13, "bold"),
            command=self.limpar_filtros
        ).pack(side="left")

        frame_botoes_topo = ctk.CTkFrame(frame_conteudo, fg_color="transparent")
        frame_botoes_topo.pack(fill="x", pady=(0, 15))

        ctk.CTkButton(
            frame_botoes_topo,
            text="← Voltar ao Dashboard",
            width=180,
            height=42,
            corner_radius=8,
            border_width=1,
            border_color=self.cor_borda,
            fg_color="#ffffff",
            hover_color=self.cor_hover_secundario,
            text_color=self.cor_texto,
            font=("Segoe UI", 13, "bold"),
            command=self.abrir_dashboard
        ).pack(side="left")

        ctk.CTkButton(
            frame_botoes_topo,
            text="+ Novo Produto",
            width=180,
            height=42,
            corner_radius=8,
            fg_color=self.cor_roxo,
            hover_color=self.cor_roxo_hover,
            text_color="#ffffff",
            font=("Segoe UI", 13, "bold"),
            command=self.abrir_cadastro_produto
        ).pack(side="right")

        frame_lista = ctk.CTkFrame(
            frame_conteudo,
            fg_color="#ffffff",
            border_width=1,
            border_color=self.cor_borda,
            corner_radius=15
        )
        frame_lista.pack(fill="both", expand=True)

        ctk.CTkLabel(
            frame_lista,
            text="Lista de Produtos",
            font=("Segoe UI", 18, "bold"),
            text_color=self.cor_texto
        ).pack(anchor="w", padx=20, pady=(20, 10))

        scroll = ctk.CTkScrollableFrame(
            frame_lista,
            fg_color="transparent"
        )
        scroll.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.lista_container = scroll