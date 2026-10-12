"""Validate built wheel/sdist names, metadata, and required package contents."""

from __future__ import annotations

import argparse
import email
import tarfile
import tomllib
import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).parents[1]
REQUIRED_PACKAGE_FILES = (
    "mnemo/py.typed",
    "mnemo/evaluation/data/recall_planning.json",
    "mnemo/persistence/postgres/migration.py",
    "mnemo/persistence/postgres/migrations/__init__.py",
    "mnemo/persistence/postgres/migrations/__main__.py",
    "mnemo/persistence/postgres/migrations/env.py",
    "mnemo/persistence/postgres/migrations/script.py.mako",
    "mnemo/persistence/postgres/migrations/versions/__init__.py",
    "mnemo/persistence/postgres/migrations/versions/20261008_0001_initial_postgres.py",
    "mnemo/persistence/postgres/migrations/versions/20261009_0002_structured_recall_index.py",
)
FORBIDDEN_SDIST_DIRECTORIES = {
    ".git",
    ".idea",
    ".mypy_cache",
    ".nox",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    ".vscode",
    "__pycache__",
    "build",
    "dist",
    "htmlcov",
    "venv",
}
FORBIDDEN_SDIST_FILENAMES = {
    ".DS_Store",
    ".env",
    "coverage.xml",
    "credentials.json",
    "service-account.json",
}
FORBIDDEN_SDIST_SUFFIXES = {
    ".key",
    ".p12",
    ".pem",
    ".pfx",
    ".pyc",
    ".pyo",
    ".swo",
    ".swp",
}
ALLOWED_SDIST_TOP_LEVEL = {
    ".cursor",
    ".gitignore",
    ".github",
    "AGENTS.md",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "LICENSE",
    "PKG-INFO",
    "README.md",
    "SECURITY.md",
    "alembic.ini",
    "docs",
    "examples",
    "pyproject.toml",
    "scripts",
    "src",
    "tests",
}


def _project_version() -> str:
    with (ROOT / "pyproject.toml").open("rb") as pyproject:
        return str(tomllib.load(pyproject)["project"]["version"])


def _single_artifact(directory: Path, pattern: str) -> Path:
    artifacts = tuple(directory.glob(pattern))
    if len(artifacts) != 1:
        raise ValueError(
            f"expected exactly one {pattern} artifact in {directory}, found {len(artifacts)}"
        )
    return artifacts[0]


def _validate_wheel(wheel: Path, *, version: str) -> None:
    expected_name = f"mnemo_memory-{version}-py3-none-any.whl"
    if wheel.name != expected_name:
        raise ValueError(f"expected wheel {expected_name}, found {wheel.name}")

    with zipfile.ZipFile(wheel) as archive:
        names = set(archive.namelist())
        missing = set(REQUIRED_PACKAGE_FILES) - names
        if missing:
            raise ValueError(f"wheel is missing required files: {sorted(missing)}")

        metadata_path = f"mnemo_memory-{version}.dist-info/METADATA"
        if metadata_path not in names:
            raise ValueError(f"wheel is missing {metadata_path}")
        metadata = email.message_from_bytes(archive.read(metadata_path))

    expected_metadata = {
        "Name": "mnemo-memory",
        "Version": version,
        "Requires-Python": ">=3.11",
        "License-Expression": "Apache-2.0",
    }
    for field, expected in expected_metadata.items():
        if metadata.get(field) != expected:
            raise ValueError(
                f"wheel metadata {field} must be {expected!r}, got {metadata.get(field)!r}"
            )


def _validate_sdist(sdist: Path, *, version: str) -> None:
    expected_name = f"mnemo_memory-{version}.tar.gz"
    if sdist.name != expected_name:
        raise ValueError(f"expected sdist {expected_name}, found {sdist.name}")

    prefix = f"mnemo_memory-{version}/"
    required = {
        f"{prefix}LICENSE",
        f"{prefix}README.md",
        f"{prefix}pyproject.toml",
        *(f"{prefix}src/{path}" for path in REQUIRED_PACKAGE_FILES),
    }
    with tarfile.open(sdist, mode="r:gz") as archive:
        names = set(archive.getnames())
    missing = required - names
    if missing:
        raise ValueError(f"sdist is missing required files: {sorted(missing)}")

    unexpected: list[str] = []
    for name in names:
        if not name.startswith(prefix):
            unexpected.append(name)
            continue
        relative = PurePosixPath(name.removeprefix(prefix))
        filename = relative.name
        if (
            not relative.parts
            or relative.parts[0] not in ALLOWED_SDIST_TOP_LEVEL
            or ".." in relative.parts
            or FORBIDDEN_SDIST_DIRECTORIES.intersection(relative.parts)
            or filename in FORBIDDEN_SDIST_FILENAMES
            or filename.startswith(".env.")
            or filename == ".coverage"
            or filename.startswith(".coverage.")
            or filename.endswith("~")
            or relative.suffix.lower() in FORBIDDEN_SDIST_SUFFIXES
        ):
            unexpected.append(name)
    if unexpected:
        raise ValueError(
            f"sdist contains forbidden local/build/secret artifacts: {sorted(unexpected)}"
        )


def validate(directory: Path) -> tuple[Path, Path]:
    """Validate exactly one wheel and sdist in ``directory``."""
    version = _project_version()
    wheel = _single_artifact(directory, "*.whl")
    sdist = _single_artifact(directory, "*.tar.gz")
    _validate_wheel(wheel, version=version)
    _validate_sdist(sdist, version=version)
    return wheel, sdist


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", nargs="?", type=Path, default=ROOT / "dist")
    args = parser.parse_args()
    wheel, sdist = validate(args.directory)
    print(f"validated wheel: {wheel.name}")
    print(f"validated sdist: {sdist.name}")


if __name__ == "__main__":
    main()
