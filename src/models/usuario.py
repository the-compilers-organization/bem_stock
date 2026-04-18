def criar_usuario(nome, email, senha, perfil, primeiro_acesso=0):
    return {
        "nome": nome,
        "email": email,
        "senha": senha,
        "perfil": perfil,
        "primeiro_acesso": primeiro_acesso
    }


def usuario_para_tupla(usuario):
    return (
        usuario["nome"],
        usuario["email"],
        usuario["senha"],
        usuario["perfil"],
        usuario["primeiro_acesso"]
    )