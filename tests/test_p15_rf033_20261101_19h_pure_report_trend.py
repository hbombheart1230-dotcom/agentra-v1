"""RF-033 A19-1/A19-3: pure Owner functions render_report, build_recent_btc_trend_context, vnext report.

In-memory inputs only; no IO, network or writers.
"""
from __future__ import annotations

import copy
import importlib

rep = importlib.import_module("libs.reporting.baseline_btc_woori_tech.report")
trend = importlib.import_module("libs.reporting.baseline_btc_woori_tech.trend_context")
vrep = importlib.import_module("libs.reporting.baseline_btc_woori_tech.vnext.report")
DAY = "2026-04-16"


def test_t1_render_report_pure_markdown(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    decisions = {"decisions": [], "decision_policy_version": "fixture"}
    forward = {"cost_model": {"round_trip_cost_pct": 0.1, "slippage_pct": 0.05}, "evidence_status": "fixture"}
    comparison = {}
    snap = copy.deepcopy((decisions, forward, comparison))
    out = rep.render_report(day=DAY, decisions=decisions, forward=forward, comparison=comparison)
    assert isinstance(out, str)
    for needle in (DAY, "shadow_only", "OrderIntent / execution: disabled", "fixture"):
        assert needle in out
    assert (decisions, forward, comparison) == snap
    assert list(tmp_path.iterdir()) == []


def test_t2_trend_context_empty_sources():
    ctx = trend.build_recent_btc_trend_context(
        {"sources": {}}, epoch=10000, momentum_15m=None, momentum_60m=None, momentum_24h=None)
    assert ctx["available"] is False
    assert ctx["source_count"] == 0
    assert ctx["state"] == "insufficient_evidence"
    assert ctx["behavior_effect"] == "observation_only"


def test_t3_trend_context_single_source_not_mutated():
    payload = {"sources": {"btc_krw": [{"ts": 9990, "close": 100.0}]}}
    snap = copy.deepcopy(payload)
    ctx = trend.build_recent_btc_trend_context(
        payload, epoch=10000, momentum_15m=None, momentum_60m=None, momentum_24h=None)
    assert payload == snap
    assert ctx["source_count"] == 1
    assert list(ctx["sources"]) == ["btc_krw"]


def test_a193_vnext_aggregate_and_render():
    assert vrep.aggregate([]) == []
    text = vrep.render({"day": DAY, "evidence_status": "fixture", "summary": [], "current_features": {}})
    assert "Q12 vNext Forward Validation" in text
    assert DAY in text
    assert "Shadow only" in text
