
from alembic import op
import sqlalchemy as sa


# Identificadores da migração
revision = "002"
down_revision = "001"
branch_labels = None
depends_on = None


def upgrade():
    """Adiciona os novos campos mantendo o campo antigo."""

    with op.batch_alter_table("transacoes") as batch_op:
        batch_op.alter_column(
            "cliente",
            existing_type=sa.String(),
            nullable=True
        )

        batch_op.add_column(
            sa.Column("primeiro_nome", sa.String(100), nullable=True)
        )

        batch_op.add_column(
            sa.Column("sobrenome", sa.String(100), nullable=True)
        )


def downgrade():
    """Reverte as alterações da etapa Expand."""

    # Recupera o nome completo antes de tornar cliente obrigatório.
    conexao = op.get_bind()

    conexao.execute(
        sa.text("""
            UPDATE transacoes
            SET cliente = TRIM(
                COALESCE(primeiro_nome, '') || ' ' ||
                COALESCE(sobrenome, '')
            )
            WHERE cliente IS NULL
        """)
    )

    with op.batch_alter_table("transacoes") as batch_op:
        batch_op.drop_column("sobrenome")
        batch_op.drop_column("primeiro_nome")

        batch_op.alter_column(
            "cliente",
            existing_type=sa.String(),
            nullable=False
        )
