from datetime import datetime


def data_atual_formatada():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def formatar_data_para_exibicao(data_texto):
    if not data_texto:
        return "-"

    try:
        return datetime.strptime(data_texto, "%Y-%m-%d").strftime("%d/%m/%Y")
    except ValueError:
        return data_texto


def formatar_data_hora_para_exibicao(data_hora_texto):
    if not data_hora_texto:
        return "-"

    try:
        return datetime.strptime(
            data_hora_texto,
            "%Y-%m-%d %H:%M:%S"
        ).strftime("%d/%m/%Y %H:%M:%S")
    except ValueError:
        return data_hora_texto


def texto_ou_traco(valor):
    if valor is None or str(valor).strip() == "":
        return "-"
    return str(valor)