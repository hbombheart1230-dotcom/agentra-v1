from datetime import datetime
from zoneinfo import ZoneInfo

from libs.runtime.quant import shadow_candidates as subject


def test_candidate_context_preserves_factor_fallbacks():
    row = {"symbol": "A", "score": 0, "features": {"cost_floor_state": "met"}}
    assert subject._candidate_context(row)["entry_quant_cost_floor_state"] == "met"


def test_normalize_minute_rows_is_sorted_and_non_mutating():
    raw = [{"ts": 2, "close": 2}, {"ts": 1, "price": 1}, None]
    assert [row["ts"] for row in subject._normalize_minute_rows(raw)] == [1, 2]
    assert raw[0] == {"ts": 2, "close": 2}


def test_market_snapshot_uses_last_same_day_eligible_row():
    tz = ZoneInfo("Asia/Seoul")
    now = int(datetime(2026, 1, 2, 9, 2, tzinfo=tz).timestamp())
    state = {"minute_ohlcv_by_symbol": {"A": [{"ts": now - 60, "close": 10}, {"ts": now + 60, "close": 11}]}}
    assert subject._market_snapshot_for_symbol(state, "A", now_epoch=now)["baseline_price"] == 10.0


def test_opening_probe_window_and_ready_reason():
    assert subject._opening_probe_payload({}, opening_minutes=21)["reason"] == "outside_opening_window"
    row = {"volume_ratio": .8, "vwap_distance": 0, "breakout_ok": True, "cost_adjusted_edge_ok": True}
    assert subject._opening_probe_payload(row, opening_minutes=20)["would_probe"] is True


def test_runner_row_respects_quality_blocks():
    result = subject._runner_row({"symbol": "A", "triggered": True, "runner_up_quality_blocked": True}, {"A": {"symbol": "A"}})
    assert result["would_enter"] is False
    assert result["shadow_role"] == "runner_up_evaluated"


def test_opening_largecap_metric_precedence_and_wrapper_shape():
    row = {"symbol": "A", "features": {"volume_ratio": 1}}
    result = subject._opening_largecap_watchlist_row(row, metric_row={"volume_ratio": 2})
    assert result["volume_ratio"] == 2
    assert result["shadow_role"] == "opening_largecap_watchlist"
