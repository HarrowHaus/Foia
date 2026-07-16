from __future__ import annotations

from .courtlistener import CourtListenerAdapter
from .federal_register import FederalRegisterAdapter
from .internet_archive import InternetArchiveAdapter
from .nara import NARAAdapter
from .osti import OSTIAdapter

ADAPTERS = {
    "osti": OSTIAdapter(),
    "internet_archive": InternetArchiveAdapter(),
    "federal_register": FederalRegisterAdapter(),
    "nara": NARAAdapter(),
    "courtlistener": CourtListenerAdapter(),
}

SOURCE_STATUS = [
    ("osti", "active_api", "implemented"),
    ("internet_archive", "active_api", "implemented"),
    ("federal_register", "active_api", "implemented"),
    ("nara", "keyed_api", "implemented; NARA_API_KEY required"),
    ("courtlistener", "keyed_api", "implemented; COURTLISTENER_TOKEN required"),
    ("govinfo", "keyed_api", "planned; verify current search contract"),
    ("congress", "keyed_api", "planned; verify current search contract"),
    ("cia_reading_room", "direct_import", "manual discovery + exact record import"),
    ("fbi_vault", "direct_import", "manual discovery + exact record import"),
    ("nsa_foia", "direct_import", "manual discovery + exact record import"),
    ("frus", "direct_import", "manual discovery + exact record import"),
]


def get_adapter(source_id: str):
    try:
        return ADAPTERS[source_id]
    except KeyError as exc:
        raise KeyError(f"No active adapter for {source_id!r}") from exc
