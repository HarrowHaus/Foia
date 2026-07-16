from __future__ import annotations

import sqlite3


def build_graph(conn: sqlite3.Connection) -> dict:
    nodes = []
    edges = []
    for row in conn.execute("SELECT entity_id, canonical_name, entity_type, status FROM entities"):
        nodes.append({"id": row["entity_id"], "label": row["canonical_name"], "type": row["entity_type"], "status": row["status"]})
    for row in conn.execute("SELECT DISTINCT entity_id, document_id FROM mentions"):
        doc_node = f"document:{row['document_id']}"
        if not any(n["id"] == doc_node for n in nodes):
            nodes.append({"id": doc_node, "label": row["document_id"], "type": "document"})
        edges.append({"source": row["entity_id"], "target": doc_node, "type": "mentioned_in"})
    for row in conn.execute("SELECT claim_id, statement, epistemic_class FROM claims"):
        nodes.append({"id": row["claim_id"], "label": row["statement"], "type": "claim", "epistemic_class": row["epistemic_class"]})
    for row in conn.execute("SELECT claim_id, document_id, relationship FROM evidence_links"):
        doc_node = f"document:{row['document_id']}"
        if not any(n["id"] == doc_node for n in nodes):
            nodes.append({"id": doc_node, "label": row["document_id"], "type": "document"})
        edges.append({"source": row["claim_id"], "target": doc_node, "type": row["relationship"]})
    return {"nodes": nodes, "edges": edges}
