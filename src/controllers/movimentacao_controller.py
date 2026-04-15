from database.connection import conectar
from models.movimentacao import criar_movimentacao, movimentacao_para_tupla
from utils.validacoes import quantidade_movimentacao_valida
from utils.formatadores import data_atual_formatada


def registrar_entrada(id_produto, quantidade, observacao, id_usuario):
    if not quantidade_movimentacao_valida(quantidade):
        return False, "A quantidade de entrada deve ser maior que zero."

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "SELECT quantidade_atual FROM produtos WHERE id_produto = ?",
        (id_produto,)
    )
    produto = cursor.fetchone()

    if produto is None:
        conexao.close()
        return False, "Produto não encontrado."

    nova_quantidade = produto["quantidade_atual"] + quantidade

    cursor.execute(
        """
        UPDATE produtos
        SET quantidade_atual = ?
        WHERE id_produto = ?
        """,
        (nova_quantidade, id_produto)
    )

    movimentacao = criar_movimentacao(
        tipo_movimentacao="entrada",
        quantidade=quantidade,
        data_movimentacao=data_atual_formatada(),
        observacao=observacao,
        id_produto=id_produto,
        id_usuario=id_usuario
    )

    cursor.execute(
        """
        INSERT INTO movimentacoes (
            tipo_movimentacao,
            quantidade,
            data_movimentacao,
            observacao,
            id_produto,
            id_usuario
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        movimentacao_para_tupla(movimentacao)
    )

    conexao.commit()
    conexao.close()

    return True, "Entrada registrada com sucesso."


def registrar_saida(id_produto, quantidade, observacao, id_usuario):
    if not quantidade_movimentacao_valida(quantidade):
        return False, "A quantidade de saída deve ser maior que zero."

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "SELECT quantidade_atual FROM produtos WHERE id_produto = ?",
        (id_produto,)
    )
    produto = cursor.fetchone()

    if produto is None:
        conexao.close()
        return False, "Produto não encontrado."

    if quantidade > produto["quantidade_atual"]:
        conexao.close()
        return False, "Estoque insuficiente para realizar a saída."

    nova_quantidade = produto["quantidade_atual"] - quantidade

    cursor.execute(
        """
        UPDATE produtos
        SET quantidade_atual = ?
        WHERE id_produto = ?
        """,
        (nova_quantidade, id_produto)
    )

    movimentacao = criar_movimentacao(
        tipo_movimentacao="saida",
        quantidade=quantidade,
        data_movimentacao=data_atual_formatada(),
        observacao=observacao,
        id_produto=id_produto,
        id_usuario=id_usuario
    )

    cursor.execute(
        """
        INSERT INTO movimentacoes (
            tipo_movimentacao,
            quantidade,
            data_movimentacao,
            observacao,
            id_produto,
            id_usuario
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        movimentacao_para_tupla(movimentacao)
    )

    conexao.commit()
    conexao.close()

    return True, "Saída registrada com sucesso."


def listar_historico():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT
            m.id_movimentacao,
            m.tipo_movimentacao,
            m.quantidade,
            m.data_movimentacao,
            m.observacao,
            p.nome AS nome_produto,
            p.categoria AS categoria_produto,
            p.lote AS lote_produto,
            u.nome AS nome_usuario,
            u.email AS email_usuario
        FROM movimentacoes m
        JOIN produtos p ON m.id_produto = p.id_produto
        JOIN usuarios u ON m.id_usuario = u.id_usuario
        ORDER BY m.data_movimentacao DESC
        """
    )
    historico = cursor.fetchall()

    conexao.close()
    return [dict(item) for item in historico]


def filtrar_historico_por_tipo(tipo_movimentacao):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT
            m.id_movimentacao,
            m.tipo_movimentacao,
            m.quantidade,
            m.data_movimentacao,
            m.observacao,
            p.nome AS nome_produto,
            p.categoria AS categoria_produto,
            p.lote AS lote_produto,
            u.nome AS nome_usuario,
            u.email AS email_usuario
        FROM movimentacoes m
        JOIN produtos p ON m.id_produto = p.id_produto
        JOIN usuarios u ON m.id_usuario = u.id_usuario
        WHERE m.tipo_movimentacao = ?
        ORDER BY m.data_movimentacao DESC
        """,
        (tipo_movimentacao,)
    )
    historico = cursor.fetchall()

    conexao.close()
    return [dict(item) for item in historico]


def filtrar_historico_por_produto(id_produto):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT
            m.id_movimentacao,
            m.tipo_movimentacao,
            m.quantidade,
            m.data_movimentacao,
            m.observacao,
            p.nome AS nome_produto,
            p.categoria AS categoria_produto,
            p.lote AS lote_produto,
            u.nome AS nome_usuario,
            u.email AS email_usuario
        FROM movimentacoes m
        JOIN produtos p ON m.id_produto = p.id_produto
        JOIN usuarios u ON m.id_usuario = u.id_usuario
        WHERE m.id_produto = ?
        ORDER BY m.data_movimentacao DESC
        """,
        (id_produto,)
    )
    historico = cursor.fetchall()

    conexao.close()
    return [dict(item) for item in historico]


def filtrar_historico_por_periodo(data_inicial, data_final):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT
            m.id_movimentacao,
            m.tipo_movimentacao,
            m.quantidade,
            m.data_movimentacao,
            m.observacao,
            p.nome AS nome_produto,
            p.categoria AS categoria_produto,
            p.lote AS lote_produto,
            u.nome AS nome_usuario,
            u.email AS email_usuario
        FROM movimentacoes m
        JOIN produtos p ON m.id_produto = p.id_produto
        JOIN usuarios u ON m.id_usuario = u.id_usuario
        WHERE date(m.data_movimentacao) BETWEEN ? AND ?
        ORDER BY m.data_movimentacao DESC
        """,
        (data_inicial, data_final)
    )
    historico = cursor.fetchall()

    conexao.close()
    return [dict(item) for item in historico]