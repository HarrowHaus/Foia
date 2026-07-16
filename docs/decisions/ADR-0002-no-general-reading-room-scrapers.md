# ADR-0002: No general reading-room scrapers

## Decision

Do not ship brittle general scrapers for CIA, FBI, NSA, presidential libraries, or similar reading rooms.

## Rationale

Search interfaces, terms, robots rules, and page structures change. The reliable workflow is source discovery through an approved browser/search tool followed by exact public-file or record-page import. Add an adapter only when a documented API or stable public data contract exists.
