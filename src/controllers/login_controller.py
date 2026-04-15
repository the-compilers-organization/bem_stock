from database.connection import conectar
from utils.validacoes import campo_preenchido, email_valido
from utils.seguranca import verificar_senha


def autenticar_usuario(email, senha):
    if not campo_preenchido(email):
        return False, "O e-mail é obrigatório."

    if not campo_preenchido(senha):
        return False, "A senha é obrigatória."

    if not email_valido(email):
        return False, "Informe um e-mail válido."

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "SELECT * FROM usuarios WHERE email = ?",
        (email,)
    )
    usuario = cursor.fetchone()

    conexao.close()

    if usuario is None:
        return False, "Usuário não encontrado."

    if not verificar_senha(senha, usuario["senha"]):
        return False, "Senha incorreta."

    return True, dict(usuario)