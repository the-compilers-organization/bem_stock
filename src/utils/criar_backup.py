import os
import shutil

from datetime import datetime


# ==================================================
# LIMPAR BACKUPS ANTIGOS
# ==================================================
def limpar_backups_antigos(limite=10):
    pasta_backup = "backups"

    if not os.path.exists(pasta_backup):
        return

    arquivos = sorted(
        [
            os.path.join(pasta_backup, arquivo)
            for arquivo in os.listdir(pasta_backup)
            if arquivo.endswith(".db")
        ],
        key=os.path.getmtime
    )

    while len(arquivos) > limite:
        try:
            os.remove(arquivos[0])
            arquivos.pop(0)

        except Exception as erro:
            print(
                f"Erro ao remover backup antigo: {erro}"
            )
            break


# ==================================================
# CRIAR BACKUP
# ==================================================
def criar_backup():
    try:
        # =========================
        # CAMINHO DO BANCO
        # =========================
        banco = "src/database/bemstock.db"

        # =========================
        # VERIFICAR BANCO
        # =========================
        if not os.path.exists(banco):
            print(
                "Banco de dados não encontrado."
            )
            return False

        # =========================
        # PASTA DE BACKUP
        # =========================
        pasta_backup = "backups"

        if not os.path.exists(pasta_backup):
            os.makedirs(pasta_backup)

        # =========================
        # DATA/HORA
        # =========================
        data_hora = datetime.now().strftime(
            "%Y-%m-%d_%H-%M-%S"
        )

        # =========================
        # NOME DO ARQUIVO
        # =========================
        nome_backup = (
            f"backup_{data_hora}.db"
        )

        destino = os.path.join(
            pasta_backup,
            nome_backup
        )

        # =========================
        # COPIAR BANCO
        # =========================
        shutil.copy2(
            banco,
            destino
        )

        # =========================
        # LIMPAR BACKUPS ANTIGOS
        # =========================
        limpar_backups_antigos()

        print(
            f"Backup criado com sucesso: {destino}"
        )

        return True

    except Exception as erro:
        print(
            f"Erro ao criar backup: {erro}"
        )

        return False