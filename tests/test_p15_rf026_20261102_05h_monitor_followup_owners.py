from libs.runtime import intraday_monitor_signals as subject


def test_monitor_evidence_owner():
    out = subject._build_monitor_signal_evidence(reclaim_score=1, volume_score=1, pullback_score=1, breakout_score=1, confidence_score=1, confidence_threshold=1, entry_quality_score=1, breakout_quality_score=1, pullback_quality_score=1, entry_quality_path="x", reclaim_ok=True, volume_ok=True, pullback_ok=True, breakout_ok=True, rebound_ok=True, reclaim_gate_ok=True, breakout_path_ok=True, pullback_volume_path_ok=True, extension_ok=True, too_extended=False, reclaim_strength=1, rebound_strength=1, transition_readiness_score=1, reclaim_distance_to_ready=None, volume_distance_to_ready=None, breakout_distance_to_ready=None)
    assert list(out) == ["scores", "checks", "derived", "weighted_scores"]


def test_candles_owner():
    assert subject._candles_from_rows([{"ts": 1, "close": 2}])


def test_merge_owner():
    assert subject._merge_candle_group([{"ts": 1, "open": 1, "high": 2, "low": 1, "close": 2, "volume": 1}])["close"] == 2


def test_session_vwap_owner():
    assert subject._session_vwap([{"ts": 1, "high": 2, "low": 2, "close": 2, "volume": 1}]) == 2


def test_compress_owner():
    assert subject._compress_candles([{"ts": 1, "close": 2}], timeframe_minutes=1)


def test_spacing_owner():
    assert subject._infer_spacing_seconds([{"ts": 1}, {"ts": 61}, {"ts": 121}, {"ts": 181}]) == 60.0


def test_kst_projection_owner():
    assert subject._kst_session_key_and_minute(0) == (None, None)


def test_current_session_owner():
    assert isinstance(subject._current_kst_session_rows([]), list)
