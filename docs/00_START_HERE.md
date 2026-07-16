# Start Here

This repository is both a research operating system and a software handoff.

## What it is designed to do

It helps a human/AI research team:

- map public archival sources;
- retrieve records through documented APIs or deliberate direct imports;
- preserve raw records and provenance;
- extract searchable page-level text;
- maintain entities, events, claims, evidence links, hypotheses, contradictions, and dead ends;
- identify cross-document phrase reuse, version divergence, redaction differences, timeline conflicts, and network bridges;
- test whether a finding is already known;
- create reproducible checkpoint and dossier reports.

## What it does not claim

- It does not prove any theory by itself.
- It does not make model-generated entity matches into facts.
- It does not bypass archives, access controls, robots restrictions, or rate limits.
- It does not guarantee that every reading room exposes an API.
- It does not treat a missing record or a redaction as proof of a specific allegation.
- It does not depend on filing new FOIA requests.

## First operator session

1. Copy `.env.example` to `.env` and add only keys you actually possess.
2. Run `scripts/bootstrap.ps1` or `scripts/bootstrap.sh`.
3. Run `pril doctor`.
4. Run `pril init ./workspace`.
5. Open `workspace/PROJECT.md` and name the investigation only after the clean-slate source-discovery phase has begun.
6. Create a Phase 0 checkpoint before any substantive theory selection.

## The first research question

Do not begin with “Which conspiracy should be proved?” Begin with:

> Which already-public records contain unresolved patterns that become intelligible only when connected across collections?
