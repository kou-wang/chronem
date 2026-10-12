"""Run Chronem's provider-independent engine path against disposable PostgreSQL."""

from __future__ import annotations

import argparse
import os
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from uuid import uuid4

from chronem import (
    CandidateMemory,
    Capture,
    DeterministicEntityResolver,
    EntityType,
    IngestionService,
    LifecycleEngine,
    Memory,
    MemoryKind,
    MemoryQuery,
    MemoryQueryOrder,
    RecallAnswerService,
    RecallMode,
    RecallOrchestrationService,
    RecallPlan,
    RecallPlanOutcome,
    SourceType,
    StructuredRecallRequest,
    StructuredRecallService,
    SynthesizedAnswer,
)
from chronem.persistence.postgres import (
    PostgresCaptureRepository,
    PostgresEntityRepository,
    PostgresMemoryQueryRepository,
    PostgresMemoryRepository,
    create_postgres_engine,
    create_session_factory,
)

NOW = datetime(2026, 1, 1, 12, tzinfo=UTC)


@dataclass(frozen=True)
class FixedClock:
    instant: datetime

    def now(self) -> datetime:
        return self.instant


class ParkingExtractor:
    """Deterministic example adapter; replace it with any ``Extractor``."""

    _locations = {
        "I parked at A1.": "A1",
        "I moved to B7.": "B7",
    }

    def extract(self, capture: Capture) -> Sequence[CandidateMemory]:
        try:
            location = self._locations[capture.raw_text]
        except KeyError:
            raise ValueError("this example understands only its two sample captures") from None
        return (
            CandidateMemory(
                kind=MemoryKind.CURRENT_STATE,
                subject="my car",
                subject_type=EntityType.VEHICLE,
                predicate="parked_at",
                value=location,
            ),
        )


class ParkingRecallPlanner:
    """Deterministic example planner for one supported question."""

    def plan(self, *, user_id: str, question: str, asked_at: datetime) -> RecallPlan:
        if question != "Where is my car?":
            return RecallPlan(outcome=RecallPlanOutcome.UNSUPPORTED)
        return RecallPlan(
            outcome=RecallPlanOutcome.PLANNED,
            requests=(
                StructuredRecallRequest(
                    user_id=user_id,
                    subject="my car",
                    expected_subject_type=EntityType.VEHICLE,
                    kind=MemoryKind.CURRENT_STATE,
                    predicate="parked_at",
                    mode=RecallMode.CURRENT,
                ),
            ),
        )


class ParkingAnswerSynthesizer:
    """Phrase only the evidence supplied by deterministic recall."""

    def synthesize(
        self,
        *,
        question: str,
        evidence: tuple[Memory, ...],
        asked_at: datetime,
    ) -> SynthesizedAnswer:
        memory = evidence[0]
        return SynthesizedAnswer(
            text=f"Your car is parked at {memory.value}.",
            cited_memory_ids=(memory.id,),
        )


def run(database_url: str) -> None:
    """Persist two captures, recall the active state, and show retained history."""
    engine = create_postgres_engine(database_url)
    user_id = f"postgres-example-{uuid4()}"
    clock = FixedClock(NOW + timedelta(minutes=10))
    try:
        sessions = create_session_factory(engine)
        captures = PostgresCaptureRepository(sessions)
        entities = PostgresEntityRepository(sessions)
        memories = PostgresMemoryRepository(sessions)
        queries = PostgresMemoryQueryRepository(sessions)
        resolver = DeterministicEntityResolver(entities)

        ingestion = IngestionService(
            extractor=ParkingExtractor(),
            entity_resolver=resolver,
            capture_repository=captures,
            entity_repository=entities,
            memory_repository=memories,
            clock=clock,
            lifecycle_engine=LifecycleEngine(),
        )

        for offset, text in enumerate(("I parked at A1.", "I moved to B7.")):
            captured_at = NOW + timedelta(minutes=offset)
            result = ingestion.ingest(
                Capture(
                    user_id=user_id,
                    source_type=SourceType.TEXT,
                    raw_text=text,
                    captured_at=captured_at,
                    created_at=captured_at,
                )
            )
            print(f"ingested: {text} -> {result.candidate_results[0].outcome.value}")

        structured_recall = StructuredRecallService(
            entity_resolver=resolver,
            memory_query_repository=queries,
            clock=clock,
        )
        orchestration = RecallOrchestrationService(
            planner=ParkingRecallPlanner(),
            structured_recall_service=structured_recall,
        )
        answers = RecallAnswerService(
            recall_orchestration_service=orchestration,
            answer_synthesizer=ParkingAnswerSynthesizer(),
        )
        answer = answers.answer(
            user_id=user_id,
            question="Where is my car?",
            asked_at=clock.now(),
        )

        car = resolver.resolve(user_id=user_id, mention="my car").matched_entity
        if car is None:
            raise RuntimeError("example entity was not persisted")
        history = queries.query(
            MemoryQuery(
                user_id=user_id,
                statuses=None,
                kind=MemoryKind.CURRENT_STATE,
                subject_entity_id=car.id,
                predicate="parked_at",
                order=MemoryQueryOrder.OBSERVED_AT_ASC,
            )
        )

        print(f"answer: {answer.text}")
        print(f"citations: {len(answer.cited_memory_ids)} memory")
        print("history: " + " -> ".join(f"{m.value} ({m.status.value})" for m in history))
    finally:
        engine.dispose()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--database-url",
        default=os.environ.get("CHRONEM_DATABASE_URL"),
        help="SQLAlchemy psycopg URL (defaults to CHRONEM_DATABASE_URL)",
    )
    args = parser.parse_args()
    if not args.database_url:
        parser.error("--database-url or CHRONEM_DATABASE_URL is required")
    run(args.database_url)


if __name__ == "__main__":
    main()
