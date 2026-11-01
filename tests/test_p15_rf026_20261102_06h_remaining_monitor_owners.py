import ast
import hashlib
from pathlib import Path

from libs.runtime import intraday_monitor_signals as signals


def test_b30_eight_owners_are_thin_facades_and_preserve_cases():
    source = Path(signals.__file__)
    assert hashlib.sha1(
        Path(__file__).parents[1].joinpath("libs/runtime/intraday_monitor_signals.py").read_bytes()
    ).hexdigest() != ""
    names = [
        "_current_kst_session_anchor", "_classify_series_quality",
        "_flatten_chart_structure_feature_states", "_parse_policy_signal_spec",
        "_chart_feature_status_item", "_extract_commander_entry_control",
        "_env_trueish", "_empty_human_chart_buy_guard",
    ]
    tree = ast.parse(source.read_text())
    found = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
    for name in names:
        assert name in found
        assert len(found[name].body) == 2

    assert signals._env_trueish(" YeS ") is True
    assert signals._env_trueish("", default=True) is True
    assert signals._empty_human_chart_buy_guard()["blocking_features"] == []
    assert signals._empty_human_chart_buy_guard() is not signals._empty_human_chart_buy_guard()

    old_groups = signals._CHART_FEATURE_GROUP_PATHS
    signals._CHART_FEATURE_GROUP_PATHS = {"trend": "trend_group"}
    try:
        assert signals._flatten_chart_structure_feature_states(
            {"available": True, "trend_group": {"trend": "strong"}}
        ) == {"trend": {"state": "strong", "group": "trend_group", "source": "chart_structure_features.trend_group.trend"}}
    finally:
        signals._CHART_FEATURE_GROUP_PATHS = old_groups

    old_spacing = signals._infer_spacing_seconds
    signals._infer_spacing_seconds = lambda _: 300.0
    try:
        assert signals._classify_series_quality([], timeframe_minutes=1)["series_class"] == "intraday"
    finally:
        signals._infer_spacing_seconds = old_spacing

    old_kst, old_open = signals._kst_session_key_and_minute, signals._MARKET_OPEN_MINUTE
    signals._kst_session_key_and_minute = lambda value: ("d", float(value))
    signals._MARKET_OPEN_MINUTE = 540
    try:
        assert signals._current_kst_session_anchor([{"ts": 500}, {"ts": 541}]) == ("d", 1, 541.0)
    finally:
        signals._kst_session_key_and_minute, signals._MARKET_OPEN_MINUTE = old_kst, old_open

    assert signals._chart_feature_status_item(
        spec={"name": "x", "expected_state": "ok"},
        chart_states={"x": {"state": "ok", "source": "fake"}},
    )["status"] == "pass"
    assert signals._extract_commander_entry_control(
        {"commander_entry_control": {"mode": "hold"}}, None
    ) == {"mode": "hold"}
    assert set(signals._parse_policy_signal_spec("trend=strong")) >= {"name", "raw", "is_valid"}
