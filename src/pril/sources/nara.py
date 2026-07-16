from __future__ import annotations

import os

from ..net import request
from .base import SearchResult


class NARAAdapter:
    source_id = "nara"
    endpoint = "https://catalog.archives.gov/api/v2/records/search"

    def search(self, query: str, limit: int = 20) -> list[SearchResult]:
        key = os.getenv("NARA_API_KEY")
        if not key:
            raise RuntimeError("NARA_API_KEY is required. Request a key from the National Archives Catalog API team.")
        data = request(
            self.endpoint,
            params={"q": query, "limit": min(limit, 100)},
            headers={"x-api-key": key, "Content-Type": "application/json"},
        ).json()
        hits = data.get("body", {}).get("hits", {}).get("hits", [])
        results = []
        for hit in hits[:limit]:
            source = hit.get("_source", {})
            record = source.get("record", source)
            naid = str(record.get("naId") or hit.get("_id") or "unknown")
            digital_objects = record.get("digitalObjects") or []
            downloads = [obj.get("objectUrl") for obj in digital_objects if obj.get("objectUrl")]
            date = None
            dates = record.get("productionDates") or []
            if dates:
                date = dates[0].get("logicalDate")
            results.append(SearchResult(
                self.source_id, naid, record.get("title") or f"NARA {naid}",
                url=f"https://catalog.archives.gov/id/{naid}", date=date,
                description=record.get("scopeAndContentNote"), downloadable_urls=downloads,
                metadata=record,
            ))
        return results
