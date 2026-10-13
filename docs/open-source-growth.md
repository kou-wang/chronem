# Open-Source Growth Log

This file records dated adoption baselines and launch reviews for Chronem. It is
evidence for roadmap decisions, not a vanity-metric scoreboard.

Strategic interpretation belongs in [Open-source plan](open-source-plan.md).
Current implementation state belongs in [Project status](project-status.md).

## v0.1.0 baseline

**Status: VERIFIED**

Observed immediately after the public release and clean-install verification.

| Signal | Baseline |
| --- | --- |
| Baseline timestamp | 2026-10-12T22:26:19Z |
| GitHub Stars | 0 |
| GitHub forks | 0 |
| External open Issues / PRs | 0 |
| External contributors | 0 verified |
| PyPI release | `chronem==0.1.0` published |
| Public install verification | PASS — clean Python 3.11 venv, site-packages import, PostgreSQL migration CLI |
| Known external integrations | 0 verified |
| Known external users | 0 verified |

Evidence:
- GitHub Release `Chronem v0.1.0` was published from tag `v0.1.0`;
- PyPI trusted publishing accepted the wheel and source distribution;
- a clean Python 3.11 virtual environment imported `chronem==0.1.0` from
  `site-packages`;
- the installed PostgreSQL extra exposed
  `python -m chronem.persistence.postgres.migrations --help`;
- at baseline observation time, the repository reported 0 Stars and 0 forks;
- Issue #34 was maintainer-created and there were no open pull requests, so no
  external open Issue/PR activity was counted.

Notes:
- distinguish maintainer-created Issues/PRs from external activity;
- do not fabricate PyPI downloads or installation counts;
- record future observations with timestamps because repository metrics change;
- this baseline is a starting point, not a success/failure judgment.

## Launch review template

After a deliberate launch/promotion cycle, append a dated review containing:

### Distribution

- channels used;
- what was posted/demonstrated;
- timing;
- meaningful referral or discussion evidence when available.

### Adoption delta

- Stars: baseline -> current;
- forks: baseline -> current;
- new external Issues/Discussions;
- new contributors;
- verified integrations/examples;
- reliable package adoption signals when available.

### Qualitative feedback

- repeated questions;
- installation/onboarding friction;
- features users ask for;
- what users appear to misunderstand;
- which positioning/message resonates.

### Decision

Choose the next action based on evidence. Typical choices include:

- improve onboarding/README/demo;
- continue the strongest distribution channel;
- build one requested integration;
- add benchmark/provider evaluation;
- fix release/install friction;
- add a capability supported by repeated external demand.

Do not automatically choose semantic/vector retrieval or another major engine
feature simply because it is present in the long-term roadmap.

## Review history

No completed launch reviews yet.
