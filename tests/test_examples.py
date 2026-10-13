from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parents[1]
ZERO_NETWORK_EXAMPLE = ROOT / "examples" / "deterministic_lifecycle.py"
POSTGRES_EXAMPLE = ROOT / "examples" / "postgres_full_engine.py"
README = ROOT / "README.md"


def test_readme_30_second_demo_runs_outside_repository(tmp_path: Path) -> None:
    readme = README.read_text(encoding="utf-8")
    marker = "python - <<'PY'\n"
    assert readme.count(marker) == 1
    demo = readme.split(marker, maxsplit=1)[1].split("\nPY", maxsplit=1)[0]

    result = subprocess.run(
        [sys.executable, "-c", demo],
        cwd=tmp_path,
        check=True,
        capture_output=True,
        text=True,
    )

    assert result.stdout.splitlines() == [
        "actions: APPEND -> NOOP -> SUPERSEDE",
        "current: B7",
        "history: A1 (SUPERSEDED) -> B7 (ACTIVE)",
    ]


def test_zero_network_example_runs_with_documented_output() -> None:
    result = subprocess.run(
        [sys.executable, str(ZERO_NETWORK_EXAMPLE)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    assert result.stdout.splitlines() == [
        "first_capture: APPEND",
        "repeat_capture: NOOP",
        "moved_capture: SUPERSEDE",
        "active_parking: B7",
        "history: A1 (SUPERSEDED) -> B7 (ACTIVE)",
    ]


def test_postgres_example_imports_and_exposes_help_without_database() -> None:
    result = subprocess.run(
        [sys.executable, str(POSTGRES_EXAMPLE), "--help"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    assert "--database-url" in result.stdout


def test_examples_use_public_package_code_and_readme_paths_are_real() -> None:
    readme = README.read_text(encoding="utf-8")
    for example in (ZERO_NETWORK_EXAMPLE, POSTGRES_EXAMPLE):
        source = example.read_text(encoding="utf-8")
        assert "from tests" not in source
        assert "import tests" not in source
        assert str(example.relative_to(ROOT)) in readme
