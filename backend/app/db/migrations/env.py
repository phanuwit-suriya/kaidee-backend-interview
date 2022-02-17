import logging
import os
import pathlib
import sys
from logging.config import fileConfig

import alembic
from psycopg2 import DatabaseError
from sqlalchemy import create_engine
from sqlalchemy import engine_from_config, pool

sys.path.append(str(pathlib.Path(__file__).resolve().parents[3]))
from app.core.config import DATABASE_URL, POSTGRES_DB

config = alembic.context.config
fileConfig(config.config_file_name)
logger = logging.getLogger("alembic.env")


def run_migrations_online() -> None:
    db_url = f"{DATABASE_URL}_test" if os.environ.get("TESTING") else str(DATABASE_URL)
    if os.environ.get("TESTING"):
        default_engine = create_engine(str(DATABASE_URL), isolation_level="AUTOCOMMIT")
        with default_engine.connect() as default_conn:
            default_conn.execute(f"DROP DATABASE IF EXISTS {POSTGRES_DB}_test")
            default_conn.execute(f"CREATE DATABASE {POSTGRES_DB}_test")

    connectable = config.attributes.get("connection", None)
    config.set_main_option("sqlalchemy.url", db_url)
    if connectable is None:
        connectable = engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )

    with connectable.connect() as connection:
        alembic.context.configure(connection=connection, target_metadata=None)
        with alembic.context.begin_transaction():
            alembic.context.run_migrations()


def run_migrations_offline() -> None:
    if os.environ.get("TESTING"):
        raise DatabaseError(
            "Running testing migrations offline currently not permitted."
        )

    alembic.context.configure(url=str(DATABASE_URL))

    with alembic.context.begin_transaction():
        alembic.context.run_migrations()


if alembic.context.is_offline_mode():
    logger.info("Running migrations offline")
    run_migrations_offline()
else:
    logger.info("Running migrations online")
    run_migrations_online()
