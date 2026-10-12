# Contributing to Mnemo

Thanks for helping make Mnemo useful as a reusable temporal memory engine.
Start with an Issue so the behavior, boundaries, and acceptance criteria are
clear before implementation.

## Local setup

Mnemo supports Python 3.11 and 3.12.

```bash
git clone https://github.com/kou-wang/mnemo-memory.git
cd mnemo-memory
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

Run the local gates before opening a pull request:

```bash
ruff check .
mypy src
pytest --cov=mnemo --cov-report=term-missing
coverage report --include="*/mnemo/lifecycle/*" --fail-under=90
```

Behavior changes require focused regression tests. Lifecycle changes are
especially suited to sequence tests that show the prior state, action, and
retained history.

## PostgreSQL tests and deterministic evaluation

These commands are destructive to their configured database. Use a disposable
database containing no data you need to retain.

```bash
docker run --name mnemo-postgres --rm -d \
  -e POSTGRES_USER=mnemo \
  -e POSTGRES_PASSWORD=mnemo \
  -e POSTGRES_DB=mnemo_test \
  -p 5432:5432 postgres:16
until docker exec mnemo-postgres pg_isready -U mnemo -d mnemo_test; do sleep 1; done

export MNEMO_TEST_DATABASE_URL="postgresql+psycopg://mnemo:mnemo@127.0.0.1:5432/mnemo_test"
pytest -m postgres
python scripts/run_deterministic_evaluation.py
docker stop mnemo-postgres
```

The deterministic evaluation checks software contracts; it is not a live-model
accuracy benchmark. See [Evaluation](docs/evaluation.md).

## Distribution changes

Packaging changes must validate built artifacts, not only an editable install:

```bash
artifact_dir="$(mktemp -d)"
python -m build --outdir "$artifact_dir"
python -m twine check --strict "$artifact_dir"/*
python scripts/validate_distribution.py "$artifact_dir"
```

Follow the complete fresh-environment smoke test in
[Releasing Mnemo](docs/releasing.md). Version changes and publishing are
maintainer decisions; ordinary contributions should keep the current version
unless their Issue explicitly authorizes a release preparation.

## Workflow and architecture changes

Use the repository workflow: Issue → focused branch → pull request → review →
repair → maintainer merge. Link the Issue in the PR, explain validation and
security/privacy impact, and do not include secrets or real personal data.

Read [Architecture](docs/architecture.md),
[accepted decisions](docs/decisions/README.md), and
[development workflow](docs/development-workflow.md) before changing engine
behavior. Ordinary fixes can use the existing contracts. New memory kinds,
lifecycle semantics, or architectural boundaries require explicit Issue scope,
maintainer agreement, and an ADR update rather than an incidental code change.

The [roadmap](docs/roadmap.md) and [project status](docs/project-status.md)
describe current priorities. `AGENTS.md` is the canonical engineering guidance
for AI-assisted contributions.
