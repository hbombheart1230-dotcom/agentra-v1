from __future__ import annotations

from typing import Any, Dict, List, Mapping, Sequence


def _candidate_context(row: Mapping[str, Any], *, facade: Any):
    suitability = facade._as_dict(row.get("tactic_suitability"))
    factor_snapshot = facade._candidate_factor_snapshot(row)
    factors = facade._as_dict(factor_snapshot.get("factors"))
    return {
        "symbol": facade._symbol(row),
        "name": facade._text(row.get("name") or row.get("stock_name") or row.get("symbol_name")),
        "rank": facade._rank(row),
        "score_total": facade._score(row),
        "theme": facade._text(row.get("theme") or row.get("matched_theme") or row.get("theme_name")),
        "quant_tactic_id": facade._text(
            row.get("quant_tactic_id")
            or row.get("tactic_id")
            or factor_snapshot.get("tactic_id")
            or row.get("tactical_strategy")
        ),
        "tactic_suitability_tier": facade._text(
            row.get("tactic_suitability_tier")
            or suitability.get("tier")
        ),
        "tactic_suitability_score": (
            row.get("tactic_suitability_score")
            if row.get("tactic_suitability_score") not in (None, "")
            else suitability.get("score")
        ),
        "entry_quant_cost_floor_state": facade._text(
            row.get("entry_quant_cost_floor_state")
            or row.get("cost_floor_state")
            or factors.get("cost_floor_state")
        ),
    }
