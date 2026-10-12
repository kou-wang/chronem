"""Installed-package PostgreSQL schema migration support."""

from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlalchemy.engine import make_url


def _migration_config(database_url: str) -> Config:
    url = make_url(database_url)
    if url.get_backend_name() != "postgresql":
        raise ValueError("Mnemo migrations require a PostgreSQL SQLAlchemy URL")

    config = Config()
    config.set_main_option(
        "script_location",
        str(Path(__file__).with_name("migrations")),
    )
    config.attributes["database_url"] = database_url
    return config


def upgrade_postgres_database(database_url: str) -> None:
    """Upgrade a PostgreSQL database to Mnemo's packaged migration head."""
    command.upgrade(_migration_config(database_url), "head")


def _downgrade_postgres_database(database_url: str) -> None:
    """Remove Mnemo's schema; reserved for tests using disposable databases."""
    command.downgrade(_migration_config(database_url), "base")
