from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

from ..db import connect, corpus_stats
from ..ids import new_id
from ..workspace import Workspace


def create_checkpoint(workspace: Workspace, phase: str = "Phase 0", decision: str = "continue") -> Path:
    now = dt.datetime.now(dt.UTC)
    checkpoint_id = new_id("chk")
    with connect(workspace.db_path) as conn:
        stats = corpus_stats(conn)
        warnings = [dict(row) for row in conn.execute(
            "SELECT document_id,title,extraction_warning FROM documents WHERE extraction_warning IS NOT NULL"
        )]
        report = f"""# {phase} Checkpoint

Checkpoint ID: `{checkpoint_id}`  
Created: `{now.isoformat()}`  
Decision: **{decision}**

## Objective

Establish and audit the current research state before any phase transition.

## Corpus statistics

"""
        for key, value in stats.items():
            report += f"- {key}: {value}\n"
        report += "\n## Extraction warnings\n\n"
        if warnings:
            for item in warnings:
                report += f"- `{item['document_id']}` — {item['title']}: {item['extraction_warning']}\n"
        else:
            report += "- None recorded.\n"
        report += """

## Required human/agent assessment

- Strongest current signals:
- Strongest disconfirming evidence:
- Dead ends:
- Source limitations:
- Extraction limitations:
- Novelty status:
- Gate decision rationale:
- Exact next-phase plan:

## Stopping criteria review

Do not advance solely because automated analyses completed. Confirm the phase gate in `docs/PHASE_GATES.md`.
"""
        conn.execute(
            "INSERT INTO phase_checkpoints(checkpoint_id,phase,objective,decision,summary,deliverables_json,stopping_criteria_json,limitations_json) VALUES(?,?,?,?,?,?,?,?)",
            (checkpoint_id, phase, "Audit current research state", decision, "Automated checkpoint scaffold", json.dumps([]), json.dumps([]), json.dumps(warnings)),
        )
        conn.commit()
    path = workspace.reports_dir / f"{now.strftime('%Y%m%dT%H%M%SZ')}_{checkpoint_id}.md"
    path.write_text(report, encoding="utf-8")
    return path
