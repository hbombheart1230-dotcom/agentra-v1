from libs.runtime import regime
from libs.runtime import decision_observability as obs


def test_regime_and_observability_owner_facades(monkeypatch):
    assert regime._to_float("2.5") == 2.5
    assert regime._to_float("bad", 3.0) == 3.0
    high = regime.classify_regime_v2(ma20_gap=0.2, volatility20=0.04)
    assert high["regime"] == "high_volatility"
    monkeypatch.setattr(obs, "_to_float", lambda value: -0.0123)
    assert "-0.0123" in obs._reclaim_evidence_explanation(reclaim_blocked=True, reclaim_gate_ok=False, vwap_hold_ok=False, vwap_reclaim_ok=False, reclaim_distance_to_ready="x", reclaim_readiness_tuned=False)
    assert obs._blocker_family(code="volume missing", primary_failure_axis="", guard_blocked=False) == "volume_confirmation"


def test_benchmark_filler_owner_is_synthetic_data_only():
    from scripts.diagnostics import benchmark_operator_visibility_memory as bench
    row = bench._filler_row("2026-01-02", 1)
    assert row["event"] == "ok"
    assert row["payload"]["api_id"] == "ka10080"
