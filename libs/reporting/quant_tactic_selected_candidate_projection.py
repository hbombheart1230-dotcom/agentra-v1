"""quant_tactic_report projections (moved verbatim from quant_tactic_report).

Module globals and helpers are resolved on ``facade`` (the quant_tactic_report module) at call time; this module never imports it.
"""
from __future__ import annotations

from typing import Any, Dict, List, Mapping


def _selected_candidate_row(report: Mapping[str, Any], symbol: str, *, facade: Any) -> Dict[str, Any]:
    target = str(symbol or "").strip()
    if not target:
        return {}
    candidates: List[Dict[str, Any]] = []
    for item in facade._nested_dicts(report):
        if facade._candidate_symbol(item) != target:
            continue
        if any(
            key in item
            for key in (
                "quant_factor_snapshot",
                "tactic_suitability",
                "scanner_chart_fit_score",
                "scanner_chart_fit_components",
                "score_total",
                "confidence",
            )
        ):
            candidates.append(dict(item))
    if not candidates:
        return {}

    def score(row: Mapping[str, Any]) -> tuple[int, int]:
        has_quant = 1 if facade._mapping(row.get("quant_factor_snapshot")) else 0
        has_suitability = 1 if facade._mapping(row.get("tactic_suitability")) else 0
        has_chart = 1 if row.get("scanner_chart_fit_score") not in (None, "") else 0
        # Prefer final/fallback candidates over top-pick snapshots when labels exist.
        final_hint = 1 if str(row.get("final_selected_symbol") or row.get("selected_symbol") or row.get("entry_final_symbol") or "") == target else 0
        return (has_quant + has_suitability + has_chart + final_hint, len(row))

    candidates.sort(key=score, reverse=True)
    return candidates[0]
