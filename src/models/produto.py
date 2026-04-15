def criar_produto(
    nome,
    descricao,
    categoria,
    lote,
    quantidade_atual,
    unidade_medida,
    estoque_minimo,
    data_validade
):
    return {
        "nome": nome,
        "descricao": descricao,
        "categoria": categoria,
        "lote": lote,
        "quantidade_atual": quantidade_atual,
        "unidade_medida": unidade_medida,
        "estoque_minimo": estoque_minimo,
        "data_validade": data_validade
    }


def produto_para_tupla(produto):
    return (
        produto["nome"],
        produto["descricao"],
        produto["categoria"],
        produto["lote"],
        produto["quantidade_atual"],
        produto["unidade_medida"],
        produto["estoque_minimo"],
        produto["data_validade"]
    )
