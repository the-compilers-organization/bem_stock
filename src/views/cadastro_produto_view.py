import customtkinter as ctk
from tkinter import messagebox

from controllers.produto_controller import (
    cadastrar_produto,
    atualizar_produto
)


class CadastroProdutoView(ctk.CTkFrame):
    def __init__(self, master, usuario, produto=None):
        super().__init__(master, fg_color="#F5E6F3")
        self.master = master
        self.usuario = usuario
        self.produto = produto

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

        self.criar_interface()

    def voltar(self):
        self.master.mostrar_produto(self.usuario)

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
        label_erro = self.labels_erro.get(chave)

        if widget is not None:
            try:
                widget.configure(border_color=self.cor_borda_erro)
            except Exception:
                pass

        if label_erro is not None:
            label_erro.configure(text=mensagem)

    def limpar_erro(self, chave):
        widget = self.campos.get(chave)
        label_erro = self.labels_erro.get(chave)

        if widget is not None:
            try:
                widget.configure(border_color=self.cor_borda)
            except Exception:
                pass

        if label_erro is not None:
            label_erro.configure(text="")

    def limpar_todos_erros(self):
        for chave in self.campos.keys():
            self.limpar_erro(chave)

    def ao_entrar_no_campo(self, chave):
        self.limpar_erro(chave)
        widget = self.campos.get(chave)
        if widget is not None:
            self.destacar_foco(widget)

    def ao_sair_do_campo(self, chave, obrigatorio=False):
        widget = self.campos.get(chave)
        if widget is not None:
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

    def validar_campos(self):
        self.limpar_todos_erros()
        valido = True

        nome = self.obter_valor_campo("nome")
        categoria = self.obter_valor_campo("categoria")
        unidade_medida = self.obter_valor_campo("unidade_medida")
        estoque_minimo_texto = self.obter_valor_campo("estoque_minimo")

        if not nome:
            self.marcar_erro("nome", "O nome é obrigatório.")
            valido = False

        if not categoria:
            self.marcar_erro("categoria", "A categoria é obrigatória.")
            valido = False

        if not unidade_medida:
            self.marcar_erro("unidade_medida", "A unidade de medida é obrigatória.")
            valido = False

        if not estoque_minimo_texto:
            self.marcar_erro("estoque_minimo", "O estoque mínimo é obrigatório.")
            valido = False
        else:
            try:
                estoque_minimo = int(estoque_minimo_texto)
                if estoque_minimo < 0:
                    self.marcar_erro("estoque_minimo", "Informe um número maior ou igual a zero.")
                    valido = False
            except ValueError:
                self.marcar_erro("estoque_minimo", "Informe um número inteiro válido.")
                valido = False

        return valido

    def salvar(self):
        if not self.validar_campos():
            return

        nome = self.obter_valor_campo("nome")
        categoria = self.obter_valor_campo("categoria")
        unidade_medida = self.obter_valor_campo("unidade_medida")
        estoque_minimo = int(self.obter_valor_campo("estoque_minimo"))
        descricao = self.obter_valor_campo("descricao")

        if self.produto is None:
            sucesso, mensagem = cadastrar_produto(
                nome,
                categoria,
                unidade_medida,
                estoque_minimo,
                descricao
            )
        else:
            sucesso, mensagem = atualizar_produto(
                self.produto["id_produto"],
                nome,
                categoria,
                unidade_medida,
                estoque_minimo,
                descricao
            )

        if sucesso:
            messagebox.showinfo("Sucesso", mensagem)
            self.master.mostrar_produto(self.usuario)
        else:
            self.tratar_erro_controller(mensagem)
            messagebox.showerror("Erro", mensagem)

    def tratar_erro_controller(self, mensagem):
        texto = mensagem.lower()

        if "nome" in texto:
            self.marcar_erro("nome", mensagem)
        elif "categoria" in texto:
            self.marcar_erro("categoria", mensagem)
        elif "unidade" in texto:
            self.marcar_erro("unidade_medida", mensagem)
        elif "estoque mínimo" in texto or "estoque minimo" in texto:
            self.marcar_erro("estoque_minimo", mensagem)

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

    def criar_entry(self, parent, chave, valor="", obrigatorio=False):
        entry = ctk.CTkEntry(
            parent,
            height=40,
            corner_radius=6,
            border_width=1,
            border_color=self.cor_borda,
            fg_color=self.cor_input,
            text_color=self.cor_texto,
            font=("Segoe UI", 14)
        )
        entry.pack(fill="x", pady=(0, 4))
        if valor is not None and str(valor) != "":
            entry.insert(0, str(valor))

        entry.bind("<FocusIn>", lambda event, c=chave: self.ao_entrar_no_campo(c))
        entry.bind("<FocusOut>", lambda event, c=chave, o=obrigatorio: self.ao_sair_do_campo(c, o))

        self.campos[chave] = entry
        self.criar_label_erro(parent, chave)

    def criar_combobox(self, parent, chave, values, valor_inicial="", obrigatorio=False):
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
            font=("Segoe UI", 14)
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

        titulo = "Cadastrar Produto" if self.produto is None else "Editar Produto"

        ctk.CTkLabel(
            topo,
            text=titulo,
            font=("Segoe UI", 28, "bold"),
            text_color=self.cor_texto
        ).pack(anchor="w", padx=25, pady=(18, 0))

        ctk.CTkLabel(
            topo,
            text="Preencha os dados do produto",
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

        self.criar_label(scroll, "Nome*")
        self.criar_entry(
            scroll,
            "nome",
            self.produto["nome"] if self.produto else "",
            obrigatorio=True
        )

        self.criar_label(scroll, "Categoria*")
        self.criar_combobox(
            scroll,
            "categoria",
            ["Alimentos", "Limpeza", "Higiene Pessoal"],
            self.produto["categoria"] if self.produto else "Alimentos",
            obrigatorio=True
        )

        self.criar_label(scroll, "Unidade de Medida*")
        self.criar_combobox(
            scroll,
            "unidade_medida",
            ["unidade", "pacote", "caixa", "litros", "ml", "kg", "grama"],
            self.produto["unidade_medida"] if self.produto else "unidade",
            obrigatorio=True
        )

        self.criar_label(scroll, "Estoque Mínimo*")
        self.criar_entry(
            scroll,
            "estoque_minimo",
            self.produto["estoque_minimo"] if self.produto else "0",
            obrigatorio=True
        )

        self.criar_label(scroll, "Descrição")
        self.criar_entry(
            scroll,
            "descricao",
            self.produto["descricao"] if self.produto else "",
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
            text="Salvar Produto",
            height=45,
            corner_radius=6,
            fg_color=self.cor_roxo,
            hover_color=self.cor_roxo_hover,
            text_color="#ffffff",
            font=("Segoe UI", 14, "bold"),
            command=self.salvar
        )
        btn_salvar.pack(side="left", expand=True, fill="x", padx=(6, 0))