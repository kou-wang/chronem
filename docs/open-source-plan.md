# Mnemo Open-Source Plan

> Strategic North Star for Mnemo's open-source development, releases, adoption,
> and community growth.
>
> Last updated: 2026-10-12

## North Star

Mnemo's primary near-term objective is to become a credible, useful, and
discoverable open-source temporal memory engine for AI applications.

**GitHub Star growth is the primary adoption signal**, but not the only signal.
Stars should come from real developer interest created by strong positioning,
easy installation, useful examples/integrations, technical credibility, and
consistent releases—not from feature count alone.

The durable product idea is:

> LLMs interpret memory. Deterministic code decides what memory becomes.

Mnemo should differentiate through temporal lifecycle, preserved history,
provenance, conservative identity handling, grounded recall, and fail-closed
behavior rather than by becoming another thin vector-memory wrapper.

## Current position

| Area | Status | Current state |
| --- | --- | --- |
| Core temporal memory engine | COMPLETE | Domain model, lifecycle, entity resolution, ingestion, PostgreSQL, recall, grounded answers |
| Deterministic evaluation | COMPLETE | Required contract domains fail closed in CI |
| External developer onboarding | COMPLETE | README, quickstart, runnable examples, contribution/security docs |
| Packaging/release foundations | COMPLETE | Wheel/sdist validation, installed-wheel PostgreSQL migrations, trusted-publishing workflow |
| First public release | **CURRENT** | Issue #34 — ship v0.1.0 and establish adoption baseline |
| Launch/discoverability | NEXT | Promotion assets and first deliberate public launch cycle |
| Integration-driven adoption | PLANNED | Choose one compelling integration from ecosystem/user evidence |
| Community benchmark/provider evaluation | PLANNED | Build credibility without confusing deterministic tests with model accuracy |
| Semantic/hybrid retrieval | CONDITIONAL | Add only when external use cases justify it |
| Consumer/mobile product | DEFERRED | Revisit after open-source adoption or market evidence supports it |

## Strategic phases

### Phase 0 — Build a trustworthy engine

**Status: COMPLETE**

Objective:
- establish a technically credible memory engine before promotion.

Completed outcomes include:
- typed memory model;
- deterministic lifecycle and history retention;
- conservative entity resolution;
- PostgreSQL persistence and migrations;
- structured/temporal recall;
- grounded answer citations and abstention;
- deterministic evaluation;
- public examples and release-quality packaging.

Exit signal:
- the project can be installed, evaluated, and understood without relying on
  undocumented maintainer knowledge.

### Phase A — First public release

**Status: CURRENT**

Current execution issue:
- **#34 — Ship v0.1.0 and establish the growth baseline**

Objective:
- make Mnemo a real installable public package rather than only a GitHub source
  repository.

Required outcomes:
- validated v0.1.0 release candidate;
- PyPI trusted publishing configured;
- GitHub Release and PyPI version aligned;
- real clean-environment public install verified;
- README switched to public install only after verification;
- dated baseline of Stars/forks/external activity recorded.

Exit signal:
- a stranger can install the released package from the public package index and
  reproduce the basic Mnemo experience.

Do not add new engine features merely to make v0.1.0 look larger.

### Phase B — Launch and discoverability

**Status: NEXT**

Objective:
- turn a technically sound repository into something developers actually find,
  understand, try, and share.

Likely work:
- one concise demo that shows why temporal lifecycle matters;
- strong repository presentation and GitHub topics;
- launch copy for appropriate developer communities;
- technical write-up explaining Mnemo's architectural difference;
- a deliberate launch cycle rather than scattered promotion.

Possible channels may include developer communities, technical social platforms,
Hacker News, Reddit, framework communities, and relevant Discord/Slack spaces.
Channel selection should be current and evidence-based at launch time.

Exit signal:
- external Stars, installs, questions, issues, or discussions show that
  positioning reaches people outside the maintainer's existing network.

After this phase, perform a **Launch Review** before creating the next major
feature Issue.

### Phase C — Integration-driven adoption

**Status: PLANNED**

