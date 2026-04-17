def criar_produto(
    nome,
    categoria,
    unidade_medida,
    estoque_minimo,
    descricao
):
    return {
        "nome": nome,
        "categoria": categoria,
        "unidade_medida": unidade_medida,
        "estoque_minimo": estoque_minimo,
        "descricao": descricao
    }


def produto_para_tupla(produto):
    return (
        produto["nome"],
        produto["categoria"],
        produto["unidade_medida"],
        produto["estoque_minimo"],
        produto["descricao"]
    )