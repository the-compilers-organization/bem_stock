from database.connection import conectar
from models.movimentacao import criar_movimentacao, movimentacao_para_tupla
from utils.validacoes import (
    categoria_valida,
    quantidade_movimentacao_valida,
    data_valida,
    destino_valido,
    campo_preenchido
)
from utils.formatadores import (
    data_atual_formatada,
    formatar_data_para_exibicao,
    formatar_data_hora_para_exibicao
)


def _enriquecer_registros(registros):
    resultado = []

    for item in registros:
        registro = dict(item)

        tipo = registro.get("tipo_movimentacao")

        if tipo == "entrada":
            registro["tipo_movimentacao"] = "Entrada"
        elif tipo == "saida":
            registro["tipo_movimentacao"] = "Saída"
        else:
            registro["tipo_movimentacao"] = "Movimentação"

        registro["data_validade_formatada"] = formatar_data_para_exibicao(
            registro.get("data_validade")
        )

        registro["data_movimentacao_formatada"] = formatar_data_hora_para_exibicao(
            registro.get("data_movimentacao")
        )

        resultado.append(registro)

    return resultado


def _contar_historico(where_clause="", params=()):
    conexao = conectar()
    cursor = conexao.cursor()

    query = f"""
        SELECT COUNT(*) AS total
        FROM movimentacoes m
        JOIN produtos p ON m.id_produto = p.id_produto
        JOIN usuarios u ON m.id_usuario = u.id_usuario
        {where_clause}
    """

    cursor.execute(query, params)
    resultado = cursor.fetchone()
    conexao.close()

    return resultado["total"] if resultado else 0


def _buscar_historico(where_clause="", params=(), limite=None, offset=None):
    conexao = conectar()
    cursor = conexao.cursor()

    query = f"""
        SELECT
            m.id_movimentacao,
            m.tipo_movimentacao,
            m.id_produto,
            m.categoria,
            m.quantidade,
            m.fornecedor,
            m.data_validade,
            m.numero_lote,
            m.destino,
            m.observacoes,
            m.data_movimentacao,
            p.nome AS nome_produto,
            p.unidade_medida AS unidade_medida_produto,
            u.nome AS nome_usuario,
            u.email AS email_usuario,
            m.id_usuario
        FROM movimentacoes m
        JOIN produtos p ON m.id_produto = p.id_produto
        JOIN usuarios u ON m.id_usuario = u.id_usuario
        {where_clause}
        ORDER BY m.data_movimentacao DESC, m.id_movimentacao DESC
    """

    parametros = list(params)

    if limite is not None:
        query += " LIMIT ?"
        parametros.append(limite)

        if offset is not None:
            query += " OFFSET ?"
            parametros.append(offset)

    cursor.execute(query, tuple(parametros))
    registros = cursor.fetchall()
    conexao.close()

    return _enriquecer_registros(registros)


