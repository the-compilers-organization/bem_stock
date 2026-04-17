import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime

from tkcalendar import Calendar

from controllers.movimentacao_controller import registrar_entrada, registrar_saida
from controllers.produto_controller import listar_produtos


class CadastroMovimentacaoView(ctk.CTkFrame):
    def __init__(self, master, usuario):
        super().__init__(master, fg_color="#F5E6F3")
        self.master = master
        self.usuario = usuario

        self.cor_texto = "#1a1a1a"
        self.cor_texto_secundario = "#666666"
        self.cor_borda = "#d0d0d0"
        self.cor_borda_foco = "#C084FC"
        self.cor_borda_erro = "#ef4444"
        self.cor_input = "#f8f8f8"
        self.cor_roxo = "#a855f7"
        self.cor_roxo_hover = "#9333ea"
        self.cor_hover_secundario = "#f5f5f5"

        self.campos = {}
        self.labels_erro = {}
        self.produtos = []
        self.produtos_map = {}
        self.calendario_popup = None

        self.carregar_produtos()
        self.criar_interface()

    def carregar_produtos(self):
        try:
            self.produtos = listar_produtos()
            self.produtos_map = {
                f"{produto['id_produto']} - {produto['nome']}": produto
                for produto in self.produtos
            }
        except Exception:
            self.produtos = []
            self.produtos_map = {}

    def voltar(self):
        self.master.mostrar_movimentacao(self.usuario)

    def destacar_foco(self, widget):
        try:
            widget.configure(border_color=self.cor_borda_foco)
        except Exception:
            pass

    def remover_destaque(self, widget):
        try:
            widget.configure(border_color=self.cor_borda)
        except Exception:
            pass

    def marcar_erro(self, chave, mensagem="Campo obrigatório."):
        widget = self.campos.get(chave)
        frame = self.campos.get(f"{chave}_frame")
        label_erro = self.labels_erro.get(chave)

        if frame is not None:
            frame.configure(border_color=self.cor_borda_erro)
        elif widget is not None:
            try:
                widget.configure(border_color=self.cor_borda_erro)
            except Exception:
                pass

        if label_erro is not None:
            label_erro.configure(text=mensagem)

    def limpar_erro(self, chave):
        widget = self.campos.get(chave)
        frame = self.campos.get(f"{chave}_frame")
        label_erro = self.labels_erro.get(chave)

        if frame is not None:
            frame.configure(border_color=self.cor_borda)
        elif widget is not None:
            try:
                widget.configure(border_color=self.cor_borda)
            except Exception:
                pass

        if label_erro is not None:
            label_erro.configure(text="")

    def limpar_todos_erros(self):
        for chave in self.labels_erro.keys():
            self.limpar_erro(chave)

    def ao_entrar_no_campo(self, chave):
        self.limpar_erro(chave)
        widget = self.campos.get(chave)
        frame = self.campos.get(f"{chave}_frame")

        if frame is not None:
            frame.configure(border_color=self.cor_borda_foco)
        elif widget is not None:
            self.destacar_foco(widget)

    def ao_sair_do_campo(self, chave, obrigatorio=False):
        widget = self.campos.get(chave)
        frame = self.campos.get(f"{chave}_frame")

        if frame is not None:
            frame.configure(border_color=self.cor_borda)
        elif widget is not None:
            self.remover_destaque(widget)

        valor = self.obter_valor_campo(chave)

        if obrigatorio and not valor:
            self.marcar_erro(chave, "Campo obrigatório.")

    def obter_valor_campo(self, chave):
        widget = self.campos.get(chave)
        if widget is None:
            return ""

        try:
            return widget.get().strip()
        except Exception:
            return ""

    def criar_label(self, parent, texto):
        ctk.CTkLabel(
            parent,
            text=texto,
            font=("Segoe UI", 13, "bold"),
            text_color=self.cor_texto,
            anchor="w"
        ).pack(anchor="w", pady=(0, 5))

    def criar_label_erro(self, parent, chave):
        label = ctk.CTkLabel(
            parent,
            text="",
            font=("Segoe UI", 11),
            text_color=self.cor_borda_erro,
            anchor="w"
        )
        label.pack(anchor="w", pady=(0, 10))
        self.labels_erro[chave] = label

    def criar_entry(self, parent, chave, valor="", placeholder="", obrigatorio=False):
        entry = ctk.CTkEntry(
            parent,
            height=40,
            corner_radius=6,
            border_width=1,
            border_color=self.cor_borda,
            fg_color=self.cor_input,
            text_color=self.cor_texto,
            font=("Segoe UI", 14),
            placeholder_text=placeholder
        )
        entry.pack(fill="x", pady=(0, 4))

        if valor not in (None, ""):
            entry.insert(0, str(valor))

        entry.bind("<FocusIn>", lambda event, c=chave: self.ao_entrar_no_campo(c))
        entry.bind("<FocusOut>", lambda event, c=chave, o=obrigatorio: self.ao_sair_do_campo(c, o))

        self.campos[chave] = entry
        self.criar_label_erro(parent, chave)
        return entry

    def criar_combobox(self, parent, chave, values, valor_inicial="", obrigatorio=False, command=None):
        combo = ctk.CTkComboBox(
            parent,
            height=40,
            values=values,
            corner_radius=6,
            border_width=1,
            border_color=self.cor_borda,
            fg_color=self.cor_input,
            button_color=self.cor_roxo,
            button_hover_color=self.cor_roxo_hover,
            text_color=self.cor_texto,
            dropdown_fg_color="#ffffff",
            dropdown_text_color=self.cor_texto,
            dropdown_hover_color="#f0f0f0",
            font=("Segoe UI", 14),
            command=command
        )
        combo.pack(fill="x", pady=(0, 4))

        if valor_inicial:
            combo.set(valor_inicial)
        elif values:
            combo.set(values[0])

        combo.bind("<FocusIn>", lambda event, c=chave: self.ao_entrar_no_campo(c))
        combo.bind("<FocusOut>", lambda event, c=chave, o=obrigatorio: self.ao_sair_do_campo(c, o))

        self.campos[chave] = combo
        self.criar_label_erro(parent, chave)
        return combo

    def abrir_calendario_popup(self, chave):
        if self.calendario_popup is not None and self.calendario_popup.winfo_exists():
            self.calendario_popup.destroy()

        entry = self.campos[chave]
        frame_input = self.campos.get(f"{chave}_frame")

        self.limpar_erro(chave)
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
                frame_input.configure(border_color=self.cor_borda)
            popup.destroy()

        def cancelar():
            if frame_input is not None:
                frame_input.configure(border_color=self.cor_borda)
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
            hover_color=self.cor_hover_secundario,
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

    def criar_dateentry(self, parent, chave, obrigatorio=False):
        frame_input = ctk.CTkFrame(
            parent,
            height=40,
            corner_radius=6,
            border_width=1,
            border_color=self.cor_borda,
            fg_color=self.cor_input
        )
        frame_input.pack(fill="x", pady=(0, 4))
        frame_input.pack_propagate(False)
        frame_input.grid_columnconfigure(0, weight=1)

        entry = ctk.CTkEntry(
            frame_input,
            height=32,
            corner_radius=0,
            border_width=0,
            fg_color=self.cor_input,
            text_color=self.cor_texto,
            font=("Segoe UI", 14)
        )
        entry.grid(row=0, column=0, sticky="nsew", padx=(8, 0), pady=4)

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

        entry.bind("<FocusIn>", lambda event, c=chave: self.ao_entrar_no_campo(c))
        entry.bind("<FocusOut>", lambda event, c=chave, o=obrigatorio: self.ao_sair_do_campo(c, o))

        self.campos[chave] = entry
        self.campos[f"{chave}_frame"] = frame_input
        self.criar_label_erro(parent, chave)

        return entry

    def atualizar_tipo_movimentacao(self, _valor=None):
        tipo = self.campos["tipo_movimentacao"].get()

        self.frame_campos_entrada.pack_forget()
        self.frame_campos_saida.pack_forget()

        if tipo == "entrada":
            self.frame_campos_entrada.pack(fill="x", pady=(0, 0))
        else:
            self.frame_campos_saida.pack(fill="x", pady=(0, 0))

    def atualizar_categoria_do_produto(self, _valor=None):
        produto_texto = self.campos["produto"].get()
        produto = self.produtos_map.get(produto_texto)

        self.campos["categoria"].configure(state="normal")
        self.campos["categoria"].delete(0, "end")

        if produto:
            self.campos["categoria"].insert(0, produto["categoria"])

        self.campos["categoria"].configure(state="disabled")

    def validar_campos(self):
        self.limpar_todos_erros()
        valido = True

        tipo = self.obter_valor_campo("tipo_movimentacao")
        produto = self.obter_valor_campo("produto")
        quantidade_texto = self.obter_valor_campo("quantidade")

        if not tipo:
            self.marcar_erro("tipo_movimentacao", "Selecione o tipo de movimentação.")
            valido = False

        if not produto or produto not in self.produtos_map:
            self.marcar_erro("produto", "Selecione um produto válido.")
            valido = False

        if not quantidade_texto:
            self.marcar_erro("quantidade", "A quantidade é obrigatória.")
            valido = False
        else:
            try:
                quantidade = int(quantidade_texto)
                if quantidade <= 0:
                    self.marcar_erro("quantidade", "Informe um número inteiro maior que zero.")
                    valido = False
            except ValueError:
                self.marcar_erro("quantidade", "Informe um número inteiro válido.")
                valido = False

        if tipo == "entrada":
            data_br = self.obter_valor_campo("data_validade")
            if not data_br:
                self.marcar_erro("data_validade", "A data de validade é obrigatória.")
                valido = False
            else:
                try:
                    datetime.strptime(data_br, "%d/%m/%Y")
                except ValueError:
                    self.marcar_erro("data_validade", "Data inválida.")
                    valido = False

        if tipo == "saida":
            destino = self.obter_valor_campo("destino")
            if not destino:
                self.marcar_erro("destino", "O destino é obrigatório.")
                valido = False

        return valido

    def tratar_erro_controller(self, mensagem, tipo):
        texto = mensagem.lower()

        if "produto" in texto:
            self.marcar_erro("produto", mensagem)
        elif "categoria" in texto:
            self.marcar_erro("categoria", mensagem)
        elif "quantidade" in texto:
            self.marcar_erro("quantidade", mensagem)
        elif "validade" in texto:
            self.marcar_erro("data_validade", mensagem)
        elif "destino" in texto:
            self.marcar_erro("destino", mensagem)
        elif "fornecedor" in texto and tipo == "entrada":
            self.marcar_erro("fornecedor", mensagem)
        elif "lote" in texto and tipo == "entrada":
            self.marcar_erro("numero_lote", mensagem)

    def salvar(self):
        if not self.validar_campos():
            return

        produto_texto = self.campos["produto"].get().strip()
        produto = self.produtos_map.get(produto_texto)

        quantidade = int(self.campos["quantidade"].get().strip())
        tipo = self.campos["tipo_movimentacao"].get().strip()
        id_usuario = self.usuario.get("id_usuario")

        if tipo == "entrada":
            data_br = self.campos["data_validade"].get().strip()

            try:
                data_validade_formatada = datetime.strptime(
                    data_br,
                    "%d/%m/%Y"
                ).strftime("%Y-%m-%d")
            except ValueError:
                self.marcar_erro("data_validade", "A data de validade informada é inválida.")
                return

            sucesso, mensagem = registrar_entrada(
                id_produto=produto["id_produto"],
                categoria=produto["categoria"],
                quantidade=quantidade,
                data_validade=data_validade_formatada,
                fornecedor=self.campos["fornecedor"].get().strip(),
                numero_lote=self.campos["numero_lote"].get().strip(),
                observacoes=self.campos["observacoes_entrada"].get().strip(),
                id_usuario=id_usuario
            )
        else:
            sucesso, mensagem = registrar_saida(
                id_produto=produto["id_produto"],
                quantidade=quantidade,
                destino=self.campos["destino"].get().strip(),
                observacoes=self.campos["observacoes_saida"].get().strip(),
                id_usuario=id_usuario
            )

        if sucesso:
            messagebox.showinfo("Sucesso", mensagem)
            self.master.mostrar_movimentacao(self.usuario)
        else:
            self.tratar_erro_controller(mensagem, tipo)
            messagebox.showerror("Erro", mensagem)

    def criar_interface(self):
        frame_principal = ctk.CTkFrame(self, fg_color="transparent")
        frame_principal.pack(fill="both", expand=True, padx=20, pady=20)

        topo = ctk.CTkFrame(
            frame_principal,
            height=90,
            corner_radius=15,
            fg_color="#ffffff",
            border_width=1,
            border_color="#e0e0e0"
        )
        topo.pack(fill="x", pady=(0, 20))
        topo.pack_propagate(False)

        ctk.CTkLabel(
            topo,
            text="Cadastrar Movimentação",
            font=("Segoe UI", 28, "bold"),
            text_color=self.cor_texto
        ).pack(anchor="w", padx=25, pady=(18, 0))

        ctk.CTkLabel(
            topo,
            text="Preencha os dados da movimentação",
            font=("Segoe UI", 13),
            text_color=self.cor_texto_secundario
        ).pack(anchor="w", padx=25, pady=(2, 0))

        frame_form = ctk.CTkFrame(
            frame_principal,
            fg_color="#ffffff",
            corner_radius=15,
            border_width=1,
            border_color="#e0e0e0"
        )
        frame_form.pack(fill="both", expand=True)

        scroll = ctk.CTkScrollableFrame(
            frame_form,
            fg_color="transparent"
        )
        scroll.pack(fill="both", expand=True, padx=24, pady=(24, 12))

        self.criar_label(scroll, "Tipo de Movimentação*")
        self.criar_combobox(
            scroll,
            "tipo_movimentacao",
            ["entrada", "saida"],
            "entrada",
            obrigatorio=True,
            command=self.atualizar_tipo_movimentacao
        )

        self.criar_label(scroll, "Produto*")
        valores_produto = list(self.produtos_map.keys()) if self.produtos_map else ["Nenhum produto cadastrado"]
        valor_inicial_produto = valores_produto[0] if valores_produto and valores_produto[0] != "Nenhum produto cadastrado" else ""
        self.criar_combobox(
            scroll,
            "produto",
            valores_produto,
            valor_inicial_produto,
            obrigatorio=True,
            command=self.atualizar_categoria_do_produto
        )

        self.criar_label(scroll, "Categoria*")
        entry_categoria = ctk.CTkEntry(
            scroll,
            height=40,
            corner_radius=6,
            border_width=1,
            border_color=self.cor_borda,
            fg_color=self.cor_input,
            text_color=self.cor_texto,
            font=("Segoe UI", 14),
            state="disabled"
        )
        entry_categoria.pack(fill="x", pady=(0, 4))
        self.campos["categoria"] = entry_categoria
        self.criar_label_erro(scroll, "categoria")

        self.criar_label(scroll, "Quantidade*")
        self.criar_entry(
            scroll,
            "quantidade",
            placeholder="Digite a quantidade",
            obrigatorio=True
        )

        self.frame_campos_entrada = ctk.CTkFrame(scroll, fg_color="transparent")

        self.criar_label(self.frame_campos_entrada, "Data de Validade*")
        self.criar_dateentry(
            self.frame_campos_entrada,
            "data_validade",
            obrigatorio=True
        )

        self.criar_label(self.frame_campos_entrada, "Fornecedor")
        self.criar_entry(
            self.frame_campos_entrada,
            "fornecedor",
            placeholder="Fornecedor (opcional)",
            obrigatorio=False
        )

        self.criar_label(self.frame_campos_entrada, "Número do Lote")
        self.criar_entry(
            self.frame_campos_entrada,
            "numero_lote",
            placeholder="Número do lote (opcional)",
            obrigatorio=False
        )

        self.criar_label(self.frame_campos_entrada, "Observações")
        self.criar_entry(
            self.frame_campos_entrada,
            "observacoes_entrada",
            placeholder="Observações (opcional)",
            obrigatorio=False
        )

        self.frame_campos_saida = ctk.CTkFrame(scroll, fg_color="transparent")

        self.criar_label(self.frame_campos_saida, "Destino*")
        self.criar_combobox(
            self.frame_campos_saida,
            "destino",
            [
                "cozinha",
                "banheiros",
                "area de servico",
                "lavanderia",
                "refeitorio",
                "outros"
            ],
            "cozinha",
            obrigatorio=True
        )

        self.criar_label(self.frame_campos_saida, "Observações")
        self.criar_entry(
            self.frame_campos_saida,
            "observacoes_saida",
            placeholder="Observações (opcional)",
            obrigatorio=False
        )

        frame_botoes = ctk.CTkFrame(frame_form, fg_color="transparent")
        frame_botoes.pack(fill="x", padx=24, pady=(0, 24))

        btn_voltar = ctk.CTkButton(
            frame_botoes,
            text="← Voltar",
            height=45,
            corner_radius=6,
            border_width=1,
            border_color="#d0d0d0",
            fg_color="#ffffff",
            hover_color=self.cor_hover_secundario,
            text_color="#1a1a1a",
            font=("Segoe UI", 14, "bold"),
            command=self.voltar
        )
        btn_voltar.pack(side="left", expand=True, fill="x", padx=(0, 6))

        btn_salvar = ctk.CTkButton(
            frame_botoes,
            text="Salvar Movimentação",
            height=45,
            corner_radius=6,
            fg_color=self.cor_roxo,
            hover_color=self.cor_roxo_hover,
            text_color="#ffffff",
            font=("Segoe UI", 14, "bold"),
            command=self.salvar
        )
        btn_salvar.pack(side="left", expand=True, fill="x", padx=(6, 0))

        self.atualizar_categoria_do_produto()
        self.atualizar_tipo_movimentacao()