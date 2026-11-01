import json
from pathlib import Path
from tempfile import TemporaryDirectory

from scripts.diagnostics import run_m26_closeout_check as closeout
from scripts.diagnostics import run_m26_dataset_manifest_check as manifest


def test_seed_demo_dataset_populated_manifest_golden(monkeypatch):
    monkeypatch.setattr(manifest, "_utc_now_iso", lambda: "2026-02-17T01:02:03+00:00")
    with TemporaryDirectory() as raw:
        root = Path(raw)
        result = manifest._seed_demo_dataset(root)
        payload = json.loads(result.read_text(encoding="utf-8"))
        assert payload == {"schema_version": manifest.SCHEMA_VERSION, "dataset_id": "m26-fixed-demo-v1", "generated_at": "2026-02-17T01:02:03+00:00", "components": manifest.REQUIRED_COMPONENT_FILES}
        assert (root / "market" / "ohlcv_1d.csv").read_text(encoding="utf-8") == "ts,symbol,open,high,low,close,volume\n2026-02-17T00:00:00+00:00,005930,70000,70500,69900,70300,120000\n"
        assert json.loads((root / "execution" / "intents.jsonl").read_text(encoding="utf-8")) == {"ts":"2026-02-17T00:01:00+00:00","intent_id":"demo-intent-1","symbol":"005930","action":"BUY","qty":1}


def test_prepare_candidate_dataset_populated_golden_and_exception():
    with TemporaryDirectory() as raw:
        root = Path(raw)
        (root / "execution").mkdir(); (root / "market").mkdir()
        closeout._prepare_candidate_dataset(root, day="2026-02-17")
        assert json.loads((root / "execution" / "fills.jsonl").read_text().splitlines()[1])["fill_price"] == 115
        assert "005930,100,116,99,115,1000" in (root / "market" / "ohlcv_1d.csv").read_text()
    with TemporaryDirectory() as raw:
        try:
            closeout._prepare_candidate_dataset(Path(raw), day="2026-02-17")
        except FileNotFoundError:
            pass
        else:
            raise AssertionError("original missing-parent exception parity lost")
