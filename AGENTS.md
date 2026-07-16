# Agent Operating Contract

This file controls any AI coding or research agent opened at the repository root.

## First action

Read, in order:

1. `docs/00_START_HERE.md`
2. `docs/WORK_MODE_HANDOFF.md`
3. `docs/PROJECT_CHARTER.md`
4. `docs/RESEARCH_OPERATING_SYSTEM.md`
5. `docs/EVIDENCE_STANDARD.md`
6. `docs/PHASE_GATES.md`
7. `docs/PROVENANCE_AND_REPRODUCIBILITY.md`
8. `docs/SOURCE_MAP.md`
9. `docs/ACCEPTANCE_TESTS.md`

Then run:

```bash
python scripts/verify_repo.py
python -m pytest -q
pril doctor
```

## Clean-slate boundary

This is an independent project. Do not import any prior project, theory, name list, person, timeline, conclusion, or source corpus unless the operator explicitly supplies it inside this repository or current session.

## Phase discipline

Before beginning any phase, present:

- phase name and objective;
- questions being tested;
- evidence targets;
- tools and source classes;
- deliverables;
- evidentiary threshold;
- stopping criteria.

Do not silently enter the next phase. Produce a checkpoint first.

## Research behavior

- Seek novel connections, but do not assume novelty.
- Follow unusual leads until they are resolved, falsified, superseded, or documented as blocked.
- Preserve contradictory evidence.
- Treat automated extraction, entity recognition, similarity, anomaly, and scoring outputs as leads only.
- Trace every material statement to the original record and exact page or item identifier.
- Prefer primary sources and official mirrors. Record derivative sources only as discovery paths.
- Do not mass-scrape archives against their terms. Use official APIs, official bulk datasets, or direct-document imports.
- Do not request new records. Record missing records as gaps unless the operator authorizes outreach.
- Do not publish personal data about private individuals merely because it is technically public. Apply public-interest minimization.

## Code behavior

- Keep the core runnable on Python 3.11+.
- Preserve deterministic IDs and schema compatibility.
- Add migrations rather than destructive schema edits after data exists.
- Keep network operations explicit, rate-limited, and logged.
- Never commit API keys, cookies, or downloaded restricted material.
- Add tests for every parser or adapter change.
- Run `python scripts/verify_repo.py`, tests, and `pril audit` before handoff.

## Required outputs per research run

- run log;
- source manifest;
- query log;
- document hashes;
- claim/evidence ledger updates;
- anomalies and dead ends;
- novelty checks;
- phase checkpoint;
- next-step queue.