Objective:
- reduce the cost of trying Mnemo inside tools and ecosystems developers already
  use.

Rule:
- build **one compelling integration at a time**, chosen from current external
  interest rather than from a fixed wishlist.

Potential categories:
- coding/agent tools;
- agent frameworks;
- protocol-based integrations;
- provider adapters;
- application examples.

The exact first integration is TBD until after the v0.1.0 launch cycle.

Exit signal:
- external users can adopt Mnemo without designing all integration glue
  themselves, and at least one integration produces measurable interest or
  usage.

### Phase D — Benchmark and technical credibility

**Status: PLANNED**

Objective:
- make Mnemo's technical claims inspectable and comparable.

Likely work:
- transparent provider/model evaluation;
- memory correctness scenarios;
- temporal/lifecycle demonstrations;
- comparisons that explain tradeoffs without fake aggregate accuracy claims;
- reproducible benchmark/report artifacts.

Rule:
- deterministic CI results remain separate from probabilistic model-quality
  results.

Exit signal:
- external readers can understand what Mnemo is good at, what is measured, and
  what remains unmeasured.

### Phase E — Community loop

**Status: PLANNED / CONTINUOUS AFTER LAUNCH**

Objective:
- move roadmap input from maintainer assumptions toward external evidence.

Signals:
- external Issues and Discussions;
- external contributors;
- community examples/integrations;
- repeated onboarding questions;
- installation pain;
- requests that recur across unrelated users.

Likely work:
- good-first issues;
- contributor-friendly extension points;
- fast issue triage;
- documentation fixes driven by actual confusion;
- release notes that make upgrades worth revisiting.

Exit signal:
- roadmap decisions increasingly cite external usage/feedback rather than only
  internal ideas.

### Phase F — Semantic/hybrid capability expansion

**Status: CONDITIONAL**

Objective:
- augment deterministic/structured recall only when real use cases need broader
  retrieval.

Do not enter this phase simply because vector retrieval is common in other
memory projects.

Entry signals may include:
- repeated user requests that structured recall cannot answer;
- integrations that need open-ended retrieval;
- benchmark evidence showing a meaningful recall gap.

Structured/temporal retrieval remains the source-of-truth baseline.

### Phase G — Consumer/mobile product

**Status: DEFERRED**

The original consumer direction remains valid as a possible future product, but
it is not the current execution priority.

Revisit only when one or more of these are true:
- open-source adoption reveals a clear end-user opportunity;
- market research validates consumer demand;
- a consumer product materially accelerates the open-source ecosystem;
- commercialization becomes strategically more valuable than continued
  open-source growth.

## Star and adoption milestones

These are **diagnostic milestones, not forecasts or promises**. There is no
fixed deadline attached to them.

| Milestone | Question to answer | Typical response |
| ---: | --- | --- |
| First 25 Stars | Does the positioning/onboarding resonate at all? | Fix README, demo, installation, or initial distribution before adding major features |
| 100 Stars | Is initial discoverability working beyond close contacts? | Double down on the strongest channel/story and identify integration demand |
| 500 Stars | Is there recurring external interest rather than one launch spike? | Strengthen integrations, contributor loop, benchmark credibility, release cadence |
| 1,000+ Stars | Is Mnemo becoming a recognizable open-source project? | Formalize community/release discipline and broaden ecosystem coverage selectively |

Do not optimize for a milestone by weakening technical credibility, inflating
claims, buying fake engagement, or shipping unrelated features.

## Metrics

Primary:
- GitHub Stars.

Supporting signals:
- forks;
- external contributors;
- external Issues/Discussions;
- external integrations/examples;
- repeat visitors/release interest when observable;
- PyPI download/install data when reliable;
- reported README/install friction;
- release adoption and upgrade feedback.

A supporting signal can outweigh raw Star growth when it indicates real usage.

## Release strategy

### v0.1.0

Purpose:
- define what Mnemo is and make the first trustworthy public installation path.

Do not use v0.1.0 as a reason to add more features.

### 0.1.x

