import math
import tkinter as tk
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
        self.label_paginacao = None
        self.btn_anterior = None
        self.btn_proxima = None

        # Cabeçalho fixo + corpo rolável, seguindo o mesmo padrão de ProdutoView e MovimentacaoView.
        self.canvas_cabecalho = None
        self.canvas_corpo = None
        self.frame_cabecalho = None
        self.frame_corpo = None
        self.scroll_x = None
        self.scroll_y = None
        self.canvas_window_id_cabecalho = None
        self.canvas_window_id_corpo = None

        self.pagina_atual = 1
        self.itens_por_pagina = 10
        self.total_registros = 0
        self.total_paginas = 1

        # Tabela com colunas de largura fixa.
        # O cabeçalho e as linhas usam exatamente as mesmas larguras,
        # evitando desalinhamento entre título e conteúdo da célula.
        self.colunas_tabela = [
            ("Nome", 330),
            ("E-mail", 420),
            ("Perfil", 210),
            ("Ações", 180),
        ]

        self.wrap_cabecalho = {
            "Nome": 290,
            "E-mail": 380,
            "Perfil": 150,
            "Ações": 120,
        }

        self.wrap_celulas = {
            "nome": 290,
            "email": 380,
            "perfil": 120,
        }

        self.paddings_colunas = {
            0: (14, 8),
            1: (8, 8),
            2: (8, 8),
            3: (8, 14),
        }

        self.colunas_centralizadas = {2, 3}

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
        for i, (_, largura) in enumerate(self.colunas_tabela):
            frame.grid_columnconfigure(i, minsize=largura, weight=0)
        frame.grid_rowconfigure(0, weight=1)

    def obter_alinhamento_coluna(self, indice_coluna):
        if indice_coluna in self.colunas_centralizadas:
            return "center", "center"
        return "w", "left"

    def criar_container_coluna(self, parent, coluna, pady=(0, 0), altura=64):
        largura = self.colunas_tabela[coluna][1]

        frame = ctk.CTkFrame(
            parent,
            fg_color="transparent",
            width=largura,
            height=altura
        )
        frame.grid(
            row=0,
            column=coluna,
            sticky="nsew",
            padx=self.paddings_colunas[coluna],
            pady=pady
        )
        frame.grid_propagate(False)
        return frame

    def criar_label_coluna(self, parent, texto, coluna, fonte, cor_texto, wraplength):
        anchor, justify = self.obter_alinhamento_coluna(coluna)

        label = ctk.CTkLabel(
            parent,
            text=texto,
            font=fonte,
            text_color=cor_texto,
            anchor=anchor,
            justify=justify,
            wraplength=wraplength
        )
        label.pack(
            anchor="center" if coluna in self.colunas_centralizadas else "w",
            fill="both",
            expand=True
        )
        return label

    def sync_xview(self, *args):
        if self.canvas_cabecalho is not None:
            self.canvas_cabecalho.xview(*args)
        if self.canvas_corpo is not None:
            self.canvas_corpo.xview(*args)

    def on_cabecalho_xscroll(self, first, last):
        if self.scroll_x is not None:
            self.scroll_x.set(first, last)
        if self.canvas_corpo is not None:
            self.canvas_corpo.xview_moveto(first)

    def on_corpo_xscroll(self, first, last):
        if self.scroll_x is not None:
            self.scroll_x.set(first, last)
        if self.canvas_cabecalho is not None:
            self.canvas_cabecalho.xview_moveto(first)

    def atualizar_scrollregion_cabecalho(self, event=None):
        if self.canvas_cabecalho is not None:
            self.canvas_cabecalho.configure(
                scrollregion=self.canvas_cabecalho.bbox("all")
            )

    def atualizar_scrollregion_corpo(self, event=None):
        if self.canvas_corpo is not None:
            self.canvas_corpo.configure(
                scrollregion=self.canvas_corpo.bbox("all")
            )

    def ajustar_largura_cabecalho(self, event):
        if self.canvas_cabecalho is None or self.canvas_window_id_cabecalho is None:
            return

        largura_conteudo = sum(largura for _, largura in self.colunas_tabela) + 120
        largura_canvas = event.width

        if largura_canvas > largura_conteudo:
            self.canvas_cabecalho.itemconfigure(
                self.canvas_window_id_cabecalho,
                width=largura_canvas
            )

    def ajustar_largura_corpo(self, event):
        if self.canvas_corpo is None or self.canvas_window_id_corpo is None:
            return

        largura_conteudo = sum(largura for _, largura in self.colunas_tabela) + 120
        largura_canvas = event.width

        if largura_canvas > largura_conteudo:
            self.canvas_corpo.itemconfigure(
                self.canvas_window_id_corpo,
                width=largura_canvas
            )

    def ativar_scroll_mouse(self, event=None):
        if self.canvas_corpo is not None:
            self.canvas_corpo.bind_all("<MouseWheel>", self.rolar_tabela_mouse)
            self.canvas_corpo.bind_all("<Button-4>", self.rolar_tabela_mouse)
            self.canvas_corpo.bind_all("<Button-5>", self.rolar_tabela_mouse)

    def desativar_scroll_mouse(self, event=None):
        if self.canvas_corpo is not None:
            self.canvas_corpo.unbind_all("<MouseWheel>")
            self.canvas_corpo.unbind_all("<Button-4>")
            self.canvas_corpo.unbind_all("<Button-5>")

    def rolar_tabela_mouse(self, event):
        if self.canvas_corpo is None:
            return

        if getattr(event, "num", None) == 4:
            self.canvas_corpo.yview_scroll(-1, "units")
        elif getattr(event, "num", None) == 5:
            self.canvas_corpo.yview_scroll(1, "units")
        else:
            self.canvas_corpo.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def obter_filtros_atuais(self):
        termo = self.entry_busca.get().strip() if self.entry_busca else ""
        tipo_busca = self.combo_tipo_busca.get().strip() if self.combo_tipo_busca else "Nome"
        return termo, tipo_busca

    def atualizar_controles_paginacao(self):
        if self.total_registros <= 0:
            self.total_paginas = 1
        else:
            self.total_paginas = math.ceil(self.total_registros / self.itens_por_pagina)

        if self.label_paginacao is not None:
            self.label_paginacao.configure(
                text=f"Página {self.pagina_atual} de {self.total_paginas}  •  {self.total_registros} usuário(s)"
            )

        if self.btn_anterior is not None:
            self.btn_anterior.configure(
                state="normal" if self.pagina_atual > 1 else "disabled"
            )

        if self.btn_proxima is not None:
            self.btn_proxima.configure(
                state="normal" if self.pagina_atual < self.total_paginas else "disabled"
            )

    def carregar_usuarios(self):
        if self.frame_cabecalho is None or self.frame_corpo is None:
            return

        for widget in self.frame_cabecalho.winfo_children():
            widget.destroy()
        for widget in self.frame_corpo.winfo_children():
            widget.destroy()

        termo, tipo_busca = self.obter_filtros_atuais()

        if termo:
            if tipo_busca == "Nome":
                usuarios, total = buscar_usuarios_por_nome(
                    termo,
                    pagina=self.pagina_atual,
                    itens_por_pagina=self.itens_por_pagina
                )
            else:
                usuarios, total = buscar_usuarios_por_email(
                    termo,
                    pagina=self.pagina_atual,
                    itens_por_pagina=self.itens_por_pagina
                )
        else:
            usuarios, total = listar_usuarios(
                pagina=self.pagina_atual,
                itens_por_pagina=self.itens_por_pagina
            )

        self.total_registros = total
        self.criar_cabecalho_tabela()

        if not usuarios:
            ctk.CTkLabel(
                self.frame_corpo,
                text="Nenhum usuário encontrado.",
                font=("Segoe UI", 14),
                text_color=self.cor_texto_secundario
            ).pack(pady=20)

            self.atualizar_controles_paginacao()
            self.after(50, self.atualizar_scrollregion_cabecalho)
            self.after(50, self.atualizar_scrollregion_corpo)
            return

        for usuario in usuarios:
            self.criar_linha_usuario(usuario)

        self.atualizar_controles_paginacao()
        self.after(50, self.atualizar_scrollregion_cabecalho)
        self.after(50, self.atualizar_scrollregion_corpo)

    def criar_cabecalho_tabela(self):
        cabecalho = ctk.CTkFrame(self.frame_cabecalho, fg_color="transparent")
        cabecalho.pack(fill="x", padx=12, pady=(0, 8))

        self.configurar_colunas_grid(cabecalho)

        for i, (titulo, _) in enumerate(self.colunas_tabela):
            frame_coluna = self.criar_container_coluna(
                cabecalho,
                i,
                pady=(0, 0),
                altura=44
            )

            self.criar_label_coluna(
                parent=frame_coluna,
                texto=titulo,
                coluna=i,
                fonte=("Segoe UI", 13, "bold"),
                cor_texto=self.cor_texto,
                wraplength=self.wrap_cabecalho.get(titulo, 120)
            )

    def criar_badge_perfil(self, parent, perfil):
        cor = "#2563eb"

        if perfil == "admin":
            cor = "#a855f7"
        elif perfil == "estoque":
            cor = "#e240d0"

        ctk.CTkLabel(
            parent,
            text=perfil,
            font=("Segoe UI", 12, "bold"),
            text_color="#ffffff",
            fg_color=cor,
            corner_radius=16,
            width=110,
            height=30,
            justify="center",
            wraplength=self.wrap_celulas["perfil"]
        ).pack(anchor="center", expand=True)

    def criar_linha_usuario(self, usuario):
        linha = ctk.CTkFrame(
            self.frame_corpo,
            fg_color="#ffffff",
            corner_radius=12,
            border_width=1,
            border_color="#eeeeee"
        )
        linha.pack(fill="x", padx=12, pady=6)

        self.configurar_colunas_grid(linha)

        frame_nome = self.criar_container_coluna(linha, 0, pady=(14, 14), altura=64)
        self.criar_label_coluna(
            parent=frame_nome,
            texto=usuario.get("nome", "-"),
            coluna=0,
            fonte=("Segoe UI", 13, "bold"),
            cor_texto=self.cor_texto,
            wraplength=self.wrap_celulas["nome"]
        )

        frame_email = self.criar_container_coluna(linha, 1, pady=(14, 14), altura=64)
        self.criar_label_coluna(
            parent=frame_email,
            texto=usuario.get("email", "-"),
            coluna=1,
            fonte=("Segoe UI", 13),
            cor_texto=self.cor_texto_secundario,
            wraplength=self.wrap_celulas["email"]
        )

        frame_perfil = self.criar_container_coluna(linha, 2, pady=(14, 14), altura=64)
        self.criar_badge_perfil(frame_perfil, usuario.get("perfil", "-"))

        frame_acoes = self.criar_container_coluna(linha, 3, pady=(14, 14), altura=64)

        container_acoes = ctk.CTkFrame(frame_acoes, fg_color="transparent")
        container_acoes.pack(anchor="center", expand=True)

        btn_editar = ctk.CTkButton(
            container_acoes,
            text="✎",
            width=34,
            height=34,
            corner_radius=8,
            fg_color="#ffffff",
            hover_color="#e4f2f7",
            text_color="#0000ff",
            border_width=0,
            font=("Segoe UI", 15),
            command=lambda u=usuario: self.abrir_edicao_usuario(u)
        )
        btn_editar.pack(side="left", padx=4)

        btn_excluir = ctk.CTkButton(
            container_acoes,
            text="🗑",
            width=34,
            height=34,
            corner_radius=8,
            fg_color="#ffffff",
            hover_color="#fef2f2",
            text_color="#dc2626",
            border_width=0,
            font=("Segoe UI", 15),
            command=lambda u=usuario: self.confirmar_exclusao(u)
        )
        btn_excluir.pack(side="left", padx=4)

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

            if self.pagina_atual > 1 and self.total_registros == 1:
                self.pagina_atual -= 1

            self.carregar_usuarios()
        else:
            messagebox.showerror("Erro", mensagem)

    def aplicar_filtros(self):
        self.pagina_atual = 1
        self.carregar_usuarios()

    def limpar_filtros(self):
        self.entry_busca.delete(0, "end")
        self.combo_tipo_busca.set("Nome")
        self.pagina_atual = 1
        self.carregar_usuarios()

    def ir_para_pagina_anterior(self):
        if self.pagina_atual > 1:
            self.pagina_atual -= 1
            self.carregar_usuarios()

    def ir_para_proxima_pagina(self):
        if self.pagina_atual < self.total_paginas:
            self.pagina_atual += 1
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

        # ctk.CTkLabel(
        #     frame_lista,
        #     text="Lista de Usuários",
        #     font=("Segoe UI", 18, "bold"),
        #     text_color=self.cor_texto
        # ).pack(anchor="w", padx=20, pady=(20, 10))

        # frame_tabela_area = ctk.CTkFrame(frame_lista, fg_color="transparent")
        # frame_tabela_area.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        frame_lista.grid_columnconfigure(0, weight=1)
        frame_lista.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            frame_lista,
            text="Lista de Usuários",
            font=("Segoe UI", 18, "bold"),
            text_color=self.cor_texto
        ).grid(row=0, column=0, sticky="w", padx=20, pady=(14, 6))

        frame_tabela_area = ctk.CTkFrame(frame_lista, fg_color="transparent")
        frame_tabela_area.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 4))

        frame_tabela_area.grid_rowconfigure(1, weight=1)
        frame_tabela_area.grid_columnconfigure(0, weight=1)

        self.canvas_cabecalho = tk.Canvas(
            frame_tabela_area,
            bg="#ffffff",
            highlightthickness=0,
            bd=0,
            height=56
        )
        self.canvas_cabecalho.grid(row=0, column=0, sticky="ew")

        self.frame_cabecalho = ctk.CTkFrame(self.canvas_cabecalho, fg_color="#ffffff")
        self.canvas_window_id_cabecalho = self.canvas_cabecalho.create_window(
            (0, 0),
            window=self.frame_cabecalho,
            anchor="nw"
        )

        self.canvas_corpo = tk.Canvas(
            frame_tabela_area,
            bg="#ffffff",
            highlightthickness=0,
            bd=0
        )
        self.canvas_corpo.grid(row=1, column=0, sticky="nsew")

        self.canvas_corpo.bind("<Enter>", self.ativar_scroll_mouse)
        self.canvas_corpo.bind("<Leave>", self.desativar_scroll_mouse)

        self.scroll_y = ctk.CTkScrollbar(
            frame_tabela_area,
            orientation="vertical",
            command=self.canvas_corpo.yview
        )
        self.scroll_y.grid(row=1, column=1, sticky="ns")

        self.scroll_x = ctk.CTkScrollbar(
            frame_tabela_area,
            orientation="horizontal",
            command=self.sync_xview
        )
        self.scroll_x.grid(row=2, column=0, sticky="ew")

        self.canvas_cabecalho.configure(xscrollcommand=self.on_cabecalho_xscroll)
        self.canvas_corpo.configure(
            yscrollcommand=self.scroll_y.set,
            xscrollcommand=self.on_corpo_xscroll
        )

        self.frame_corpo = ctk.CTkFrame(self.canvas_corpo, fg_color="#ffffff")
        self.canvas_window_id_corpo = self.canvas_corpo.create_window(
            (0, 0),
            window=self.frame_corpo,
            anchor="nw"
        )

        self.frame_cabecalho.bind("<Configure>", self.atualizar_scrollregion_cabecalho)
        self.frame_corpo.bind("<Configure>", self.atualizar_scrollregion_corpo)

        self.canvas_cabecalho.bind("<Configure>", self.ajustar_largura_cabecalho)
        self.canvas_corpo.bind("<Configure>", self.ajustar_largura_corpo)

        # frame_paginacao = ctk.CTkFrame(frame_lista, fg_color="transparent")
        # frame_paginacao.pack(fill="x", padx=20, pady=(0, 20))

        frame_paginacao = ctk.CTkFrame(frame_lista, fg_color="transparent", height=48)
        frame_paginacao.grid(row=2, column=0, sticky="ew", padx=20, pady=(4, 12))
        frame_paginacao.grid_propagate(False)

        self.btn_anterior = ctk.CTkButton(
            frame_paginacao,
            text="← Anterior",
            width=120,
            height=36,
            corner_radius=8,
            border_width=1,
            border_color="#d0d0d0",
            fg_color="#ffffff",
            hover_color="#f5f5f5",
            text_color="#1a1a1a",
            font=("Segoe UI", 12, "bold"),
            command=self.ir_para_pagina_anterior
        )
        self.btn_anterior.pack(side="left")

        self.label_paginacao = ctk.CTkLabel(
            frame_paginacao,
            text="Página 1 de 1  •  0 usuário(s)",
            font=("Segoe UI", 13),
            text_color=self.cor_texto_secundario
        )
        self.label_paginacao.pack(side="left", padx=20)

        self.btn_proxima = ctk.CTkButton(
            frame_paginacao,
            text="Próxima →",
            width=120,
            height=36,
            corner_radius=8,
            fg_color=self.cor_roxo,
            hover_color=self.cor_roxo_hover,
            text_color="#ffffff",
            font=("Segoe UI", 12, "bold"),
            command=self.ir_para_proxima_pagina
        )
        self.btn_proxima.pack(side="right")