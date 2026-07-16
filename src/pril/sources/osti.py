from __future__ import annotations

from ..net import request
from .base import SearchResult


class OSTIAdapter:
    source_id = "osti"
    endpoint = "https://www.osti.gov/api/v1/records"

    def search(self, query: str, limit: int = 20) -> list[SearchResult]:
        data = request(self.endpoint, params={"q": query, "rows": min(limit, 100), "page": 1}).json()
        records = data if isinstance(data, list) else data.get("records", data.get("results", []))
        results = []
        for item in records[:limit]:
            external_id = str(item.get("osti_id") or item.get("id") or item.get("doi") or "unknown")
            title = item.get("title") or item.get("product_title") or f"OSTI record {external_id}"
            url = item.get("product_url") or item.get("fulltext_url") or item.get("url")
            results.append(SearchResult(
                self.source_id, external_id, title, url=url,
                date=item.get("publication_date") or item.get("entry_date"),
                description=item.get("description") or item.get("abstract"),
                downloadable_urls=[u for u in [item.get("fulltext_url")] if u], metadata=item,
            ))
        return results
