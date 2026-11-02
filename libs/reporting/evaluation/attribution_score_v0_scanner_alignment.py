"""attribution_score_v0: ``_scanner_alignment`` body (moved verbatim from ``attribution_score_v0``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping


def _scanner_alignment(selection_authority: Mapping[str, Any], models: list[Mapping[str, Any]], *, facade: Any) -> dict[str, Any]:
    rows = facade._as_rows(selection_authority.get("rows"))
    if not rows:
        return facade._score(facade.INSUFFICIENT, None, ["selection_authority_rows_missing"])
    model_by_trade = {str(row.get("trade_id") or ""): row for row in models}
    row_scores: list[float] = []
    reasons: list[str] = []
    for row in rows:
        trade_id = str(row.get("trade_id") or "")
        selected = str(row.get("selected_symbol") or "")
        raw = str(row.get("raw_scanner_top1") or "")
        post = str(row.get("post_strategy_top1") or "")
        model = facade._mapping(model_by_trade.get(trade_id))
        selection = facade._mapping(model.get("selection"))
        selected_candidate = facade._mapping(selection.get("selected_candidate"))
        rank = facade._num(selection.get("selected_rank") or selected_candidate.get("rank"))
        penalty = 0.0
        if selected and raw and selected != raw:
            penalty += 20.0
            reasons.append(f"{trade_id}:selected_not_raw_top1")
        if selected and post and selected != post:
            penalty += 20.0
            reasons.append(f"{trade_id}:selected_not_post_strategy_top1")
        if rank is not None and rank > 1:
            rank_penalty = min(40.0, (float(rank) - 1.0) * 15.0)
            penalty += rank_penalty
            reasons.append(f"{trade_id}:selected_rank_{int(rank)}")
        if row.get("raw_to_post_changed") is True:
            penalty += 5.0
            reasons.append(f"{trade_id}:raw_to_post_changed")
        row_scores.append(max(0.0, 100.0 - min(100.0, penalty)))
    if not row_scores:
        return facade._score(facade.INSUFFICIENT, None, ["scanner_alignment_rows_unavailable"])
    return facade._score(
        facade.OK,
        facade._clamp_score(sum(row_scores) / len(row_scores)),
        reasons or ["selected_candidates_aligned_with_scanner"],
        {"trade_count": len(row_scores)},
    )
