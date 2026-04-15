from datetime import datetime, timedelta

from database.connection import conectar
from models.produto import criar_produto, produto_para_tupla
from utils.validacoes import (
    campo_preenchido,
    categoria_valida,
    quantidade_valida,
    data_valida
)


def cadastrar_produto(
    nome,
    descricao,
    categoria,
    lote,
    quantidade_atual,
    unidade_medida,
    estoque_minimo,
    data_validade
):
    if not campo_preenchido(nome):
        return False, "O nome do produto é obrigatório."

    if not categoria_valida(categoria):
        return False, "Categoria inválida."

    if not campo_preenchido(unidade_medida):
        return False, "A unidade de medida é obrigatória."

    if not quantidade_valida(quantidade_atual):
        return False, "A quantidade atual deve ser um número inteiro maior ou igual a zero."

    if not quantidade_valida(estoque_minimo):
        return False, "O estoque mínimo deve ser um número inteiro maior ou igual a zero."

    if not data_valida(data_validade):
        return False, "A data de validade deve estar no formato YYYY-MM-DD."

    if lote is None:
        lote = ""

    produto = criar_produto(
        nome=nome,
        descricao=descricao,
        categoria=categoria,
        lote=lote,
        quantidade_atual=quantidade_atual,
        unidade_medida=unidade_medida,
        estoque_minimo=estoque_minimo,
        data_validade=data_validade
    )

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        """
        INSERT INTO produtos (
            nome,
            descricao,
            categoria,
            lote,
            quantidade_atual,
            unidade_medida,
            estoque_minimo,
            data_validade
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        produto_para_tupla(produto)
    )

    conexao.commit()
    conexao.close()

    return True, "Produto cadastrado com sucesso."


def listar_produtos():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT *
        FROM produtos
        ORDER BY nome
        """
    )
    produtos = cursor.fetchall()

    conexao.close()
    return [dict(produto) for produto in produtos]


def buscar_produtos_por_nome(nome):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT *
        FROM produtos
        WHERE nome LIKE ?
        ORDER BY nome
        """,
        (f"%{nome}%",)
    )
    produtos = cursor.fetchall()

    conexao.close()
    return [dict(produto) for produto in produtos]


def buscar_produtos_por_lote(lote):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT *
        FROM produtos
        WHERE lote LIKE ?
        ORDER BY nome
        """,
        (f"%{lote}%",)
    )
    produtos = cursor.fetchall()

    conexao.close()
    return [dict(produto) for produto in produtos]


def buscar_produto_por_id(id_produto):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT *
        FROM produtos
        WHERE id_produto = ?
        """,
        (id_produto,)
    )
    produto = cursor.fetchone()

    conexao.close()

    if produto is None:
        return None

    return dict(produto)


def atualizar_produto(
    id_produto,
    nome,
    descricao,
    categoria,
    lote,
    quantidade_atual,
    unidade_medida,
    estoque_minimo,
    data_validade
):
    if not campo_preenchido(nome):
        return False, "O nome do produto é obrigatório."

    if not categoria_valida(categoria):
        return False, "Categoria inválida."

    if not campo_preenchido(unidade_medida):
        return False, "A unidade de medida é obrigatória."

    if not quantidade_valida(quantidade_atual):
        return False, "A quantidade atual deve ser um número inteiro maior ou igual a zero."

    if not quantidade_valida(estoque_minimo):
        return False, "O estoque mínimo deve ser um número inteiro maior ou igual a zero."

    if not data_valida(data_validade):
        return False, "A data de validade deve estar no formato YYYY-MM-DD."

    if lote is None:
        lote = ""

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "SELECT id_produto FROM produtos WHERE id_produto = ?",
        (id_produto,)
    )
    produto = cursor.fetchone()

    if produto is None:
        conexao.close()
        return False, "Produto não encontrado."

    cursor.execute(
        """
        UPDATE produtos
        SET nome = ?, descricao = ?, categoria = ?, lote = ?,
            quantidade_atual = ?, unidade_medida = ?, estoque_minimo = ?, data_validade = ?
        WHERE id_produto = ?
        """,
        (
            nome,
            descricao,
            categoria,
            lote,
            quantidade_atual,
            unidade_medida,
            estoque_minimo,
            data_validade,
            id_produto
        )
    )

    conexao.commit()
    conexao.close()

    return True, "Produto atualizado com sucesso."


def excluir_produto(id_produto):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "SELECT id_produto FROM produtos WHERE id_produto = ?",
        (id_produto,)
    )
    produto = cursor.fetchone()

    if produto is None:
        conexao.close()
        return False, "Produto não encontrado."

    cursor.execute(
        "SELECT id_movimentacao FROM movimentacoes WHERE id_produto = ? LIMIT 1",
        (id_produto,)
    )
    movimentacao = cursor.fetchone()

    if movimentacao is not None:
        conexao.close()
        return False, "Não é possível excluir um produto que possui movimentações registradas."

    cursor.execute(
        "DELETE FROM produtos WHERE id_produto = ?",
        (id_produto,)
    )

    conexao.commit()
    conexao.close()

    return True, "Produto excluído com sucesso."


def filtrar_produtos_por_categoria(categoria):
    if not categoria_valida(categoria):
        return []

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT *
        FROM produtos
        WHERE categoria = ?
        ORDER BY nome
        """,
        (categoria,)
    )
    produtos = cursor.fetchall()

    conexao.close()
    return [dict(produto) for produto in produtos]


def listar_produtos_estoque_baixo():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT *
        FROM produtos
        WHERE quantidade_atual < estoque_minimo
        ORDER BY nome
        """
    )
    produtos = cursor.fetchall()

    conexao.close()
    return [dict(produto) for produto in produtos]


def listar_produtos_vencidos():
    hoje = datetime.now().strftime("%Y-%m-%d")

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT *
        FROM produtos
        WHERE data_validade < ?
        ORDER BY data_validade
        """,
        (hoje,)
    )
    produtos = cursor.fetchall()

    conexao.close()
    return [dict(produto) for produto in produtos]


def listar_produtos_proximos_validade(dias=30):
    hoje = datetime.now().date()
    limite = hoje + timedelta(days=dias)

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT *
        FROM produtos
        WHERE data_validade >= ? AND data_validade <= ?
        ORDER BY data_validade
        """,
        (
            hoje.strftime("%Y-%m-%d"),
            limite.strftime("%Y-%m-%d")
        )
    )
    produtos = cursor.fetchall()

    conexao.close()
    return [dict(produto) for produto in produtos]