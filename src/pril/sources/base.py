from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Protocol


@dataclass
class SearchResult:
    source_id: str
    external_id: str
    title: str
    url: str | None = None
    date: str | None = None
    description: str | None = None
    downloadable_urls: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class SourceAdapter(Protocol):
    source_id: str

    def search(self, query: str, limit: int = 20) -> list[SearchResult]: ...
