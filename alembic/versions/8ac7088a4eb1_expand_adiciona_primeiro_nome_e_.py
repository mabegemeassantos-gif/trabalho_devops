from alembic import op
import sqlalchemy as sa


# Identificadores da migração
revision = "002"
down_revision = "001"
branch_labels = None
depends_on = None


def upgrade():
    """Adiciona os novos campos sem remover o campo antigo."""

    with op.batch_alter_table("transacoes") as batch_op:

        batch_op.add_column(
            sa.Column("primeiro_nome", sa.String(100), nullable=True)
        )

        batch_op.add_column(
            sa.Column("sobrenome", sa.String(100), nullable=True)
        )


def downgrade():
    """Remove os campos adicionados na etapa Expand."""

    with op.batch_alter_table("transacoes") as batch_op:

        batch_op.drop_column("sobrenome")
        batch_op.drop_column("primeiro_nome")