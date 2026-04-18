import customtkinter as ctk
from tkinter import messagebox

from controllers.usuario_controller import (
    listar_usuarios,
    buscar_usuarios_por_nome,
    buscar_usuarios_por_email,
    excluir_usuario
)


class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.after_id = None

        self.widget.bind("<Enter>", self.agendar_exibicao, add="+")
        self.widget.bind("<Leave>", self.esconder_tooltip, add="+")
        self.widget.bind("<ButtonPress>", self.esconder_tooltip, add="+")
        self.widget.bind("<Destroy>", self.esconder_tooltip, add="+")

    def agendar_exibicao(self, event=None):
        self.cancelar_agendamento()
        self.after_id = self.widget.after(300, self.mostrar_tooltip)

    def cancelar_agendamento(self):
        if self.after_id is not None:
            try:
                self.widget.after_cancel(self.after_id)
            except Exception:
                pass
            self.after_id = None

    def mostrar_tooltip(self):
        if self.tooltip_window is not None:
            return

        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 6

        self.tooltip_window = tw = ctk.CTkToplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.attributes("-topmost", True)
        tw.geometry(f"+{x}+{y}")

        label = ctk.CTkLabel(
            tw,
            text=self.text,
            fg_color="#1f2937",
            text_color="#ffffff",
            corner_radius=8,
            padx=10,
            pady=5,
            font=("Segoe UI", 12)
        )
        label.pack()

        tw.bind("<Leave>", self.esconder_tooltip)
        tw.bind("<ButtonPress>", self.esconder_tooltip)

    def esconder_tooltip(self, event=None):
        self.cancelar_agendamento()

        if self.tooltip_window is not None:
            try:
                self.tooltip_window.destroy()
            except Exception:
                pass
            self.tooltip_window = None


