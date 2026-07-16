from __future__ import annotations

from ..net import request
from .base import SearchResult


class InternetArchiveAdapter:
    source_id = "internet_archive"
    endpoint = "https://archive.org/advancedsearch.php"

    def search(self, query: str, limit: int = 20) -> list[SearchResult]:
        fields = ["identifier", "title", "date", "description", "creator", "collection", "mediatype"]
        data = request(self.endpoint, params={
            "q": query, "fl[]": fields, "rows": min(limit, 100), "page": 1, "output": "json"
        }).json()
        docs = data.get("response", {}).get("docs", [])
        results = []
        for item in docs[:limit]:
            identifier = str(item.get("identifier", "unknown"))
            title = item.get("title") or identifier
            results.append(SearchResult(
                self.source_id, identifier, title,
                url=f"https://archive.org/details/{identifier}",
                date=str(item.get("date")) if item.get("date") else None,
                description=_text(item.get("description")), metadata=item,
            ))
        return results


def _text(value):
    if isinstance(value, list):
        return " | ".join(str(v) for v in value)
    return str(value) if value is not None else None
