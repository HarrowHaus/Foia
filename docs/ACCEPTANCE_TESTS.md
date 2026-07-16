# Acceptance Tests

## Repository

- `python scripts/verify_repo.py` exits zero.
- `python -m pytest -q` exits zero.
- package installs in a fresh virtual environment.
- `pril doctor` reports FTS5 available.

## Workspace

- `pril init` creates the documented directory tree and database.
- re-running `pril init` is safe.
- ingesting identical bytes twice returns the same document ID and does not duplicate pages.
- original bytes are preserved under a hash-derived path.
- page text is searchable through FTS5.

## Analysis

Using `examples/synthetic_corpus`:

- repeated phrases are detected across the two documents;
- date-like strings are exported to the timeline candidate file;
- redaction-like markers are counted;
- near-duplicate comparison runs without treating similarity as identity;
- checkpoint report includes corpus statistics and warnings;
- audit confirms raw-file hashes.

## Source adapters

- no-key adapters normalize results into the common result schema;
- keyed adapters fail with actionable missing-key messages;
- all network requests use the configured user agent, timeout, delay, and result limits;
- adapters do not crawl result links automatically.

## Evidence integrity

- original raw files are never modified;
- extracted text is marked derivative;
- document provenance survives export;
- no claim can be marked `publication_candidate` without at least one evidence link and one novelty check in future workflow enforcement.
