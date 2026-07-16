from __future__ import annotations

import re
import sqlite3

DATE_PATTERNS = [
    re.compile(r"\b(18|19|20)\d{2}-\d{2}-\d{2}\b"),
    re.compile(r"\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{1,2},\s+(?:18|19|20)\d{2}\b", re.I),
    re.compile(r"\b\d{1,2}\s+(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+(?:18|19|20)\d{2}\b", re.I),
]


def date_candidates(conn: sqlite3.Connection, context_chars: int = 120, limit: int = 5000):
    out = []
    for row in conn.execute("SELECT document_id, page_number, text FROM pages"):
        text = row["text"]
        for pattern in DATE_PATTERNS:
            for match in pattern.finditer(text):
                start = max(0, match.start() - context_chars)
                end = min(len(text), match.end() + context_chars)
                out.append({
                    "document_id": row["document_id"], "page_number": row["page_number"],
                    "date_text": match.group(0), "context": text[start:end].replace("\n", " "),
                })
                if len(out) >= limit:
                    return out
    return out