Use for:
- packaging/install fixes;
- documentation;
- compatibility fixes;
- regressions;
- small backward-compatible usability improvements.

### 0.MINOR.0

Use for:
- meaningful new public capability;
- a new integration surface;
- a significant evaluation/extension milestone;
- an intentional breaking change during pre-1.0 development.

A minor release should give an external developer a clear reason to look at
Mnemo again.

Do not bump versions mechanically for every merged PR.

## Operating loop

Mnemo does **not** use a fixed "finish Issue -> automatically create next feature
Issue" process.

Use this loop:

```text
Plan
  -> scoped GitHub Issue
  -> implementation PR
  -> independent review / repair
  -> merge
  -> release or expose the change when appropriate
  -> measure external response
  -> review what changed
  -> adjust this plan
  -> choose the next Issue
```

After launch-oriented work, always include a measurement/review step before
committing to the next major technical capability.

## Direction change log

### 2026-10-12 — Open-source adoption became the primary near-term objective

Before:
- open-source engine work and a possible consumer product were progressing in
  parallel conceptually.

Change:
- prioritize the reusable open-source engine, technical credibility, community
  usability, and GitHub adoption;
- defer consumer/mobile implementation.

Reason:
- commercial consumer demand is not yet validated, while a strong open-source
  project has independent value through adoption, technical credibility,
  ecosystem learning, and reusable community infrastructure.

### 2026-10-12 — Release/adoption work moved ahead of more engine features

Before:
- semantic/hybrid retrieval and additional capabilities were natural next
  technical steps.

Change:
- complete evaluation, onboarding, packaging, first release, launch, and
  adoption loops before automatically expanding retrieval.

Reason:
- more code does not create adoption if developers cannot discover, install,
  understand, or integrate the project.

### 2026-10-12 — Roadmap became evidence-adjusted rather than fixed

Change:
- keep long-term phases, but choose each next major Issue after reviewing real
  release/community signals.

Reason:
- integrations, benchmark priorities, and missing capabilities should be driven
  by external evidence wherever possible.

## Current next actions

1. Complete the **v0.1.0 release-preparation PR** under Issue #34.
2. Run the release dry-run workflow against the exact merged release commit.
3. Confirm PyPI/GitHub trusted-publishing account configuration.
4. Create `v0.1.0` and run the release workflow with publishing disabled.
5. Obtain explicit maintainer approval before enabling PyPI publishing.
6. Verify the real public package installation and PostgreSQL extra.
7. Record the first adoption baseline in
   [Open-source growth log](open-source-growth.md).
8. Perform a Launch Review and create the Phase B launch/discoverability Issue.
9. After the launch cycle, inspect real feedback before selecting the first
   major integration or new engine capability.

## AI / maintainer resume checklist

When resuming Mnemo work:

1. Read the current GitHub Issue first for task scope.
2. Read `AGENTS.md`.
3. Read **this file** to understand the strategic objective and current phase.
4. Read `docs/project-status.md` for the latest implementation state.
5. Read `docs/roadmap.md` for technical sequencing.
6. For code/semantic work, read `docs/architecture.md` and relevant ADRs.
7. Inspect current open PRs and recent merged PRs before assuming status.
8. Do not infer the next major feature only from the roadmap. Check current
   adoption/release/community evidence and this plan first.
9. If strategy changes materially, update the Direction Change Log in this file
   and the roadmap/status in the same planning cycle.

## Relationship to other project documents

- **GitHub Issue** — exact scope and acceptance criteria for the current task.
- **AGENTS.md** — engineering/workflow rules shared by human and AI contributors.
- **open-source-plan.md** — strategic North Star, growth phases, and why the
  current priority exists.
- **architecture.md / decisions/** — technical boundaries and accepted decisions.
- **product-requirements.md** — established product requirements.
- **roadmap.md** — technical/project phase ordering.
- **project-status.md** — what is currently implemented/in progress.
- **open-source-growth.md** — dated adoption baselines and launch-review evidence.

If a task-specific Issue conflicts with an accepted architecture decision or this
strategic direction, surface the conflict rather than silently choosing one.
