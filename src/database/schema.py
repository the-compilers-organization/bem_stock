from database.connection import conectar
from utils.seguranca import gerar_hash_senha


def criar_tabelas():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL,
            perfil TEXT NOT NULL CHECK (perfil IN ('admin', 'estoque'))
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            descricao TEXT,
            categoria TEXT NOT NULL CHECK (
                categoria IN (
                    'Alimentos',
                    'Limpeza',
                    'Higiene Pessoal'
                )
            ),
            lote TEXT,
            quantidade_atual INTEGER NOT NULL DEFAULT 0,
            unidade_medida TEXT NOT NULL,
            estoque_minimo INTEGER NOT NULL,
            data_validade TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movimentacoes (
            id_movimentacao INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo_movimentacao TEXT NOT NULL CHECK (
                tipo_movimentacao IN ('entrada', 'saida')
            ),
            quantidade INTEGER NOT NULL,
            data_movimentacao TEXT NOT NULL,
            observacao TEXT,
            id_produto INTEGER NOT NULL,
            id_usuario INTEGER NOT NULL,
            FOREIGN KEY (id_produto) REFERENCES produtos(id_produto),
            FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
        )
    """)

    conexao.commit()
    conexao.close()


def criar_admin_inicial():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "SELECT id_usuario FROM usuarios WHERE email = ?",
        ("admin@bemstock.com",)
    )
    admin = cursor.fetchone()

    if admin is None:
        senha_hash = gerar_hash_senha("123456")

        cursor.execute(
            """
            INSERT INTO usuarios (nome, email, senha, perfil)
            VALUES (?, ?, ?, ?)
            """,
            ("Administrador", "admin@bemstock.com", senha_hash, "admin")
        )

        conexao.commit()

    conexao.close()


def inicializar_banco():
    criar_tabelas()
    criar_admin_inicial()