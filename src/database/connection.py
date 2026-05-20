import sqlite3

from pathlib import Path

from utils.caminho_recurso import caminho_recurso


# ==================================================
# CAMINHO DO BANCO
# ==================================================
def obter_caminho_banco():
    return Path(
        caminho_recurso(
            "src/database/bemstock.db"
        )
    )


# ==================================================
# CONEXÃO
# ==================================================
def conectar():
    caminho_banco = obter_caminho_banco()

    conexao = sqlite3.connect(
        caminho_banco
    )

    conexao.row_factory = sqlite3.Row

    return conexao