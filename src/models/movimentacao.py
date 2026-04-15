def criar_movimentacao(
    tipo_movimentacao,
    quantidade,
    data_movimentacao,
    observacao,
    id_produto,
    id_usuario
):
    return {
        "tipo_movimentacao": tipo_movimentacao,
        "quantidade": quantidade,
        "data_movimentacao": data_movimentacao,
        "observacao": observacao,
        "id_produto": id_produto,
        "id_usuario": id_usuario
    }


def movimentacao_para_tupla(movimentacao):
    return (
        movimentacao["tipo_movimentacao"],
        movimentacao["quantidade"],
        movimentacao["data_movimentacao"],
        movimentacao["observacao"],
        movimentacao["id_produto"],
        movimentacao["id_usuario"]
    )
