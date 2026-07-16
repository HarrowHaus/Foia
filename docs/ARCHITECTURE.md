# Architecture

## Layers

1. **Source adapters** return normalized discovery results but do not make evidence claims.
2. **Acquisition** downloads or copies exact records with size limits, logging, and hashes.
3. **Extraction** produces page-level text and extraction metadata.
4. **SQLite evidence store** holds documents, pages, entities, events, claims, evidence links, hypotheses, contradictions, leads, novelty checks, runs, and phase checkpoints.
5. **FTS5** provides deterministic local full-text search.
6. **Analysis modules** create candidate signals: near duplicates, repeated phrases, redaction markers, timeline exports, contradictions, and graph data.
7. **Reports** produce checkpoints and dossier scaffolds.

## Data directories

```text
workspace/
  PROJECT.md
  pril.sqlite3
  raw/              immutable acquired files by hash prefix
  extracted/        optional exported page text
  ledgers/          JSONL operator/agent records
  manifests/        source and document inventories
  analysis/         machine-generated leads
  reports/          phase checkpoints and dossiers
  logs/             network and run logs
  exports/          reproduction bundles
```

## Trust boundary

Raw documents are evidence candidates. Extracted text is a derivative convenience. Automated analysis is a lead generator. Human-reviewed evidence links are the bridge to claims.
