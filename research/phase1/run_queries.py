"""Run a Phase 1 query bank through registered adapters with full logging.

Usage: python research/phase1/run_queries.py <workspace> <query_bank.jsonl> <round_tag>

Appends one record per query to <workspace>/ledgers/query_log.jsonl
(including empty results) and writes normalized results to
<workspace>/manifests/<round_tag>_results.jsonl. Requests inherit the
configured user agent, timeout, and inter-request delay from pril.
"""

from __future__ import annotations

import datetime as dt
import json
import sys
import time
from pathlib import Path

from pril.sources.registry import get_adapter

LIMIT = 10


def main() -> int:
    workspace = Path(sys.argv[1])
    bank_path = Path(sys.argv[2])
    round_tag = sys.argv[3]
    query_log = workspace / "ledgers" / "query_log.jsonl"
    manifest = workspace / "manifests" / f"{round_tag}_results.jsonl"

    queries = [
        json.loads(line)
        for line in bank_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    empties = 0
    with query_log.open("a", encoding="utf-8") as qlog, manifest.open(
        "a", encoding="utf-8"
    ) as out:
        for q in queries:
            ts = dt.datetime.now(dt.UTC).isoformat()
            entry = {**q, "round": round_tag, "limit": LIMIT, "executed_at": ts}
            try:
                results = get_adapter(q["source"]).search(q["query"], limit=LIMIT)
                entry["result_count"] = len(results)
                entry["status"] = "ok" if results else "empty"
                empties += 0 if results else 1
                for r in results:
                    out.write(
                        json.dumps(
                            {"query_id": q["query_id"], "round": round_tag, **r.to_dict()},
                            ensure_ascii=False,
                        )
                        + "\n"
                    )
            except Exception as exc:  # noqa: BLE001 - log and continue the bank
                entry["result_count"] = 0
                entry["status"] = f"error: {exc}"
            qlog.write(json.dumps(entry, ensure_ascii=False) + "\n")
            print(f"{q['query_id']} [{q['source']}] {q['query']!r} -> {entry['status']} ({entry['result_count']})")
            time.sleep(1.0)
    print(f"done: {len(queries)} queries, {empties} empty")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
