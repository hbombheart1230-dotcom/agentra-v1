import pytest

from libs.runtime import intraday_monitor_signals as subject


def test_empty_human_chart_entry_setup_is_fresh_and_ordered():
    first, second = subject._empty_human_chart_entry_setup(), subject._empty_human_chart_entry_setup()
    assert list(first)[:4] == ["schema_version", "available", "applied", "mode"]
    first["thresholds"]["min_a_setup_score"] = 0
    assert second["thresholds"]["min_a_setup_score"] == .72


def test_session_gap_context_missing_and_rounded(monkeypatch):
    monkeypatch.setattr(subject, "_current_kst_session_anchor", lambda rows: (None, None, None))
    assert subject._session_gap_context([], 10)["session_context_available"] is False
    monkeypatch.setattr(subject, "_current_kst_session_anchor", lambda rows: (None, 1, None))
    rows = [{"ts": 0, "close": 10}, {"ts": 60, "open": 11, "close": 12}, {"ts": 150, "close": 12}]
    result = subject._session_gap_context(rows, 12)
    assert result["open_gap_pct"] == pytest.approx(.1)
    assert result["minutes_since_session_open"] == 1.5
