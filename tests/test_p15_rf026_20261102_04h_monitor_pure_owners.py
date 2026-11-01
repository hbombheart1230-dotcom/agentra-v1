from libs.runtime import intraday_monitor_signals as subject


def test_to_bool_cases():
    assert [subject._to_bool(x) for x in (None, True, "", 0, 1, "yes", "no")] == [False, True, False, False, True, True, False]


def test_min_threshold_and_facade_patch(monkeypatch):
    monkeypatch.setattr(subject, "_clamp_score", lambda value: 9.0)
    assert subject._min_threshold_score(1, 2) == 9.0


def test_range_threshold():
    assert subject._range_threshold_score(2, 1, 3) == 1.0
    assert subject._range_threshold_score(0, 1, 3) == 0.0


def test_entry_quality_tier():
    assert [subject._entry_quality_tier(x) for x in (.64, .65, .8)] == ["weak", "watch", "strong"]


def test_resolve_scoring_settings_order():
    result = subject._resolve_monitor_scoring_settings({"enabled": "yes", "threshold": 0})
    assert list(result) == ["enabled", "shadow_mode", "entry_threshold", "scoring_mode"]


def test_score_breakdown_chart_penalty():
    result = subject._build_monitor_score_breakdown(vwap_reclaim_ok=True, breakout_ok=True, pullback_mature=True, volume_ok=True, confidence_gate_ok=True, chart_structure_features={"human_chart_context": {"available": True, "entry_chart_score": 1, "exit_risk_score": .55, "late_entry_risk": "high"}})
    assert result["chart_exit_risk_penalty"] == -.25


def test_dedupe_non_empty_order():
    assert subject._dedupe_non_empty([None, " a ", "a", "", 1, 1]) == ["a", "1"]


def test_volume_priority_boundaries():
    assert [subject._volume_priority_hint(x) for x in (.74, .75, .76, 1.0)] == ["low", "low", "normal", "high"]
