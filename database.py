import sqlite3
from datetime import datetime


def conectar_banco(db_path="sistema.db"):
    """Cria a conexão com o banco de dados SQLite."""
    return sqlite3.connect(db_path)


def inicializar_banco(db_path="sistema.db"):
    """Cria a tabela com a estrutura atualizada."""

    conexao = conectar_banco(db_path)
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transacoes (
            id_transacao TEXT PRIMARY KEY,
            primeiro_nome TEXT,
            sobrenome TEXT,
            cpf TEXT NOT NULL,
            idade INTEGER,
            valor_bruto REAL,
            valor_final REAL,
            status TEXT,
            motivo_rejeicao TEXT,
            data_processamento TIMESTAMP
        )
    """)

    conexao.commit()
    conexao.close()


def salvar_transacao(dados: dict, db_path="sistema.db"):
    """Salva ou atualiza uma transação usando os novos campos."""

    conexao = conectar_banco(db_path)
    cursor = conexao.cursor()

    cliente = dados.get("cliente", "").strip()
    partes = cliente.split(maxsplit=1)

    primeiro_nome = dados.get(
        "primeiro_nome",
        partes[0] if partes else ""
    )

    sobrenome = dados.get(
        "sobrenome",
        partes[1] if len(partes) > 1 else ""
    )

    data_processamento = dados.get(
        "data_processamento",
        datetime.now().isoformat()
    )

    cursor.execute("""
        INSERT OR REPLACE INTO transacoes (
            id_transacao,
            primeiro_nome,
            sobrenome,
            cpf,
            idade,
            valor_bruto,
            valor_final,
            status,
            motivo_rejeicao,
            data_processamento
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        dados["id_transacao"],
        primeiro_nome,
        sobrenome,
        dados["cpf"],
        dados["idade"],
        dados["valor_bruto"],
        dados.get("valor_final"),
        dados["status"],
        dados.get("motivo_rejeicao"),
        data_processamento
    ))

    conexao.commit()
    conexao.close()


def buscar_transacao_por_id(id_transacao: str, db_path="sistema.db"):
    """Busca uma transação pelo identificador."""

    conexao = conectar_banco(db_path)
    conexao.row_factory = sqlite3.Row
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT * FROM transacoes
        WHERE id_transacao = ?
    """, (id_transacao,))

    resultado = cursor.fetchone()
    conexao.close()

    if resultado:
        return dict(resultado)

    return None