"""Zero-network walkthrough of Mnemo's deterministic CURRENT_STATE lifecycle."""

from datetime import UTC, datetime, timedelta
from uuid import UUID

from mnemo import LifecycleAction, LifecycleEngine, Memory, MemoryKind, MemoryStatus

USER_ID = "quickstart-user"
CAR_ID = UUID("00000000-0000-0000-0000-000000000001")
START = datetime(2026, 1, 1, 12, tzinfo=UTC)


def parking_memory(*, number: int, location: str, observed_at: datetime) -> Memory:
    """Build one public ``Memory`` model for the car's parking state."""
    return Memory(
        id=UUID(int=number),
        user_id=USER_ID,
        kind=MemoryKind.CURRENT_STATE,
        subject_entity_id=CAR_ID,
        predicate="parked_at",
        value=location,
        observed_at=observed_at,
        memory_key=Memory.build_memory_key(CAR_ID, "parked_at"),
        created_at=observed_at,
        updated_at=observed_at,
    )


def main() -> None:
    """Reconcile A1, repeat A1, then move to B7 while retaining history."""
    lifecycle = LifecycleEngine()
    first = parking_memory(number=101, location="A1", observed_at=START)
    first_decision = lifecycle.reconcile(existing_active=[], incoming=first)
    if first_decision.action != LifecycleAction.APPEND:
        raise RuntimeError("unexpected first parking decision")

    repeat = parking_memory(
        number=102,
        location="A1",
        observed_at=START + timedelta(minutes=5),
    )
    repeat_decision = lifecycle.reconcile(existing_active=[first], incoming=repeat)

    moved = parking_memory(
        number=103,
        location="B7",
        observed_at=START + timedelta(minutes=10),
    )
    moved_decision = lifecycle.reconcile(existing_active=[first], incoming=moved)
    if moved_decision.action != LifecycleAction.SUPERSEDE:
        raise RuntimeError("unexpected moved-parking decision")

    superseded = first.model_copy(
        update={
            "status": MemoryStatus.SUPERSEDED,
            "superseded_by_id": moved.id,
            "updated_at": moved.observed_at,
        }
    )

    print(f"first_capture: {first_decision.action.value}")
    print(f"repeat_capture: {repeat_decision.action.value}")
    print(f"moved_capture: {moved_decision.action.value}")
    print(f"active_parking: {moved.value}")
    print(
        f"history: {superseded.value} ({superseded.status.value})"
        f" -> {moved.value} ({moved.status.value})"
    )


if __name__ == "__main__":
    main()
