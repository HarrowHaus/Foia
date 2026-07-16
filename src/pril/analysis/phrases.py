from __future__ import annotations

import collections
import re
import sqlite3
from collections.abc import Iterable

WORD_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9'./-]*")


def ngrams(text: str, n: int) -> Iterable[str]:
    words = [w.lower() for w in WORD_RE.findall(text)]
    for i in range(0, max(0, len(words) - n + 1)):
        yield " ".join(words[i : i + n])


def repeated_phrases(conn: sqlite3.Connection, n: int = 9, min_documents: int = 2, limit: int = 100):
    phrase_docs: dict[str, set[str]] = collections.defaultdict(set)
    for row in conn.execute("SELECT document_id, text FROM pages"):
        unique = set(ngrams(row["text"], n))
        for phrase in unique:
            phrase_docs[phrase].add(row["document_id"])
    ranked = [
        {"phrase": phrase, "document_count": len(docs), "document_ids": sorted(docs)}
        for phrase, docs in phrase_docs.items()
        if len(docs) >= min_documents
    ]
    ranked.sort(key=lambda item: (-item["document_count"], item["phrase"]))
    return ranked[:limit]
