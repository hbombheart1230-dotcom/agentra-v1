from __future__ import annotations

import sys
from collections import defaultdict
from collections import Counter
from statistics import median
from typing import Any, Iterable, Mapping

from libs.reporting.evaluation.metrics import performance_metrics

from . import analysis_blocked_opportunity_analysis as _a25_blocked_opportunity_analysis
from . import analysis_actual_trade_analysis as _a25_actual_trade_analysis
from . import analysis_summarize_rows as _a25_summarize_rows
from . import analysis_discovery_cohorts as _a25_discovery_cohorts
from . import analysis_score_component_diagnostics as _a25_score_component_diagnostics
from . import analysis_grouped_horizon_summary as _a25_grouped_horizon_summary
from . import analysis_split_summary as _a25_split_summary
from . import analysis_simulate_path_policies as _a25_simulate_path_policies
from .contracts import HORIZONS, LIVE_COST_PCT, PATH_POLICIES, PRIMARY_HORIZON


def _observed_return(row: Mapping[str, Any], horizon: str) -> float | None:
    checkpoints = row.get("checkpoints") if isinstance(row.get("checkpoints"), Mapping) else {}
    checkpoint = checkpoints.get(horizon)
    if not isinstance(checkpoint, Mapping) or checkpoint.get("status") != "observed":
        return None
    return float(checkpoint.get("live_net_return_pct") or 0.0)


def summarize_rows(rows: list[Mapping[str, Any]], horizon: str) -> dict[str, Any]:
    return _a25_summarize_rows.summarize_rows(rows=rows, horizon=horizon, facade=sys.modules[__name__])


def grouped_horizon_summary(
    episodes: list[Mapping[str, Any]],
    *,
    field: str,
) -> dict[str, Any]:
    return _a25_grouped_horizon_summary.grouped_horizon_summary(episodes=episodes, field=field, facade=sys.modules[__name__])


def split_summary(
    episodes: list[Mapping[str, Any]],
    *,
    field: str,
    calibration_end: str,
    retrospective_start: str,
) -> dict[str, Any]:
    return _a25_split_summary.split_summary(episodes=episodes, field=field, calibration_end=calibration_end, retrospective_start=retrospective_start, facade=sys.modules[__name__])


def score_component_diagnostics(episodes: list[Mapping[str, Any]]) -> dict[str, Any]:
    return _a25_score_component_diagnostics.score_component_diagnostics(episodes=episodes, facade=sys.modules[__name__])


def discovery_cohorts(episodes: list[Mapping[str, Any]]) -> dict[str, Any]:
    return _a25_discovery_cohorts.discovery_cohorts(episodes=episodes, facade=sys.modules[__name__])


def blocked_opportunity_analysis(samples: list[Mapping[str, Any]]) -> dict[str, Any]:
    return _a25_blocked_opportunity_analysis.blocked_opportunity_analysis(samples=samples, facade=sys.modules[__name__])


def simulate_path_policies(
    episodes: list[Mapping[str, Any]],
    *,
    minute_rows_by_symbol: Mapping[str, list[Mapping[str, Any]]],
) -> dict[str, Any]:
    return _a25_simulate_path_policies.simulate_path_policies(episodes=episodes, minute_rows_by_symbol=minute_rows_by_symbol, facade=sys.modules[__name__])


def actual_trade_analysis(rows: list[Mapping[str, Any]]) -> dict[str, Any]:
    return _a25_actual_trade_analysis.actual_trade_analysis(rows=rows, facade=sys.modules[__name__])
