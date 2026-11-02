"""scanner_quality: ``build_scanner_quality_review`` body (moved verbatim from ``scanner_quality``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Mapping


def build_scanner_quality_review(
    payloads: list[dict[str, Any]],
    *,
    cost_pct: float,
    slippage_pct: float,
    minute_rows_by_symbol: Mapping[str, list[Mapping[str, Any]]] | None = None,
    facade: Any,
) -> dict[str, Any]:
    rows = facade.pre_strategist_candidate_rows(
        payloads,
        minute_rows_by_symbol=minute_rows_by_symbol,
    )
    return {
        "schema_version": "q9_scanner_quality_review.v1",
        "behavior_effect": "evaluation_only",
        "pre_strategist_universe_available": bool(rows),
        "topk_forward_performance": facade.build_scanner_topk_forward_performance(
            rows,
            cost_pct=cost_pct,
            slippage_pct=slippage_pct,
        ),
        "source_performance": facade.build_scanner_source_performance(
            rows,
            cost_pct=cost_pct,
            slippage_pct=slippage_pct,
        ),
    }
