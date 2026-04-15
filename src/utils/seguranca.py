import hashlib


def gerar_hash_senha(senha):
    return hashlib.sha256(senha.encode("utf-8")).hexdigest()


def verificar_senha(senha_digitada, senha_hash):
    return gerar_hash_senha(senha_digitada) == senha_hash