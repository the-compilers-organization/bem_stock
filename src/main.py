# from database.schema import inicializar_banco


# def main():
#     print("Iniciando BemStock...")
#     inicializar_banco()
#     print("Banco inicializado com sucesso.")


# if __name__ == "__main__":
#     main()

# from database.schema import inicializar_banco
# from views.login_view import abrir_login


# def main():
#     print("Iniciando BemStock...")
#     inicializar_banco()
#     abrir_login()


# if __name__ == "__main__":
#     main()


# from database.schema import inicializar_banco
# from views.login_view import abrir_login


# def main():
#     print("Iniciando BemStock...")
#     inicializar_banco()
#     abrir_login()


# if __name__ == "__main__":
#     main()


import customtkinter as ctk

from database.schema import inicializar_banco
from views.login_view import LoginView
from views.primeiro_acesso_view import PrimeiroAcessoView
from views.cadastro_usuario_view import CadastroUsuarioView
from views.dashboard_view import DashboardView
from views.produto_view import ProdutoView
from views.cadastro_produto_view import CadastroProdutoView
from views.movimentacao_view import MovimentacaoView
from views.cadastro_movimentacao_view import CadastroMovimentacaoView
from views.usuario_view import UsuarioView


class BemStockApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.title("BemStock")
        self.configure(fg_color="#F5E6F3")

        try:
            self.state("zoomed")
        except Exception:
            self.attributes("-zoomed", True)

        self.resizable(True, True)

        self.usuario_logado = None
        self.frame_atual = None

        self.mostrar_login()

    def limpar_tela(self):
        if self.frame_atual is not None:
            self.frame_atual.destroy()
            self.frame_atual = None

    def mostrar_login(self):
        self.usuario_logado = None
        self.limpar_tela()
        self.title("BemStock - Login")
        self.frame_atual = LoginView(self)
        self.frame_atual.pack(fill="both", expand=True)

    def mostrar_primeiro_acesso(self, usuario):
        self.usuario_logado = usuario
        self.limpar_tela()
        self.title("BemStock - Primeiro Acesso")
        self.frame_atual = PrimeiroAcessoView(self, usuario)
        self.frame_atual.pack(fill="both", expand=True)

    def mostrar_dashboard(self, usuario):
        self.usuario_logado = usuario
        self.limpar_tela()
        self.title("BemStock - Dashboard")
        self.frame_atual = DashboardView(self, usuario)
        self.frame_atual.pack(fill="both", expand=True)

    def mostrar_produto(self, usuario):
        self.usuario_logado = usuario
        self.limpar_tela()
        self.title("BemStock - Produtos")
        self.frame_atual = ProdutoView(self, usuario)
        self.frame_atual.pack(fill="both", expand=True)

    def mostrar_cadastro_produto(self, usuario, produto=None):
        self.usuario_logado = usuario
        self.limpar_tela()
        self.title("BemStock - Cadastro de Produto")
        self.frame_atual = CadastroProdutoView(self, usuario, produto)
        self.frame_atual.pack(fill="both", expand=True)

    def mostrar_movimentacao(self, usuario):
        self.usuario_logado = usuario
        self.limpar_tela()
        self.title("BemStock - Movimentações")
        self.frame_atual = MovimentacaoView(self, usuario)
        self.frame_atual.pack(fill="both", expand=True)

    # def mostrar_cadastro_movimentacao(self, usuario):
    #     self.usuario_logado = usuario
    #     self.limpar_tela()
    #     self.title("BemStock - Cadastro de Movimentação")
    #     self.frame_atual = CadastroMovimentacaoView(self, usuario)
    #     self.frame_atual.pack(fill="both", expand=True)

    def mostrar_cadastro_movimentacao(self, usuario, movimentacao=None):
        self.usuario_logado = usuario
        self.limpar_tela()
        self.title("BemStock - Cadastro de Movimentação")
        self.frame_atual = CadastroMovimentacaoView(self, usuario, movimentacao)
        self.frame_atual.pack(fill="both", expand=True)

    def mostrar_usuario(self, usuario):
        self.usuario_logado = usuario
        self.limpar_tela()
        self.title("BemStock - Usuários")
        self.frame_atual = UsuarioView(self, usuario)
        self.frame_atual.pack(fill="both", expand=True)

    def mostrar_cadastro_usuario(self, usuario, usuario_edicao=None):
        self.usuario_logado = usuario
        self.limpar_tela()
        self.title("BemStock - Cadastro de Usuário")
        self.frame_atual = CadastroUsuarioView(self, usuario, usuario_edicao)
        self.frame_atual.pack(fill="both", expand=True)


def main():
    print("Iniciando BemStock...")
    inicializar_banco()
    app = BemStockApp()
    app.mainloop()


if __name__ == "__main__":
    main()