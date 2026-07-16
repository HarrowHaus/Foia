# Data Dictionary

## documents
One row per unique byte sequence. ID is based on SHA-256.

## pages
Page/segment text with text hash and extraction confidence.

## entities / entity_aliases / mentions
Normalized people, organizations, programs, places, facilities, technologies, and identifiers.

## events
Date-bounded occurrences with precision and source linkage.

## claims
Research propositions with epistemic class, status, confidence, and scope.

## evidence_links
Exact relationship between a claim and a source location.

## hypotheses
Competing explanations with predictions and disconfirmers.

## contradictions
Pairs of propositions or records requiring reconciliation.

## leads
Anomalies and candidate research paths with explicit score components.

## novelty_checks
Prior-art searches and novelty interpretation.

## runs
Software operations with parameters and outputs.

## phase_checkpoints
Frozen summaries and gate decisions.
