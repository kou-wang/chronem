# Chronem

> Temporal memory with lifecycle and provenance.

Chronem is an open-source temporal memory engine for AI applications. It turns
natural-language captures into structured, lifecycle-aware memory while keeping
identity, state changes, persistence, and recall under deterministic control.

LLMs may interpret language. They do not decide what gets persisted, silently
merge identities, overwrite history, or invent evidence. Chronem preserves source
provenance and temporal history, and its recall path can abstain when stored
evidence does not support an answer.

> Status: early-stage Python library. The core engine, PostgreSQL adapter,
> OpenAI adapters, structured recall, grounded answers, and deterministic
> contract evaluation are implemented. Semantic/vector retrieval is not.

## Why Chronem?

| Approach | What it is good at | What Chronem adds |
| --- | --- | --- |
| Notes or key-value memory | Simple storage and direct lookup | Typed facts, preferences, current state, events, and intents with explicit lifecycle rules |
| Chat-history storage | Preserving a conversation transcript | Durable memories separated from raw captures, with identity, semantic time, and provenance |
| Vector stores | Similarity search over unstructured content | Deterministic structured/temporal lookup and state transitions; vector search is not the source of truth |
| Thin RAG memory wrappers | Retrieving context for a model | A controlled memory lifecycle, conservative entity resolution, history retention, evidence validation, and abstention |

Chronem is an engine rather than a notes app or a complete assistant. Applications
provide their own interface and may plug model providers into the interpretation
and phrasing boundaries.

## Architecture

```mermaid
flowchart LR
    subgraph P["Probabilistic boundaries (replaceable adapters)"]
        E[Extractor]
        RP[Recall Planner]
        GA[Grounded Answer phrasing]
    end
    subgraph D["Deterministic engine"]
        C[Capture]
        CM[CandidateMemory]
        ER[Entity Resolution]
        LE[Lifecycle Engine]
        DB[(PostgreSQL)]
        SR[Structured / Temporal Recall]
    end

    C --> E --> CM --> ER --> LE --> DB
    RP --> SR
    DB --> SR --> GA
```

The implemented path is capture → extraction → candidate memory → entity
resolution → lifecycle engine → PostgreSQL → recall planning → structured recall
→ grounded answer. Provider-independent interfaces separate the grouped
boundaries. There is currently no semantic/vector retrieval implementation.

## 5-minute quickstart — no API key or database

Requirements: Python 3.11 or 3.12.

Install the public release from PyPI:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install "chronem==0.1.0"
```

To run the repository's zero-network lifecycle walkthrough against that installed
package:

```bash
git clone --depth 1 https://github.com/kou-wang/chronem.git
cd chronem
python examples/deterministic_lifecycle.py
```

Expected output:

```text
first_capture: APPEND
repeat_capture: NOOP
moved_capture: SUPERSEDE
active_parking: B7
history: A1 (SUPERSEDED) -> B7 (ACTIVE)
```

This is the distinctive deterministic core: an identical current state is a
no-op, a changed value supersedes the active record, and the old value remains
in history. See [the example](examples/deterministic_lifecycle.py) for the public
API calls.

## PostgreSQL engine example

This longer example exercises capture, a local deterministic extractor, entity
resolution, ingestion, lifecycle persistence, structured recall, and a grounded
answer. It needs a disposable PostgreSQL database but no API key or external AI
service.

```bash
docker run --name chronem-postgres --rm -d \
  -e POSTGRES_USER=chronem \
  -e POSTGRES_PASSWORD=chronem \
  -e POSTGRES_DB=chronem \
  -p 5432:5432 postgres:16
until docker exec chronem-postgres pg_isready -U chronem -d chronem; do sleep 1; done

python -m pip install -e ".[postgres]"
export CHRONEM_DATABASE_URL="postgresql+psycopg://chronem:chronem@127.0.0.1:5432/chronem"
alembic upgrade head
python examples/postgres_full_engine.py
docker stop chronem-postgres
```

That is the **source-checkout** workflow: the repository's `alembic.ini` points
to the same migrations packaged with the PostgreSQL adapter. From an installed
wheel, no repository-local Alembic configuration is needed:

```bash
python -m pip install "chronem[postgres]==0.1.0"
python -m chronem.persistence.postgres.migrations \
  --database-url "$CHRONEM_DATABASE_URL"
```

Applications may instead call the public
`chronem.persistence.postgres.upgrade_postgres_database(database_url)` helper.
Both installed-package paths locate the migration environment and version
scripts inside Chronem's wheel.

The final lines show an evidence-backed answer with one validated citation and
the retained `A1 (SUPERSEDED) -> B7 (ACTIVE)` history.

Use only a disposable database: the example writes synthetic records. The local
extractor and answer phrasing make its output reproducible; applications can
replace those protocol implementations with the optional OpenAI adapters or
their own providers without giving a model persistence authority.

## Memory model and guarantees

Chronem models five top-level kinds:

- `FACT` — durable information; uncertain conflicting values are preserved.
- `PREFERENCE` — preferences that may coexist.
- `CURRENT_STATE` — one active value per state slot, with superseded history.
- `EVENT` — append-oriented occurrences with event time.
- `INTENT` — future actions that may complete, cancel, or expire.

The engine enforces user scope, timezone-aware temporal data, conservative
entity resolution, atomic PostgreSQL current-state supersession, capture
provenance, and citation validation for grounded answers. See
[Architecture](docs/architecture.md) and [accepted decisions](docs/decisions/README.md)
for the complete invariants.

## Deterministic evaluation

CI runs a deterministic contract evaluation over lifecycle, entity resolution,
the recall-planning fixture contract, real PostgreSQL structured recall, and
grounded-answer invariants. Every required domain must be present, contain at
least one case, and have no failures or the gate fails closed.

This is a software-contract result, **not a claim of AI or live-model accuracy**.
Provider/model quality evaluation is separate and is not currently a CI gate.
See [Evaluation](docs/evaluation.md) for the exact scope and command.

## Distribution status

CI builds both a wheel and source distribution, validates their metadata and
required package data, installs the wheel into a fresh virtual environment, and
runs the public lifecycle smoke test plus the zero-network example from that
installed wheel. It also installs the wheel's PostgreSQL extra, migrates a fresh
database using only packaged resources, and exercises a PostgreSQL repository.
The first public release, `chronem==0.1.0`, is published on PyPI and was
verified from a clean Python 3.11 virtual environment, including the packaged
PostgreSQL migration entrypoint.

Public releases are intentional maintainer actions using version tags and PyPI
trusted publishing; no static package-index credential is stored in the
repository. See the [changelog](CHANGELOG.md), [GitHub releases](https://github.com/kou-wang/chronem/releases),
and [release process](docs/releasing.md).

## Optional OpenAI adapters

```bash
python -m pip install "chronem[openai]==0.1.0"
```

`OpenAIExtractor`, `OpenAIRecallPlanner`, and `OpenAIAnswerSynthesizer` are
optional adapters behind provider-independent interfaces. Applications choose
the model and provide `OPENAI_API_KEY`. The basic quickstart and all
deterministic examples require neither an API key nor a live model call.

## Contributing and security

- [Contributing](CONTRIBUTING.md)
- [Security policy](SECURITY.md)
- [Roadmap](docs/roadmap.md)
- [Project status](docs/project-status.md)
- [Development workflow](docs/development-workflow.md)
- [Release process](docs/releasing.md)
- [Changelog](CHANGELOG.md)

## License

Licensed under [Apache-2.0](LICENSE).
