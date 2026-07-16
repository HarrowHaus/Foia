# Public-Record Inference Lab

A clean-slate, reproducible research repository for discovering previously unrecognized facts, relationships, timelines, and narratives across already-public government and archival records.

This repository is **not preloaded with a conspiracy theory**. It begins with source mapping, evidence capture, provenance, contradiction analysis, entity/timeline reconstruction, anomaly discovery, novelty screening, and adversarial review.

## Non-negotiable operating rules

1. Do not import claims, people, timelines, evidence, assumptions, or conclusions from any earlier project unless the operator explicitly introduces them.
2. Prefer already-public records. Do not make a new FOIA request unless the operator separately authorizes one.
3. Separate documented fact, corroborated fact, strong inference, working theory, speculative lead, and disconfirmed lead.
4. Preserve the original file, cryptographic hash, retrieval URL, retrieval date, archive identifier, extraction method, and page-level text.
5. Never call a result novel until a recorded novelty search has been completed.
6. Before each phase, state the plan, objectives, evidence targets, deliverables, evidentiary threshold, and stopping criteria.
7. A dead end is a valid result. Fabrication, certainty inflation, and circular sourcing are not.

## Start here

Read these files in order:

1. [`AGENTS.md`](AGENTS.md)
2. [`docs/00_START_HERE.md`](docs/00_START_HERE.md)
3. [`docs/WORK_MODE_HANDOFF.md`](docs/WORK_MODE_HANDOFF.md)
4. [`docs/PROJECT_CHARTER.md`](docs/PROJECT_CHARTER.md)
5. [`docs/RESEARCH_OPERATING_SYSTEM.md`](docs/RESEARCH_OPERATING_SYSTEM.md)
6. [`docs/EVIDENCE_STANDARD.md`](docs/EVIDENCE_STANDARD.md)
7. [`docs/PHASE_GATES.md`](docs/PHASE_GATES.md)

## Quick setup

### Windows PowerShell

```powershell
Set-ExecutionPolicy -Scope Process Bypass
./scripts/bootstrap.ps1
.\.venv\Scripts\Activate.ps1
pril doctor
pril init ./workspace
```

### Linux/macOS

```bash
chmod +x scripts/bootstrap.sh
./scripts/bootstrap.sh
source .venv/bin/activate
pril doctor
pril init ./workspace
```

### Run the synthetic acceptance corpus

```bash
pril ingest-file ./workspace ./examples/synthetic_corpus/memo_a.txt --source-id synthetic
pril ingest-file ./workspace ./examples/synthetic_corpus/memo_b.txt --source-id synthetic
pril search ./workspace "North Annex"
pril analyze ./workspace
pril checkpoint ./workspace
```

Generated reports are written to `workspace/reports/`.

## Principal commands

```text
pril doctor
pril init WORKSPACE
pril source-list
pril source-search SOURCE QUERY [--limit N]
pril ingest-file WORKSPACE FILE [metadata options]
pril ingest-url WORKSPACE URL [metadata options]
pril search WORKSPACE QUERY
pril stats WORKSPACE
pril analyze WORKSPACE
pril checkpoint WORKSPACE
pril audit WORKSPACE
```

## Repository status

This handoff provides a complete operational foundation, not a claim that every archive has a stable public API. Source integrations are explicitly classified as:

- `active_api`: implemented against a documented endpoint.
- `keyed_api`: implemented but requires an operator-provided key.
- `direct_import`: use public search manually, then import the exact document URL/file.
- `bulk_dataset`: use the archive's official bulk path rather than crawling.
- `planned`: documented source, adapter intentionally not activated until its current contract is verified.

See [`docs/SOURCE_MAP.md`](docs/SOURCE_MAP.md) and [`configs/sources.toml`](configs/sources.toml).
