"""scanner_alignment_root_cause: ``build_scanner_alignment_root_cause_range`` body (moved verbatim from ``scanner_alignment_root_cause``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any


def build_scanner_alignment_root_cause_range(
    *,
    reports_root: Path = Path("reports"),
    start: str,
    end: str,
    facade: Any,
) -> dict[str, Any]:
    from datetime import date, timedelta

    reports_root = facade.Path(reports_root)
    cursor = date.fromisoformat(start)
    final = date.fromisoformat(end)
    daily_payloads: list[dict[str, Any]] = []
    while cursor <= final:
        day = cursor.isoformat()
        selection_authority = facade._read_json(
            reports_root / "evaluation" / "daily" / day / "selection_authority_audit.json"
        )
        models, evaluations = facade._load_day_models_and_evaluations(reports_root, day)
        if selection_authority or models or evaluations:
            daily_payloads.append(
                facade.build_scanner_alignment_root_cause_report(
                    day=day,
                    models=models,
                    evaluations=evaluations,
                    selection_authority=selection_authority,
                )
            )
        cursor += timedelta(days=1)

    all_rows = [row for payload in daily_payloads for row in payload.get("rows") or []]
    grouped: dict[str, list[dict[str, Any]]] = facade.defaultdict(list)
    for row in all_rows:
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
    return {
        "schema_version": "scanner_alignment_root_cause_range.v1",
        "evaluation_program_id": "Q14_SCANNER_ALIGNMENT_ROOT_CAUSE_RANGE",
        "behavior_effect": "observation_only",
        "start": start,
        "end": end,
        "day_count": len(daily_payloads),
        "trade_count": len(all_rows),
        "cause_summary": cause_summary,
        "largest_root_cause": largest,
        "largest_observed_root_cause": largest,
        "largest_behavior_root_cause": largest_behavior,
        "largest_structural_root_cause": largest_structural,
        "outcome_conditioned_causes": sorted(facade.OUTCOME_CONDITIONED_CAUSES),
        "measurement_contract_version": "q14_structural_causality.v2",
        "q15_behavior_patch_candidate": facade._patch_candidate(str(largest_structural.get("root_cause") or "")),
        "daily_rows": [
            {
                "day": payload.get("day"),
                "trade_count": payload.get("trade_count"),
                "largest_root_cause": facade._mapping(payload.get("largest_root_cause")).get("root_cause") or "",
            }
            for payload in daily_payloads
        ],
        "rows": all_rows,
        "interpretation_rule": (
            "Range aggregate for Q14. Outcome-conditioned labels are descriptive only. "
            "Use largest_structural_root_cause and independent Q9 forward evidence before "
            "choosing a behavior candidate."
        ),
    }
