# Handoff Manifest

Prepared: 2026-07-15

## Delivered

- clean-slate agent contract and pasteable Work Mode prompt;
- full project charter, evidence rules, research loop, phase gates, novelty protocol, contradiction protocol, redaction-differential method, provenance standard, source map, runbook, architecture, data dictionary, security controls, acceptance tests, and roadmap;
- Python 3.11+ package with CLI;
- SQLite/FTS5 evidence store;
- deterministic content-derived document IDs;
- immutable raw-file preservation and SHA-256 audit;
- PDF, HTML, text, JSON, and CSV extraction;
- direct URL and local-file ingestion;
- normalized discovery adapters for NARA, OSTI, Internet Archive, Federal Register, and CourtListener;
- explicit registry entries for direct-import and planned/keyed sources;
- repeated-phrase, near-duplicate, redaction-marker, timeline-candidate, contradiction, and graph outputs;
- checkpoint report generation;
- JSON schemas and JSONL ledger templates;
- synthetic acceptance corpus;
- Windows and Unix bootstrap scripts;
- Dockerfile, CI workflow, issue templates, tests, verification script, and export script.

## Validation completed

- repository verification: passed;
- Python compile check: passed;
- Ruff static check: passed;
- Pytest: 5 passed;
- editable package installation: passed;
- `pril doctor`: passed with SQLite FTS5 available;
- workspace initialization: passed;
- duplicate ingestion idempotency: passed;
- local FTS search: passed;
- deterministic analysis run: passed;
- checkpoint generation: passed;
- raw-file hash audit: passed.

## Network-validation boundary

The build container did not provide outbound DNS/network access. Live calls to OSTI, Internet Archive, Federal Register, NARA, and CourtListener could not be executed from the container. Endpoint design and source notes were checked against current official public documentation on 2026-07-15. Work Mode must run small, rate-limited contract checks after setup and before any broad collection run.

## Required first Work Mode action

Read `AGENTS.md`, run verification/tests/doctor, initialize a workspace, and produce the Phase 0 plan. Do not begin Phase 1 until the acceptance gate is explicitly reviewed.
