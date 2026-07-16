from __future__ import annotations

import uuid


def document_id(sha256_hex: str) -> str:
    if len(sha256_hex) != 64:
        raise ValueError("sha256_hex must contain 64 hexadecimal characters")
    return f"doc_{sha256_hex[:24]}"


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex}"
