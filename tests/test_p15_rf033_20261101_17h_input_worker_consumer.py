"""RF-033 A17-1: real InputWorker.tick -> publish_input call seam, fake-only.

All four collaborators are replaced on the imported module with in-memory fakes.
``load_woori_candles`` (allow_fresh_fetch=True, a potential network effect) is
NEVER executed: only its call boundary is recorded (G1_NETWORK_BOUNDARY_HOLD).
"""
from __future__ import annotations

import importlib

import pytest

iw = importlib.import_module("libs.reporting.baseline_btc_woori_tech.input_worker")
DAY = "2026-04-16"
RESEARCH = {"research_context": {"btc_usd_daily": [{"x": 1}], "woori_daily": [{"x": 2}]}}
SENTINEL = object()
CANDLES = [{"ts": 1, "close": 10.0}]


@pytest.fixture
def rec(monkeypatch):
    r = {"merge": [], "research": [], "candles": [], "publish": [], "capture": "CAPTURED",
         "research_raises": False}

    def merge(payload, *, day, **k):
        r["merge"].append((dict(payload), day))
        return {"btc_0855_capture_status": r["capture"]}

    def research(*, day):
        r["research"].append(day)
        if r["research_raises"]:
            raise RuntimeError("fake research failure")
        return RESEARCH

    def candles(*, day, state_path, allow_fresh_fetch):
        r["candles"].append({"day": day, "state_path": state_path, "allow_fresh_fetch": allow_fresh_fetch})
        return CANDLES

    def publish(**kw):
        r["publish"].append(kw)
        return SENTINEL

    monkeypatch.setattr(iw, "merge_capture_into_signal_payload", merge)
    monkeypatch.setattr(iw, "load_btc_signal_rows", research)
    monkeypatch.setattr(iw, "load_woori_candles", candles)
    monkeypatch.setattr(iw, "publish_input", publish)
    return r


def test_w1_before_open_no_candle_load(rec, tmp_path):
    now = iw.epoch(DAY, "08:59")
    w = iw.InputWorker(DAY, str(tmp_path / "reports"), tmp_path / "state.json")
    assert w.tick(now) is SENTINEL
    assert len(rec["candles"]) == 0 and len(rec["publish"]) == 1
    kw = rec["publish"][0]
    assert kw["candles"] == [] and kw["now_epoch"] == now and kw["day"] == DAY
    assert kw["signals"]["research_context"] == RESEARCH["research_context"]
    assert kw["signals"]["btc_0855_capture_status"] == "CAPTURED"


def test_w2_after_open_candle_boundary_and_research_cached(rec, tmp_path):
    now = iw.epoch(DAY, "09:01")
    state_path = tmp_path / "state.json"
    w = iw.InputWorker(DAY, str(tmp_path / "reports"), state_path)
    assert w.tick(now) is SENTINEL
    assert rec["candles"] == [{"day": DAY, "state_path": state_path, "allow_fresh_fetch": True}]
    kw = rec["publish"][0]
    assert kw["candles"] is CANDLES and kw["now_epoch"] == now
    assert kw["signals"]["research_context"] == RESEARCH["research_context"]
    w.tick(now + 15)
    assert len(rec["research"]) == 1  # cached, not re-fetched
    assert len(rec["publish"]) == 2 and len(rec["candles"]) == 2


def test_w3_capture_missing_and_research_failure(rec, tmp_path):
    rec["capture"] = "MISSING"
    rec["research_raises"] = True
    w = iw.InputWorker(DAY, str(tmp_path / "reports"), tmp_path / "state.json")
    assert w.tick(iw.epoch(DAY, "09:01")) is SENTINEL
    assert len(rec["candles"]) == 0
    kw = rec["publish"][0]
    assert kw["candles"] == []
    assert kw["signals"]["research_context"] == {}
    assert kw["signals"]["btc_0855_capture_status"] == "MISSING"
    assert "orders" not in kw["signals"] and "intents" not in kw["signals"]
