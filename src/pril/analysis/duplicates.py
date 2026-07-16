from __future__ import annotations

import difflib
import itertools
import re
import sqlite3


def _normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text[:200_000]


def near_duplicates(conn: sqlite3.Connection, threshold: float = 0.82, max_documents: int = 250):
    rows = list(conn.execute(
        "SELECT d.document_id, d.title, group_concat(p.text, '\n') AS text "
        "FROM documents d LEFT JOIN pages p ON p.document_id=d.document_id "
        "GROUP BY d.document_id ORDER BY d.document_id LIMIT ?",
        (max_documents,),
    ))
    results = []
    for a, b in itertools.combinations(rows, 2):
        ta, tb = _normalize(a["text"] or ""), _normalize(b["text"] or "")
        if not ta or not tb:
            continue
        length_ratio = min(len(ta), len(tb)) / max(len(ta), len(tb))
        if length_ratio < 0.4:
            continue
        ratio = difflib.SequenceMatcher(None, ta, tb, autojunk=True).ratio()
        if ratio >= threshold:
            results.append({
                "document_a": a["document_id"], "title_a": a["title"],
                "document_b": b["document_id"], "title_b": b["title"],
                "similarity": round(ratio, 4),
            })
    return sorted(results, key=lambda x: -x["similarity"])
