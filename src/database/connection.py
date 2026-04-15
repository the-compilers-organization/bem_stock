import sqlite3
from pathlib import Path


def obter_caminho_banco():
    return Path(__file__).resolve().parent.parent.parent / "bemstock.db"


def conectar():
    caminho_banco = obter_caminho_banco()
    conexao = sqlite3.connect(caminho_banco)
    conexao.row_factory = sqlite3.Row
    return conexao
