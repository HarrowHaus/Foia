from __future__ import annotations

from .db import connect
from .ingest.hashing import sha256_file
from .workspace import Workspace


def audit_workspace(workspace: Workspace) -> dict:
    failures = []
    checked = 0
    with connect(workspace.db_path) as conn:
        integrity = conn.execute("PRAGMA integrity_check").fetchone()[0]
        if integrity != "ok":
            failures.append(f"SQLite integrity_check: {integrity}")
        for row in conn.execute("SELECT document_id,sha256,local_path FROM documents"):
            checked += 1
            path = workspace.root / row["local_path"]
            if not path.is_file():
                failures.append(f"Missing raw file for {row['document_id']}: {path}")
                continue
            actual = sha256_file(path)
            if actual != row["sha256"]:
                failures.append(f"Hash mismatch for {row['document_id']}")
    return {"ok": not failures, "documents_checked": checked, "failures": failures}
