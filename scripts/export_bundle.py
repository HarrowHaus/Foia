from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT.parent / f"{ROOT.name}-handoff"


def main() -> int:
    archive = shutil.make_archive(str(OUT), "zip", ROOT.parent, ROOT.name)
    print(archive)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
