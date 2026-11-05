
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import os

# Configuração do Alembic
config = context.config

# Configuração dos registros de log
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Caminho do banco de dados SQLite
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Permite escolher um banco de teste sem alterar o banco principal
DB_PATH = os.environ.get(
    "ALEMBIC_DB_PATH",
    os.path.join(BASE_DIR, "sistema.db")
)

config.set_main_option(
    "sqlalchemy.url",
    "sqlite:///" + DB_PATH.replace("\\", "/")
)

# Metadados das tabelas
target_metadata = None


def run_migrations_offline() -> None:
    """Executa migrações sem conexão direta com o banco."""

    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        render_as_batch=True
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Executa migrações com conexão ao banco."""

    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_as_batch=True
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
