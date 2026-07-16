from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .db import init_db


@dataclass(frozen=True)
class Workspace:
    root: Path

    @property
    def db_path(self) -> Path:
        return self.root / "pril.sqlite3"

    @property
    def raw_dir(self) -> Path:
        return self.root / "raw"

    @property
    def reports_dir(self) -> Path:
        return self.root / "reports"

    @property
    def analysis_dir(self) -> Path:
        return self.root / "analysis"

    @property
    def logs_dir(self) -> Path:
        return self.root / "logs"


def init_workspace(path: str | Path) -> Workspace:
    root = Path(path).expanduser().resolve()
    for name in (
        "raw",
        "extracted",
        "ledgers",
        "manifests",
        "analysis",
        "reports",
        "logs",
        "exports",
    ):
        (root / name).mkdir(parents=True, exist_ok=True)
    project_file = root / "PROJECT.md"
    if not project_file.exists():
        project_file.write_text(
            "# Investigation Workspace\n\n"
            "Status: clean-slate / Phase 0\n\n"
            "Do not add a preferred theory before broad source and signal discovery.\n",
            encoding="utf-8",
        )
    ledgers = {
        "claims.jsonl": "",
        "hypotheses.jsonl": "",
        "entities.jsonl": "",
        "events.jsonl": "",
        "contradictions.jsonl": "",
        "novelty_checks.jsonl": "",
        "research_tasks.jsonl": "",
        "query_log.jsonl": "",
        "dead_ends.jsonl": "",
    }
    for name, initial in ledgers.items():
        p = root / "ledgers" / name
        if not p.exists():
            p.write_text(initial, encoding="utf-8")
    init_db(root / "pril.sqlite3")
    return Workspace(root)
