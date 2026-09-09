import os
from pathlib import Path

from alembic import command
from alembic.config import Config


def run_database_migrations():
    database_url = os.getenv("DATABASE_URL", "")

    # Local SQLite database ko touch nahi karna hai.
    if not database_url.startswith(("postgresql://", "postgres://")):
        return

    backend_dir = Path(__file__).resolve().parent.parent
    alembic_ini = backend_dir / "alembic.ini"

    config = Config(str(alembic_ini))

    print("Running PostgreSQL database migrations...")
    command.upgrade(config, "head")
    print("PostgreSQL database migrations completed.")
