# Phase 1 Plan — Broad Signal Discovery

Prepared: 2026-07-16. Gate 0 approved by operator on 2026-07-16.

## Phase name and objective

Phase 1: broad signal discovery without a preferred conclusion
(`docs/WORK_MODE_HANDOFF.md`). The objective is to surface anomaly-cluster
candidates from already-public records across unrelated source families,
not to validate any theory.

## Questions being tested

- Which signal classes (`docs/RESEARCH_OPERATING_SYSTEM.md`) actually
  appear in the reachable no-key source families, and at what density?
- Which vocabulary (program names, form names, routing terms, org names)
  recurs across independent collections and should seed later rounds?
- Which queries return nothing, bounding what these families can show?

## Clean-slate boundary handling

No prior theory, person list, or program list is imported. Because
entity-specific queries (people, contractors, facilities, acronyms)
cannot be seeded from a clean slate, round 1 uses **theory-neutral
signal-class vocabulary** (routing terms, records-schedule terms, budget
terms, missing-reference phrases, successor terminology, redaction
markers). Entity and program queries are generated only from vocabulary
harvested out of round-1 results — this is the research loop's
reinterpretation step, bootstrapped.

## Evidence targets

- A logged query bank spanning the required categories, with negative
  results recorded.
- At least two candidate anomaly clusters containing more than one
  document each (clusters, not isolated exciting documents).
- Preserved raw records with provenance for every ingested document.
- A harvested-vocabulary list for round 2+.

## Tools and source classes

- Source families this round (no-key, live-verified in Phase 0): OSTI
  (DOE technical literature), Internet Archive government-document
  mirrors, Federal Register. These are institutionally independent
  families (energy/technical, intelligence/agency mirrors,
  regulatory/administrative).
- NARA, CourtListener, govinfo, Congress: deferred until keys/contract
  verification (recorded as a source limitation, not a dead end).
- All requests: configured user agent, 1.0 s request delay, small result
  limits (≤10), no automatic crawling of result links.

## Deliverables

- `workspace/ledgers/query_log.jsonl` — every query, including empties;
- `workspace/manifests/` — normalized search results per round;
- ingested cluster-candidate documents with hashes and provenance;
- analysis outputs and a Phase 1 round-1 checkpoint;
- committed run report (`research/phase1/`) so results survive this
  ephemeral environment (raw files and the database stay uncommitted per
  repository policy; the manifest's URLs + SHA-256 hashes make the corpus
  reproducible).

## Evidentiary threshold

Everything found this round is a **lead** at lifecycle stage
`captured`/`triaged`. No claim, hypothesis, or conclusion may be recorded
from search snippets alone; promotion requires ingestion of the primary
record, evidence links, competing explanations, and a novelty check.

## Stopping criteria (this round)

Stop and checkpoint when the round-1 bank plus one harvested round-2 pass
have been executed and logged, cluster candidates are ranked by
documentary density, cross-source independence, consequence, testability,
and novelty potential, and disconfirming/ordinary explanations are noted
for each. Gate 1 itself requires multiple rounds; this round does not
claim Gate 1.
