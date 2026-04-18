import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from tkcalendar import Calendar

from controllers.movimentacao_controller import (
    listar_historico,
    filtrar_historico_por_produto,
    filtrar_historico_por_categoria,
    filtrar_historico_por_destino,
    filtrar_historico_por_periodo,
    filtrar_historico_por_fornecedor,
    filtrar_historico_por_lote,
    filtrar_historico_por_tipo
)


class MovimentacaoView(ctk.CTkFrame):
    def __init__(self, master, usuario):
        super().__init__(master, fg_color="#F5E6F3")
        self.master = master
        self.usuario = usuario

        self.cor_sidebar = "#ffffff"
        self.cor_card = "#ffffff"
        self.cor_borda = "#e0e0e0"
        self.cor_borda_foco = "#C084FC"
        self.cor_texto = "#1a1a1a"
        self.cor_texto_secundario = "#666666"
        self.cor_roxo = "#a855f7"
        self.cor_roxo_hover = "#9333ea"
        self.cor_hover_secundario = "#f5f5f5"
        self.cor_input = "#f8f8f8"

        self.nome_usuario = self.usuario.get("nome", "Usuário")
        self.perfil_usuario = self.usuario.get("perfil", "N/A")

        self.combo_filtro = None
        self.entry_valor_filtro = None
        self.entry_data_inicial = None
        self.entry_data_final = None
        self.cards_container = None

        self.campos_datas = {}
        self.campos_datas_frames = {}
        self.calendario_popup = None

        self.colunas_historico = [
            ("Data/Hora", 145),
            ("Tipo", 120),
            ("Produto", 175),
            ("Categoria", 145),
            ("Quantidade", 110),
            ("Fornecedor / Destino", 190),
            ("Responsável", 145),
            ("Observações", 180),
        ]

        self.criar_interface()
        self.carregar_historico()

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
            lambda e: self.destacar_foco_widget(entry),
            add="+"
        )
        entry.bind(
            "<FocusOut>",
            lambda e: self.remover_foco_widget(entry),
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
            lambda e: self.destacar_foco_widget(combo),
            add="+"
        )
        combo.bind(
            "<FocusOut>",
            lambda e: self.remover_foco_widget(combo),
            add="+"
        )

        combo.bind(
            "<Button-1>",
            lambda e: (
                self.destacar_foco_widget(combo),
                self.after(1, lambda: self.abrir_dropdown_combobox(combo))
            ),
            add="+"
        )

    def abrir_dashboard(self):
        self.master.mostrar_dashboard(self.usuario)

    def abrir_produto(self):
        self.master.mostrar_produto(self.usuario)

    def abrir_usuarios(self):
        self.master.mostrar_usuario(self.usuario)

    # def abrir_usuarios(self):
    #     messagebox.showinfo("Usuários", "Tela de usuários ainda será conectada.")

    # def abrir_relatorios(self):
    #     messagebox.showinfo("Relatórios", "Tela de relatórios ainda será conectada.")

    def sair(self):
        confirmar = messagebox.askyesno("Sair", "Deseja realmente sair do sistema?")
        if confirmar:
            self.master.usuario_logado = None
            self.master.mostrar_login()

    def abrir_cadastro_movimentacao(self):
        self.master.mostrar_cadastro_movimentacao(self.usuario)

    def configurar_colunas_grid(self, frame):
        for i, (_, largura) in enumerate(self.colunas_historico):
            frame.grid_columnconfigure(i, minsize=largura, weight=0)

    def carregar_historico(self, historico=None):
        for widget in self.cards_container.winfo_children():
            widget.destroy()

        if historico is None:
            historico = listar_historico()

        if not historico:
            ctk.CTkLabel(
                self.cards_container,
                text="Nenhuma movimentação encontrada.",
                font=("Segoe UI", 14),
                text_color=self.cor_texto_secundario
            ).pack(pady=20)
            return

        self.criar_cabecalho_historico()

        for item in historico:
            self.criar_linha_movimentacao(item)

    def criar_cabecalho_historico(self):
        cabecalho = ctk.CTkFrame(
            self.cards_container,
            fg_color="transparent"
        )
        cabecalho.pack(fill="x", padx=12, pady=(0, 8))

        self.configurar_colunas_grid(cabecalho)

        for i, (titulo, _) in enumerate(self.colunas_historico):
            label = ctk.CTkLabel(
                cabecalho,
                text=titulo,
                font=("Segoe UI", 13, "bold"),
                text_color=self.cor_texto,
                anchor="w"
            )
            label.grid(row=0, column=i, sticky="w", padx=(0, 10))

    def criar_linha_movimentacao(self, item):
        linha = ctk.CTkFrame(
            self.cards_container,
            fg_color="#ffffff",
            corner_radius=10,
            border_width=1,
            border_color="#eeeeee"
        )
        linha.pack(fill="x", padx=12, pady=6)

        self.configurar_colunas_grid(linha)

        tipo = item.get("tipo_movimentacao", "Movimentação")
        eh_entrada = tipo.lower() == "entrada"

        cor_badge = "#10c44c" if eh_entrada else "#ff3131"
        simbolo = "↓" if eh_entrada else "↑"

        data_hora = item.get("data_movimentacao_formatada", "-")
        if data_hora != "-" and " " in data_hora:
            data_parte, hora_parte = data_hora.split(" ", 1)
        else:
            data_parte, hora_parte = data_hora, "-"

        if eh_entrada:
            valor_fornecedor_destino = item.get("fornecedor") or "-"
        else:
            valor_fornecedor_destino = item.get("destino") or "-"

        observacoes = item.get("observacoes", "").strip() if item.get("observacoes") else "-"
        responsavel = item.get("nome_usuario") or "-"
        quantidade = f"{item['quantidade']} {item['unidade_medida_produto']}"

        frame_data = ctk.CTkFrame(linha, fg_color="transparent")
        frame_data.grid(row=0, column=0, sticky="w", padx=(12, 10), pady=12)

        ctk.CTkLabel(
            frame_data,
            text=data_parte,
            font=("Segoe UI", 13, "bold"),
            text_color=self.cor_texto,
            anchor="w"
        ).pack(anchor="w")

        ctk.CTkLabel(
            frame_data,
            text=hora_parte,
            font=("Segoe UI", 12),
            text_color=self.cor_texto_secundario,
            anchor="w"
        ).pack(anchor="w")

        frame_tipo = ctk.CTkFrame(linha, fg_color="transparent")
        frame_tipo.grid(row=0, column=1, sticky="w", padx=(0, 10), pady=12)

        badge = ctk.CTkLabel(
            frame_tipo,
            text=f"{simbolo} {tipo}",
            font=("Segoe UI", 12, "bold"),
            text_color="#ffffff",
            fg_color=cor_badge,
            corner_radius=20,
            # width=100,
            width=70,
            height=28
        )
        badge.pack(anchor="w")

        ctk.CTkLabel(
            linha,
            text=item["nome_produto"],
            font=("Segoe UI", 13, "bold"),
            text_color=self.cor_texto,
            anchor="w"
        ).grid(row=0, column=2, sticky="w", padx=(0, 10), pady=12)

        ctk.CTkLabel(
            linha,
            text=item["categoria"],
            font=("Segoe UI", 13),
            text_color=self.cor_texto,
            anchor="w"
        ).grid(row=0, column=3, sticky="w", padx=(0, 10), pady=12)

        ctk.CTkLabel(
            linha,
            text=quantidade,
            font=("Segoe UI", 13),
            text_color=self.cor_texto,
            anchor="w"
        ).grid(row=0, column=4, sticky="w", padx=(0, 10), pady=12)

        ctk.CTkLabel(
            linha,
            text=valor_fornecedor_destino,
            font=("Segoe UI", 13),
            text_color=self.cor_texto,
            anchor="w"
        ).grid(row=0, column=5, sticky="w", padx=(0, 10), pady=12)

        ctk.CTkLabel(
            linha,
            text=responsavel,
            font=("Segoe UI", 13),
            text_color=self.cor_texto,
            anchor="w"
        ).grid(row=0, column=6, sticky="w", padx=(0, 10), pady=12)

        ctk.CTkLabel(
            linha,
            text=observacoes,
            font=("Segoe UI", 13),
            text_color=self.cor_texto_secundario,
            anchor="w",
            justify="left",
            wraplength=170
        ).grid(row=0, column=7, sticky="w", padx=(0, 10), pady=12)

    def abrir_calendario_popup(self, chave):
        if self.calendario_popup is not None and self.calendario_popup.winfo_exists():
            self.calendario_popup.destroy()

        entry = self.campos_datas[chave]
        frame_input = self.campos_datas_frames.get(chave)

        if frame_input is not None:
            frame_input.configure(border_color=self.cor_borda_foco)

        popup = ctk.CTkToplevel(self)
        popup.title("Selecionar data")
        popup.geometry("300x320")
        popup.resizable(False, False)
        popup.transient(self.winfo_toplevel())
        popup.grab_set()

        try:
            valor_atual = entry.get().strip()
            if valor_atual:
                data_inicial = datetime.strptime(valor_atual, "%d/%m/%Y")
            else:
                data_inicial = datetime.now()
        except Exception:
            data_inicial = datetime.now()

        calendario = Calendar(
            popup,
            selectmode="day",
            date_pattern="dd/mm/yyyy",
            year=data_inicial.year,
            month=data_inicial.month,
            day=data_inicial.day,
            locale="pt_BR"
        )
        calendario.pack(fill="both", expand=True, padx=12, pady=12)

        def confirmar_data():
            data_escolhida = calendario.get_date()
            entry.delete(0, "end")
            entry.insert(0, data_escolhida)
            if frame_input is not None:
                frame_input.configure(border_color="#d0d0d0")
            popup.destroy()

        def cancelar():
            if frame_input is not None:
                frame_input.configure(border_color="#d0d0d0")
            popup.destroy()

        frame_botoes = ctk.CTkFrame(popup, fg_color="transparent")
        frame_botoes.pack(fill="x", padx=12, pady=(0, 12))

        ctk.CTkButton(
            frame_botoes,
            text="Cancelar",
            height=36,
            corner_radius=6,
            border_width=1,
            border_color="#d0d0d0",
            fg_color="#ffffff",
            hover_color="#f5f5f5",
            text_color="#1a1a1a",
            font=("Segoe UI", 13, "bold"),
            command=cancelar
        ).pack(side="left", expand=True, fill="x", padx=(0, 6))

        ctk.CTkButton(
            frame_botoes,
            text="Selecionar",
            height=36,
            corner_radius=6,
            fg_color=self.cor_roxo,
            hover_color=self.cor_roxo_hover,
            text_color="#ffffff",
            font=("Segoe UI", 13, "bold"),
            command=confirmar_data
        ).pack(side="left", expand=True, fill="x", padx=(6, 0))

        self.calendario_popup = popup

    def criar_campo_data_filtro(self, parent, chave, placeholder=""):
        frame_input = ctk.CTkFrame(
            parent,
            height=40,
            corner_radius=6,
            border_width=1,
            border_color="#d0d0d0",
            fg_color=self.cor_input
        )
        frame_input.pack(side="left", padx=(0, 10))
        frame_input.pack_propagate(False)
        # frame_input.configure(width=170)
        frame_input.configure(width=60)
        frame_input.grid_columnconfigure(0, weight=1)

        frame_input.bind(
            "<Button-1>",
            lambda e: frame_input.configure(border_color=self.cor_borda_foco),
            add="+"
        )

        entry = ctk.CTkEntry(
            frame_input,
            height=32,
            corner_radius=0,
            border_width=0,
            fg_color=self.cor_input,
            text_color=self.cor_texto,
            font=("Segoe UI", 14),
            placeholder_text=placeholder
        )
        entry.grid(row=0, column=0, sticky="nsew", padx=(8, 0), pady=4)

        entry.bind(
            "<FocusIn>",
            lambda e: frame_input.configure(border_color=self.cor_borda_foco),
            add="+"
        )
        entry.bind(
            "<FocusOut>",
            lambda e: frame_input.configure(border_color="#d0d0d0"),
            add="+"
        )

        botao_calendario = ctk.CTkButton(
            frame_input,
            text="📅",
            width=40,
            height=32,
            corner_radius=4,
            fg_color="#ffffff",
            hover_color="#f3f4f6",
            text_color="#1a1a1a",
            font=("Segoe UI", 14),
            command=lambda c=chave: self.abrir_calendario_popup(c)
        )
        botao_calendario.grid(row=0, column=1, padx=6, pady=4)

        self.campos_datas[chave] = entry
        self.campos_datas_frames[chave] = frame_input

        return entry

    def aplicar_filtros(self):
        filtro = self.combo_filtro.get()
        valor = self.entry_valor_filtro.get().strip()

        data_inicial_br = self.entry_data_inicial.get().strip()
        data_final_br = self.entry_data_final.get().strip()

        data_inicial = ""
        data_final = ""

        if data_inicial_br:
            try:
                data_inicial = datetime.strptime(
                    data_inicial_br,
                    "%d/%m/%Y"
                ).strftime("%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Erro", "A data inicial deve estar no formato dd/mm/aaaa.")
                return

        if data_final_br:
            try:
                data_final = datetime.strptime(
                    data_final_br,
                    "%d/%m/%Y"
                ).strftime("%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Erro", "A data final deve estar no formato dd/mm/aaaa.")
                return

        try:
            if filtro == "Todos":
                historico = listar_historico()

            elif filtro == "Por Produto":
                if not valor:
                    messagebox.showerror("Erro", "Informe o ID do produto.")
                    return
                historico = filtrar_historico_por_produto(int(valor))

            elif filtro == "Por Categoria":
                if not valor:
                    messagebox.showerror("Erro", "Informe a categoria.")
                    return
                historico = filtrar_historico_por_categoria(valor)

            elif filtro == "Por Destino":
                if not valor:
                    messagebox.showerror("Erro", "Informe o destino.")
                    return
                historico = filtrar_historico_por_destino(valor)

            elif filtro == "Por Fornecedor":
                if not valor:
                    messagebox.showerror("Erro", "Informe o fornecedor.")
                    return
                historico = filtrar_historico_por_fornecedor(valor)

            elif filtro == "Por Lote":
                if not valor:
                    messagebox.showerror("Erro", "Informe o lote.")
                    return
                historico = filtrar_historico_por_lote(valor)

            elif filtro == "Por Entrada":
                historico = filtrar_historico_por_tipo("entrada")

            elif filtro == "Por Saída":
                historico = filtrar_historico_por_tipo("saida")

            elif filtro == "Por Período":
                if not data_inicial or not data_final:
                    messagebox.showerror("Erro", "Informe a data inicial e a data final.")
                    return
                historico = filtrar_historico_por_periodo(data_inicial, data_final)

            else:
                historico = listar_historico()

            self.carregar_historico(historico)

        except ValueError:
            messagebox.showerror("Erro", "O ID do produto deve ser um número inteiro.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao aplicar filtros: {str(e)}")

    def limpar_filtros(self):
        self.combo_filtro.set("Todos")
        self.entry_valor_filtro.delete(0, "end")
        self.entry_data_inicial.delete(0, "end")
        self.entry_data_final.delete(0, "end")
        self.carregar_historico()

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
            fg_color="#ffffff",
            hover_color=self.cor_hover_secundario,
            text_color=self.cor_texto,
            border_width=1,
            border_color=self.cor_borda,
            font=("Segoe UI", 14, "bold"),
            command=self.abrir_produto
        ).pack(fill="x", padx=20, pady=6)

        ctk.CTkButton(
            frame_sidebar,
            text="Movimentações",
            height=42,
            corner_radius=8,
            fg_color=self.cor_roxo,
            hover_color=self.cor_roxo_hover,
            text_color="#ffffff",
            font=("Segoe UI", 14, "bold")
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

        # ctk.CTkButton(
        #     frame_sidebar,
        #     text="Relatórios",
        #     height=42,
        #     corner_radius=8,
        #     fg_color="#ffffff",
        #     hover_color=self.cor_hover_secundario,
        #     text_color=self.cor_texto,
        #     border_width=1,
        #     border_color=self.cor_borda,
        #     font=("Segoe UI", 14, "bold"),
        #     command=self.abrir_relatorios
        # ).pack(fill="x", padx=20, pady=6)

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
            text="Movimentações",
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
        linha1.pack(fill="x", padx=20, pady=(0, 10))

        self.combo_filtro = ctk.CTkComboBox(
            linha1,
            # width=220,
            width=150,
            height=40,
            values=[
                "Todos",
                "Por Produto",
                "Por Categoria",
                "Por Destino",
                "Por Fornecedor",
                "Por Lote",
                "Por Entrada",
                "Por Saída",
                "Por Período"
            ],
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
        self.combo_filtro.pack(side="left", padx=(0, 10))
        self.combo_filtro.set("Todos")
        self.configurar_foco_combobox(self.combo_filtro)

        self.entry_valor_filtro = ctk.CTkEntry(
            linha1,
            # width=220,
            width=160,
            height=40,
            placeholder_text="Valor do filtro",
            corner_radius=6,
            border_width=1,
            border_color="#d0d0d0",
            fg_color=self.cor_input,
            text_color=self.cor_texto,
            font=("Segoe UI", 14)
        )
        self.entry_valor_filtro.pack(side="left", padx=(0, 10))
        self.configurar_foco_entry(self.entry_valor_filtro)

        self.entry_data_inicial = self.criar_campo_data_filtro(
            linha1,
            "data_inicial",
            "Data inicial"
        )

        self.entry_data_final = self.criar_campo_data_filtro(
            linha1,
            "data_final",
            "Data final"
        )

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
            text="+ Nova Movimentação",
            width=180,
            height=42,
            corner_radius=8,
            fg_color=self.cor_roxo,
            hover_color=self.cor_roxo_hover,
            text_color="#ffffff",
            font=("Segoe UI", 13, "bold"),
            command=self.abrir_cadastro_movimentacao
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
            text="Histórico de movimentações",
            font=("Segoe UI", 18, "bold"),
            text_color=self.cor_texto
        ).pack(anchor="w", padx=20, pady=(20, 10))

        scroll = ctk.CTkScrollableFrame(
            frame_lista,
            fg_color="transparent"
        )
        scroll.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.cards_container = scroll