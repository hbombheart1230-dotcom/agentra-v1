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


def test_target_day_events_owner_is_ordered_synthetic_data():
    from scripts.diagnostics import benchmark_operator_visibility_memory as bench
    rows = bench._target_day_events_for_run("2026-01-02", 3, 0)
    assert len(rows) == 7
    assert rows[2]["payload"]["decision_packet"]["intent"]["action"] == "BUY"
    assert rows[-1]["payload"]["allowed"] is False


def test_build_feature_map_owner_preserves_tied_rank_and_context_facade(monkeypatch):
    from libs.runtime import feature_engine

    calls = []

    def fake_build_feature_row(rows, **kwargs):
        symbol = rows[0]["symbol"]
        calls.append((symbol, kwargs))
        return {
            "signal_score": 0.25,
            "return20": 0.1 if symbol == "BBB" else 0.3,
            "volatility20": 0.02 if symbol == "BBB" else 0.04,
        }

    monkeypatch.setattr(feature_engine, "build_feature_row", fake_build_feature_row)
    source = {
        " BBB ": [{"symbol": "BBB"}],
        "AAA": [{"symbol": "AAA"}],
        "": [{"symbol": "ignored-empty"}],
        "BAD": "not-a-list",
        "EMPTY": [],
    }
    result = feature_engine.build_feature_map(
        source,
        context={
            "global_sentiment": "0.4",
            "market_breadth": "0.6",
            "index_trend": "0.2",
            "realized_volatility": "0.03",
        },
    )

    assert list(result) == ["BBB", "AAA"]
    assert result["BBB"]["cross_section_rank"] == 0.0
    assert result["AAA"]["cross_section_rank"] == 1.0
    assert result["BBB"]["relative_strength20"] == -0.1
    assert round(result["AAA"]["relative_strength20"], 2) == 0.1
    assert result["BBB"]["volatility_percentile"] == 0.0
    assert result["AAA"]["volatility_percentile"] == 1.0
    assert result["BBB"]["market_breadth"] == 1.0
    assert [symbol for symbol, _kwargs in calls] == ["BBB", "AAA"]
    assert calls[0][1]["realized_vol"] == calls[0][1]["realized_volatility"] == 0.03
    assert feature_engine.build_feature_map({}) == {}


def test_human_chart_detail_context_owner_uses_facade_projection_helpers(monkeypatch):
    from libs.runtime import intraday_monitor_signals as signals

    empty = {"available": False, "notes": []}
    monkeypatch.setattr(signals, "_empty_human_chart_detail_context", lambda: empty)
    no_candles = signals._build_human_chart_detail_context(
        [], current_close=10.0, current_vwap=9.8, recent_high=10.0,
        breakout_level=10.1, volume_ratio=1.2,
    )
    assert no_candles is empty
    assert no_candles["notes"] == ["minute_candles_unavailable"]

    calls = []
    original_clamp = signals._clamp_score

    def tracked_clamp(value):
        calls.append(value)
        return original_clamp(value)

    monkeypatch.setattr(signals, "_clamp_score", tracked_clamp)
    candles = [
        {"open": 10.0, "high": 10.8, "low": 9.8, "close": 10.5, "volume": 120, "vwap": 10.2},
        {"open": 10.2, "high": 10.6, "low": 10.0, "close": 10.4, "volume": 110, "vwap": 10.25},
        {"open": 10.3, "high": 10.7, "low": 10.1, "close": 10.5, "volume": 105, "vwap": 10.3},
        {"open": 10.4, "high": 10.7, "low": 10.2, "close": 10.6, "volume": 100, "vwap": 10.35},
        {"open": 10.5, "high": 10.9, "low": 10.3, "close": 10.7, "volume": 130, "vwap": 10.4},
    ]
    result = signals._build_human_chart_detail_context(
        candles, current_close=10.7, current_vwap=10.4, recent_high=10.9,
        breakout_level=10.6, volume_ratio=1.3,
    )
    assert result["available"] is True
    assert result["observed"]["explicit_vwap_count"] == 5
    assert result["observed"]["volume_presence_ratio"] == 1.0
    assert result["observed"]["vwap_source"] == "explicit_bar_vwap"
    assert calls