def registrar_entrada(
    id_produto,
    categoria,
    quantidade,
    data_validade,
    fornecedor,
    numero_lote,
    observacoes,
    id_usuario
):
    if not isinstance(id_produto, int) or id_produto <= 0:
        return False, "Produto inválido."

    if not categoria_valida(categoria):
        return False, "Categoria inválida."

    if not quantidade_movimentacao_valida(quantidade):
        return False, "A quantidade de entrada deve ser maior que zero."

    if not data_valida(data_validade):
        return False, "A data de validade é obrigatória e deve estar no formato YYYY-MM-DD."

    if not campo_preenchido(fornecedor):
        return False, "O fornecedor é obrigatório para entrada."

    if not isinstance(id_usuario, int) or id_usuario <= 0:
        return False, "Usuário inválido."

    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute(
            """
            SELECT id_produto, categoria
            FROM produtos
            WHERE id_produto = ?
            """,
            (id_produto,)
        )
        produto = cursor.fetchone()

        if produto is None:
            return False, "Produto não encontrado."

        if produto["categoria"] != categoria:
            return False, "A categoria informada não corresponde à categoria do produto."

        cursor.execute(
            """
            SELECT id_usuario
            FROM usuarios
            WHERE id_usuario = ?
            """,
            (id_usuario,)
        )
        usuario = cursor.fetchone()

        if usuario is None:
            return False, "Usuário não encontrado."

        movimentacao = criar_movimentacao(
            tipo_movimentacao="entrada",
            id_produto=id_produto,
            categoria=categoria,
            quantidade=quantidade,
            fornecedor=fornecedor.strip(),
            data_validade=data_validade.strip(),
            numero_lote=numero_lote.strip() if numero_lote else None,
            destino=None,
            observacoes=observacoes.strip() if observacoes else None,
            data_movimentacao=data_atual_formatada(),
            id_usuario=id_usuario
        )

        cursor.execute(
            """
            INSERT INTO movimentacoes (
                tipo_movimentacao,
                id_produto,
                categoria,
                quantidade,
                fornecedor,
                data_validade,
                numero_lote,
                destino,
                observacoes,
                data_movimentacao,
                id_usuario
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            movimentacao_para_tupla(movimentacao)
        )

        conexao.commit()
        return True, "Entrada registrada com sucesso."

    except Exception as e:
        return False, f"Erro ao registrar entrada: {str(e)}"

    finally:
        conexao.close()


def registrar_saida(
    id_produto,
    quantidade,
    destino,
    observacoes,
    id_usuario
):
    if not isinstance(id_produto, int) or id_produto <= 0:
        return False, "Produto inválido."

    if not quantidade_movimentacao_valida(quantidade):
        return False, "A quantidade de saída deve ser maior que zero."

    if not campo_preenchido(destino):
        return False, "O destino é obrigatório para saída."

    if not destino_valido(destino):
        return False, "Destino inválido."

    if not isinstance(id_usuario, int) or id_usuario <= 0:
        return False, "Usuário inválido."

    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute(
            """
            SELECT id_produto, categoria
            FROM produtos
            WHERE id_produto = ?
            """,
            (id_produto,)
        )
        produto = cursor.fetchone()

        if produto is None:
            return False, "Produto não encontrado."

        cursor.execute(
            """
            SELECT id_usuario
            FROM usuarios
            WHERE id_usuario = ?
            """,
            (id_usuario,)
        )
        usuario = cursor.fetchone()

        if usuario is None:
            return False, "Usuário não encontrado."

        movimentacao = criar_movimentacao(
            tipo_movimentacao="saida",
            id_produto=id_produto,
            categoria=produto["categoria"],
            quantidade=quantidade,
            fornecedor=None,
            data_validade=None,
            numero_lote=None,
            destino=destino.strip(),
            observacoes=observacoes.strip() if observacoes else None,
            data_movimentacao=data_atual_formatada(),
            id_usuario=id_usuario
        )

        cursor.execute(
            """
            INSERT INTO movimentacoes (
                tipo_movimentacao,
                id_produto,
                categoria,
                quantidade,
                fornecedor,
                data_validade,
                numero_lote,
                destino,
                observacoes,
                data_movimentacao,
                id_usuario
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            movimentacao_para_tupla(movimentacao)
        )

        conexao.commit()
        return True, "Saída registrada com sucesso."

    except Exception as e:
        return False, f"Erro ao registrar saída: {str(e)}"

    finally:
        conexao.close()


def listar_historico(pagina=1, itens_por_pagina=10):
    if pagina < 1:
        pagina = 1

    offset = (pagina - 1) * itens_por_pagina
    total = _contar_historico()

    registros = _buscar_historico(
        limite=itens_por_pagina,
        offset=offset
    )

    return registros, total


def buscar_movimentacao_por_id(id_movimentacao):
    registros = _buscar_historico(
        "WHERE m.id_movimentacao = ?",
        (id_movimentacao,)
    )

    if not registros:
        return None

    return registros[0]


def excluir_movimentacao(id_movimentacao):
    if not isinstance(id_movimentacao, int) or id_movimentacao <= 0:
        return False, "Movimentação inválida."

    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute(
            """
            SELECT id_movimentacao
            FROM movimentacoes
            WHERE id_movimentacao = ?
            """,
            (id_movimentacao,)
        )
        movimentacao = cursor.fetchone()

        if movimentacao is None:
            return False, "Movimentação não encontrada."

        cursor.execute(
            """
            DELETE FROM movimentacoes
            WHERE id_movimentacao = ?
            """,
            (id_movimentacao,)
        )

        conexao.commit()
        return True, "Movimentação excluída com sucesso."

    except Exception as e:
        return False, f"Erro ao excluir movimentação: {str(e)}"

    finally:
        conexao.close()


def atualizar_movimentacao_entrada(
    id_movimentacao,
    id_produto,
    categoria,
    quantidade,
    data_validade,
    fornecedor,
    numero_lote,
    observacoes,
    id_usuario
):
    if not isinstance(id_movimentacao, int) or id_movimentacao <= 0:
        return False, "Movimentação inválida."

    if not isinstance(id_produto, int) or id_produto <= 0:
        return False, "Produto inválido."

    if not categoria_valida(categoria):
        return False, "Categoria inválida."

    if not quantidade_movimentacao_valida(quantidade):
        return False, "A quantidade de entrada deve ser maior que zero."

    if not data_valida(data_validade):
        return False, "A data de validade é obrigatória e deve estar no formato YYYY-MM-DD."

    if not campo_preenchido(fornecedor):
        return False, "O fornecedor é obrigatório para entrada."

    if not isinstance(id_usuario, int) or id_usuario <= 0:
        return False, "Usuário inválido."

    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute(
            """
            SELECT id_movimentacao, tipo_movimentacao
            FROM movimentacoes
            WHERE id_movimentacao = ?
            """,
            (id_movimentacao,)
        )
        movimentacao = cursor.fetchone()

        if movimentacao is None:
            return False, "Movimentação não encontrada."

        if movimentacao["tipo_movimentacao"] != "entrada":
            return False, "A movimentação informada não é do tipo entrada."

        cursor.execute(
            """
            SELECT id_produto, categoria
            FROM produtos
            WHERE id_produto = ?
            """,
            (id_produto,)
        )
        produto = cursor.fetchone()

        if produto is None:
            return False, "Produto não encontrado."

        if produto["categoria"] != categoria:
            return False, "A categoria informada não corresponde à categoria do produto."

        cursor.execute(
            """
            SELECT id_usuario
            FROM usuarios
            WHERE id_usuario = ?
            """,
            (id_usuario,)
        )
        usuario = cursor.fetchone()

        if usuario is None:
            return False, "Usuário não encontrado."

        cursor.execute(
            """
            UPDATE movimentacoes
            SET
                id_produto = ?,
                categoria = ?,
                quantidade = ?,
                fornecedor = ?,
                data_validade = ?,
                numero_lote = ?,
                destino = NULL,
                observacoes = ?,
                id_usuario = ?
            WHERE id_movimentacao = ?
            """,
            (
                id_produto,
                categoria,
                quantidade,
                fornecedor.strip(),
                data_validade.strip(),
                numero_lote.strip() if numero_lote else None,
                observacoes.strip() if observacoes else None,
                id_usuario,
                id_movimentacao
            )
        )

        conexao.commit()
        return True, "Movimentação de entrada atualizada com sucesso."

    except Exception as e:
        return False, f"Erro ao atualizar movimentação de entrada: {str(e)}"

    finally:
        conexao.close()


def atualizar_movimentacao_saida(
    id_movimentacao,
    id_produto,
    quantidade,
    destino,
    observacoes,
    id_usuario
):
    if not isinstance(id_movimentacao, int) or id_movimentacao <= 0:
        return False, "Movimentação inválida."

    if not isinstance(id_produto, int) or id_produto <= 0:
        return False, "Produto inválido."

    if not quantidade_movimentacao_valida(quantidade):
        return False, "A quantidade de saída deve ser maior que zero."

    if not campo_preenchido(destino):
        return False, "O destino é obrigatório para saída."

    if not destino_valido(destino):
        return False, "Destino inválido."

    if not isinstance(id_usuario, int) or id_usuario <= 0:
        return False, "Usuário inválido."

    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute(
            """
            SELECT id_movimentacao, tipo_movimentacao
            FROM movimentacoes
            WHERE id_movimentacao = ?
            """,
            (id_movimentacao,)
        )
        movimentacao = cursor.fetchone()

        if movimentacao is None:
            return False, "Movimentação não encontrada."

        if movimentacao["tipo_movimentacao"] != "saida":
            return False, "A movimentação informada não é do tipo saída."

        cursor.execute(
            """
            SELECT id_produto, categoria
            FROM produtos
            WHERE id_produto = ?
            """,
            (id_produto,)
        )
        produto = cursor.fetchone()

        if produto is None:
            return False, "Produto não encontrado."

        cursor.execute(
            """
            SELECT id_usuario
            FROM usuarios
            WHERE id_usuario = ?
            """,
            (id_usuario,)
        )
        usuario = cursor.fetchone()

        if usuario is None:
            return False, "Usuário não encontrado."

        cursor.execute(
            """
            UPDATE movimentacoes
            SET
                id_produto = ?,
                categoria = ?,
                quantidade = ?,
                fornecedor = NULL,
                data_validade = NULL,
                numero_lote = NULL,
                destino = ?,
                observacoes = ?,
                id_usuario = ?
            WHERE id_movimentacao = ?
            """,
            (
                id_produto,
                produto["categoria"],
                quantidade,
                destino.strip(),
                observacoes.strip() if observacoes else None,
                id_usuario,
                id_movimentacao
            )
        )

        conexao.commit()
        return True, "Movimentação de saída atualizada com sucesso."

    except Exception as e:
        return False, f"Erro ao atualizar movimentação de saída: {str(e)}"

    finally:
        conexao.close()


def filtrar_historico_por_produto(id_produto, pagina=1, itens_por_pagina=10):
    if pagina < 1:
        pagina = 1

    where_clause = "WHERE m.id_produto = ?"
    params = (id_produto,)
    offset = (pagina - 1) * itens_por_pagina

    total = _contar_historico(where_clause, params)

    registros = _buscar_historico(
        where_clause,
        params,
        limite=itens_por_pagina,
        offset=offset
    )

    return registros, total


def filtrar_historico_por_categoria(categoria, pagina=1, itens_por_pagina=10):
    if not categoria_valida(categoria):
        return [], 0

    if pagina < 1:
        pagina = 1

    where_clause = "WHERE m.categoria = ?"
    params = (categoria,)
    offset = (pagina - 1) * itens_por_pagina

    total = _contar_historico(where_clause, params)

    registros = _buscar_historico(
        where_clause,
        params,
        limite=itens_por_pagina,
        offset=offset
    )

    return registros, total


def filtrar_historico_por_destino(destino, pagina=1, itens_por_pagina=10):
    if not destino_valido(destino):
        return [], 0

    if pagina < 1:
        pagina = 1

    where_clause = "WHERE m.destino = ?"
    params = (destino,)
    offset = (pagina - 1) * itens_por_pagina

    total = _contar_historico(where_clause, params)

    registros = _buscar_historico(
        where_clause,
        params,
        limite=itens_por_pagina,
        offset=offset
    )

    return registros, total


def filtrar_historico_por_periodo(data_inicial, data_final, pagina=1, itens_por_pagina=10):
    if not data_valida(data_inicial) or not data_valida(data_final):
        return [], 0

    if pagina < 1:
        pagina = 1

    where_clause = "WHERE date(m.data_movimentacao) BETWEEN ? AND ?"
    params = (data_inicial, data_final)
    offset = (pagina - 1) * itens_por_pagina

    total = _contar_historico(where_clause, params)

    registros = _buscar_historico(
        where_clause,
        params,
        limite=itens_por_pagina,
        offset=offset
    )

    return registros, total


def filtrar_historico_por_fornecedor(fornecedor, pagina=1, itens_por_pagina=10):
    if pagina < 1:
        pagina = 1

    where_clause = "WHERE m.fornecedor LIKE ?"
    params = (f"%{fornecedor.strip()}%",)
    offset = (pagina - 1) * itens_por_pagina

    total = _contar_historico(where_clause, params)

    registros = _buscar_historico(
        where_clause,
        params,
        limite=itens_por_pagina,
        offset=offset
    )

    return registros, total


def filtrar_historico_por_lote(numero_lote, pagina=1, itens_por_pagina=10):
    if pagina < 1:
        pagina = 1

    where_clause = "WHERE m.numero_lote LIKE ?"
    params = (f"%{numero_lote.strip()}%",)
    offset = (pagina - 1) * itens_por_pagina

    total = _contar_historico(where_clause, params)

    registros = _buscar_historico(
        where_clause,
        params,
        limite=itens_por_pagina,
        offset=offset
    )

    return registros, total


def filtrar_historico_por_tipo(tipo_movimentacao, pagina=1, itens_por_pagina=10):
    if tipo_movimentacao not in ("entrada", "saida"):
        return [], 0

    if pagina < 1:
        pagina = 1

    where_clause = "WHERE m.tipo_movimentacao = ?"
    params = (tipo_movimentacao,)
    offset = (pagina - 1) * itens_por_pagina

    total = _contar_historico(where_clause, params)

    registros = _buscar_historico(
        where_clause,
        params,
        limite=itens_por_pagina,
        offset=offset
    )

    return registros, total