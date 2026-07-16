from __future__ import annotations

import sqlite3


def contradiction_summary(conn: sqlite3.Connection):
    explicit = [dict(row) for row in conn.execute("SELECT * FROM contradictions ORDER BY created_at")]
    mixed_claims = [dict(row) for row in conn.execute(
        """
        SELECT c.claim_id, c.statement,
               SUM(CASE WHEN e.relationship='supports' THEN 1 ELSE 0 END) AS supports,
               SUM(CASE WHEN e.relationship='contradicts' THEN 1 ELSE 0 END) AS contradicts
        FROM claims c JOIN evidence_links e ON e.claim_id=c.claim_id
        GROUP BY c.claim_id
        HAVING supports > 0 AND contradicts > 0
        """
    )]
    return {"explicit": explicit, "claims_with_mixed_evidence": mixed_claims}
