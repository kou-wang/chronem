# Changelog

All notable changes to Mnemo will be documented in this file. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and releases follow
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Mnemo has not yet been published to PyPI. Version `0.1.0` is the first public
release candidate and must not be advertised as published until the release
workflow and clean public-install verification succeed.

## [Unreleased]

## [0.1.0] - 2026-10-12

### Added

- Typed temporal memory model for facts, preferences, current state, events, and
  intents.
- Deterministic lifecycle behavior with no-op deduplication, current-state
  supersession, retained history, intent transitions, and source provenance.
- Conservative, user-scoped entity resolution with explicit matched,
  unmatched, and ambiguous outcomes.
- PostgreSQL persistence, structured/temporal queries, and packaged Alembic
  migrations that work from an installed wheel.
- Provider-independent ingestion, recall planning, recall orchestration, and
  grounded-answer interfaces.
- Optional OpenAI Structured Outputs adapters for extraction, recall planning,
  and answer synthesis.
- Grounded answer citations, deterministic abstention, and fail-closed
  cross-user/invariant checks.
- Deterministic contract evaluation across lifecycle, entity resolution,
  recall-planning fixtures, real PostgreSQL structured recall, and answer
  grounding.
- External-developer README, zero-network lifecycle example, PostgreSQL
  full-engine example, contribution/security guidance, and typed-package marker.
- Repeatable wheel and source-distribution validation, installed-wheel core and
  PostgreSQL migration smoke tests, release dry-run workflow, and PyPI trusted
  publishing foundation.

### Security

- User isolation is enforced as a domain invariant rather than relying only on
  application-layer filtering.
- Grounded answers reject citations outside supplied recall evidence.
- Release publishing is designed for GitHub Actions OIDC trusted publishing
  without a static PyPI credential in the repository.

[Unreleased]: https://github.com/kou-wang/mnemo-memory/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/kou-wang/mnemo-memory/releases/tag/v0.1.0
