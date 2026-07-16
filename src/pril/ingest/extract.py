from __future__ import annotations

import csv
import io
import json
import mimetypes
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .hashing import sha256_text


@dataclass
class ExtractionResult:
    pages: list[dict[str, Any]]
    method: str
    media_type: str
    metadata: dict[str, Any]
    warning: str | None = None


def _page(number: int, text: str, confidence: float = 1.0) -> dict[str, Any]:
    cleaned = text.replace("\x00", "").strip()
    return {
        "page_number": number,
        "text": cleaned,
        "text_sha256": sha256_text(cleaned),
        "extraction_confidence": confidence,
    }


def extract(path: str | Path) -> ExtractionResult:
    p = Path(path)
    suffix = p.suffix.lower()
    media_type = mimetypes.guess_type(p.name)[0] or "application/octet-stream"
    if suffix == ".pdf":
        return _extract_pdf(p)
    if suffix in {".html", ".htm"}:
        return _extract_html(p)
    if suffix == ".json":
        obj = json.loads(p.read_text(encoding="utf-8", errors="replace"))
        text = json.dumps(obj, indent=2, ensure_ascii=False, sort_keys=True)
        return ExtractionResult([_page(1, text)], "json-normalized", media_type, {})
    if suffix == ".csv":
        raw = p.read_text(encoding="utf-8", errors="replace")
        rows = list(csv.reader(io.StringIO(raw)))
        text = "\n".join(" | ".join(cell for cell in row) for row in rows)
        return ExtractionResult([_page(1, text)], "csv-normalized", media_type, {"rows": len(rows)})
    if suffix in {".txt", ".md", ".rst", ".xml", ".log"}:
        text = p.read_text(encoding="utf-8", errors="replace")
        return ExtractionResult([_page(1, text)], "plain-text", media_type, {})
    try:
        text = p.read_text(encoding="utf-8", errors="strict")
        return ExtractionResult([_page(1, text)], "utf8-fallback", media_type, {}, "Unknown extension decoded as UTF-8")
    except (UnicodeDecodeError, OSError):
        return ExtractionResult([], "none", media_type, {}, "No extractor available for this binary type")


def _extract_pdf(path: Path) -> ExtractionResult:
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise RuntimeError("PDF extraction requires pypdf. Install the project dependencies.") from exc
    reader = PdfReader(str(path))
    pages = []
    empty = 0
    for idx, pdf_page in enumerate(reader.pages, start=1):
        text = pdf_page.extract_text() or ""
        if not text.strip():
            empty += 1
        pages.append(_page(idx, text, 1.0 if text.strip() else 0.0))
    metadata = {str(k): str(v) for k, v in (reader.metadata or {}).items()}
    warning = None
    if empty:
        warning = f"{empty} PDF page(s) produced no text; OCR review may be required"
    return ExtractionResult(pages, "pypdf", "application/pdf", metadata, warning)


def _extract_html(path: Path) -> ExtractionResult:
    raw = path.read_text(encoding="utf-8", errors="replace")
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(raw, "html.parser")
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()
        title = soup.title.get_text(" ", strip=True) if soup.title else None
        text = soup.get_text("\n", strip=True)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return ExtractionResult([_page(1, text)], "beautifulsoup", "text/html", {"html_title": title})
    except ImportError:
        text = re.sub(r"<[^>]+>", " ", raw)
        text = re.sub(r"\s+", " ", text)
        return ExtractionResult([_page(1, text)], "html-regex-fallback", "text/html", {}, "BeautifulSoup not installed")
