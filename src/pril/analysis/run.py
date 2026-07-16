from __future__ import annotations

import csv
import json
from pathlib import Path

from ..db import connect
from ..workspace import Workspace
from .contradictions import contradiction_summary
from .duplicates import near_duplicates
from .graph import build_graph
from .phrases import repeated_phrases
from .redactions import redaction_summary
from .timeline import date_candidates


def write_json(path: Path, value) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, default=str) + "\n", encoding="utf-8")


def run_analysis(workspace: Workspace) -> dict:
    workspace.analysis_dir.mkdir(parents=True, exist_ok=True)
    with connect(workspace.db_path) as conn:
        phrases = repeated_phrases(conn)
        duplicates = near_duplicates(conn)
        redactions = redaction_summary(conn)
        timeline = date_candidates(conn)
        contradictions = contradiction_summary(conn)
        graph = build_graph(conn)
    outputs = {
        "repeated_phrases": phrases,
        "near_duplicates": duplicates,
        "redactions": redactions,
        "timeline_candidates": timeline,
        "contradictions": contradictions,
        "graph": graph,
    }
    for key, value in outputs.items():
        write_json(workspace.analysis_dir / f"{key}.json", value)
    csv_path = workspace.analysis_dir / "timeline_candidates.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["date_text", "document_id", "page_number", "context"])
        writer.writeheader()
        writer.writerows(timeline)
    return {key: len(value) if isinstance(value, list) else (len(value.get("nodes", [])) if key == "graph" else len(value)) for key, value in outputs.items()}
