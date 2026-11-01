"""RF-033 A18-1: data_provider network boundary, fake-only.

``load_existing_candles``, ``_yf_rows`` and ``merge_capture_into_signal_payload`` are replaced
with in-memory fakes. The real reader, yfinance and any writer are never reached.
"""
from __future__ import annotations

import copy
import importlib

import pytest

dp = importlib.import_module("libs.reporting.baseline_btc_woori_tech.data_provider")
pit = importlib.import_module("libs.reporting.baseline_btc_woori_tech.point_in_time_capture")
contracts = importlib.import_module("libs.reporting.baseline_btc_woori_tech.contracts")
DAY = "2026-04-16"


def test_load_woori_candles_delegates_with_exact_kwargs(monkeypatch, tmp_path):
    calls = []
    rows = [{"ts": 1, "close": 1.0}]

    def fake(**kwargs):
        calls.append(kwargs)
        return {contracts.TARGET_SYMBOL: rows}

    monkeypatch.setattr(dp, "load_existing_candles", fake)
    state_path = tmp_path / "state.json"
    for flag in (False, True):
        out = dp.load_woori_candles(day=DAY, state_path=state_path, allow_fresh_fetch=flag)
        assert out == [{"ts": 1, "close": 1.0}]
    assert calls == [
        {"state_path": state_path, "day": DAY, "symbols": (contracts.TARGET_SYMBOL,),
         "allow_fresh_fetch": flag, "run_id_prefix": "baseline_btc_woori_tech"}
        for flag in (False, True)
    ]
    assert not state_path.exists()
    assert list(tmp_path.iterdir()) == []


def test_load_woori_candles_missing_symbol_returns_empty(monkeypatch, tmp_path):
    monkeypatch.setattr(dp, "load_existing_candles", lambda **k: {})
    assert dp.load_woori_candles(day=DAY, state_path=tmp_path / "s.json") == []


@pytest.fixture
def yf(monkeypatch):
    rec = {"yf": [], "merge": []}

    def fake_yf(ticker, *, day, **kwargs):
        rec["yf"].append((ticker, day, kwargs))
        return []

    def fake_merge(payload, *, day, **kwargs):
        rec["merge"].append((copy.deepcopy(payload), day))
        return {"sources": dict(payload.get("sources") or {}), "available_sources": []}

    monkeypatch.setattr(dp, "_yf_rows", fake_yf)
    monkeypatch.setattr(dp, "_momentum_rows", lambda rows, *, source: [])
    monkeypatch.setattr(pit, "merge_capture_into_signal_payload", fake_merge)
    monkeypatch.setattr(dp, "_DAILY_RESEARCH_CACHE", {})
    return rec


def test_signal_rows_without_research(yf, tmp_path):
    out = dp.load_btc_signal_rows(day=DAY, include_research_context=False)
    assert [c[0] for c in yf["yf"]] == ["BTC-USD", "COIN", "KRW=X"]
    assert out["research_context"]["btc_usd_daily"] == []
    assert out["research_context"]["woori_daily"] == []
    assert out["research_context"]["behavior_effect"] == "observation_only"
    assert len(yf["merge"]) == 1 and yf["merge"][0][1] == DAY
    assert "research_context" not in out["sources"]
    for key in ("orders", "intents"):
        assert key not in out
    assert list(tmp_path.iterdir()) == []


def test_signal_rows_with_research_daily_calls(yf):
    out = dp.load_btc_signal_rows(day=DAY, include_research_context=True)
    assert [c[0] for c in yf["yf"]] == ["BTC-USD", "COIN", "KRW=X", "BTC-USD", contracts.TARGET_TICKER]
    for ticker, day, kwargs in yf["yf"][3:]:
        assert day == DAY
        assert kwargs == {"period": "max", "interval": "1d", "restrict_to_recent_days": False}
    assert yf["yf"][0][2] == {} and yf["yf"][1][2] == {} and yf["yf"][2][2] == {}
    assert out["research_context"]["behavior_effect"] == "observation_only"
    assert "btc_usd_daily" not in out["sources"] and "woori_daily" not in out["sources"]
    assert set(out["sources"]) == {"btc_krw", "btc_usd", "coinbase_proxy"}
