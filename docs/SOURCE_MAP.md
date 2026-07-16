# Source Map

Last verified: 2026-07-15. Re-verify contracts before major collection runs.

## Implemented APIs

### National Archives Catalog API v2

- Mode: `keyed_api`
- Endpoint: `https://catalog.archives.gov/api/v2/records/search`
- Header: `x-api-key`
- Strengths: descriptions, authority records, digital object metadata, extracted text, public contributions.
- Important limits: official terms state a default 10,000 queries/month; do not use the API to mirror the full catalog; use the official bulk dataset for full exports; current terms also caution against caching API content, so this repository stores only operator-selected research records and their provenance rather than an indiscriminate mirror.
- Official documentation: `https://www.archives.gov/research/catalog/help/api`

### OSTI.GOV API v1

- Mode: `active_api`
- Endpoint: `https://www.osti.gov/api/v1/records`
- Query: `q`, plus fielded filters such as `title`, `author`, `identifier`, `sponsor_org`, `research_org`, date bounds, and `has_fulltext`.
- Strengths: DOE-funded technical literature, reports, contract/report identifiers, full-text availability metadata.
- Official documentation: `https://www.osti.gov/api/v1/docs`

### Internet Archive APIs

- Mode: `active_api`
- Search endpoint used here: `https://archive.org/advancedsearch.php`
- Item metadata: `https://archive.org/metadata/{identifier}`
- Strengths: government-document mirrors, historical scans, withdrawn web material, item metadata, Wayback discovery.
- Important limits: do not deep-page blindly; respect current bot, user-agent, rate-limit, and access guidance.
- Official developer portal: `https://archive.org/developers/index-apis.html`

### FederalRegister.gov API

- Mode: `active_api`
- Endpoint: `https://www.federalregister.gov/api/v1/documents.json`
- Strengths: notices, rules, proposed rules, executive actions, agencies, dates, document numbers.
- Official developer page: `https://www.federalregister.gov/developers/documentation/api/v1`

### CourtListener REST API

- Mode: `keyed_api`
- Endpoint used here: `https://www.courtlistener.com/api/rest/v3/search/`
- Strengths: case law, RECAP dockets/documents, judges, oral arguments, financial disclosures.
- Current developer documentation is maintained by Free Law Project: `https://www.courtlistener.com/help/` links to the wiki.

## Deliberate direct-import sources

These sources are in scope but are not treated as stable general APIs in this package. Search them manually or with an approved browser tool, then ingest the exact public record URL/file.

- CIA FOIA Electronic Reading Room: `https://www.cia.gov/readingroom/`
- FBI Vault: `https://vault.fbi.gov/`
- NSA FOIA Reading Room and declassification releases: `https://www.nsa.gov/Helpful-Links/NSA-FOIA/`
- State Department Office of the Historian / FRUS: `https://history.state.gov/historicaldocuments`
- presidential-library digital collections;
- inspectors general reading rooms;
- agency FOIA logs and reading rooms;
- congressional committee sites;
- university special collections.

## Keyed/planned adapters

GovInfo and Congress.gov are recorded in `configs/sources.toml`. Their public APIs require keys. Before enabling broad automated searches, verify the exact current endpoint contract and add contract tests from official examples.

## Source-selection principle

Use official API or bulk access where documented. Use direct import for exact records. Never turn this repository into an indiscriminate crawler.
