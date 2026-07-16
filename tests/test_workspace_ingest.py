from pathlib import Path

from pril.db import connect, corpus_stats, search_pages
from pril.ingest.pipeline import ingest_file
from pril.workspace import init_workspace


def test_workspace_and_duplicate_ingest(tmp_path: Path):
    ws = init_workspace(tmp_path / "workspace")
    source = tmp_path / "memo.txt"
    source.write_text("A meeting occurred at the North Annex on 1968-04-11.", encoding="utf-8")
    first = ingest_file(ws, source, source_id="synthetic")
    second = ingest_file(ws, source, source_id="synthetic")
    assert first["document_id"] == second["document_id"]
    assert first["inserted"] is True
    assert second["inserted"] is False
    with connect(ws.db_path) as conn:
        stats = corpus_stats(conn)
        assert stats["documents"] == 1
        assert stats["pages"] == 1
        hits = search_pages(conn, '"North Annex"')
        assert len(hits) == 1
