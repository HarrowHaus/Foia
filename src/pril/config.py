from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class NetworkConfig:
    user_agent: str
    timeout_seconds: float
    max_download_mb: int
    request_delay_seconds: float


def network_config() -> NetworkConfig:
    return NetworkConfig(
        user_agent=os.getenv(
            "PRIL_USER_AGENT",
            "PublicRecordInferenceLab/0.1 (set PRIL_USER_AGENT with research contact)",
        ),
        timeout_seconds=float(os.getenv("PRIL_HTTP_TIMEOUT", "30")),
        max_download_mb=int(os.getenv("PRIL_MAX_DOWNLOAD_MB", "250")),
        request_delay_seconds=float(os.getenv("PRIL_REQUEST_DELAY_SECONDS", "1.0")),
    )
