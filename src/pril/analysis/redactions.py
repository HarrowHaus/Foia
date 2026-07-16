from __future__ import annotations

import re
import sqlite3

PATTERNS = {
    "literal_redacted": re.compile(r"\bREDACTED\b", re.I),
    "black_blocks": re.compile(r"[█■]{2,}"),
    "foia_exemptions": re.compile(r"\b(?:b\s*\(\s*[1-9]\s*\)|5\s*U\.S\.C\.\s*552)\b", re.I),
    "deleted_markers": re.compile(r"\b(?:DELETED|WITHHELD|EXCISED)\b", re.I),
}


def redaction_summary(conn: sqlite3.Connection):
    results = []
    for row in conn.execute("SELECT document_id, page_number, text FROM pages"):
        counts = {name: len(pattern.findall(row["text"])) for name, pattern in PATTERNS.items()}
        total = sum(counts.values())
        if total:
            results.append({"document_id": row["document_id"], "page_number": row["page_number"], "total": total, "counts": counts})
    return results
