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
from views.login_view import abrir_login


def main():
    try:
        print("Iniciando BemStock...")
        inicializar_banco()
        abrir_login()
    except Exception as e:
        print("Erro ao iniciar o sistema:")
        print(e)


if __name__ == "__main__":
    main()