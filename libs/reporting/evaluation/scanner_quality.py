from __future__ import annotations

from collections import defaultdict
from typing import Any, Mapping
import sys

from libs.reporting.q8_evaluation_contract import candidate_day
from libs.reporting.quant_shadow_forward_outcomes import attach_forward_outcomes

from .metrics import performance_metrics
from . import scanner_quality_number as _a47_number
from . import scanner_quality_checkpoint_return as _a47_checkpoint_return
from . import scanner_quality_extract_pre_strategist_candidate_rows as _a47_extract_pre_strategist_candidate_rows
from . import scanner_quality_build_scanner_topk_forward_performance as _a48_build_scanner_topk_forward_performance
from . import scanner_quality_build_scanner_source_performance as _a48_build_scanner_source_performance


TOP_K_VALUES = (1, 3, 5, 10)
SCANNER_HORIZONS = ("+5m", "+15m", "+30m", "EOD")


def _number(value: Any) -> float | None:
    return _a47_number._number(value, facade=sys.modules[__name__])


def _checkpoint_return(row: Mapping[str, Any], horizon: str) -> float | None:
    return _a47_checkpoint_return._checkpoint_return(row, horizon, facade=sys.modules[__name__])


def extract_pre_strategist_candidate_rows(
    payloads: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    return _a47_extract_pre_strategist_candidate_rows.extract_pre_strategist_candidate_rows(payloads, facade=sys.modules[__name__])


def pre_strategist_candidate_rows(
    payloads: list[dict[str, Any]],
    *,
    minute_rows_by_symbol: Mapping[str, list[Mapping[str, Any]]] | None = None,
) -> list[dict[str, Any]]:
    rows = extract_pre_strategist_candidate_rows(payloads)
    if minute_rows_by_symbol is None:
        return attach_forward_outcomes(rows)
    return attach_forward_outcomes(
        rows,
        minute_rows_by_symbol=minute_rows_by_symbol,
    )


def build_scanner_topk_forward_performance(
    rows: list[dict[str, Any]],
    *,
    cost_pct: float,
    slippage_pct: float,
) -> dict[str, Any]:
    return _a48_build_scanner_topk_forward_performance.build_scanner_topk_forward_performance(rows, cost_pct=cost_pct, slippage_pct=slippage_pct, facade=sys.modules[__name__])


def build_scanner_source_performance(
    rows: list[dict[str, Any]],
    *,
    cost_pct: float,
    slippage_pct: float,
) -> dict[str, Any]:
    return _a48_build_scanner_source_performance.build_scanner_source_performance(rows, cost_pct=cost_pct, slippage_pct=slippage_pct, facade=sys.modules[__name__])


def build_scanner_quality_review(
    payloads: list[dict[str, Any]],
    *,
    cost_pct: float,
    slippage_pct: float,
    minute_rows_by_symbol: Mapping[str, list[Mapping[str, Any]]] | None = None,
) -> dict[str, Any]:
    rows = pre_strategist_candidate_rows(
        payloads,
        minute_rows_by_symbol=minute_rows_by_symbol,
    )
    return {
        "schema_version": "q9_scanner_quality_review.v1",
        "behavior_effect": "evaluation_only",
        "pre_strategist_universe_available": bool(rows),
        "topk_forward_performance": build_scanner_topk_forward_performance(
            rows,
            cost_pct=cost_pct,
            slippage_pct=slippage_pct,
        ),
        "source_performance": build_scanner_source_performance(
            rows,
            cost_pct=cost_pct,
            slippage_pct=slippage_pct,
        ),
    }


__all__ = [
    "SCANNER_HORIZONS",
    "TOP_K_VALUES",
    "build_scanner_quality_review",
    "build_scanner_source_performance",
    "build_scanner_topk_forward_performance",
    "pre_strategist_candidate_rows",
]
