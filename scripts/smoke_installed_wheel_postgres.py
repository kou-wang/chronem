"""Migrate and use PostgreSQL through an isolated installed Mnemo wheel."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from uuid import UUID


def _resolved_sys_path() -> set[Path]:
    return {Path(entry or ".").resolve() for entry in sys.path}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database-url", required=True)
    parser.add_argument("--source-root", required=True, type=Path)
    args = parser.parse_args()

    source_root = args.source_root.resolve()
    forbidden_import_paths = {source_root, source_root / "src"}
    overlap = forbidden_import_paths & _resolved_sys_path()
    if overlap:
        raise RuntimeError(f"source checkout is present on sys.path: {sorted(overlap)}")

    import mnemo
    from mnemo import Entity, EntityType
    from mnemo.persistence.postgres import (
        PostgresEntityRepository,
        create_postgres_engine,
        create_session_factory,
        upgrade_postgres_database,
    )

    installed_module = Path(mnemo.__file__).resolve()
    if installed_module.is_relative_to(source_root):
        raise RuntimeError(f"mnemo imported from source checkout: {installed_module}")

    upgrade_postgres_database(args.database_url)
    engine = create_postgres_engine(args.database_url)
    try:
        repository = PostgresEntityRepository(create_session_factory(engine))
        entity = Entity(
            id=UUID("00000000-0000-0000-0000-000000000321"),
            user_id="installed-wheel-postgres-user",
            type=EntityType.PLACE,
            canonical_name="Installed wheel garage",
            aliases=["wheel garage"],
        )
        repository.add(user_id=entity.user_id, entity=entity)
        if repository.get(user_id=entity.user_id, entity_id=entity.id) != entity:
            raise RuntimeError("installed PostgreSQL repository round trip failed")
    finally:
        engine.dispose()

    print("installed-wheel PostgreSQL migration and repository smoke: PASS")


if __name__ == "__main__":
    main()
