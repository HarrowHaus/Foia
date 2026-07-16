# ADR-0001: SQLite-first local evidence store

## Decision

Use SQLite with FTS5 as the authoritative local index.

## Rationale

It is portable, inspectable, reproducible, easy to back up, and capable of handling a substantial targeted corpus without requiring cloud infrastructure. Optional graph or semantic systems may be derived from it, not replace it.
