"""Smoke-test Chronem after installing its wheel into a fresh environment."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from importlib import import_module
from importlib.metadata import version
from importlib.resources import files
from uuid import UUID

import chronem
from chronem import LifecycleAction, LifecycleEngine, Memory, MemoryKind


def _parking_memory(*, number: int, value: str, instant: datetime) -> Memory:
    subject_id = UUID("00000000-0000-0000-0000-000000000001")
    return Memory(
        id=UUID(int=number),
        user_id="wheel-smoke-user",
        kind=MemoryKind.CURRENT_STATE,
        subject_entity_id=subject_id,
        predicate="parked_at",
        value=value,
        observed_at=instant,
        memory_key=Memory.build_memory_key(subject_id, "parked_at"),
        created_at=instant,
        updated_at=instant,
    )


def main() -> None:
    """Verify import, packaged resources, and public lifecycle behavior."""
    try:
        import_module("mnemo")
    except ModuleNotFoundError as error:
        if error.name != "mnemo":
            raise
    else:
        raise RuntimeError("legacy mnemo import must not exist in the Chronem wheel")

    if not chronem.__all__:
        raise RuntimeError("chronem public API exports are empty")
    if not files("chronem").joinpath("py.typed").is_file():
        raise RuntimeError("installed wheel is missing chronem/py.typed")
    fixture = files("chronem.evaluation.data").joinpath("recall_planning.json")
    if not fixture.is_file() or not fixture.read_text(encoding="utf-8").strip():
        raise RuntimeError("installed wheel is missing recall_planning.json")

    start = datetime(2026, 1, 1, 12, tzinfo=UTC)
    first = _parking_memory(number=201, value="A1", instant=start)
    repeated = _parking_memory(
        number=202,
        value="A1",
        instant=start + timedelta(minutes=5),
    )
    moved = _parking_memory(
        number=203,
        value="B7",
        instant=start + timedelta(minutes=10),
    )
    lifecycle = LifecycleEngine()
    if lifecycle.reconcile(existing_active=[], incoming=first).action != LifecycleAction.APPEND:
        raise RuntimeError("installed lifecycle APPEND smoke failed")
    if (
        lifecycle.reconcile(existing_active=[first], incoming=repeated).action
        != LifecycleAction.NOOP
    ):
        raise RuntimeError("installed lifecycle NOOP smoke failed")
    if (
        lifecycle.reconcile(existing_active=[first], incoming=moved).action
        != LifecycleAction.SUPERSEDE
    ):
        raise RuntimeError("installed lifecycle SUPERSEDE smoke failed")

    print(f"installed chronem {version('chronem')} wheel smoke: PASS")


if __name__ == "__main__":
    main()
