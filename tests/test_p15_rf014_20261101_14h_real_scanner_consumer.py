"""RF-014 A14-R1: REAL ``scanner_node(state)`` consumer with controlled fakes.

Only IO / event / feature-hydration boundaries are faked. ``scanner_node``,
``score_scanner_candidate_row``, the repeat penalty computation and the ranking
overlay are the real production code. Temp dirs only; no network, no orders.
"""
from __future__ import annotations

import copy

import pytest

import graphs.nodes.scanner_node as sn

_FEATURE_KEYS = (
    "return20", "ma20_gap", "ma60_gap", "ma120_gap", "trend_strength", "adx14",
    "volume_spike20", "vwap_distance", "cross_section_rank", "volatility20",
    "signal_score",
)


def _neutral_scanner_features(*symbols):
    return {
        s: {k: (1.0 if k == "volume_spike20" else 0.0) for k in _FEATURE_KEYS}
        for s in symbols
    }


def _flat_candidate_metrics(*symbols):
    return {s: {"change_pct": 0.0, "volume": 1.0, "trading_value": 1.0} for s in symbols}


@pytest.fixture
def calls(monkeypatch):
    c = {k: 0 for k in (
        "record_raw_input", "emit_event", "log_summary", "append_trace",
        "hydrate_features", "hydrate_skill", "asset_filter", "broker_filter",
        "event_logger",
    )}

    def _record_raw_input(*a, **k):
        c["record_raw_input"] += 1

    def _emit(*a, **k):
        c["emit_event"] += 1

    def _log(*a, **k):
        c["log_summary"] += 1

    def _trace(state, *a, **k):
        c["append_trace"] += 1
        return state

    def _hydrate(*, state, candidates, skill_quotes=None, policy=None, refresh_existing=False, **k):
        c["hydrate_features"] += 1
        fm = dict((state or {}).get("scanner_features") or {})
        return fm, "rf014_fake_hydration", []

    def _skill(state, candidates, *a, **k):
        c["hydrate_skill"] += 1
        return state

    def _asset(candidates, *a, **k):
        c["asset_filter"] += 1
        return candidates, {}

    def _broker(candidates, *a, **k):
        c["broker_filter"] += 1
        return candidates, {}

    def _logger(state, *a, **k):
        c["event_logger"] += 1
        return lambda *x, **y: None

    monkeypatch.setattr(sn, "record_raw_input", _record_raw_input)
    monkeypatch.setattr(sn, "_emit_scanner_event", _emit)
    monkeypatch.setattr(sn, "_log_scanner_summary", _log)
    monkeypatch.setattr(sn, "append_decision_trace", _trace)
    monkeypatch.setattr(sn, "hydrate_scanner_feature_map", _hydrate)
    monkeypatch.setattr(sn, "_maybe_hydrate_scanner_skill_results", _skill)
    monkeypatch.setattr(sn, "apply_asset_universe_filter", _asset)
    monkeypatch.setattr(sn, "_filter_mock_broker_restricted_candidates", _broker)
    monkeypatch.setattr(sn, "_make_event_logger", _logger)
    return c


def _two_candidate_state(tmp_path):
    syms = ("AAPL", "MSFT")
    return {
        "run_id": "rf014-a14",
        "now_epoch": 1800000000,
        "persisted_state": {"last_trade_symbol": "AAPL", "last_trade_epoch": 1799999940},
        "portfolio_snapshot": {"positions": []},
        "candidates": list(syms),
        "mock_scan_results": {
            "AAPL": {"score": 0.80, "confidence": 0.9, "risk_score": 0.1},
            "MSFT": {"score": 0.75, "confidence": 0.8, "risk_score": 0.2},
        },
        "commander_decision": {"scanner_policy": {
            "avoid_recent_symbol": True,
            "recent_symbol_penalty": 0.05,
            "reentry_score_gap_threshold": 0.01,
            "allow_same_symbol_reentry": True,
        }},
        "policy": {},
        "scanner_features": _neutral_scanner_features(*syms),
        "mock_candidate_metrics": _flat_candidate_metrics(*syms),
        "reports_root": str(tmp_path / "reports"),
    }


def _assert_no_effects(before, out):
    for key in ("orders", "fills", "intents"):
        assert key not in before
        assert key not in out, key


def test_real_repeat_penalty_drives_selection(tmp_path, calls):
    state = _two_candidate_state(tmp_path)
    before = copy.deepcopy(state)
    out = sn.scanner_node(state)

    assert out["selected"]["symbol"] == "MSFT"
    rows = {str(r["symbol"]): r for r in out["scan_results"]}
    assert float(rows["AAPL"]["score_breakdown"]["repeat_symbol_penalty"]) < 0.0
    assert out["scanner_output"]["reentry_penalty_applied"] is False
    assert calls["hydrate_features"] >= 1
    _assert_no_effects(before, out)


def test_real_risk_snapshot_matches_selected(tmp_path, calls):
    out = sn.scanner_node(_two_candidate_state(tmp_path))
    sel = out["selected"]
    assert out["risk"]["risk_score"] == float(sel["risk_score"])
    assert out["risk"]["confidence"] == float(sel["confidence"])
    assert sel["symbol"] == "MSFT"
    assert out["top_stock"] == sel["symbol"]


def test_real_empty_candidates_risk_is_zero(tmp_path, calls):
    state = _two_candidate_state(tmp_path)
    state.update(candidates=[], mock_scan_results={}, scanner_features={}, mock_candidate_metrics={})
    out = sn.scanner_node(state)
    assert out["risk"]["risk_score"] == 0.0
    assert out["risk"]["confidence"] == 0.0


def test_real_strict_empty_pool_noop(tmp_path, calls):
    state = {
        "run_id": "rf014-a14-strict",
        "now_epoch": 1800000000,
        "persisted_state": {},
        "portfolio_snapshot": {"positions": []},
        "candidates": [],
        "mock_scan_results": {},
        "policy": {},
        "applied_policy": {"scanner": {
            "source": {"type": "kiwoom"},
            "kiwoom": {"strict_only": True, "live_fetch": False},
            "fallback": {"block_static_when_empty": True},
        }},
        "reports_root": str(tmp_path / "reports"),
    }
    before = copy.deepcopy(state)
    out = sn.scanner_node(state)
    assert out.get("top_stock") in ("", None)
    assert out.get("selected") is None
    assert out["scanner_output"]["fallback_reason"] == "kiwoom_candidate_pool_empty_strict_mode"
    _assert_no_effects(before, out)
