"""Alembic environment.

Design notes:
- The database URL is the single source of truth in the project-level `.env`.
  We deliberately do NOT keep it in `alembic.ini` to avoid drifted/duplicated
  credentials and dialect mismatches between the app and migrations.
- `backend/` is added to `sys.path` so `app.*` imports resolve regardless of
  how Alembic is invoked (from `backend/` or from the repo root).
"""

from __future__ import annotations

import os
import sys
from logging.config import fileConfig
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool

from alembic import context

BACKEND_DIR = Path(__file__).resolve().parents[1]
PROJECT_ROOT = BACKEND_DIR.parent

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

load_dotenv(PROJECT_ROOT / ".env")

config = context.config

database_url = os.getenv("DATABASE_URL")
if not database_url:
    raise RuntimeError(
        "DATABASE_URL is not set. Define it in the project-level .env "
        "before running Alembic."
    )
config.set_main_option("sqlalchemy.url", database_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Import the models package so every mapped class registers on Base.metadata
# before autogenerate compares against the database.
from app.db.database import Base  # noqa: E402
import app.models  # noqa: F401,E402

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode (emit SQL, no DBAPI required)."""
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations against a live database connection."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
