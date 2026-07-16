# Work Mode Handoff

This document tells a capable coding/research agent exactly how to take over the repository.

## Assignment

Turn the repository into a continuously auditable research workspace, then run the phased discovery program without importing any prior theory.

## Mandatory opening sequence

1. Read `AGENTS.md` and all documents it lists.
2. Run repository verification and tests.
3. Run `pril doctor` and report missing optional capabilities without blocking core work.
4. Initialize a workspace.
5. Produce a Phase 0 plan before changing code or collecting a substantive corpus.

## Phase 0 objective

Establish reliable ingestion, provenance, search, evidence ledgers, analysis outputs, source mapping, and checkpoints.

### Phase 0 evidence targets

Evidence that the system can:

- ingest PDF, HTML, text, JSON, and CSV;
- retain source URL, retrieval timestamp, cryptographic hash, archive ID, and raw file;
- extract page-level text and search it;
- detect exact and near duplicates;
- compare document versions and redaction indicators;
- record entities, events, claims, evidence links, hypotheses, contradictions, and novelty checks;
- generate source manifests, graphs, timelines, and checkpoints;
- survive a clean reinstall and reproduce the same document IDs.

### Phase 0 deliverables

- passing tests;
- `pril doctor` report;
- initialized workspace;
- synthetic acceptance corpus results;
- source adapter status report;
- Phase 0 checkpoint with remaining limitations.

### Phase 0 stopping criteria

Do not enter Phase 1 until the acceptance tests in `docs/ACCEPTANCE_TESTS.md` pass or every exception is explicitly recorded.

## Phase 1 objective

Broad signal discovery without a preferred conclusion.

### Required search behavior

- Build a diverse query bank spanning people, organizations, programs, contractors, facilities, acronyms, technical phrases, budgets, routing terms, records schedules, and successor terminology.
- Search across unrelated source families.
- Record queries that return nothing.
- Promote anomaly clusters, not isolated exciting documents.
- Rank candidates by documentary density, cross-source independence, consequence, testability, and novelty potential.

## Phase 2 objective

Create adversarial candidate files for the strongest clusters. Each file must contain earliest appearance, full timeline, people, institutions, locations, funding, public explanation, internal explanation, contradictions, missing references, alternative explanations, and discriminating evidence.

## Phase 3 objective

Run recursive interpretation: each new document updates the corpus model, and the updated model causes old documents and old queries to be revisited.

## Phase 4 objective

Perform explicit novelty verification against scholarship, journalism, books, archival discussion, official histories, specialist communities, and prior conspiracy literature.

## Phase 5 objective

Build claim-by-claim evidence chains with exact citations, limits, corroboration, contradiction, and confidence.

## Phase 6 objective

Produce a publication package with a source manifest, documentary narrative, chronology, network, contradiction analysis, competing explanations, confidence assessment, novelty assessment, and reproduction instructions.

## Agent roles

A single agent may perform all roles, but it must keep their outputs distinct.

- **Orchestrator:** phase gates, task queue, checkpoints, stopping decisions.
- **Source Cartographer:** archives, finding aids, APIs, bulk paths, terms, coverage gaps.
- **Archivist:** raw-file preservation, metadata, hashes, identifiers, extraction quality.
- **Entity Resolver:** aliases, organizations, role dates, ambiguous identities.
- **Timeline Analyst:** event normalization, date conflicts, precursor/successor sequences.
- **Network Analyst:** personnel, institutional, contractual, technical, and location bridges.
- **Contradiction Analyst:** incompatible claims and public/internal divergence.
- **Novelty Auditor:** searches prior art and prevents false novelty claims.
- **Adversarial Reviewer:** ordinary explanations, source dependence, circularity, overclaiming.
- **Dossier Compiler:** reproducible narrative and evidence matrix.

## Communication rules

At each checkpoint, report:

- what was completed;
- strongest current signals;
- strongest disconfirming evidence;
- dead ends;
- source and extraction limitations;
- changes in confidence;
- exact next-phase plan.

Do not phrase an automated score as a factual conclusion.
