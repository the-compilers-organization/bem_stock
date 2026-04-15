from database.connection import conectar
from models.usuario import criar_usuario, usuario_para_tupla
from utils.validacoes import campo_preenchido, email_valido, perfil_valido
from utils.seguranca import gerar_hash_senha


def cadastrar_usuario(nome, email, senha, perfil):
    if not campo_preenchido(nome):
        return False, "O nome é obrigatório."

    if not campo_preenchido(email):
        return False, "O e-mail é obrigatório."

    if not email_valido(email):
        return False, "Informe um e-mail válido."

    if not campo_preenchido(senha):
        return False, "A senha é obrigatória."

    if not perfil_valido(perfil):
        return False, "Perfil inválido."

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "SELECT id_usuario FROM usuarios WHERE email = ?",
        (email,)
    )
    usuario_existente = cursor.fetchone()

    if usuario_existente is not None:
        conexao.close()
        return False, "Já existe um usuário com esse e-mail."

    usuario = criar_usuario(
        nome=nome,
        email=email,
        senha=gerar_hash_senha(senha),
        perfil=perfil
    )

    cursor.execute(
        """
        INSERT INTO usuarios (nome, email, senha, perfil)
        VALUES (?, ?, ?, ?)
        """,
        usuario_para_tupla(usuario)
    )

    conexao.commit()
    conexao.close()

    return True, "Usuário cadastrado com sucesso."


def listar_usuarios():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT id_usuario, nome, email, perfil
        FROM usuarios
        ORDER BY nome
        """
    )
    usuarios = cursor.fetchall()

    conexao.close()
    return [dict(usuario) for usuario in usuarios]


def buscar_usuarios_por_nome(nome):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT id_usuario, nome, email, perfil
        FROM usuarios
        WHERE nome LIKE ?
        ORDER BY nome
        """,
        (f"%{nome}%",)
    )
    usuarios = cursor.fetchall()

    conexao.close()
    return [dict(usuario) for usuario in usuarios]


def buscar_usuarios_por_email(email):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT id_usuario, nome, email, perfil
        FROM usuarios
        WHERE email LIKE ?
        ORDER BY nome
        """,
        (f"%{email}%",)
    )
    usuarios = cursor.fetchall()

    conexao.close()
    return [dict(usuario) for usuario in usuarios]


def buscar_usuario_por_id(id_usuario):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT id_usuario, nome, email, perfil
        FROM usuarios
        WHERE id_usuario = ?
        """,
        (id_usuario,)
    )
    usuario = cursor.fetchone()

    conexao.close()

    if usuario is None:
        return None

    return dict(usuario)


def atualizar_usuario(id_usuario, nome, email, perfil):
    if not campo_preenchido(nome):
        return False, "O nome é obrigatório."

    if not campo_preenchido(email):
        return False, "O e-mail é obrigatório."

    if not email_valido(email):
        return False, "Informe um e-mail válido."

    if not perfil_valido(perfil):
        return False, "Perfil inválido."

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "SELECT id_usuario FROM usuarios WHERE id_usuario = ?",
        (id_usuario,)
    )
    usuario = cursor.fetchone()

    if usuario is None:
        conexao.close()
        return False, "Usuário não encontrado."

    cursor.execute(
        """
        SELECT id_usuario FROM usuarios
        WHERE email = ? AND id_usuario != ?
        """,
        (email, id_usuario)
    )
    email_existente = cursor.fetchone()

    if email_existente is not None:
        conexao.close()
        return False, "Já existe outro usuário com esse e-mail."

    cursor.execute(
        """
        UPDATE usuarios
        SET nome = ?, email = ?, perfil = ?
        WHERE id_usuario = ?
        """,
        (nome, email, perfil, id_usuario)
    )

    conexao.commit()
    conexao.close()

    return True, "Usuário atualizado com sucesso."


def atualizar_senha_usuario(id_usuario, nova_senha):
    if not campo_preenchido(nova_senha):
        return False, "A nova senha é obrigatória."

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "SELECT id_usuario FROM usuarios WHERE id_usuario = ?",
        (id_usuario,)
    )
    usuario = cursor.fetchone()

    if usuario is None:
        conexao.close()
        return False, "Usuário não encontrado."

    senha_hash = gerar_hash_senha(nova_senha)

    cursor.execute(
        """
        UPDATE usuarios
        SET senha = ?
        WHERE id_usuario = ?
        """,
        (senha_hash, id_usuario)
    )

    conexao.commit()
    conexao.close()

    return True, "Senha atualizada com sucesso."


def excluir_usuario(id_usuario):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "SELECT id_usuario, email FROM usuarios WHERE id_usuario = ?",
        (id_usuario,)
    )
    usuario = cursor.fetchone()

    if usuario is None:
        conexao.close()
        return False, "Usuário não encontrado."

    if usuario["email"] == "admin@bemstock.com":
        conexao.close()
        return False, "O usuário administrador padrão não pode ser excluído."

    cursor.execute(
        "DELETE FROM usuarios WHERE id_usuario = ?",
        (id_usuario,)
    )

    conexao.commit()
    conexao.close()

    return True, "Usuário excluído com sucesso."