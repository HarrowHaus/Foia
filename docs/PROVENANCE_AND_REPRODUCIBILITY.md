# Provenance and Reproducibility

## Preserve

- original bytes;
- SHA-256 hash;
- retrieval URL and referring record page;
- retrieval timestamp in UTC;
- archive or local identifier;
- source institution;
- media type and size;
- extraction software and version where available;
- per-page extracted text and text hash;
- operator-supplied metadata;
- any transformation or OCR step.

## Deterministic IDs

Document IDs derive from the content hash. Re-ingesting identical bytes returns the same document ID. Claims, events, entities, and hypotheses receive stable prefixed UUIDs.

## Citation form

Preferred citation:

`[Institution], [Collection/Record Group], [Title], [date], [identifier], p. [page], document_id=[ID], sha256=[hash prefix].`

For born-digital records without pages, cite the item ID, section, paragraph, timestamp, or file name.

## Reproduction bundle

A publication candidate exports:

- source manifest;
- query log;
- hashes;
- raw-public-record inventory;
- page/excerpt map;
- claim/evidence matrix;
- timeline;
- graph data;
- novelty log;
- software version and configuration.
