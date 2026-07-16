from __future__ import annotations

import mimetypes
import tempfile
import urllib.parse
from pathlib import Path

from ..config import network_config
from ..net import request
from ..workspace import Workspace
from .pipeline import ingest_file


def ingest_url(
    workspace: Workspace,
    url: str,
    *,
    source_id: str = "url",
    archive_identifier: str | None = None,
    title: str | None = None,
) -> dict:
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("Only http and https URLs are supported")
    response = request(url, headers={"Accept": "application/pdf,text/html,text/plain,application/json,*/*"})
    cfg = network_config()
    max_bytes = cfg.max_download_mb * 1024 * 1024
    if len(response.body) > max_bytes:
        raise ValueError(f"Download exceeds configured maximum of {cfg.max_download_mb} MB")
    content_type = response.headers.get("Content-Type", "").split(";", 1)[0].strip()
    suffix = Path(parsed.path).suffix
    if not suffix:
        suffix = mimetypes.guess_extension(content_type) or ".bin"
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp.write(response.body)
        tmp_path = Path(tmp.name)
    try:
        return ingest_file(
            workspace,
            tmp_path,
            source_id=source_id,
            source_url=response.url,
            archive_identifier=archive_identifier,
            title=title,
            ingestion_method="direct-url-download",
            provenance={"http_status": response.status, "response_headers": response.headers},
        )
    finally:
        tmp_path.unlink(missing_ok=True)
