def criar_usuario(nome, email, senha, perfil):
    return {
        "nome": nome,
        "email": email,
        "senha": senha,
        "perfil": perfil
    }


def usuario_para_tupla(usuario):
    return (
        usuario["nome"],
        usuario["email"],
        usuario["senha"],
        usuario["perfil"]
    )