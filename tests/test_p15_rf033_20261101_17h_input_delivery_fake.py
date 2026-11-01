"""RF-033 A17-2: publish_input delivery seam; ``publish`` and the feature builder are faked.

No real storage write, no network.
"""
from __future__ import annotations

import copy
import importlib
from datetime import datetime

import pytest

idv = importlib.import_module("libs.reporting.baseline_btc_woori_tech.input_delivery")
DAY = "2026-04-16"


@pytest.fixture
def rec(monkeypatch):
    r = {"features": [], "publish": []}

    def feats(*, day, candles, btc_signals):
        r["features"].append({"day": day, "candles": copy.deepcopy(candles), "signals": btc_signals})
        return {"fixture": "ok"}

    def pub(path, payload):
        r["publish"].append((path, copy.deepcopy(payload)))

    monkeypatch.setattr(idv, "build_hypothesis_features", feats)
    monkeypatch.setattr(idv, "publish", pub)
    return r


def test_filter_window_and_payload(rec, tmp_path):
    ep = idv.epoch
    now = ep(DAY, "09:05")
    candles = [{"ts": ep(DAY, t)} for t in ("08:59", "09:00", "09:05")] + [
        {"ts": ep(DAY, "09:06")}, {"ts": ep(DAY, "15:31")}]
    signals = {"btc_0855_capture_status": "CAPTURED"}
    snap = copy.deepcopy((candles, signals))

    out = idv.publish_input(day=DAY, reports_root=str(tmp_path), signals=signals,
                            candles=candles, now_epoch=now)

    assert (candles, signals) == snap
    assert len(rec["features"]) == 1
    f = rec["features"][0]
    assert f["day"] == DAY and f["signals"] is signals
    assert [r["ts"] for r in f["candles"]] == [ep(DAY, "09:00"), ep(DAY, "09:05")]
    assert len(rec["publish"]) == 1
    path, payload = rec["publish"][0]
    assert path == tmp_path / "evaluation/baseline_btc_woori_tech" / DAY / "q12_candidate_input.json"
    assert payload == out
    assert out["schema_version"] == "q12_candidate_input.v1"
    assert out["delivery_owner"] == "q12_input_worker"
    assert out["day"] == DAY and out["generated_epoch"] == now
    assert out["candle_latest_epoch"] == now
    assert out["features"] == {"fixture": "ok"}
    assert out["btc_capture_status"] == "CAPTURED"
    assert list(tmp_path.iterdir()) == []  # nothing written to disk


def test_empty_candles(rec, tmp_path):
    out = idv.publish_input(day=DAY, reports_root=str(tmp_path), signals={},
                            candles=[], now_epoch=idv.epoch(DAY, "09:05"))
    assert out["candle_latest_epoch"] is None
    assert rec["features"][0]["candles"] == []
    assert len(rec["publish"]) == 1
    assert datetime.fromisoformat(out["generated_at"]).timestamp() == out["generated_epoch"]
