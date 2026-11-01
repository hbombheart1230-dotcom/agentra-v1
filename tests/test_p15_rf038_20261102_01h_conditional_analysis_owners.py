import ast
import copy
from pathlib import Path

from libs.research.conditional_alpha_diagnosis import analysis


ROWS = [
    {"trade_id": "a", "day": "2026-01-01", "symbol": "AAA", "strategy_horizon": "5m", "playbook": "p", "exit_reason": "hard_stop", "holding_seconds": 30, "selected_rank": 1, "chart_fit_score": .5, "scanner_score": 1., "risk_score": .3, "actual_live_net_return_pct": -1., "net_return_30m_pct": 3., "return_5m_pct": 1., "return_15m_pct": 2., "return_60m_pct": 1., "return_eod_pct": 1., "opening_relative_volume": 1., "decision_from_open_sec": 20, "above_vwap": True, "rank1_prev5m_observations": 1, "precompleted_return_1m_pct": 1, "source_class": "scanner", "strategist_scenario": "s", "scenario_returns": {"actual_exit": {"live_net_return_pct": -1}, "hold": {"live_net_return_pct": 2}}},
    {"trade_id": "b", "day": "2026-01-02", "symbol": "BBB", "strategy_horizon": "15m", "playbook": "q", "exit_reason": "other", "holding_seconds": 600, "selected_rank": 2, "actual_live_net_return_pct": 1., "net_return_30m_pct": -1., "return_5m_pct": -1., "return_15m_pct": -1., "return_60m_pct": -1., "return_eod_pct": -1., "opening_relative_volume": 2., "decision_from_open_sec": 400, "source_class": "manual", "strategist_scenario": "t", "scenario_returns": {"actual_exit": {"live_net_return_pct": 1}, "hold": {"live_net_return_pct": -1}}},
]


def test_rf038_source_is_thin_facade_wrappers():
    tree = ast.parse(Path(analysis.__file__).read_text())
    targets = {"horizon_cross_sections", "predefined_opening_screens", "precursor_profiles", "opening_archetype_analysis", "actual_live_cost_cross_sections", "research_candidates", "_group_summary", "horizon_reversals"}
    found = {node.name: node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name in targets}
    assert found.keys() == targets
    for node in found.values():
        assert any(isinstance(item, ast.ImportFrom) for item in node.body)
        assert any(isinstance(item, ast.Return) for item in node.body)
        assert len(node.body) <= 3


def test_rf038_horizon_and_cost_owners():
    rows = copy.deepcopy(ROWS)
    reversals, _ = analysis.horizon_reversals(rows, {})
    assert analysis.horizon_cross_sections(reversals)
    assert analysis.actual_live_cost_cross_sections(rows)


def test_rf038_predefined_and_precursor_owners():
    rows = copy.deepcopy(ROWS)
    assert len(analysis.predefined_opening_screens(rows)) == 50
    assert analysis.precursor_profiles(rows)["STRONG_30M"]["count"] == 1


def test_rf038_archetype_and_group_summary_owners():
    rows = copy.deepcopy(ROWS)
    assert analysis.opening_archetype_analysis(rows)["IMMEDIATE_0_1M"]["strong_30m_count"] == 1
    assert analysis._group_summary(rows, "net_return_30m_pct")["count"] == 2


def test_rf038_research_candidates_owner():
    candidates = analysis.research_candidates([{"point_in_time_eligible": True, "value": "x", "evidence_status": "SCREENABLE", "average_pct": 1, "profit_factor": 2, "positive_day_rate": .6, "average_without_top3_pct": .1, "count": 2}])
    assert candidates[0]["value"] == "x"


def test_rf038_horizon_reversals_owner():
    result, summary = analysis.horizon_reversals(copy.deepcopy(ROWS), {"a": {"day": "fallback"}})
    assert result[0]["loss_to_win"] is True
    assert "hold" in summary


def test_rf038_wrappers_preserve_call_time_facade(monkeypatch):
    monkeypatch.setattr(analysis, "number", lambda value: 7 if value == "sentinel" else None)
    assert analysis.research_candidates([]) == []


def test_rf038_empty_inputs_are_safe():
    assert analysis.actual_live_cost_cross_sections([]) == []
    assert analysis.opening_archetype_analysis([]) == {}
4443bc57f07e51945f2b833a478f3ca931b3e8d9
