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

from database.schema import inicializar_banco
from views.login_view import LoginView
from views.cadastro_usuario_view import CadastroUsuarioView
from views.dashboard_view import DashboardView
import customtkinter as ctk


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
        self.limpar_tela()
        self.title("BemStock - Login")
        self.frame_atual = LoginView(self)
        self.frame_atual.pack(fill="both", expand=True)

    def mostrar_cadastro(self):
        self.limpar_tela()
        self.title("BemStock - Cadastro de Usuário")
        self.frame_atual = CadastroUsuarioView(self)
        self.frame_atual.pack(fill="both", expand=True)

    def mostrar_dashboard(self, usuario):
        self.usuario_logado = usuario
        self.limpar_tela()
        self.title("BemStock - Dashboard")
        self.frame_atual = DashboardView(self, usuario)
        self.frame_atual.pack(fill="both", expand=True)


def main():
    print("Iniciando BemStock...")
    inicializar_banco()
    app = BemStockApp()
    app.mainloop()


if __name__ == "__main__":
    main()