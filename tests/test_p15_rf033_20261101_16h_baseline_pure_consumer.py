"""RF-033 A16-2: pure baseline_btc_woori_tech helpers. In-memory fakes only; no IO/network."""
from __future__ import annotations

import copy

from libs.reporting.baseline_btc_woori_tech import comparison, forward_returns


def test_q1_metric_coercion_and_empty():
    row = {"count": "2", "win_rate": "0.5", "average_return_pct": "1.25",
           "profit_factor": "2", "maximum_drawdown_pct": "-0.5"}
    assert comparison._metric(row) == {
        "trade_count": 2, "win_rate": 0.5, "avg_return_pct": 1.25,
        "profit_factor": 2.0, "max_drawdown_pct": -0.5}
    assert comparison._metric({}) == {
        "trade_count": 0, "win_rate": 0.0, "avg_return_pct": 0.0,
        "profit_factor": 0.0, "max_drawdown_pct": 0.0}


def test_q2_gross_returns_observed_only():
    rows = [
        {"returns": {"5m": {"status": "observed", "return_pct": 1.5}}},
        {"returns": {"5m": {"status": "pending", "return_pct": 8}}},
        {"returns": {"5m": {"status": "observed", "return_pct": None}}},
    ]
    snap = copy.deepcopy(rows)
    assert comparison._gross_returns(rows, "5m") == [1.5, 0.0]
    assert rows == snap


def _run(monkeypatch, policy_id):
    calls = []

    def fake(rows, **kwargs):
        calls.append((copy.deepcopy(rows), rows, kwargs))
        return {"ok": True}

    monkeypatch.setattr(forward_returns, "summarize_forward_returns", fake)
    rows = [{"baseline_decision_id": "a"}, {"baseline_decision_id": "b"}]
    decisions = [{"decision_id": "a", "policy_variants": {"p": {"eligible": True}}},
                 {"decision_id": "b", "policy_variants": {"p": {"eligible": False}}}]
    snap = copy.deepcopy((rows, decisions))
    out = forward_returns.summarize_policy_variant(
        rows, decisions, policy_id=policy_id, cost_pct=0.1, slippage_pct=0.2)
    assert (rows, decisions) == snap
    return out, calls, rows


def test_q3_policy_variant_copies_rows_and_delegates(monkeypatch):
    out, calls, orig_rows = _run(monkeypatch, "p")
    assert out == {"ok": True}
    assert len(calls) == 1
    snapshot, passed, kwargs = calls[0]
    assert kwargs == {"cost_pct": 0.1, "slippage_pct": 0.2}
    assert [r["eligible"] for r in passed] == [True, False]
    assert all(r["policy_variant_id"] == "p" for r in passed)
    assert all(a is not b for a, b in zip(passed, orig_rows))
    assert all("eligible" not in r for r in orig_rows)


def test_q4_unknown_policy_both_ineligible(monkeypatch):
    out, calls, _ = _run(monkeypatch, "unknown")
    assert out == {"ok": True}
    assert [r["eligible"] for r in calls[0][1]] == [False, False]
    assert all(r["policy_variant_id"] == "unknown" for r in calls[0][1])
