# Phase 0 Plan and Execution Report

Prepared: 2026-07-16 (first Work Mode session after handoff)

## Objective

Establish reliable ingestion, provenance, search, evidence ledgers, analysis
outputs, source mapping, and checkpoints, per `docs/WORK_MODE_HANDOFF.md`.

## Questions being tested

- Does the delivered system pass its own acceptance tests in a fresh environment?
- Are document IDs deterministic and reproducible across clean workspaces?
- Do the no-key discovery adapters honor their live API contracts?
- What capabilities are missing, and do any block Phase 1?

## Tools and source classes

- Local: `scripts/verify_repo.py`, pytest, ruff, `pril` CLI against the
  synthetic acceptance corpus in `examples/synthetic_corpus`.
- Network: single small, rate-limited contract check per no-key adapter
  (OSTI, Internet Archive, Federal Register), per the network-validation
  boundary recorded in `docs/HANDOFF_MANIFEST.md`. No broad collection runs.

## Execution results (2026-07-16)

Environment: Python 3.11.15, SQLite 3.45.1 with FTS5, Linux container.

- Handoff integrity: 93/93 files match `SHA256SUMS.txt`.
- `python scripts/verify_repo.py`: passed.
- `python -m pytest -q`: 5 passed.
- `ruff check src tests scripts`: passed.
- `pril doctor`: FTS5 available; `pypdf`, `bs4`, `networkx`, `rapidfuzz` present.
- `pril init ./workspace`: created documented tree and database; re-run safe.
- Synthetic corpus ingestion: both memos ingested; re-ingesting identical
  bytes returned the same `doc_64ab8efeab279b49fecab503` with
  `inserted: false` and no duplicate pages; raw bytes preserved under
  hash-derived paths.
- Deterministic reproduction: a second, fresh workspace reproduced the
  identical document ID from the same bytes.
- FTS5 search: page-level snippets returned for corpus terms
  (note: titles are not FTS-indexed by design; only page text is).
- `pril analyze`: 15 repeated phrases, 0 near duplicates, 2 redaction
  markers, 3 timeline candidates, 2 contradiction candidates.
- `pril checkpoint`: report generated under `workspace/reports/`.
- `pril audit`: 2 documents checked, 0 hash failures.
- Live adapter contract checks (small, rate-limited, custom user agent):
  - `federal_register`: normalized results returned, including PDF URLs.
  - `internet_archive`: normalized results returned.
  - `osti`: normalized results returned.
  - `nara` (keyed, no key present): failed with the actionable message
    "NARA_API_KEY is required…" as specified.

## Remaining limitations

- OCR stack absent (`pytesseract`, `fitz`): image-only PDFs will extract no
  text until installed. Non-blocking for Phase 0; flag on first scanned PDF.
- No API keys configured (`NARA_API_KEY`, `GOVINFO_API_KEY`,
  `CONGRESS_API_KEY`, `COURTLISTENER_TOKEN`): keyed adapters unusable until
  the operator supplies keys in `.env`.
- `govinfo` and `congress` adapters remain `planned`; their current search
  contracts must be verified before implementation.
- `courtlistener` is implemented but could not be live-checked without a token.
- Live checks used one query per adapter; sustained rate-limit behavior is
  untested and should be observed during the first Phase 1 collection runs.

## Evidentiary threshold

Phase 0 asserts only system capability, not any research finding. No
entities, events, claims, hypotheses, or leads were recorded.

## Stopping criteria and gate status

Gate 0 (`docs/PHASE_GATES.md`) requires verification, tests, doctor,
workspace initialization, synthetic ingestion, FTS search, analysis,
checkpoint, and audit to complete. All completed as recorded above.

**Gate 0 status: criteria met pending operator review.** Per
`docs/WORK_MODE_HANDOFF.md`, Phase 1 will not begin until the operator
explicitly reviews this acceptance gate.

## Next-step queue (Phase 1, upon gate approval)

1. Operator supplies any available API keys in `.env` and confirms the
   research contact in `PRIL_USER_AGENT`.
2. Build the diverse Phase 1 query bank across source families
   (people, organizations, programs, contractors, facilities, acronyms,
   technical phrases, budgets, routing terms, records schedules,
   successor terminology) with no preferred conclusion.
3. Run small, logged, rate-limited searches across OSTI, Internet Archive,
   and Federal Register; record negative results in the query log.
4. Install the OCR stack before the first scanned-PDF corpus.
5. Verify current govinfo and Congress API contracts before enabling those
   adapters.
