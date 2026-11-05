from alembic import op
import sqlalchemy as sa


revision = "004"
down_revision = "003"
branch_labels = None
depends_on = None


def upgrade():
    """Remove o campo antigo cliente na etapa Contract."""

    with op.batch_alter_table("transacoes") as batch_op:
        batch_op.drop_column("cliente")


def downgrade():
    """Recria o campo cliente caso seja necessário voltar."""

    with op.batch_alter_table("transacoes") as batch_op:
        batch_op.add_column(
            sa.Column("cliente", sa.String(150), nullable=True)
        )