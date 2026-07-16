from __future__ import annotations

import json
import sqlite3
from collections.abc import Iterable
from pathlib import Path
from typing import Any

SCHEMA_VERSION = 1

SCHEMA_SQL = r"""
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS schema_info (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS sources (
    source_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    mode TEXT NOT NULL,
    base_url TEXT,
    notes TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS documents (
    document_id TEXT PRIMARY KEY,
    sha256 TEXT NOT NULL UNIQUE,
    title TEXT,
    source_id TEXT,
    source_url TEXT,
    archive_identifier TEXT,
    local_path TEXT NOT NULL,
    media_type TEXT,
    byte_size INTEGER NOT NULL,
    retrieved_at TEXT NOT NULL,
    date_created TEXT,
    date_published TEXT,
    date_released TEXT,
    classification_marking TEXT,
    ingestion_method TEXT NOT NULL,
    extraction_method TEXT,
    extraction_warning TEXT,
    provenance_json TEXT NOT NULL,
    metadata_json TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(source_id) REFERENCES sources(source_id)
);

CREATE INDEX IF NOT EXISTS idx_documents_archive_identifier
ON documents(archive_identifier);
CREATE INDEX IF NOT EXISTS idx_documents_source_id ON documents(source_id);

CREATE TABLE IF NOT EXISTS pages (
    document_id TEXT NOT NULL,
    page_number INTEGER NOT NULL,
    text TEXT NOT NULL,
    text_sha256 TEXT NOT NULL,
    extraction_confidence REAL,
    PRIMARY KEY(document_id, page_number),
    FOREIGN KEY(document_id) REFERENCES documents(document_id) ON DELETE CASCADE
);

CREATE VIRTUAL TABLE IF NOT EXISTS page_fts USING fts5(
    document_id UNINDEXED,
    page_number UNINDEXED,
    text,
    tokenize = 'unicode61 remove_diacritics 2'
);

CREATE TABLE IF NOT EXISTS entities (
    entity_id TEXT PRIMARY KEY,
    canonical_name TEXT NOT NULL,
    entity_type TEXT NOT NULL,
    description TEXT,
    status TEXT NOT NULL DEFAULT 'unreviewed',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS entity_aliases (
    entity_id TEXT NOT NULL,
    alias TEXT NOT NULL,
    source_document_id TEXT,
    page_number INTEGER,
    PRIMARY KEY(entity_id, alias),
    FOREIGN KEY(entity_id) REFERENCES entities(entity_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS mentions (
    mention_id TEXT PRIMARY KEY,
    entity_id TEXT NOT NULL,
    document_id TEXT NOT NULL,
    page_number INTEGER,
    surface_form TEXT NOT NULL,
    context TEXT,
    confidence REAL,
    review_status TEXT NOT NULL DEFAULT 'unreviewed',
    FOREIGN KEY(entity_id) REFERENCES entities(entity_id),
    FOREIGN KEY(document_id) REFERENCES documents(document_id)
);

CREATE TABLE IF NOT EXISTS events (
    event_id TEXT PRIMARY KEY,
    label TEXT NOT NULL,
    start_date TEXT,
    end_date TEXT,
    date_precision TEXT NOT NULL,
    location_entity_id TEXT,
    description TEXT,
    source_document_id TEXT,
    page_number INTEGER,
    review_status TEXT NOT NULL DEFAULT 'unreviewed',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    FOREIGN KEY(source_document_id) REFERENCES documents(document_id)
);

CREATE TABLE IF NOT EXISTS claims (
    claim_id TEXT PRIMARY KEY,
    statement TEXT NOT NULL,
    epistemic_class TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'draft',
    confidence REAL,
    scope TEXT,
    limitations TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS evidence_links (
    evidence_id TEXT PRIMARY KEY,
    claim_id TEXT NOT NULL,
    document_id TEXT NOT NULL,
    page_number INTEGER,
    relationship TEXT NOT NULL,
    excerpt TEXT,
    establishes TEXT,
    does_not_establish TEXT,
    source_strength TEXT,
    extraction_confidence REAL,
    notes TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(claim_id) REFERENCES claims(claim_id) ON DELETE CASCADE,
    FOREIGN KEY(document_id) REFERENCES documents(document_id)
);

CREATE TABLE IF NOT EXISTS hypotheses (
    hypothesis_id TEXT PRIMARY KEY,
    statement TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'proposed',
    predictions_json TEXT NOT NULL DEFAULT '[]',
    disconfirmers_json TEXT NOT NULL DEFAULT '[]',
    alternatives_json TEXT NOT NULL DEFAULT '[]',
    confidence REAL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS contradictions (
    contradiction_id TEXT PRIMARY KEY,
    proposition_a TEXT NOT NULL,
    proposition_b TEXT NOT NULL,
    source_a_document_id TEXT,
    source_b_document_id TEXT,
    status TEXT NOT NULL DEFAULT 'open',
    ordinary_explanations TEXT,
    assessment TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS leads (
    lead_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'captured',
    documentary_density REAL NOT NULL DEFAULT 0,
    source_independence REAL NOT NULL DEFAULT 0,
    consequence REAL NOT NULL DEFAULT 0,
    testability REAL NOT NULL DEFAULT 0,
    novelty_potential REAL NOT NULL DEFAULT 0,
    alternative_explanation_penalty REAL NOT NULL DEFAULT 0,
    score REAL NOT NULL DEFAULT 0,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS novelty_checks (
    novelty_check_id TEXT PRIMARY KEY,
    subject TEXT NOT NULL,
    surface TEXT NOT NULL,
    query TEXT NOT NULL,
    checked_at TEXT NOT NULL,
    result_summary TEXT,
    relevant_citation TEXT,
    classification TEXT NOT NULL DEFAULT 'novelty_unresolved',
    limitations TEXT
);

CREATE TABLE IF NOT EXISTS runs (
    run_id TEXT PRIMARY KEY,
    command TEXT NOT NULL,
    parameters_json TEXT NOT NULL,
    started_at TEXT NOT NULL,
    finished_at TEXT,
    status TEXT NOT NULL,
    output_json TEXT NOT NULL DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS phase_checkpoints (
    checkpoint_id TEXT PRIMARY KEY,
    phase TEXT NOT NULL,
    objective TEXT NOT NULL,
    decision TEXT NOT NULL,
    summary TEXT NOT NULL,
    deliverables_json TEXT NOT NULL,
    stopping_criteria_json TEXT NOT NULL,
    limitations_json TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""


def connect(db_path: str | Path) -> sqlite3.Connection:
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(db_path: str | Path) -> None:
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with connect(path) as conn:
        conn.executescript(SCHEMA_SQL)
        conn.execute(
            "INSERT INTO schema_info(key, value) VALUES('schema_version', ?) "
            "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
            (str(SCHEMA_VERSION),),
        )
        seed_sources(conn)


def seed_sources(conn: sqlite3.Connection) -> None:
    rows = [
        ("synthetic", "Synthetic acceptance corpus", "direct_import", None, "Testing only"),
        ("local", "Local operator-provided files", "direct_import", None, None),
        ("url", "Direct public URL import", "direct_import", None, None),
        ("nara", "National Archives Catalog API v2", "keyed_api", "https://catalog.archives.gov", None),
        ("osti", "OSTI.GOV API v1", "active_api", "https://www.osti.gov", None),
        ("internet_archive", "Internet Archive", "active_api", "https://archive.org", None),
        ("federal_register", "FederalRegister.gov", "active_api", "https://www.federalregister.gov", None),
        ("courtlistener", "CourtListener", "keyed_api", "https://www.courtlistener.com", None),
        ("agency-reading-room", "Agency reading room direct import", "direct_import", None, None),
    ]
    conn.executemany(
        "INSERT OR IGNORE INTO sources(source_id,name,mode,base_url,notes) VALUES(?,?,?,?,?)",
        rows,
    )


def insert_document(conn: sqlite3.Connection, record: dict[str, Any]) -> bool:
    cur = conn.execute(
        """
        INSERT OR IGNORE INTO documents(
            document_id,sha256,title,source_id,source_url,archive_identifier,local_path,
            media_type,byte_size,retrieved_at,date_created,date_published,date_released,
            classification_marking,ingestion_method,extraction_method,extraction_warning,
            provenance_json,metadata_json
        ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """,
        (
            record["document_id"], record["sha256"], record.get("title"), record.get("source_id"),
            record.get("source_url"), record.get("archive_identifier"), record["local_path"],
            record.get("media_type"), record["byte_size"], record["retrieved_at"],
            record.get("date_created"), record.get("date_published"), record.get("date_released"),
            record.get("classification_marking"), record["ingestion_method"],
            record.get("extraction_method"), record.get("extraction_warning"),
            json.dumps(record.get("provenance", {}), sort_keys=True),
            json.dumps(record.get("metadata", {}), sort_keys=True),
        ),
    )
    return cur.rowcount > 0


def replace_pages(conn: sqlite3.Connection, document_id: str, pages: Iterable[dict[str, Any]]) -> None:
    conn.execute("DELETE FROM page_fts WHERE document_id = ?", (document_id,))
    conn.execute("DELETE FROM pages WHERE document_id = ?", (document_id,))
    for page in pages:
        conn.execute(
            "INSERT INTO pages(document_id,page_number,text,text_sha256,extraction_confidence) VALUES(?,?,?,?,?)",
            (document_id, page["page_number"], page["text"], page["text_sha256"], page.get("extraction_confidence")),
        )
        conn.execute(
            "INSERT INTO page_fts(document_id,page_number,text) VALUES(?,?,?)",
            (document_id, page["page_number"], page["text"]),
        )


def search_pages(conn: sqlite3.Connection, query: str, limit: int = 25) -> list[sqlite3.Row]:
    return list(
        conn.execute(
            """
            SELECT f.document_id, CAST(f.page_number AS INTEGER) AS page_number,
                   snippet(page_fts, 2, '[', ']', ' … ', 24) AS snippet,
                   d.title, d.source_id, d.archive_identifier, d.source_url
            FROM page_fts f
            JOIN documents d ON d.document_id = f.document_id
            WHERE page_fts MATCH ?
            ORDER BY bm25(page_fts)
            LIMIT ?
            """,
            (query, limit),
        )
    )


def corpus_stats(conn: sqlite3.Connection) -> dict[str, int]:
    tables = ["documents", "pages", "entities", "events", "claims", "evidence_links", "hypotheses", "contradictions", "leads", "novelty_checks"]
    return {table: int(conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]) for table in tables}
