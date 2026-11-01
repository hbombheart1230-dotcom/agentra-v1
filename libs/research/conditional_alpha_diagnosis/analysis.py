from __future__ import annotations

from collections import Counter, defaultdict
import sys
from typing import Any, Callable, Mapping

from .metrics import evidence_profile, evidence_status, number, performance, positive_day_rate

HORIZONS = {
    "5m": "return_5m_pct",
    "15m": "return_15m_pct",
    "30m": "net_return_30m_pct",
    "60m": "return_60m_pct",
    "EOD": "return_eod_pct",
}


def _bucket(value: Any, cuts: tuple[float, ...], labels: tuple[str, ...]) -> str:
    observed = number(value)
    if observed is None:
        return "MISSING"
    for cut, label in zip(cuts, labels):
        if observed < cut:
            return label
    return labels[-1]


def _decision_bucket(row: Mapping[str, Any]) -> str:
    seconds = number(row.get("decision_from_open_sec"))
    if seconds is None:
        return "MISSING"
    if seconds < 300:
        return "09:00-09:04"
    if seconds < 600:
        return "09:05-09:09"
    if seconds < 900:
        return "09:10-09:14"
    return "09:15-09:19"


def _market_bucket(row: Mapping[str, Any]) -> str:
    kospi = number(row.get("kospi_pct"))
    sentiment = number(row.get("global_sentiment_score"))
    if kospi is not None:
        if kospi <= -1.5:
            return "SHARP_RISK_OFF"
        if kospi < -0.3:
            return "RISK_OFF"
        if kospi >= 1.0:
            return "RISK_ON"
        return "NEUTRAL"
    if sentiment is not None:
        if sentiment <= -0.35:
            return "RISK_OFF_PROXY"
        if sentiment >= 0.35:
            return "RISK_ON_PROXY"
        return "NEUTRAL_PROXY"
    return "MISSING"


DIMENSIONS: dict[str, Callable[[Mapping[str, Any]], str]] = {
    "decision_time": _decision_bucket,
    "source_class": lambda row: str(row.get("source_class") or "MISSING"),
    "tactic": lambda row: str(row.get("tactic_id") or "MISSING"),
    "playbook": lambda row: str(row.get("playbook") or "MISSING"),
    "scenario": lambda row: str(row.get("strategist_scenario") or "MISSING"),
    "path_type": lambda row: str(row.get("path_type") or "MISSING"),
    "price_arc": lambda row: str(row.get("price_arc") or "MISSING"),
    "above_vwap": lambda row: str(row.get("above_vwap") if row.get("above_vwap") is not None else "MISSING"),
    "market_regime": lambda row: str(row.get("engine_regime") or "MISSING"),
    "market_state": _market_bucket,
    "opening_gap": lambda row: _bucket(row.get("opening_gap_pct"), (-2, 0, 2, 5), ("<-2%", "-2~0%", "0~2%", "2~5%", ">=5%")),
    "entry_extension": lambda row: _bucket(row.get("entry_vs_prior_close_pct"), (0, 2, 5, 10), ("<0%", "0~2%", "2~5%", "5~10%", ">=10%")),
    "relative_volume": lambda row: _bucket(row.get("opening_relative_volume"), (1, 1.5, 2, 4), ("<1x", "1~1.5x", "1.5~2x", "2~4x", ">=4x")),
    "scanner_score": lambda row: _bucket(row.get("scanner_score"), (0.5, 0.75, 1.0, 1.25), ("<0.50", "0.50~0.75", "0.75~1.00", "1.00~1.25", ">=1.25")),
    "risk_score": lambda row: _bucket(row.get("risk_score"), (0.4, 0.7), ("LOW", "MEDIUM", "HIGH")),
    "chart_fit": lambda row: _bucket(row.get("scanner_chart_fit_score"), (0.35, 0.65), ("LOW", "MEDIUM", "HIGH")),
    "macro_chart_fit": lambda row: _bucket(row.get("scanner_macro_chart_fit_score"), (0.35, 0.65), ("LOW", "MEDIUM", "HIGH")),
}

OUTCOME_DERIVED_DIMENSIONS = {"path_type", "price_arc"}


def _group_summary(rows: list[dict[str, Any]], field: str) -> dict[str, Any]:
    from . import analysis_group_summary as _owner
    return _owner._group_summary(rows, field, facade=sys.modules[__name__])


