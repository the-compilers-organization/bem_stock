import math
import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from tkcalendar import Calendar
from PIL import Image
from utils.caminho_recurso import caminho_recurso

from controllers.movimentacao_controller import (
    listar_historico,
    filtrar_historico_por_produto,
    filtrar_historico_por_categoria,
    filtrar_historico_por_destino,
    filtrar_historico_por_periodo,
    filtrar_historico_por_fornecedor,
    filtrar_historico_por_lote,
    filtrar_historico_por_tipo,
    filtrar_historico_combinado,
    excluir_movimentacao
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
        self.label_paginacao = None
        self.btn_anterior = None
        self.btn_proxima = None

        self.campos_datas = {}
        self.campos_datas_frames = {}
        self.calendario_popup = None

        # Cabeçalho fixo + corpo rolável
        self.canvas_cabecalho = None
        self.frame_cabecalho = None
        self.canvas_corpo = None
        self.frame_corpo = None
        self.scroll_x = None
        self.scroll_y = None
        self.canvas_window_id_cabecalho = None
        self.canvas_window_id_corpo = None

        self.pagina_atual = 1
        self.itens_por_pagina = 10
        self.total_registros = 0
        self.total_paginas = 1

        self.colunas_historico = [
            ("Data/Hora", 170),
            ("Tipo", 140),
            ("Produto", 170),
            ("Categoria", 170),
            ("Quantidade", 170),
            ("Lote", 140),  # nova
            ("Fornecedor /\nDestino", 210),
            ("Responsável", 190),
            ("Observações", 190),
            ("Ações", 130),
        ]

        self.wrap_cabecalho = {
            "Data/Hora": 130,
            "Tipo": 100,
            "Produto": 140,
            "Categoria": 140,
            "Quantidade": 130,
            "Lote": 120, # novo
            "Fornecedor /\nDestino": 160,
            "Responsável": 140,
            "Observações": 140,
            "Ações": 90,
        }

        self.wrap_celulas = {
            "data": 130,
            "hora": 130,
            "produto": 140,
            "categoria": 140,
            "quantidade": 130,
            "lote": 120, # novo
            "fornecedor_destino": 160,
            "responsavel": 140,
            "observacoes": 140,
        }

        self.paddings_colunas = {
            0: (14, 8),
            1: (0, 8),
            2: (0, 8),
            3: (0, 8),
            4: (0, 8),
            5: (0, 8), #lote novo
            6: (0, 8),
            7: (0, 8),
            8: (0, 8),
            9: (0, 14),
        }

        # self.colunas_centralizadas = {1, 8}
        self.colunas_centralizadas = {1, 9}

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
        entry.bind("<FocusIn>", lambda e: self.destacar_foco_widget(entry), add="+")
        entry.bind("<FocusOut>", lambda e: self.remover_foco_widget(entry), add="+")

    def abrir_dropdown_combobox(self, combo):
        try:
            combo._open_dropdown_menu()
        except Exception:
            try:
                combo._clicked()
            except Exception:
                pass

    def configurar_foco_combobox(self, combo):
        combo.bind("<FocusIn>", lambda e: self.destacar_foco_widget(combo), add="+")
        combo.bind("<FocusOut>", lambda e: self.remover_foco_widget(combo), add="+")
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

    def sair(self):
        confirmar = messagebox.askyesno("Sair", "Deseja realmente sair do sistema?")
        if confirmar:
            self.master.usuario_logado = None
            self.master.mostrar_login()

    def abrir_cadastro_movimentacao(self):
        self.master.mostrar_cadastro_movimentacao(self.usuario)

    def abrir_edicao_movimentacao(self, movimentacao):
        self.master.mostrar_cadastro_movimentacao(self.usuario, movimentacao)

    def confirmar_exclusao_movimentacao(self, movimentacao):
        confirmar = messagebox.askyesno(
            "Excluir movimentação",
            "Deseja realmente excluir esta movimentação?"
        )
        if not confirmar:
            return

        sucesso, mensagem = excluir_movimentacao(movimentacao["id_movimentacao"])

        if sucesso:
            messagebox.showinfo("Sucesso", mensagem)

            if self.pagina_atual > 1 and self.total_registros == 1:
                self.pagina_atual -= 1

            historico, total = self.obter_resultado_paginado_atual()
            self.carregar_historico(historico, total)
        else:
            messagebox.showerror("Erro", mensagem)

    def configurar_colunas_grid(self, frame):
        for i, (_, largura) in enumerate(self.colunas_historico):
            frame.grid_columnconfigure(i, minsize=largura, weight=0)

    def obter_alinhamento_coluna(self, indice_coluna):
        if indice_coluna in self.colunas_centralizadas:
            return "center", "center"
        return "w", "left"

    def criar_container_coluna(self, parent, coluna, pady=(0, 0)):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.grid(
            row=0,
            column=coluna,
            sticky="nsew",
            padx=self.paddings_colunas[coluna],
            pady=pady
        )
        return frame

    def criar_label_padrao(self, parent, texto, coluna, fonte, cor_texto, wraplength):
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
            fill="x"
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
            self.canvas_cabecalho.configure(scrollregion=self.canvas_cabecalho.bbox("all"))

    def atualizar_scrollregion_corpo(self, event=None):
        if self.canvas_corpo is not None:
            self.canvas_corpo.configure(scrollregion=self.canvas_corpo.bbox("all"))

    def ajustar_largura_cabecalho(self, event):
        if self.canvas_cabecalho is None or self.canvas_window_id_cabecalho is None:
            return

        largura_conteudo = sum(l for _, l in self.colunas_historico) + 120
        largura_canvas = event.width

        if largura_canvas > largura_conteudo:
            self.canvas_cabecalho.itemconfigure(self.canvas_window_id_cabecalho, width=largura_canvas)

    def ajustar_largura_corpo(self, event):
        if self.canvas_corpo is None or self.canvas_window_id_corpo is None:
            return

        largura_conteudo = sum(l for _, l in self.colunas_historico) + 120
        largura_canvas = event.width

        if largura_canvas > largura_conteudo:
            self.canvas_corpo.itemconfigure(self.canvas_window_id_corpo, width=largura_canvas)

    def atualizar_controles_paginacao(self):
        if self.total_registros <= 0:
            self.total_paginas = 1
        else:
            self.total_paginas = math.ceil(self.total_registros / self.itens_por_pagina)

        if self.pagina_atual > self.total_paginas:
            self.pagina_atual = self.total_paginas

        if self.label_paginacao is not None:
            self.label_paginacao.configure(
                text=f"Página {self.pagina_atual} de {self.total_paginas}  •  {self.total_registros} movimentação(ões)"
            )

        if self.btn_anterior is not None:
            self.btn_anterior.configure(
                state="normal" if self.pagina_atual > 1 else "disabled"
            )

        if self.btn_proxima is not None:
            self.btn_proxima.configure(
                state="normal" if self.pagina_atual < self.total_paginas else "disabled"
            )

    def carregar_historico(self, historico=None, total=None):
        for widget in self.frame_cabecalho.winfo_children():
            widget.destroy()
        for widget in self.frame_corpo.winfo_children():
            widget.destroy()

        if historico is None:
            historico, total = listar_historico(
                pagina=self.pagina_atual,
                itens_por_pagina=self.itens_por_pagina
            )

        self.total_registros = total if total is not None else len(historico)

        self.criar_cabecalho_historico()

        if not historico:
            ctk.CTkLabel(
                self.frame_corpo,
                text="Nenhuma movimentação encontrada.",
                font=("Segoe UI", 14),
                text_color=self.cor_texto_secundario
            ).pack(pady=20)

            self.atualizar_controles_paginacao()
            self.after(50, self.atualizar_scrollregion_cabecalho)
            self.after(50, self.atualizar_scrollregion_corpo)
            return

        for item in historico:
            self.criar_linha_movimentacao(item)

        self.atualizar_controles_paginacao()
        self.after(50, self.atualizar_scrollregion_cabecalho)
        self.after(50, self.atualizar_scrollregion_corpo)

    def criar_cabecalho_historico(self):
        cabecalho = ctk.CTkFrame(self.frame_cabecalho, fg_color="transparent")
        cabecalho.pack(fill="x", padx=12, pady=(0, 8))

        self.configurar_colunas_grid(cabecalho)
        cabecalho.grid_rowconfigure(0, weight=1)

        for i, (titulo, _) in enumerate(self.colunas_historico):
            frame_coluna = self.criar_container_coluna(cabecalho, i, pady=(0, 0))

            self.criar_label_padrao(
                parent=frame_coluna,
                texto=titulo,
                coluna=i,
                fonte=("Segoe UI", 13, "bold"),
                cor_texto=self.cor_texto,
                wraplength=self.wrap_cabecalho.get(titulo, 120)
            )

    def criar_linha_movimentacao(self, item):
        linha = ctk.CTkFrame(
            self.frame_corpo,
            fg_color="#ffffff",
            corner_radius=10,
            border_width=1,
            border_color="#eeeeee"
        )
        linha.pack(fill="x", padx=12, pady=6)

        self.configurar_colunas_grid(linha)
        linha.grid_rowconfigure(0, weight=1)

        tipo = item.get("tipo_movimentacao", "Movimentação")
        eh_entrada = tipo.lower() == "entrada"

        cor_badge = "#10c44c" if eh_entrada else "#ff3131"
        simbolo = "↓" if eh_entrada else "↑"

        data_hora = item.get("data_movimentacao_formatada", "-")
        if data_hora != "-" and " " in data_hora:
            data_parte, hora_parte = data_hora.split(" ", 1)
        else:
            data_parte, hora_parte = data_hora, "-"

        valor_fornecedor_destino = item.get("fornecedor") if eh_entrada else item.get("destino")
        valor_fornecedor_destino = valor_fornecedor_destino or "-"

        observacoes = item.get("observacoes", "").strip() if item.get("observacoes") else "-"
        responsavel = item.get("nome_usuario") or "-"
        quantidade = f"{item['quantidade']} {item['unidade_medida_produto']}"

        frame_data = self.criar_container_coluna(linha, 0, pady=(12, 12))
        ctk.CTkLabel(
            frame_data,
            text=data_parte,
            font=("Segoe UI", 13, "bold"),
            text_color=self.cor_texto,
            anchor="w",
            justify="left",
            wraplength=self.wrap_celulas["data"]
        ).pack(anchor="w", fill="x")

        ctk.CTkLabel(
            frame_data,
            text=hora_parte,
            font=("Segoe UI", 12),
            text_color=self.cor_texto_secundario,
            anchor="w",
            justify="left",
            wraplength=self.wrap_celulas["hora"]
        ).pack(anchor="w", fill="x", pady=(4, 0))

        frame_tipo = self.criar_container_coluna(linha, 1, pady=(12, 12))
        badge = ctk.CTkLabel(
            frame_tipo,
            text=f"{simbolo} {tipo}",
            font=("Segoe UI", 11, "bold"),
            text_color="#ffffff",
            fg_color=cor_badge,
            corner_radius=13,
            width=82,
            height=34,
            justify="center",
            anchor="center"
        )
        badge.pack(anchor="center", pady=2)

        frame_produto = self.criar_container_coluna(linha, 2, pady=(12, 12))
        self.criar_label_padrao(
            frame_produto, item["nome_produto"], 2,
            ("Segoe UI", 13, "bold"), self.cor_texto, self.wrap_celulas["produto"]
        )

        frame_categoria = self.criar_container_coluna(linha, 3, pady=(12, 12))
        self.criar_label_padrao(
            frame_categoria, item["categoria"], 3,
            ("Segoe UI", 13), self.cor_texto, self.wrap_celulas["categoria"]
        )

        frame_quantidade = self.criar_container_coluna(linha, 4, pady=(12, 12))
        self.criar_label_padrao(
            frame_quantidade, quantidade, 4,
            ("Segoe UI", 13), self.cor_texto, self.wrap_celulas["quantidade"]
        )

        lote = item.get("numero_lote") or "-"

        frame_lote = self.criar_container_coluna(linha, 5, pady=(12, 12))
        self.criar_label_padrao(
            frame_lote, lote, 5,
            ("Segoe UI", 13), self.cor_texto, self.wrap_celulas["lote"]
        )

        frame_fd = self.criar_container_coluna(linha, 6, pady=(12, 12))
        self.criar_label_padrao(
            frame_fd, valor_fornecedor_destino, 6,
            ("Segoe UI", 13), self.cor_texto, self.wrap_celulas["fornecedor_destino"]
        )

        frame_responsavel = self.criar_container_coluna(linha, 7, pady=(12, 12))
        self.criar_label_padrao(
            frame_responsavel, responsavel, 7,
            ("Segoe UI", 13), self.cor_texto, self.wrap_celulas["responsavel"]
        )

        frame_observacoes = self.criar_container_coluna(linha, 8, pady=(12, 12))
        self.criar_label_padrao(
            frame_observacoes, observacoes, 8,
            ("Segoe UI", 13), self.cor_texto_secundario, self.wrap_celulas["observacoes"]
        )

        frame_acoes = self.criar_container_coluna(linha, 9, pady=(12, 12))
        container_acoes = ctk.CTkFrame(frame_acoes, fg_color="transparent")
        container_acoes.pack(anchor="center")

        btn_editar = ctk.CTkButton(
            container_acoes,
            text="✎",
            width=30,
            height=30,
            corner_radius=8,
            fg_color="#ffffff",
            hover_color="#e4f2f7",
            text_color="#0000ff",
            border_width=0,
            font=("Segoe UI", 14),
            command=lambda m=item: self.abrir_edicao_movimentacao(m)
        )
        btn_editar.pack(side="left", padx=(0, 2))

        btn_excluir = ctk.CTkButton(
            container_acoes,
            text="🗑",
            width=30,
            height=30,
            corner_radius=8,
            fg_color="#ffffff",
            hover_color="#fef2f2",
            text_color="#dc2626",
            border_width=0,
            font=("Segoe UI", 14),
            command=lambda m=item: self.confirmar_exclusao_movimentacao(m)
        )
        btn_excluir.pack(side="left")

        ToolTip(btn_editar, "Editar")
        ToolTip(btn_excluir, "Excluir")

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
        frame_input.configure(width=160)
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

    # def aplicar_filtros(self):
    #     filtro = self.combo_filtro.get()
    #     valor = self.entry_valor_filtro.get().strip()

    #     data_inicial_br = self.entry_data_inicial.get().strip()
    #     data_final_br = self.entry_data_final.get().strip()

    #     data_inicial = ""
    #     data_final = ""

    #     if data_inicial_br:
    #         try:
    #             data_inicial = datetime.strptime(data_inicial_br, "%d/%m/%Y").strftime("%Y-%m-%d")
    #         except ValueError:
    #             messagebox.showerror("Erro", "A data inicial deve estar no formato dd/mm/aaaa.")
    #             return

    #     if data_final_br:
    #         try:
    #             data_final = datetime.strptime(data_final_br, "%d/%m/%Y").strftime("%Y-%m-%d")
    #         except ValueError:
    #             messagebox.showerror("Erro", "A data final deve estar no formato dd/mm/aaaa.")
    #             return

    #     try:
    #         self.pagina_atual = 1

    #         if filtro == "Todos":
    #             historico, total = listar_historico(
    #                 pagina=self.pagina_atual,
    #                 itens_por_pagina=self.itens_por_pagina
    #             )
    #         elif filtro == "Por Produto":
    #             if not valor:
    #                 messagebox.showerror("Erro", "Informe o ID do produto.")
    #                 return
    #             historico, total = filtrar_historico_por_produto(
    #                 int(valor), pagina=self.pagina_atual, itens_por_pagina=self.itens_por_pagina
    #             )
    #         elif filtro == "Por Categoria":
    #             if not valor:
    #                 messagebox.showerror("Erro", "Informe a categoria.")
    #                 return
    #             historico, total = filtrar_historico_por_categoria(
    #                 valor, pagina=self.pagina_atual, itens_por_pagina=self.itens_por_pagina
    #             )
    #         elif filtro == "Por Destino":
    #             if not valor:
    #                 messagebox.showerror("Erro", "Informe o destino.")
    #                 return
    #             historico, total = filtrar_historico_por_destino(
    #                 valor, pagina=self.pagina_atual, itens_por_pagina=self.itens_por_pagina
    #             )
    #         elif filtro == "Por Fornecedor":
    #             if not valor:
    #                 messagebox.showerror("Erro", "Informe o fornecedor.")
    #                 return
    #             historico, total = filtrar_historico_por_fornecedor(
    #                 valor, pagina=self.pagina_atual, itens_por_pagina=self.itens_por_pagina
    #             )
    #         elif filtro == "Por lote":
    #             if not valor:
    #                 messagebox.showerror("Erro", "Informe o lote.")
    #                 return
    #             historico, total = filtrar_historico_por_lote(
    #                 valor, pagina=self.pagina_atual, itens_por_pagina=self.itens_por_pagina
    #             )
    #         elif filtro == "Por Entrada":
    #             historico, total = filtrar_historico_por_tipo(
    #                 "entrada", pagina=self.pagina_atual, itens_por_pagina=self.itens_por_pagina
    #             )
    #         elif filtro == "Por Saída":
    #             historico, total = filtrar_historico_por_tipo(
    #                 "saida", pagina=self.pagina_atual, itens_por_pagina=self.itens_por_pagina
    #             )
    #         elif filtro == "Por Período":
    #             if not data_inicial or not data_final:
    #                 messagebox.showerror("Erro", "Informe a data inicial e a data final.")
    #                 return
    #             historico, total = filtrar_historico_por_periodo(
    #                 data_inicial, data_final,
    #                 pagina=self.pagina_atual,
    #                 itens_por_pagina=self.itens_por_pagina
    #             )
    #         else:
    #             historico, total = listar_historico(
    #                 pagina=self.pagina_atual,
    #                 itens_por_pagina=self.itens_por_pagina
    #             )

    #         self.carregar_historico(historico, total)

    #     except ValueError:
    #         messagebox.showerror("Erro", "O ID do produto deve ser um número inteiro.")
    #     except Exception as e:
    #         messagebox.showerror("Erro", f"Erro ao aplicar filtros: {str(e)}")


    def aplicar_filtros(self):
        filtro = self.combo_filtro.get()
        valor = self.entry_valor_filtro.get().strip()

        data_inicial_br = self.entry_data_inicial.get().strip()
        data_final_br = self.entry_data_final.get().strip()

        data_inicial = ""
        data_final = ""

        try:
            if data_inicial_br:
                data_inicial = datetime.strptime(
                    data_inicial_br, "%d/%m/%Y"
                ).strftime("%Y-%m-%d")
                data_inicial += " 00:00:00"

            if data_final_br:
                data_final = datetime.strptime(
                    data_final_br, "%d/%m/%Y"
                ).strftime("%Y-%m-%d")
                data_final += " 23:59:59"

            if (data_inicial and not data_final) or (data_final and not data_inicial):
                messagebox.showerror("Erro", "Informe a data inicial e a data final.")
                return

            if data_inicial and data_final and data_inicial > data_final:
                messagebox.showerror(
                    "Erro",
                    "A data inicial não pode ser maior que a data final."
                )
                return

            if filtro == "Por Período" and (not data_inicial or not data_final):
                messagebox.showerror("Erro", "Informe a data inicial e a data final.")
                return

            if filtro in [
                "Por Produto",
                "Por Categoria",
                "Por Destino",
                "Por Fornecedor",
                "Por Lote"
            ] and not valor:
                messagebox.showerror("Erro", "Informe o valor do filtro.")
                return

            self.pagina_atual = 1

            historico, total = filtrar_historico_combinado(
                filtro=filtro,
                valor=valor,
                data_inicial=data_inicial,
                data_final=data_final,
                pagina=self.pagina_atual,
                itens_por_pagina=self.itens_por_pagina
            )

            self.carregar_historico(historico, total)

        except ValueError:
            messagebox.showerror("Erro", "As datas devem estar no formato dd/mm/aaaa.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao aplicar filtros: {str(e)}")


    def limpar_filtros(self):
        self.combo_filtro.set("Todos")
        self.entry_valor_filtro.delete(0, "end")
        self.entry_data_inicial.delete(0, "end")
        self.entry_data_final.delete(0, "end")
        self.pagina_atual = 1
        self.carregar_historico()

    # def obter_resultado_paginado_atual(self):
    #     filtro = self.combo_filtro.get()
    #     valor = self.entry_valor_filtro.get().strip()

    #     data_inicial_br = self.entry_data_inicial.get().strip()
    #     data_final_br = self.entry_data_final.get().strip()

    #     data_inicial = ""
    #     data_final = ""

    #     if data_inicial_br:
    #         data_inicial = datetime.strptime(data_inicial_br, "%d/%m/%Y").strftime("%Y-%m-%d")
    #     if data_final_br:
    #         data_final = datetime.strptime(data_final_br, "%d/%m/%Y").strftime("%Y-%m-%d")

    #     if filtro == "Todos":
    #         return listar_historico(pagina=self.pagina_atual, itens_por_pagina=self.itens_por_pagina)
    #     if filtro == "Por Produto":
    #         return filtrar_historico_por_produto(int(valor), pagina=self.pagina_atual, itens_por_pagina=self.itens_por_pagina)
    #     if filtro == "Por Categoria":
    #         return filtrar_historico_por_categoria(valor, pagina=self.pagina_atual, itens_por_pagina=self.itens_por_pagina)
    #     if filtro == "Por Destino":
    #         return filtrar_historico_por_destino(valor, pagina=self.pagina_atual, itens_por_pagina=self.itens_por_pagina)
    #     if filtro == "Por Fornecedor":
    #         return filtrar_historico_por_fornecedor(valor, pagina=self.pagina_atual, itens_por_pagina=self.itens_por_pagina)
    #     if filtro == "Por lote":
    #         return filtrar_historico_por_lote(valor, pagina=self.pagina_atual, itens_por_pagina=self.itens_por_pagina)
    #     if filtro == "Por Entrada":
    #         return filtrar_historico_por_tipo("entrada", pagina=self.pagina_atual, itens_por_pagina=self.itens_por_pagina)
    #     if filtro == "Por Saída":
    #         return filtrar_historico_por_tipo("saida", pagina=self.pagina_atual, itens_por_pagina=self.itens_por_pagina)
    #     if filtro == "Por Período":
    #         return filtrar_historico_por_periodo(data_inicial, data_final, pagina=self.pagina_atual, itens_por_pagina=self.itens_por_pagina)

    #     return listar_historico(pagina=self.pagina_atual, itens_por_pagina=self.itens_por_pagina)


    def obter_resultado_paginado_atual(self):
        filtro = self.combo_filtro.get()
        valor = self.entry_valor_filtro.get().strip()

        data_inicial = ""
        data_final = ""

        if self.entry_data_inicial.get().strip():
            data_inicial = datetime.strptime(
                self.entry_data_inicial.get().strip(),
                "%d/%m/%Y"
            ).strftime("%Y-%m-%d")
            # ).strftime("%Y-%m-%d 00:00:00")

        if self.entry_data_final.get().strip():
            data_final = datetime.strptime(
                self.entry_data_final.get().strip(),
                "%d/%m/%Y"
            ).strftime("%Y-%m-%d")
            # ).strftime("%Y-%m-%d 23:59:59")

        if data_inicial:
            data_inicial += " 00:00:00"

        if data_final:
            data_final += " 23:59:59"

        if data_inicial and data_final:
            filtro = "Por Período"

        if filtro == "Todos":
            return listar_historico(
                pagina=self.pagina_atual,
                itens_por_pagina=self.itens_por_pagina
            )

        if filtro == "Por Produto":
            return filtrar_historico_por_produto(
                valor,
                pagina=self.pagina_atual,
                itens_por_pagina=self.itens_por_pagina
            )

        if filtro == "Por Categoria":
            return filtrar_historico_por_categoria(
                valor,
                pagina=self.pagina_atual,
                itens_por_pagina=self.itens_por_pagina
            )

        if filtro == "Por Destino":
            return filtrar_historico_por_destino(
                valor,
                pagina=self.pagina_atual,
                itens_por_pagina=self.itens_por_pagina
            )

        if filtro == "Por Fornecedor":
            return filtrar_historico_por_fornecedor(
                valor,
                pagina=self.pagina_atual,
                itens_por_pagina=self.itens_por_pagina
            )

        if filtro == "Por Lote":
            return filtrar_historico_por_lote(
                valor,
                pagina=self.pagina_atual,
                itens_por_pagina=self.itens_por_pagina
            )

        if filtro == "Por Entrada":
            return filtrar_historico_por_tipo(
                "entrada",
                pagina=self.pagina_atual,
                itens_por_pagina=self.itens_por_pagina
            )

        if filtro == "Por Saída":
            return filtrar_historico_por_tipo(
                "saida",
                pagina=self.pagina_atual,
                itens_por_pagina=self.itens_por_pagina
            )
        
        if filtro == "Por Período":
            if not data_inicial or not data_final:
                return [], 0

            return filtrar_historico_por_periodo(
                data_inicial,
                data_final,
                pagina=self.pagina_atual,
                itens_por_pagina=self.itens_por_pagina
            )


        return listar_historico(
            pagina=self.pagina_atual,
            itens_por_pagina=self.itens_por_pagina
        )

    def ir_para_pagina_anterior(self):
        if self.pagina_atual > 1:
            self.pagina_atual -= 1
            historico, total = self.obter_resultado_paginado_atual()
            self.carregar_historico(historico, total)

    def ir_para_proxima_pagina(self):
        if self.pagina_atual < self.total_paginas:
            self.pagina_atual += 1
            historico, total = self.obter_resultado_paginado_atual()
            self.carregar_historico(historico, total)

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
            self.logo_img = ctk.CTkImage(
                light_image=Image.open(
                    caminho_recurso(
                        "assets/logo_1.ico"
                    )
                ),
                size=(42, 42)
            )
            label_logo = ctk.CTkLabel(frame_logo, image=self.logo_img, text="")
            label_logo.image = self.logo_img
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

        self.entry_data_inicial = self.criar_campo_data_filtro(linha1, "data_inicial", "Data inicial")
        self.entry_data_final = self.criar_campo_data_filtro(linha1, "data_final", "Data final")

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

        # ctk.CTkLabel(
        #     frame_lista,
        #     text="Histórico de movimentações",
        #     font=("Segoe UI", 18, "bold"),
        #     text_color=self.cor_texto
        # ).pack(anchor="w", padx=20, pady=(20, 10))

        # frame_tabela_area = ctk.CTkFrame(frame_lista, fg_color="transparent")
        # frame_tabela_area.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        frame_lista.grid_columnconfigure(0, weight=1)
        frame_lista.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            frame_lista,
            text="Histórico de movimentações",
            font=("Segoe UI", 18, "bold"),
            text_color=self.cor_texto
        ).grid(row=0, column=0, sticky="w", padx=20, pady=(14, 6))

        frame_tabela_area = ctk.CTkFrame(frame_lista, fg_color="transparent")
        frame_tabela_area.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 4))

        frame_tabela_area.grid_rowconfigure(1, weight=1)
        frame_tabela_area.grid_columnconfigure(0, weight=1)

        # Cabeçalho fixo
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

        # Corpo rolável
        self.canvas_corpo = tk.Canvas(
            frame_tabela_area,
            bg="#ffffff",
            highlightthickness=0,
            bd=0
        )
        self.canvas_corpo.grid(row=1, column=0, sticky="nsew")

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
            text="Página 1 de 1  •  0 movimentação(ões)",
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