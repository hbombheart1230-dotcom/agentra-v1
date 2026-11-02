"""scanner_alignment_root_cause: ``build_scanner_alignment_root_cause_report`` body (moved verbatim from ``scanner_alignment_root_cause``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Mapping, Sequence


def build_scanner_alignment_root_cause_report(
    *,
    day: str,
    models: Sequence[Mapping[str, Any]],
    evaluations: Sequence[Mapping[str, Any]],
    selection_authority: Mapping[str, Any],
    facade: Any,
) -> dict[str, Any]:
    model_by_trade = {str(model.get("trade_id") or ""): model for model in models}
    evaluation_by_trade = {str(row.get("trade_id") or ""): row for row in evaluations}
    rows: list[dict[str, Any]] = []
    for row in facade._rows(selection_authority.get("rows")):
        trade_id = str(row.get("trade_id") or "")
        model = facade._mapping(model_by_trade.get(trade_id))
        evaluation = facade._mapping(evaluation_by_trade.get(trade_id))
        net_return = facade._outcome_return(evaluation, model)
        classification = facade.classify_scanner_alignment_root_cause(
            row=row,
            model=model,
            net_return_pct=net_return,
        )
        rows.append(
            {
                "trade_id": trade_id,
                "symbol": row.get("executed_symbol") or row.get("symbol"),
                "raw_scanner_top1": row.get("raw_scanner_top1"),
                "post_strategy_top1": row.get("post_strategy_top1"),
                "selected_symbol": row.get("selected_symbol"),
                "executed_symbol": row.get("executed_symbol"),
                "net_return_pct": net_return,
                "root_cause": classification["root_cause"],
                "diagnostic_kind": facade._diagnostic_kind(classification["root_cause"]),
                "causal_eligible": facade._diagnostic_kind(classification["root_cause"]) == "structural",
                "confidence": classification["confidence"],
                "selected_rank": classification["selected_rank"],
                "score_gap": classification["score_gap"],
                "reasons": classification["reasons"],
            }
        )

    grouped: dict[str, list[dict[str, Any]]] = facade.defaultdict(list)
    for row in rows:
        grouped[str(row.get("root_cause") or "Missing Evidence")].append(row)

    cause_summary: list[dict[str, Any]] = []
    for cause in facade.ROOT_CAUSES:
        cause_rows = grouped.get(cause, [])
        returns = [
            float(row["net_return_pct"])
            for row in cause_rows
            if row.get("net_return_pct") is not None
        ]
        metrics = facade.performance_metrics(returns)
        cause_summary.append(
            {
                "root_cause": cause,
                "diagnostic_kind": facade._diagnostic_kind(cause),
                "causal_eligible": facade._diagnostic_kind(cause) == "structural",
                "trade_count": len(cause_rows),
                "return_observation_count": len(returns),
                "win_rate": metrics["win_rate"],
                "avg_return_pct": metrics["average_return_pct"],
                "profit_factor": metrics["profit_factor"],
                "max_drawdown_pct": metrics["maximum_drawdown_pct"],
                "negative_impact_pct": facade._impact_score(returns),
            }
        )

    largest = facade._largest_cause(cause_summary)
    largest_behavior = facade._largest_cause(
        cause_summary,
        excluded={"Missing Evidence", "Aligned / No Alignment Issue"},
    )
    largest_structural = facade._largest_cause(
        cause_summary,
        excluded=facade.OUTCOME_CONDITIONED_CAUSES | facade.EVIDENCE_GAP_CAUSES,
    )
    patch_candidate = facade._patch_candidate(str(largest_structural.get("root_cause") or ""))

    return {
        "schema_version": "scanner_alignment_root_cause.v1",
        "measurement_contract_version": "q14_structural_causality.v2",
        "evaluation_program_id": "Q14_SCANNER_ALIGNMENT_ROOT_CAUSE",
        "behavior_effect": "observation_only",
        "day": day,
        "trade_count": len(rows),
        "cause_summary": cause_summary,
        "largest_root_cause": largest,
        "largest_observed_root_cause": largest,
        "largest_behavior_root_cause": largest_behavior,
        "largest_structural_root_cause": largest_structural,
        "outcome_conditioned_causes": sorted(facade.OUTCOME_CONDITIONED_CAUSES),
        "q15_behavior_patch_candidate": patch_candidate,
        "rows": rows,
        "interpretation_rule": (
            "Q14 explains why scanner_alignment_score is low. It does not authorize behavior changes. "
            "Scanner Ranking Failure and Aligned / No Alignment Issue are outcome-conditioned labels, "
            "not independent causal proof. Structural behavior candidates must use "
            "largest_structural_root_cause plus Q9 forward evidence."
        ),
    }
