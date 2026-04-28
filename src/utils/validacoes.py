from datetime import datetime

from utils.constantes import (
    CATEGORIAS_PREDEFINIDAS,
    PERFIS_USUARIO,
    UNIDADES_MEDIDA,
    DESTINOS_MOVIMENTACAO
)


def campo_preenchido(valor):
    return valor is not None and str(valor).strip() != ""


def senha_valida(senha):
    if not campo_preenchido(senha):
        return False

    senha = str(senha).strip()

    return 6 <= len(senha) <= 10


def email_valido(email):
    if not campo_preenchido(email):
        return False

    email = email.strip()

    if "@" not in email or "." not in email:
        return False

    if email.startswith("@") or email.endswith("@"):
        return False

    return True


def perfil_valido(perfil):
    return perfil in PERFIS_USUARIO


def categoria_valida(categoria):
    return categoria in CATEGORIAS_PREDEFINIDAS


def unidade_medida_valida(unidade_medida):
    return unidade_medida in UNIDADES_MEDIDA


def destino_valido(destino):
    return destino in DESTINOS_MOVIMENTACAO


def quantidade_valida(quantidade):
    return isinstance(quantidade, int) and quantidade >= 0


def quantidade_movimentacao_valida(quantidade):
    return isinstance(quantidade, int) and quantidade > 0


def data_valida(data_texto):
    if not campo_preenchido(data_texto):
        return False

    try:
        datetime.strptime(data_texto, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def periodo_valido(data_inicial, data_final):
    if not data_valida(data_inicial) or not data_valida(data_final):
        return False

    data_inicio = datetime.strptime(data_inicial, "%Y-%m-%d")
    data_fim = datetime.strptime(data_final, "%Y-%m-%d")

    return data_inicio <= data_fim