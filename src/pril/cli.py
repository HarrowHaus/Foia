from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .analysis.run import run_analysis
from .audit import audit_workspace
from .db import connect, corpus_stats, search_pages
from .doctor import doctor_report
from .ingest.download import ingest_url
from .ingest.pipeline import ingest_file
from .reports.checkpoint import create_checkpoint
from .sources.registry import SOURCE_STATUS, get_adapter
from .workspace import Workspace, init_workspace


def print_json(value) -> None:
    print(json.dumps(value, indent=2, ensure_ascii=False, default=str))


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="pril", description="Public-Record Inference Lab")
    sub = p.add_subparsers(dest="command", required=True)
    sub.add_parser("doctor")

    sp = sub.add_parser("init")
    sp.add_argument("workspace")

    sub.add_parser("source-list")
    sp = sub.add_parser("source-search")
    sp.add_argument("source")
    sp.add_argument("query")
    sp.add_argument("--limit", type=int, default=20)

    sp = sub.add_parser("ingest-file")
    sp.add_argument("workspace")
    sp.add_argument("file")
    _metadata_args(sp)

    sp = sub.add_parser("ingest-url")
    sp.add_argument("workspace")
    sp.add_argument("url")
    _metadata_args(sp)

    sp = sub.add_parser("search")
    sp.add_argument("workspace")
    sp.add_argument("query")
    sp.add_argument("--limit", type=int, default=25)

    for name in ["stats", "analyze", "checkpoint", "audit"]:
        sp = sub.add_parser(name)
        sp.add_argument("workspace")
    return p


def _metadata_args(sp):
    sp.add_argument("--source-id", default=None)
    sp.add_argument("--source-url", default=None)
    sp.add_argument("--archive-id", default=None)
    sp.add_argument("--title", default=None)


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.command == "doctor":
            report = doctor_report()
            print_json(report)
            return 0 if report["fts5"] else 2
        if args.command == "init":
            ws = init_workspace(args.workspace)
            print_json({"workspace": str(ws.root), "database": str(ws.db_path)})
            return 0
        if args.command == "source-list":
            print_json([{"source_id": a, "mode": b, "status": c} for a, b, c in SOURCE_STATUS])
            return 0
        if args.command == "source-search":
            results = get_adapter(args.source).search(args.query, args.limit)
            print_json([r.to_dict() for r in results])
            return 0
        ws = Workspace(Path(args.workspace).expanduser().resolve())
        if not ws.db_path.exists():
            raise FileNotFoundError(f"Workspace is not initialized: {ws.root}")
        if args.command == "ingest-file":
            print_json(ingest_file(ws, args.file, source_id=args.source_id or "local", source_url=args.source_url, archive_identifier=args.archive_id, title=args.title))
        elif args.command == "ingest-url":
            print_json(ingest_url(ws, args.url, source_id=args.source_id or "url", archive_identifier=args.archive_id, title=args.title))
        elif args.command == "search":
            with connect(ws.db_path) as conn:
                print_json([dict(row) for row in search_pages(conn, args.query, args.limit)])
        elif args.command == "stats":
            with connect(ws.db_path) as conn:
                print_json(corpus_stats(conn))
        elif args.command == "analyze":
            print_json(run_analysis(ws))
        elif args.command == "checkpoint":
            print_json({"checkpoint": str(create_checkpoint(ws))})
        elif args.command == "audit":
            report = audit_workspace(ws)
            print_json(report)
            return 0 if report["ok"] else 3
        return 0
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
