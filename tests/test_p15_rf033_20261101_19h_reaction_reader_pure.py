"""RF-033 A19-2: reaction_reader load_index_timeline (tmp files) and _stock_reaction (in-memory).

``_collector_raw_row`` (protected Q10 collector) is never called.
"""
from __future__ import annotations

import copy
import importlib
import json

rr = importlib.import_module("libs.reporting.baseline_samsung_hynix.forward_validation.reaction_reader")
DAY = "2026-04-16"


def _macro(path, current):
    path.write_text(json.dumps({"generated_at": "2026-04-16T09:30:00+09:00",
                                "korea_indices": {"indices": {"KOSPI": {"current": current}}}}),
                    encoding="utf-8")


def test_r1_index_timeline_dedup_and_malformed(tmp_path):
    d = tmp_path / DAY
    d.mkdir()
    _macro(d / "a_macro_indicators.json", 100)
    _macro(d / "b_macro_indicators.json", 101)
    (d / "c_macro_indicators.json").write_text("{not json", encoding="utf-8")
    rows = rr.load_index_timeline(day=DAY, macro_root=tmp_path, index_name="KOSPI")
    assert len(rows) == 1
    assert rows[0]["close"] == 101.0
    assert str(rows[0]["source_path"]).startswith(str(tmp_path))
    assert rows[0]["source_path"].endswith("b_macro_indicators.json")
    assert rr.load_index_timeline(day=DAY, macro_root=tmp_path, index_name="MISSING") == []


def _rows():
    ep = rr._checkpoint_epoch
    return [{"ts": ep(DAY, "09:00"), "open": 100.0, "close": 100.0, "high": 101.0, "low": 99.0, "volume": 10},
            {"ts": ep(DAY, "09:30"), "open": 101.0, "close": 102.0, "high": 103.0, "low": 100.0, "volume": 10}]


def test_r2_integrity_failure_close_pending(monkeypatch):
    rows = _rows()
    snap = copy.deepcopy(rows)

    def override(label):
        if label == "CLOSE":
            return {"integrity_failure": True, "reason": "fixture", "collector_status": "CORRUPT_STATE"}
        return None

    out = rr._stock_reaction(day=DAY, target={"symbol": "X"}, rows=rows, previous_close=100.0,
                             collector_override=override)
    close = out["points"]["CLOSE"]
    assert close["status"] == "PENDING"
    assert close["integrity_failure"] is True
    assert close["integrity_reason"] == "fixture"
    assert close["collector_status"] == "CORRUPT_STATE"
    assert close["price"] is None
    assert out["points"]["09:00"]["status"] == "OBSERVED"
    assert rows == snap


def test_r3_absent_override_no_integrity_key():
    out = rr._stock_reaction(day=DAY, target={"symbol": "X"}, rows=_rows(), previous_close=100.0,
                             collector_override=lambda label: None)
    close = out["points"]["CLOSE"]
    assert close["status"] == "PENDING"
    assert "integrity_failure" not in close
    assert out["evidence_status"] == "AVAILABLE"
