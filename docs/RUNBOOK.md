# Operator Runbook

## Initialize

```bash
pril doctor
pril init ./workspace
```

## Search a source

```bash
pril source-list
pril source-search osti "behavior modification" --limit 20
pril source-search internet_archive 'collection:usgovdocs AND title:(research)' --limit 20
pril source-search federal_register "records retention" --limit 20
pril source-search nara '"project name"' --limit 20
```

NARA requires `NARA_API_KEY`.

## Ingest exact records

```bash
pril ingest-file ./workspace ./downloads/record.pdf \
  --source-id nara \
  --source-url "https://catalog.archives.gov/id/000000" \
  --archive-id "NAID 000000" \
  --title "Exact archival title"

pril ingest-url ./workspace "https://example.gov/released-record.pdf" \
  --source-id agency-reading-room \
  --archive-id "DOC-123"
```

## Search local corpus

```bash
pril search ./workspace '"North Annex" AND transfer'
```

## Run deterministic analysis

```bash
pril analyze ./workspace
pril checkpoint ./workspace
pril audit ./workspace
```

## Research ledgers

The CLI handles core ingestion and analysis. Human/agent research records may be entered using the JSON schemas in `schemas/` and imported in future extensions. The initialized workspace includes JSONL ledger templates under `workspace/ledgers/`.
