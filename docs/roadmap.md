# Roadmap

This roadmap records technical/project sequence and intended outcomes. The
[Open-source plan](open-source-plan.md) is the strategic North Star for adoption,
release, promotion, milestone interpretation, and major direction changes.
Detailed implementation belongs in GitHub Issues and accepted architecture
choices belong under [decisions](decisions/README.md).

## 1. Sprint 1 — complete

Repository bootstrap, typed domain models, deterministic lifecycle behavior,
canonical scenario fixtures, and Python 3.11/3.12 quality gates are complete.
See the historical [Sprint 1 specification](sprint-1-spec.md).

## 2. Shared developer workflow — Issue #7

Establish one durable Issue → implementation → PR → review → repair → merge
workflow shared by ChatGPT/maintainers, Codex, and Cursor.

## 3. Sprint 2 interfaces — Issue #5

Define provider-independent extraction and storage interfaces after Issue #7 is
reviewed and merged. Do not add concrete providers or persistence technology as
part of the interface task unless Issue #5 explicitly requires it.

## 4. Extraction

Implement natural-language interpretation behind the approved extraction
boundary. Provider and model choices are `TBD`.

## 5. Entity resolution

Add conservative, explainable, reversible entity resolution without silent
ambiguous merges. Issue #16 adds explicit probabilistic entity-type hints to
unresolved extraction mentions as the bridge to future ingestion orchestration;
it does not change deterministic name/alias matching or create entities.
Detailed future algorithms and orchestration remain `TBD`.

## 6. Persistence

Persist structured and temporal memory behind the approved storage boundary.
Issue #14 establishes PostgreSQL through SQLAlchemy 2.x and psycopg 3, with
Alembic migrations and database-enforced current-state/user-scope invariants.
Vector and semantic indexing choices remain `TBD`.

## 7. Ingestion orchestration

Issue #18 connects capture-first provenance, typed entity resolution/creation,
validated memory materialization, deterministic lifecycle reconciliation, and
repository writes. It is the internal write-path bridge before recall and does
not add lifecycle-command interpretation or a cross-repository unit of work.

## 8. Retrieval and temporal recall

Issue #20 adds the first deterministic structured and temporal recall layer:
explicit subject resolution outcomes, current/active/history/latest modes,
temporal validity, stable PostgreSQL queries, and provenance-preserving evidence.
Issue #22 adds probabilistic natural-language planning into one or more existing
structured recall requests, with explicit unsupported/ambiguous abstention and
relative time anchored only to the supplied question timestamp. Issue #24 adds
provider-independent execution of those exact requests through deterministic
structured recall, retaining per-request results and grounded provenance while
preserving planner abstention. Issue #26 adds grounded answer synthesis over only
that evidence, with deterministic abstention, validated memory citations,
conservative multi-value preservation, and an explicitly partial answer path.
Category-aware aggregation and semantic/hybrid retrieval remain later work.
Semantic/vector lookup is a fallback or augmentation after structured retrieval,
not the primary path.

## 9. Evaluation

Issue #28 establishes typed, serializable evaluation contracts and a 100%
deterministic CI gate for lifecycle, entity resolution, planning fixtures,
PostgreSQL structured/temporal recall, and grounded-answer invariants. Real
provider/model quality remains a separate non-CI activity; its datasets,
execution policy, and thresholds are `TBD` and mocked outputs are not accuracy
evidence. See [Evaluation](evaluation.md).

## 10. Open-source developer experience and launch readiness

Issue #30 makes open-source adoption, technical credibility, and community
usability the primary near-term direction. Priorities are a clear external
README, runnable network-free and PostgreSQL examples, public package metadata,
contributor/security entrypoints, and smoke coverage that keeps onboarding
instructions executable. This work changes presentation and usability, not
memory semantics.

## 11. Packaging and release foundations

Issue #32 establishes repeatable wheel and sdist builds, metadata and packaged-
data checks, package-contained PostgreSQL migrations, isolated installed-wheel
core and database smoke coverage, pre-1.0 versioning and changelog policy,
manual release dry runs, and an intentional release workflow designed for PyPI
trusted publishing. Publishing still requires explicit maintainer action plus
repository/PyPI configuration; no static credential or automatic version bump
belongs in the repository.

## 12. Examples, integrations, and extension points

Expand provider, framework, and application examples according to demonstrated
external-developer needs while keeping provider-independent contracts
authoritative. Integrations must not bypass deterministic lifecycle,
user-isolation, provenance, or grounded-recall boundaries.

## 13. Community-facing provider-quality evaluation

Define transparent datasets, model/provider metadata, execution policy, and
thresholds for live quality evaluation. Keep these results separate from the
deterministic contract gate; mocked outputs are never model-accuracy evidence.

## 14. Semantic and hybrid retrieval

Consider semantic/hybrid retrieval only when reusable engine use cases justify
it. Structured and temporal recall remain the baseline and source of truth;
technology and ranking choices are `TBD`.

## 15. Consumer and mobile application work — deferred

The historical direction remains a low-friction iOS-first consumer experience
using React Native + Expo while preserving an Android path. It is explicitly
deferred behind open-source engine adoption, packaging, examples/integrations,
and evaluation work. Detailed implementation, release planning, and rollout
remain future-scoped.

Current implementation and review state lives in
[Project status](project-status.md), not in this roadmap.
