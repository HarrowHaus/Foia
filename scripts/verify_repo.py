from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "README.md", "AGENTS.md", "pyproject.toml", "configs/project.toml", "configs/sources.toml",
    "docs/00_START_HERE.md", "docs/WORK_MODE_HANDOFF.md", "docs/PROJECT_CHARTER.md",
    "docs/RESEARCH_OPERATING_SYSTEM.md", "docs/EVIDENCE_STANDARD.md", "docs/PHASE_GATES.md",
    "docs/SOURCE_MAP.md", "docs/ACCEPTANCE_TESTS.md", "src/pril/cli.py", "src/pril/db.py",
]


def main() -> int:
    failures = []
    for rel in REQUIRED:
        path = ROOT / rel
        if not path.is_file() or path.stat().st_size == 0:
            failures.append(f"missing or empty: {rel}")
    for schema in (ROOT / "schemas").glob("*.json"):
        try:
            json.loads(schema.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            failures.append(f"invalid JSON schema {schema.name}: {exc}")
    if "clean-slate" not in (ROOT / "AGENTS.md").read_text(encoding="utf-8").lower():
        failures.append("AGENTS.md does not preserve clean-slate boundary")
    if failures:
        print("Repository verification failed:")
        for item in failures:
            print(f"- {item}")
        return 1
    print("Repository verification passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
