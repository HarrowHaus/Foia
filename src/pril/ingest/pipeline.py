from __future__ import annotations

import datetime as dt
import mimetypes
import shutil
from pathlib import Path
from typing import Any

from ..db import connect, insert_document, replace_pages
from ..ids import document_id
from ..workspace import Workspace
from .extract import extract
from .hashing import sha256_file


def utc_now() -> str:
    return dt.datetime.now(dt.UTC).isoformat()


def ingest_file(
    workspace: Workspace,
    file_path: str | Path,
    *,
    source_id: str = "local",
    source_url: str | None = None,
    archive_identifier: str | None = None,
    title: str | None = None,
    metadata: dict[str, Any] | None = None,
    provenance: dict[str, Any] | None = None,
    ingestion_method: str = "file-copy",
    retrieved_at: str | None = None,
) -> dict[str, Any]:
    src = Path(file_path).expanduser().resolve()
    if not src.is_file():
        raise FileNotFoundError(src)
    digest = sha256_file(src)
    doc_id = document_id(digest)
    destination_dir = workspace.raw_dir / digest[:2]
    destination_dir.mkdir(parents=True, exist_ok=True)
    destination = destination_dir / f"{digest}{src.suffix.lower()}"
    if not destination.exists():
        shutil.copy2(src, destination)
    result = extract(destination)
    record = {
        "document_id": doc_id,
        "sha256": digest,
        "title": title or result.metadata.get("html_title") or src.name,
        "source_id": source_id,
        "source_url": source_url,
        "archive_identifier": archive_identifier,
        "local_path": str(destination.relative_to(workspace.root)),
        "media_type": result.media_type or mimetypes.guess_type(src.name)[0],
        "byte_size": destination.stat().st_size,
        "retrieved_at": retrieved_at or utc_now(),
        "ingestion_method": ingestion_method,
        "extraction_method": result.method,
        "extraction_warning": result.warning,
        "provenance": {
            "original_filename": src.name,
            "source_url": source_url,
            "archive_identifier": archive_identifier,
            **(provenance or {}),
        },
        "metadata": {**result.metadata, **(metadata or {})},
    }
    with connect(workspace.db_path) as conn:
        inserted = insert_document(conn, record)
        if inserted:
            replace_pages(conn, doc_id, result.pages)
        conn.commit()
    return {**record, "inserted": inserted, "pages": len(result.pages)}
