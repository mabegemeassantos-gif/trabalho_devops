from alembic import op
import sqlalchemy as sa


# Identificadores da migração
revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """Cria a tabela inicial de transações."""

    op.create_table(
        "transacoes",

        sa.Column(
            "id_transacao",
            sa.String(50),
            primary_key=True
        ),

        sa.Column(
            "cliente",
            sa.String(150),
            nullable=False
        ),

        sa.Column(
            "cpf",
            sa.String(11),
            nullable=False
        ),

        sa.Column(
            "idade",
            sa.Integer(),
            nullable=True
        ),

        sa.Column(
            "valor_bruto",
            sa.Float(),
            nullable=True
        ),

        sa.Column(
            "valor_final",
            sa.Float(),
            nullable=True
        ),

        sa.Column(
            "status",
            sa.String(20),
            nullable=True
        ),

        sa.Column(
            "motivo_rejeicao",
            sa.Text(),
            nullable=True
        ),

        sa.Column(
            "data_processamento",
            sa.DateTime(),
            nullable=True
        )
    )


def downgrade():
    """Remove a tabela de transações."""

    op.drop_table("transacoes")