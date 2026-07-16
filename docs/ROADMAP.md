# Roadmap

## Included now

- deterministic workspace and SQLite schema;
- exact-file and direct-URL ingestion;
- PDF/HTML/text/JSON/CSV extraction;
- FTS5 search;
- source adapter registry;
- NARA, OSTI, Internet Archive, Federal Register, and CourtListener discovery adapters;
- hash audit;
- repeated-phrase, near-duplicate, redaction-marker, timeline-candidate, contradiction-summary, and graph exports;
- checkpoint reports;
- schemas, documentation, tests, and bootstrap scripts.

## Next engineering priorities

1. SQLite migrations and schema version commands.
2. OCR quality scoring and page-image alignment.
3. Review UI for claims/evidence links.
4. entity-resolution queue with alias evidence.
5. document-version page alignment.
6. query-bank runner with budgets and resumable pagination.
7. citation exporter for Markdown/CSL-JSON.
8. reproducibility bundle command.
9. current contract tests for GovInfo and Congress.gov.
10. optional semantic retrieval that never replaces deterministic search.
