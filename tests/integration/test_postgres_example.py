from __future__ import annotations

import os
import subprocess
import sys
from collections.abc import Iterator
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config

pytestmark = pytest.mark.postgres

ROOT = Path(__file__).parents[2]


@pytest.fixture(scope="module")
def migrated_example_database() -> Iterator[str]:
    database_url = os.environ.get("MNEMO_TEST_DATABASE_URL")
    if not database_url:
        pytest.skip("MNEMO_TEST_DATABASE_URL is required for PostgreSQL integration tests")

    alembic_config = Config(str(ROOT / "alembic.ini"))
    alembic_config.set_main_option("script_location", str(ROOT / "migrations"))
    alembic_config.set_main_option("sqlalchemy.url", database_url.replace("%", "%%"))
    command.upgrade(alembic_config, "head")
    yield database_url
    command.downgrade(alembic_config, "base")


def test_postgres_full_engine_example_runs(migrated_example_database: str) -> None:
    environment = os.environ.copy()
    environment["MNEMO_DATABASE_URL"] = migrated_example_database
    result = subprocess.run(
        [sys.executable, str(ROOT / "examples" / "postgres_full_engine.py")],
        cwd=ROOT,
        env=environment,
        check=True,
        capture_output=True,
        text=True,
    )

    assert "answer: Your car is parked at B7." in result.stdout
    assert "citations: 1 memory" in result.stdout
    assert "history: A1 (SUPERSEDED) -> B7 (ACTIVE)" in result.stdout