def opening_cross_sections(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for dimension, resolver in DIMENSIONS.items():
        grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for row in rows:
            grouped[resolver(row)].append(row)
        for value, group in sorted(grouped.items()):
            for horizon, field in HORIZONS.items():
                summary = _group_summary(group, field)
                output.append(
                    {
                        "dimension": dimension,
                        "value": value,
                        "horizon": horizon,
                        "point_in_time_eligible": dimension not in OUTCOME_DERIVED_DIMENSIONS,
                        **summary,
                    }
                )
    return output


def themes_cross_sections(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        themes = row.get("themes")
        if isinstance(themes, list):
            for theme in {str(item) for item in themes if str(item)}:
                grouped[theme].append(row)
    result = []
    for theme, group in sorted(grouped.items()):
        for horizon, field in HORIZONS.items():
            result.append(
                {
                    "dimension": "theme",
                    "value": theme,
                    "horizon": horizon,
                    "point_in_time_eligible": True,
                    **_group_summary(group, field),
                }
            )
    return result


def research_candidates(cross_sections: list[dict[str, Any]]) -> list[dict[str, Any]]:
    from . import analysis_research_candidates as _owner
    return _owner.research_candidates(cross_sections, facade=sys.modules[__name__])


def predefined_opening_screens(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    from . import analysis_predefined_opening_screens as _owner
    return _owner.predefined_opening_screens(rows, facade=sys.modules[__name__])


def _scenario_value(row: Mapping[str, Any], scenario: str) -> float | None:
    scenarios = row.get("scenario_returns")
    scenarios = scenarios if isinstance(scenarios, Mapping) else {}
    payload = scenarios.get(scenario)
    payload = payload if isinstance(payload, Mapping) else {}
    return number(payload.get("live_net_return_pct"))


def horizon_reversals(
    horizon_rows: list[dict[str, Any]], contexts: Mapping[str, Mapping[str, Any]]
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    from . import analysis_horizon_reversals as _owner
    return _owner.horizon_reversals(horizon_rows, contexts, facade=sys.modules[__name__])


def _holding_bucket(value: Any) -> str:
    seconds = number(value)
    if seconds is None:
        return "MISSING"
    if seconds < 60:
        return "<1m"
    if seconds < 300:
        return "1~5m"
    if seconds < 900:
        return "5~15m"
    if seconds < 1800:
        return "15~30m"
    return ">=30m"


def _exit_class(value: Any) -> str:
    text = str(value or "").lower()
    for key in ("hard_stop", "stop_loss", "trend_breakdown", "vwap_breakdown", "intraday_low_break", "eod_flat"):
        if key in text:
            return key
    if "reconciled" in text:
        return "broker_reconciled"
    return "other"


def horizon_cross_sections(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    from . import analysis_horizon_cross_sections as _owner
    return _owner.horizon_cross_sections(rows, facade=sys.modules[__name__])


def actual_live_cost_cross_sections(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    from . import analysis_actual_live_cost_cross_sections as _owner
    return _owner.actual_live_cost_cross_sections(rows, facade=sys.modules[__name__])


def delayed_reactivation(events: list[dict[str, Any]]) -> dict[str, Any]:
    labels: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in events:
        labels[str(row.get("selection_horizon_label") or "MISSING")].append(row)
    return {
        label: {
            "count": len(group),
            "30m": performance(row.get("net_return_30m_pct") for row in group),
            "same_day_close": performance(row.get("same_day_close_net_pct") for row in group),
            "d1_close": performance(row.get("d1_close_net_pct") for row in group),
            "d5_close": performance(row.get("d5_close_net_pct") for row in group),
            "d5_high": performance(row.get("d5_max_high_net_pct") for row in group),
            "playbooks": dict(sorted(Counter(str(row.get("playbook") or "MISSING") for row in group).items())),
            "scenarios": dict(sorted(Counter(str(row.get("strategist_scenario") or "MISSING") for row in group).items())),
        }
        for label, group in sorted(labels.items())
    }


def casebook(opening_rows: list[dict[str, Any]], horizon_rows: list[dict[str, Any]], events: list[dict[str, Any]]) -> dict[str, Any]:
    valid = [row for row in opening_rows if number(row.get("net_return_30m_pct")) is not None]
    winners = sorted(valid, key=lambda row: number(row.get("net_return_30m_pct")) or -999, reverse=True)[:15]
    losers = sorted(valid, key=lambda row: number(row.get("net_return_30m_pct")) or 999)[:15]
    reversals = sorted(
        [row for row in horizon_rows if row.get("loss_to_win")],
        key=lambda row: number((row.get("best_alternative") or {}).get("delta_vs_actual_pct")) or -999,
        reverse=True,
    )[:20]
    delayed = sorted(
        [row for row in events if row.get("delayed_high_opportunity")],
        key=lambda row: number(row.get("d5_max_high_net_pct")) or -999,
        reverse=True,
    )[:20]
    return {"opening_winners": winners, "opening_losers": losers, "hold_loss_to_win": reversals, "delayed_reactivation": delayed}


def precursor_profiles(rows: list[dict[str, Any]]) -> dict[str, Any]:
    from . import analysis_precursor_profiles as _owner
    return _owner.precursor_profiles(rows, facade=sys.modules[__name__])


def _archetype(row: Mapping[str, Any]) -> str:
    kospi = number(row.get("kospi_pct"))
    extension = number(row.get("entry_vs_prior_close_pct"))
    seconds = number(row.get("decision_from_open_sec"))
    if (kospi is not None and kospi <= -3) or (
        extension is not None and extension <= -8
    ):
        return "DISLOCATION_REBOUND"
    if seconds is not None and seconds < 60:
        return "IMMEDIATE_0_1M"
    if seconds is not None and seconds < 300:
        return "EARLY_1_5M"
    if seconds is not None and seconds < 1200:
        return "MATURED_5_20M"
    return "OTHER"


def opening_archetype_analysis(rows: list[dict[str, Any]]) -> dict[str, Any]:
    from . import analysis_opening_archetype_analysis as _owner
    return _owner.opening_archetype_analysis(rows, facade=sys.modules[__name__])


def _mean(rows: list[dict[str, Any]], field: str) -> float | None:
    values = [value for row in rows if (value := number(row.get(field))) is not None]
    return round(sum(values) / len(values), 4) if values else None
