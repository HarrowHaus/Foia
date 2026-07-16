from __future__ import annotations

import os

from ..net import request
from .base import SearchResult


class CourtListenerAdapter:
    source_id = "courtlistener"
    endpoint = "https://www.courtlistener.com/api/rest/v3/search/"

    def search(self, query: str, limit: int = 20) -> list[SearchResult]:
        token = os.getenv("COURTLISTENER_TOKEN")
        if not token:
            raise RuntimeError("COURTLISTENER_TOKEN is required for this adapter")
        data = request(
            self.endpoint,
            params={"q": query, "page_size": min(limit, 20)},
            headers={"Authorization": f"Token {token}"},
        ).json()
        results = []
        for item in data.get("results", [])[:limit]:
            external_id = str(item.get("id") or item.get("cluster_id") or "unknown")
            absolute = item.get("absolute_url")
            url = f"https://www.courtlistener.com{absolute}" if absolute and absolute.startswith("/") else absolute
            results.append(SearchResult(
                self.source_id, external_id,
                item.get("caseName") or item.get("case_name") or item.get("description") or external_id,
                url=url, date=item.get("dateFiled") or item.get("date_filed"),
                description=item.get("snippet") or item.get("text"), metadata=item,
            ))
        return results
