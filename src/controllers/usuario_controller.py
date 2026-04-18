from database.connection import conectar
from models.usuario import criar_usuario, usuario_para_tupla
from utils.validacoes import campo_preenchido, email_valido, perfil_valido
from utils.seguranca import gerar_hash_senha


def _contar_usuarios(where_clause="", params=()):
    conexao = conectar()
    cursor = conexao.cursor()

    query = f"""
        SELECT COUNT(*) AS total
        FROM usuarios
        {where_clause}
    """

    cursor.execute(query, params)
    resultado = cursor.fetchone()
    conexao.close()

    return resultado["total"] if resultado else 0


def _listar_usuarios_base(where_clause="", params=(), limite=None, offset=None):
    conexao = conectar()
    cursor = conexao.cursor()

    query = f"""
        SELECT id_usuario, nome, email, perfil, primeiro_acesso
        FROM usuarios
        {where_clause}
        ORDER BY nome
    """

    parametros = list(params)

    if limite is not None:
        query += " LIMIT ?"
        parametros.append(limite)

        if offset is not None:
            query += " OFFSET ?"
            parametros.append(offset)

    cursor.execute(query, tuple(parametros))
    usuarios = cursor.fetchall()

    conexao.close()
    return [dict(usuario) for usuario in usuarios]


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
        (email.strip(),)
    )
    usuario_existente = cursor.fetchone()

    if usuario_existente is not None:
        conexao.close()
        return False, "Já existe um usuário com esse e-mail."

    usuario = criar_usuario(
        nome=nome.strip(),
        email=email.strip(),
        senha=gerar_hash_senha(senha),
        perfil=perfil,
        primeiro_acesso=0
    )

    cursor.execute(
        """
        INSERT INTO usuarios (nome, email, senha, perfil, primeiro_acesso)
        VALUES (?, ?, ?, ?, ?)
        """,
        usuario_para_tupla(usuario)
    )

    conexao.commit()
    conexao.close()

    return True, "Usuário cadastrado com sucesso."


def listar_usuarios(pagina=1, itens_por_pagina=10):
    if pagina < 1:
        pagina = 1

    offset = (pagina - 1) * itens_por_pagina
    total = _contar_usuarios()
    usuarios = _listar_usuarios_base(
        limite=itens_por_pagina,
        offset=offset
    )

    return usuarios, total


def buscar_usuarios_por_nome(nome, pagina=1, itens_por_pagina=10):
    if pagina < 1:
        pagina = 1

    where_clause = "WHERE nome LIKE ?"
    params = (f"%{nome.strip()}%",)
    offset = (pagina - 1) * itens_por_pagina

    total = _contar_usuarios(where_clause, params)
    usuarios = _listar_usuarios_base(
        where_clause,
        params,
        limite=itens_por_pagina,
        offset=offset
    )

    return usuarios, total


def buscar_usuarios_por_email(email, pagina=1, itens_por_pagina=10):
    if pagina < 1:
        pagina = 1

    where_clause = "WHERE email LIKE ?"
    params = (f"%{email.strip()}%",)
    offset = (pagina - 1) * itens_por_pagina

    total = _contar_usuarios(where_clause, params)
    usuarios = _listar_usuarios_base(
        where_clause,
        params,
        limite=itens_por_pagina,
        offset=offset
    )

    return usuarios, total


def buscar_usuario_por_id(id_usuario):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT id_usuario, nome, email, perfil, primeiro_acesso
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
        (email.strip(), id_usuario)
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
        (nome.strip(), email.strip(), perfil, id_usuario)
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


def concluir_primeiro_acesso(id_usuario, novo_email, nova_senha):
    if not campo_preenchido(novo_email):
        return False, "O e-mail é obrigatório."

    if not email_valido(novo_email):
        return False, "Informe um e-mail válido."

    if not campo_preenchido(nova_senha):
        return False, "A senha é obrigatória."

    novo_email = novo_email.strip()

    if novo_email.lower() == "teste@bemstock.com":
        return False, "Informe um novo e-mail diferente do temporário."

    if nova_senha == "123456":
        return False, "Informe uma nova senha diferente da temporária."

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT id_usuario, perfil, primeiro_acesso
        FROM usuarios
        WHERE id_usuario = ?
        """,
        (id_usuario,)
    )
    usuario = cursor.fetchone()

    if usuario is None:
        conexao.close()
        return False, "Usuário não encontrado."

    cursor.execute(
        """
        SELECT id_usuario
        FROM usuarios
        WHERE email = ? AND id_usuario != ?
        """,
        (novo_email, id_usuario)
    )
    email_existente = cursor.fetchone()

    if email_existente is not None:
        conexao.close()
        return False, "Já existe um usuário com esse e-mail."

    try:
        cursor.execute(
            """
            UPDATE usuarios
            SET email = ?, senha = ?, primeiro_acesso = 0
            WHERE id_usuario = ?
            """,
            (
                novo_email,
                gerar_hash_senha(nova_senha),
                id_usuario
            )
        )

        conexao.commit()
        return True, "Primeiro acesso concluído com sucesso."

    except Exception as e:
        return False, f"Erro ao concluir primeiro acesso: {str(e)}"

    finally:
        conexao.close()


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

    if usuario["email"] == "teste@bemstock.com":
        conexao.close()
        return False, "O usuário administrador temporário não pode ser excluído."

    cursor.execute(
        "DELETE FROM usuarios WHERE id_usuario = ?",
        (id_usuario,)
    )

    conexao.commit()
    conexao.close()

    return True, "Usuário excluído com sucesso."