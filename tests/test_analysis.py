from pathlib import Path

from pril.analysis.run import run_analysis
from pril.ingest.pipeline import ingest_file
from pril.workspace import init_workspace


def test_analysis_outputs(tmp_path: Path):
    ws = init_workspace(tmp_path / "workspace")
    phrase = "the transfer ledger was routed through the north annex office"
    a = tmp_path / "a.txt"
    b = tmp_path / "b.txt"
    a.write_text(f"Memo 1968-04-11. {phrase}. REDACTED.", encoding="utf-8")
    b.write_text(f"Memo April 12, 1968. {phrase}. WITHHELD.", encoding="utf-8")
    ingest_file(ws, a, source_id="synthetic")
    ingest_file(ws, b, source_id="synthetic")
    result = run_analysis(ws)
    assert result["repeated_phrases"] >= 1
    assert result["redactions"] >= 2
    assert (ws.analysis_dir / "timeline_candidates.csv").is_file()