class UsuarioView(ctk.CTkFrame):
    def __init__(self, master, usuario):
        super().__init__(master, fg_color="#F5E6F3")
        self.master = master
        self.usuario = usuario

        self.cor_sidebar = "#ffffff"
        self.cor_borda = "#e0e0e0"
        self.cor_borda_foco = "#C084FC"
        self.cor_texto = "#1a1a1a"
        self.cor_texto_secundario = "#6b7280"
        self.cor_roxo = "#a855f7"
        self.cor_roxo_hover = "#9333ea"
        self.cor_hover_secundario = "#f5f5f5"
        self.cor_input = "#f8f8f8"

        self.nome_usuario = self.usuario.get("nome", "Usuário")
        self.perfil_usuario = self.usuario.get("perfil", "N/A")

        self.entry_busca = None
        self.combo_tipo_busca = None
        self.lista_container = None

        self.colunas_tabela = [
            ("Nome", 3, 230),
            ("E-mail", 3, 280),
            ("Perfil", 2, 140),
            ("Ações", 2, 180),
        ]

        self.criar_interface()
        self.carregar_usuarios()

    def destacar_foco_widget(self, widget):
        try:
            widget.configure(border_color=self.cor_borda_foco)
        except Exception:
            pass

    def remover_foco_widget(self, widget):
        try:
            widget.configure(border_color="#d0d0d0")
        except Exception:
            pass

    def configurar_foco_entry(self, entry):
        entry.bind(
            "<FocusIn>",
            lambda event: self.destacar_foco_widget(entry),
            add="+"
        )
        entry.bind(
            "<FocusOut>",
            lambda event: self.remover_foco_widget(entry),
            add="+"
        )

    def abrir_dropdown_combobox(self, combo):
        try:
            combo._open_dropdown_menu()
        except Exception:
            try:
                combo._clicked()
            except Exception:
                pass

    def configurar_foco_combobox(self, combo):
        combo.bind(
            "<FocusIn>",
            lambda event: self.destacar_foco_widget(combo),
            add="+"
        )
        combo.bind(
            "<FocusOut>",
            lambda event: self.remover_foco_widget(combo),
            add="+"
        )

        combo.bind(
            "<Button-1>",
            lambda event: (
                self.destacar_foco_widget(combo),
                self.after(1, lambda: self.abrir_dropdown_combobox(combo))
            ),
            add="+"
        )

    def abrir_dashboard(self):
        self.master.mostrar_dashboard(self.usuario)

    def abrir_produtos(self):
        self.master.mostrar_produto(self.usuario)

    def abrir_movimentacao(self):
        self.master.mostrar_movimentacao(self.usuario)

    def abrir_usuarios(self):
        self.master.mostrar_usuario(self.usuario)

    def sair(self):
        confirmar = messagebox.askyesno("Sair", "Deseja realmente sair do sistema?")
        if confirmar:
            self.master.usuario_logado = None
            self.master.mostrar_login()

    def abrir_cadastro_usuario(self):
        self.master.mostrar_cadastro_usuario(self.usuario)

    def abrir_edicao_usuario(self, usuario_edicao):
        self.master.mostrar_cadastro_usuario(self.usuario, usuario_edicao)

    def configurar_colunas_grid(self, frame):
        for i, (_, peso, largura_minima) in enumerate(self.colunas_tabela):
            frame.grid_columnconfigure(
                i,
                weight=peso,
                minsize=largura_minima
            )
        frame.grid_rowconfigure(0, weight=1)

    def carregar_usuarios(self, usuarios=None):
        for widget in self.lista_container.winfo_children():
            widget.destroy()

        if usuarios is None:
            usuarios = listar_usuarios()

        if not usuarios:
            ctk.CTkLabel(
                self.lista_container,
                text="Nenhum usuário encontrado.",
                font=("Segoe UI", 14),
                text_color=self.cor_texto_secundario
            ).pack(pady=20)
            return

        self.criar_cabecalho_tabela()

        for usuario in usuarios:
            self.criar_linha_usuario(usuario)

    def criar_cabecalho_tabela(self):
        cabecalho = ctk.CTkFrame(self.lista_container, fg_color="transparent")
        cabecalho.pack(fill="x", expand=True, padx=14, pady=(0, 8))

        self.configurar_colunas_grid(cabecalho)

        for i, (titulo, _, _) in enumerate(self.colunas_tabela):
            anchor = "w"
            justify = "left"

            if titulo == "Ações":
                anchor = "center"
                justify = "center"

            ctk.CTkLabel(
                cabecalho,
                text=titulo,
                font=("Segoe UI", 13, "bold"),
                text_color=self.cor_texto,
                anchor=anchor,
                justify=justify
            ).grid(row=0, column=i, sticky="nsew", padx=10, pady=4)

    def criar_badge_perfil(self, parent, perfil):
        cor = "#2563eb"

        if perfil == "admin":
            cor = "#a855f7"
        elif perfil == "estoque":
            # cor = "#22c55e"
            cor = "#e240d0"

        ctk.CTkLabel(
            parent,
            text=perfil,
            font=("Segoe UI", 12, "bold"),
            text_color="#ffffff",
            fg_color=cor,
            corner_radius=16,
            width=110,
            height=30
        ).pack(anchor="center")

    def criar_linha_usuario(self, usuario):
        linha = ctk.CTkFrame(
            self.lista_container,
            fg_color="#ffffff",
            corner_radius=12,
            border_width=1,
            border_color="#eeeeee"
        )
        linha.pack(fill="x", expand=True, padx=14, pady=6)

        self.configurar_colunas_grid(linha)

        ctk.CTkLabel(
            linha,
            text=usuario.get("nome", "-"),
            font=("Segoe UI", 13, "bold"),
            text_color=self.cor_texto,
            anchor="w",
            justify="left"
        ).grid(row=0, column=0, sticky="nsew", padx=10, pady=14)

        ctk.CTkLabel(
            linha,
            text=usuario.get("email", "-"),
            font=("Segoe UI", 13),
            text_color=self.cor_texto_secundario,
            anchor="w",
            justify="left"
        ).grid(row=0, column=1, sticky="nsew", padx=10, pady=14)

        frame_perfil = ctk.CTkFrame(linha, fg_color="transparent")
        frame_perfil.grid(row=0, column=2, sticky="nsew", padx=10, pady=14)
        self.criar_badge_perfil(frame_perfil, usuario.get("perfil", "-"))

        frame_acoes = ctk.CTkFrame(linha, fg_color="transparent")
        frame_acoes.grid(row=0, column=3, sticky="nsew", padx=4, pady=14)

        container_acoes = ctk.CTkFrame(frame_acoes, fg_color="transparent")
        container_acoes.pack(anchor="center")

        btn_editar = ctk.CTkButton(
            container_acoes,
            text="✎",
            width=38,
            height=38,
            corner_radius=8,
            fg_color="#ffffff",
            hover_color="#e4f2f7",
            text_color="#0000ff",
            border_width=0,
            font=("Segoe UI", 16),
            command=lambda u=usuario: self.abrir_edicao_usuario(u)
        )
        btn_editar.pack(side="left", padx=(0, 4))

        btn_excluir = ctk.CTkButton(
            container_acoes,
            text="🗑",
            width=38,
            height=38,
            corner_radius=8,
            fg_color="#ffffff",
            hover_color="#fef2f2",
            text_color="#dc2626",
            border_width=0,
            font=("Segoe UI", 16),
            command=lambda u=usuario: self.confirmar_exclusao(u)
        )
        btn_excluir.pack(side="left")

        ToolTip(btn_editar, "Editar")
        ToolTip(btn_excluir, "Excluir")

    def confirmar_exclusao(self, usuario):
        confirmar = messagebox.askyesno(
            "Excluir usuário",
            f"Deseja realmente excluir o usuário '{usuario.get('nome', '')}'?"
        )
        if not confirmar:
            return

        sucesso, mensagem = excluir_usuario(usuario["id_usuario"])

        if sucesso:
            messagebox.showinfo("Sucesso", mensagem)
            self.carregar_usuarios()
        else:
            messagebox.showerror("Erro", mensagem)

    def aplicar_filtros(self):
        termo = self.entry_busca.get().strip()
        tipo_busca = self.combo_tipo_busca.get().strip()

        try:
            usuarios = listar_usuarios()

            if termo:
                if tipo_busca == "Nome":
                    usuarios = buscar_usuarios_por_nome(termo)
                elif tipo_busca == "E-mail":
                    usuarios = buscar_usuarios_por_email(termo)

            self.carregar_usuarios(usuarios)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao aplicar filtros: {str(e)}")

    def limpar_filtros(self):
        self.entry_busca.delete(0, "end")
        self.combo_tipo_busca.set("Nome")
        self.carregar_usuarios()

    def criar_interface(self):
        if self.perfil_usuario != "admin":
            ctk.CTkLabel(
                self,
                text="Acesso restrito a administradores.",
                font=("Segoe UI", 18, "bold"),
                text_color="#b91c1c"
            ).pack(expand=True)
            return

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
            command=self.abrir_movimentacao
        ).pack(fill="x", padx=20, pady=6)

        ctk.CTkButton(
            frame_sidebar,
            text="Usuários",
            height=42,
            corner_radius=8,
            fg_color=self.cor_roxo,
            hover_color=self.cor_roxo_hover,
            text_color="#ffffff",
            font=("Segoe UI", 14, "bold")
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
            text="Usuários",
            font=("Segoe UI", 28, "bold"),
            text_color=self.cor_texto
        ).pack(anchor="w", pady=(0, 10))

        frame_filtros = ctk.CTkFrame(
            frame_conteudo,
            fg_color="#ffffff",
            border_width=1,
            border_color="#d0d0d0",
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
            placeholder_text="Buscar usuário",
            corner_radius=6,
            border_width=1,
            border_color="#d0d0d0",
            fg_color=self.cor_input,
            text_color=self.cor_texto,
            font=("Segoe UI", 14)
        )
        self.entry_busca.pack(side="left", padx=(0, 10))
        self.configurar_foco_entry(self.entry_busca)

        self.combo_tipo_busca = ctk.CTkComboBox(
            linha1,
            width=180,
            height=40,
            values=["Nome", "E-mail"],
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
        self.combo_tipo_busca.pack(side="left", padx=(0, 10))
        self.combo_tipo_busca.set("Nome")
        self.configurar_foco_combobox(self.combo_tipo_busca)

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
            text="+ Novo Usuário",
            width=180,
            height=42,
            corner_radius=8,
            fg_color=self.cor_roxo,
            hover_color=self.cor_roxo_hover,
            text_color="#ffffff",
            font=("Segoe UI", 13, "bold"),
            command=self.abrir_cadastro_usuario
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
            text="Lista de Usuários",
            font=("Segoe UI", 18, "bold"),
            text_color=self.cor_texto
        ).pack(anchor="w", padx=20, pady=(20, 10))

        scroll = ctk.CTkScrollableFrame(
            frame_lista,
            fg_color="transparent"
        )
        scroll.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.lista_container = scroll