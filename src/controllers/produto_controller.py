from datetime import datetime

from database.connection import conectar
from models.produto import criar_produto, produto_para_tupla
from utils.validacoes import (
    campo_preenchido,
    categoria_valida,
    quantidade_valida,
    unidade_medida_valida
)
from utils.formatadores import formatar_data_para_exibicao


def _obter_data_hoje():
    return datetime.now().date()


def _calcular_estoque_atual(cursor, id_produto):
    cursor.execute(
        """
        SELECT
            COALESCE(SUM(
                CASE
                    WHEN tipo_movimentacao = 'entrada' THEN quantidade
                    WHEN tipo_movimentacao = 'saida' THEN -quantidade
                    ELSE 0
                END
            ), 0) AS estoque_atual
        FROM movimentacoes
        WHERE id_produto = ?
        """,
        (id_produto,)
    )
    resultado = cursor.fetchone()
    return resultado["estoque_atual"] if resultado and resultado["estoque_atual"] is not None else 0


def _obter_validade_mais_proxima(cursor, id_produto):
    cursor.execute(
        """
        SELECT data_validade
        FROM movimentacoes
        WHERE id_produto = ?
          AND tipo_movimentacao = 'entrada'
          AND data_validade IS NOT NULL
          AND TRIM(data_validade) <> ''
        ORDER BY date(data_validade) ASC
        LIMIT 1
        """,
        (id_produto,)
    )
    resultado = cursor.fetchone()
    return resultado["data_validade"] if resultado else None


def _calcular_status_estoque(estoque_atual, estoque_minimo):
    if estoque_atual <= 0:
        return "Esgotado"

    if estoque_minimo <= 0:
        return "Normal"

    if estoque_atual < estoque_minimo:
        return "Baixo"

    if estoque_atual <= estoque_minimo + 5:
        return "Próximo ao Mínimo"

    return "Normal"


def _calcular_status_validade(data_validade):
    if not data_validade:
        return {
            "validade_exibicao": "-",
            "status_validade": "normal",
            "dias_para_vencer": None
        }

    try:
        data_validade_date = datetime.strptime(data_validade, "%Y-%m-%d").date()
    except ValueError:
        return {
            "validade_exibicao": data_validade,
            "status_validade": "normal",
            "dias_para_vencer": None
        }

    hoje = _obter_data_hoje()
    dias_para_vencer = (data_validade_date - hoje).days

    if dias_para_vencer < 0:
        return {
            "validade_exibicao": "Vencido",
            "status_validade": "vencido",
            "dias_para_vencer": dias_para_vencer
        }

    if dias_para_vencer <= 30:
        return {
            "validade_exibicao": formatar_data_para_exibicao(data_validade),
            "status_validade": "proximo",
            "dias_para_vencer": dias_para_vencer
        }

    return {
        "validade_exibicao": formatar_data_para_exibicao(data_validade),
        "status_validade": "normal",
        "dias_para_vencer": dias_para_vencer
    }


def _enriquecer_produto(cursor, produto):
    produto_dict = dict(produto)

    estoque_atual = _calcular_estoque_atual(cursor, produto_dict["id_produto"])
    data_validade = _obter_validade_mais_proxima(cursor, produto_dict["id_produto"])

    produto_dict["estoque_atual"] = estoque_atual
    produto_dict["status_estoque"] = _calcular_status_estoque(
        estoque_atual,
        produto_dict["estoque_minimo"]
    )

    info_validade = _calcular_status_validade(data_validade)
    produto_dict["validade_exibicao"] = info_validade["validade_exibicao"]
    produto_dict["status_validade"] = info_validade["status_validade"]
    produto_dict["dias_para_vencer"] = info_validade["dias_para_vencer"]

    return produto_dict


def _listar_produtos_base(where_clause="", params=()):
    conexao = conectar()
    cursor = conexao.cursor()

    query = f"""
        SELECT *
        FROM produtos
        {where_clause}
        ORDER BY nome
    """

    cursor.execute(query, params)
    produtos = cursor.fetchall()

    resultado = [_enriquecer_produto(cursor, produto) for produto in produtos]

    conexao.close()
    return resultado


def cadastrar_produto(
    nome,
    categoria,
    unidade_medida,
    estoque_minimo,
    descricao
):
    if not campo_preenchido(nome):
        return False, "O nome do produto é obrigatório."

    if not categoria_valida(categoria):
        return False, "Categoria inválida."

    if not campo_preenchido(unidade_medida):
        return False, "A unidade de medida é obrigatória."

    if not unidade_medida_valida(unidade_medida):
        return False, "Unidade de medida inválida."

    if not quantidade_valida(estoque_minimo):
        return False, "O estoque mínimo deve ser um número inteiro maior ou igual a zero."

    produto = criar_produto(
        nome=nome.strip(),
        categoria=categoria,
        unidade_medida=unidade_medida,
        estoque_minimo=estoque_minimo,
        descricao=descricao.strip() if descricao else ""
    )

    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO produtos (
                nome,
                categoria,
                unidade_medida,
                estoque_minimo,
                descricao
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            produto_para_tupla(produto)
        )

        conexao.commit()
        return True, "Produto cadastrado com sucesso."

    except Exception as e:
        return False, f"Erro ao cadastrar produto: {str(e)}"

    finally:
        conexao.close()


def listar_produtos():
    return _listar_produtos_base()


def buscar_produto_por_id(id_produto):
    produtos = _listar_produtos_base(
        "WHERE id_produto = ?",
        (id_produto,)
    )
    if not produtos:
        return None
    return produtos[0]


def buscar_produtos_por_nome(nome):
    return _listar_produtos_base(
        "WHERE nome LIKE ?",
        (f"%{nome.strip()}%",)
    )


def atualizar_produto(
    id_produto,
    nome,
    categoria,
    unidade_medida,
    estoque_minimo,
    descricao
):
    if not campo_preenchido(nome):
        return False, "O nome do produto é obrigatório."

    if not categoria_valida(categoria):
        return False, "Categoria inválida."

    if not campo_preenchido(unidade_medida):
        return False, "A unidade de medida é obrigatória."

    if not unidade_medida_valida(unidade_medida):
        return False, "Unidade de medida inválida."

    if not quantidade_valida(estoque_minimo):
        return False, "O estoque mínimo deve ser um número inteiro maior ou igual a zero."

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

    try:
        cursor.execute(
            """
            UPDATE produtos
            SET
                nome = ?,
                categoria = ?,
                unidade_medida = ?,
                estoque_minimo = ?,
                descricao = ?
            WHERE id_produto = ?
            """,
            (
                nome.strip(),
                categoria,
                unidade_medida,
                estoque_minimo,
                descricao.strip() if descricao else "",
                id_produto
            )
        )

        conexao.commit()
        return True, "Produto atualizado com sucesso."

    except Exception as e:
        return False, f"Erro ao atualizar produto: {str(e)}"

    finally:
        conexao.close()


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

    try:
        cursor.execute(
            "DELETE FROM produtos WHERE id_produto = ?",
            (id_produto,)
        )

        conexao.commit()
        return True, "Produto excluído com sucesso."

    except Exception as e:
        return False, f"Erro ao excluir produto: {str(e)}"

    finally:
        conexao.close()


def filtrar_produtos_por_categoria(categoria):
    if not categoria_valida(categoria):
        return []

    return _listar_produtos_base(
        "WHERE categoria = ?",
        (categoria,)
    )