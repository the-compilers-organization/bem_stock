from database.connection import conectar
from utils.seguranca import gerar_hash_senha


def criar_tabelas():
    conexao = conectar()
    cursor = conexao.cursor()

    # =========================
    # USUÁRIOS
    # =========================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL,
            perfil TEXT NOT NULL CHECK (perfil IN ('admin', 'estoque')),
            primeiro_acesso INTEGER NOT NULL DEFAULT 1
        )
    """)

    # GARANTIR COLUNA EM BANCOS ANTIGOS
    cursor.execute("PRAGMA table_info(usuarios)")
    colunas = [coluna[1] for coluna in cursor.fetchall()]

    if "primeiro_acesso" not in colunas:
        cursor.execute("""
            ALTER TABLE usuarios
            ADD COLUMN primeiro_acesso INTEGER NOT NULL DEFAULT 1
        """)

    # =========================
    # PRODUTOS
    # =========================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            categoria TEXT NOT NULL CHECK (
                categoria IN (
                    'Alimentos',
                    'Limpeza',
                    'Higiene Pessoal'
                )
            ),
            unidade_medida TEXT NOT NULL CHECK (
                unidade_medida IN (
                    'unidade',
                    'pacote',
                    'caixa',
                    'litros',
                    'ml',
                    'kg',
                    'grama'
                )
            ),
            estoque_minimo INTEGER NOT NULL,
            descricao TEXT
        )
    """)

    # =========================
    # MOVIMENTAÇÕES
    # =========================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movimentacoes (
            id_movimentacao INTEGER PRIMARY KEY AUTOINCREMENT,

            tipo_movimentacao TEXT NOT NULL CHECK (
                tipo_movimentacao IN ('entrada', 'saida')
            ),

            id_produto INTEGER NOT NULL,

            categoria TEXT NOT NULL CHECK (
                categoria IN (
                    'Alimentos',
                    'Limpeza',
                    'Higiene Pessoal'
                )
            ),

            quantidade INTEGER NOT NULL,

            fornecedor TEXT,
            data_validade TEXT,
            numero_lote TEXT,

            destino TEXT CHECK (
                destino IN (
                    'cozinha',
                    'banheiros',
                    'area de servico',
                    'lavanderia',
                    'refeitorio',
                    'outros'
                )
            ),

            observacoes TEXT,

            data_movimentacao TEXT NOT NULL,

            id_usuario INTEGER,

            CHECK (
                tipo_movimentacao = 'saida'
                OR (
                    fornecedor IS NOT NULL
                    AND TRIM(fornecedor) <> ''
                    AND data_validade IS NOT NULL
                    AND TRIM(data_validade) <> ''
                )
            ),

            CHECK (
                tipo_movimentacao = 'entrada'
                OR (
                    destino IS NOT NULL
                    AND TRIM(destino) <> ''
                )
            ),

            FOREIGN KEY (id_produto) REFERENCES produtos(id_produto),
            FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE SET NULL
        )
    """)

    conexao.commit()
    conexao.close()


# =========================
# ADMIN TEMPORÁRIO (PRIMEIRO ACESSO)
# =========================
def criar_admin_inicial():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id_usuario
        FROM usuarios
        WHERE perfil = 'admin'
        LIMIT 1
    """)
    admin = cursor.fetchone()

    if admin is None:
        senha_hash = gerar_hash_senha("123456")

        cursor.execute(
            """
            INSERT INTO usuarios (nome, email, senha, perfil, primeiro_acesso)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                "Administrador",
                "teste@bemstock.com",
                senha_hash,
                "admin",
                1
            )
        )

        conexao.commit()

    conexao.close()


# =========================
# INICIALIZAÇÃO
# =========================
def inicializar_banco():
    criar_tabelas()
    criar_admin_inicial()