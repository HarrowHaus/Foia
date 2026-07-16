from __future__ import annotations

from ..net import request
from .base import SearchResult


class FederalRegisterAdapter:
    source_id = "federal_register"
    endpoint = "https://www.federalregister.gov/api/v1/documents.json"

    def search(self, query: str, limit: int = 20) -> list[SearchResult]:
        data = request(self.endpoint, params={
            "conditions[term]": query,
            "per_page": min(limit, 100),
            "order": "newest",
        }).json()
        results = []
        for item in data.get("results", [])[:limit]:
            external_id = str(item.get("document_number") or item.get("slug") or "unknown")
            downloads = [u for u in [item.get("pdf_url"), item.get("raw_text_url")] if u]
            results.append(SearchResult(
                self.source_id, external_id, item.get("title") or external_id,
                url=item.get("html_url"), date=item.get("publication_date"),
                description=item.get("abstract"), downloadable_urls=downloads, metadata=item,
            ))
        return results
