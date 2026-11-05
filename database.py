
import sqlite3
from datetime import datetime


def conectar_banco(db_path="sistema.db"):
    """Cria a conexão com o banco de dados SQLite."""
    return sqlite3.connect(db_path)


def inicializar_banco(db_path="sistema.db"):
    """Cria a tabela na estrutura final do projeto."""

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
    """Salva uma transação, respeitando a versão atual do banco."""

    conexao = conectar_banco(db_path)
    cursor = conexao.cursor()

    try:
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

        # Identifica as colunas existentes na tabela.
        cursor.execute("PRAGMA table_info(transacoes)")
        colunas = [coluna[1] for coluna in cursor.fetchall()]

        campos = [
            "id_transacao",
            "primeiro_nome",
            "sobrenome",
            "cpf",
            "idade",
            "valor_bruto",
            "valor_final",
            "status",
            "motivo_rejeicao",
            "data_processamento"
        ]

        valores = [
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
        ]

        # Dual Write: mantém o campo antigo durante o Expand.
        if "cliente" in colunas:
            campos.insert(1, "cliente")
            valores.insert(1, cliente)

        campos_existentes = [
            campo for campo in campos if campo in colunas
        ]

        valores_existentes = [
            valores[campos.index(campo)]
            for campo in campos_existentes
        ]

        nomes_campos = ", ".join(campos_existentes)
        marcadores = ", ".join(["?"] * len(campos_existentes))

        cursor.execute(
            f"""
            INSERT OR REPLACE INTO transacoes ({nomes_campos})
            VALUES ({marcadores})
            """,
            valores_existentes
        )

        conexao.commit()

    finally:
        conexao.close()


def buscar_transacao_por_id(id_transacao: str, db_path="sistema.db"):
    """Busca uma transação pelo identificador."""

    conexao = conectar_banco(db_path)
    conexao.row_factory = sqlite3.Row

    try:
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT * FROM transacoes
            WHERE id_transacao = ?
        """, (id_transacao,))

        resultado = cursor.fetchone()

        if resultado:
            return dict(resultado)

        return None

    finally:
        conexao.close()
