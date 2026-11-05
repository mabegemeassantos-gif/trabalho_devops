from alembic import op
import sqlalchemy as sa


revision = "003"
down_revision = "002"
branch_labels = None
depends_on = None


def upgrade():
    """Preenche primeiro_nome e sobrenome usando o campo cliente."""

    conexao = op.get_bind()

    transacoes = conexao.execute(
        sa.text("""
            SELECT id_transacao, cliente
            FROM transacoes
        """)
    ).fetchall()

    for transacao in transacoes:

        nome_completo = (transacao.cliente or "").strip()
        partes = nome_completo.split(maxsplit=1)

        primeiro_nome = partes[0] if partes else ""
        sobrenome = partes[1] if len(partes) > 1 else ""

        conexao.execute(
            sa.text("""
                UPDATE transacoes
                SET primeiro_nome = :primeiro_nome,
                    sobrenome = :sobrenome
                WHERE id_transacao = :id_transacao
            """),
            {
                "primeiro_nome": primeiro_nome,
                "sobrenome": sobrenome,
                "id_transacao": transacao.id_transacao
            }
        )


def downgrade():
    """Limpa os campos preenchidos pelo Backfill."""

    conexao = op.get_bind()

    conexao.execute(
        sa.text("""
            UPDATE transacoes
            SET primeiro_nome = NULL,
                sobrenome = NULL
        """)
    )