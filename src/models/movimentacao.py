def criar_movimentacao(
    tipo_movimentacao,
    id_produto,
    categoria,
    quantidade,
    fornecedor=None,
    data_validade=None,
    numero_lote=None,
    destino=None,
    observacoes=None,
    data_movimentacao=None,
    id_usuario=None
):
    return {
        "tipo_movimentacao": tipo_movimentacao,  
        "id_produto": id_produto,
        "categoria": categoria,
        "quantidade": quantidade,
        "fornecedor": fornecedor.strip() if fornecedor else None,
        "data_validade": data_validade.strip() if data_validade else None,
        "numero_lote": numero_lote.strip() if numero_lote else None,
        "destino": destino.strip() if destino else None,
        "observacoes": observacoes.strip() if observacoes else None,
        "data_movimentacao": data_movimentacao,
        "id_usuario": id_usuario
    }


def movimentacao_para_tupla(movimentacao):
    return (
        movimentacao["tipo_movimentacao"],  
        movimentacao["id_produto"],
        movimentacao["categoria"],
        movimentacao["quantidade"],
        movimentacao["fornecedor"],
        movimentacao["data_validade"],
        movimentacao["numero_lote"],
        movimentacao["destino"],
        movimentacao["observacoes"],
        movimentacao["data_movimentacao"],
        movimentacao["id_usuario"]
    )