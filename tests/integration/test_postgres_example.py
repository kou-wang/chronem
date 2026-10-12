from __future__ import annotations

import os
import subprocess
import sys
from collections.abc import Iterator
from pathlib import Path

import pytest

from chronem.persistence.postgres.migration import (
    _downgrade_postgres_database,
    upgrade_postgres_database,
)

pytestmark = pytest.mark.postgres

ROOT = Path(__file__).parents[2]


@pytest.fixture(scope="module")
def migrated_example_database() -> Iterator[str]:
    database_url = os.environ.get("CHRONEM_TEST_DATABASE_URL")
    if not database_url:
        pytest.skip("CHRONEM_TEST_DATABASE_URL is required for PostgreSQL integration tests")

    upgrade_postgres_database(database_url)
    yield database_url
    _downgrade_postgres_database(database_url)


def test_postgres_full_engine_example_runs(migrated_example_database: str) -> None:
    environment = os.environ.copy()
    environment["CHRONEM_DATABASE_URL"] = migrated_example_database
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
