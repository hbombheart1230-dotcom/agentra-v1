from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any, Mapping, Sequence
import sys

from .metrics import performance_metrics
from . import scanner_alignment_root_cause_mapping as _a49_sca_mapping
from . import scanner_alignment_root_cause_rows as _a49_sca_rows
from . import scanner_alignment_root_cause_num as _a49_sca_num
from . import scanner_alignment_root_cause_symbol as _a50_symbol
from . import scanner_alignment_root_cause_selected_rank as _a50_selected_rank
from . import scanner_alignment_root_cause_score_gap as _a50_score_gap
from . import scanner_alignment_root_cause_outcome_return as _a50_outcome_return
from . import scanner_alignment_root_cause_impact_score as _a50_impact_score
from . import scanner_alignment_root_cause_diagnostic_kind as _a50_diagnostic_kind
from . import scanner_alignment_root_cause_largest_cause as _a50_largest_cause
from . import scanner_alignment_root_cause_patch_candidate as _a50_patch_candidate
from . import scanner_alignment_root_cause_classify as _a53_classify
from . import scanner_alignment_root_cause_render as _a53_render


ROOT_CAUSES = (
    "Scanner Ranking Failure",
    "Rank Drift",
    "Strategist Override",
    "Candidate Filtering",
    "Symbol Mapping",
    "Missing Evidence",
    "Aligned / No Alignment Issue",
)

OUTCOME_CONDITIONED_CAUSES = {
    "Scanner Ranking Failure",
    "Aligned / No Alignment Issue",
}

EVIDENCE_GAP_CAUSES = {"Missing Evidence"}


def _mapping(value: Any) -> Mapping[str, Any]:
    return _a49_sca_mapping._mapping(value, facade=sys.modules[__name__])


def _rows(value: Any) -> list[Mapping[str, Any]]:
    return _a49_sca_rows._rows(value, facade=sys.modules[__name__])


def _num(value: Any) -> float | None:
    return _a49_sca_num._num(value, facade=sys.modules[__name__])


def _symbol(value: Any) -> str:
    return _a50_symbol._symbol(value, facade=sys.modules[__name__])


def _read_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        return payload if isinstance(payload, dict) else {}
    except Exception:
        return {}


def _selected_rank(model: Mapping[str, Any]) -> int | None:
    return _a50_selected_rank._selected_rank(model, facade=sys.modules[__name__])


def _score_gap(model: Mapping[str, Any]) -> float | None:
    return _a50_score_gap._score_gap(model, facade=sys.modules[__name__])


def _outcome_return(evaluation: Mapping[str, Any], model: Mapping[str, Any]) -> float | None:
    return _a50_outcome_return._outcome_return(evaluation, model, facade=sys.modules[__name__])


def classify_scanner_alignment_root_cause(
    *,
    row: Mapping[str, Any],
    model: Mapping[str, Any],
    net_return_pct: float | None,
) -> dict[str, Any]:
    return _a53_classify.classify_scanner_alignment_root_cause(row=row, model=model, net_return_pct=net_return_pct, facade=sys.modules[__name__])


def _impact_score(returns: list[float]) -> float:
    return _a50_impact_score._impact_score(returns, facade=sys.modules[__name__])


def _diagnostic_kind(cause: str) -> str:
    return _a50_diagnostic_kind._diagnostic_kind(cause, facade=sys.modules[__name__])


def _largest_cause(
    cause_summary: Sequence[Mapping[str, Any]],
    *,
    excluded: set[str] | None = None,
) -> dict[str, Any]:
    return _a50_largest_cause._largest_cause(cause_summary, excluded=excluded, facade=sys.modules[__name__])


def _patch_candidate(cause: str) -> str:
    return _a50_patch_candidate._patch_candidate(cause, facade=sys.modules[__name__])


def build_scanner_alignment_root_cause_report(
    *,
    day: str,
    models: Sequence[Mapping[str, Any]],
    evaluations: Sequence[Mapping[str, Any]],
    selection_authority: Mapping[str, Any],
) -> dict[str, Any]:
    model_by_trade = {str(model.get("trade_id") or ""): model for model in models}
    evaluation_by_trade = {str(row.get("trade_id") or ""): row for row in evaluations}
    rows: list[dict[str, Any]] = []
    for row in _rows(selection_authority.get("rows")):
        trade_id = str(row.get("trade_id") or "")
        model = _mapping(model_by_trade.get(trade_id))
        evaluation = _mapping(evaluation_by_trade.get(trade_id))
        net_return = _outcome_return(evaluation, model)
        classification = classify_scanner_alignment_root_cause(
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
                "diagnostic_kind": _diagnostic_kind(classification["root_cause"]),
                "causal_eligible": _diagnostic_kind(classification["root_cause"]) == "structural",
                "confidence": classification["confidence"],
                "selected_rank": classification["selected_rank"],
                "score_gap": classification["score_gap"],
                "reasons": classification["reasons"],
            }
        )

    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[str(row.get("root_cause") or "Missing Evidence")].append(row)

    cause_summary: list[dict[str, Any]] = []
    for cause in ROOT_CAUSES:
        cause_rows = grouped.get(cause, [])
        returns = [
            float(row["net_return_pct"])
            for row in cause_rows
            if row.get("net_return_pct") is not None
        ]
        metrics = performance_metrics(returns)
        cause_summary.append(
            {
                "root_cause": cause,
                "diagnostic_kind": _diagnostic_kind(cause),
                "causal_eligible": _diagnostic_kind(cause) == "structural",
                "trade_count": len(cause_rows),
                "return_observation_count": len(returns),
                "win_rate": metrics["win_rate"],
                "avg_return_pct": metrics["average_return_pct"],
                "profit_factor": metrics["profit_factor"],
                "max_drawdown_pct": metrics["maximum_drawdown_pct"],
                "negative_impact_pct": _impact_score(returns),
            }
        )

    largest = _largest_cause(cause_summary)
    largest_behavior = _largest_cause(
        cause_summary,
        excluded={"Missing Evidence", "Aligned / No Alignment Issue"},
    )
    largest_structural = _largest_cause(
        cause_summary,
        excluded=OUTCOME_CONDITIONED_CAUSES | EVIDENCE_GAP_CAUSES,
    )
    patch_candidate = _patch_candidate(str(largest_structural.get("root_cause") or ""))

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
        "outcome_conditioned_causes": sorted(OUTCOME_CONDITIONED_CAUSES),
        "q15_behavior_patch_candidate": patch_candidate,
        "rows": rows,
        "interpretation_rule": (
            "Q14 explains why scanner_alignment_score is low. It does not authorize behavior changes. "
            "Scanner Ranking Failure and Aligned / No Alignment Issue are outcome-conditioned labels, "
            "not independent causal proof. Structural behavior candidates must use "
            "largest_structural_root_cause plus Q9 forward evidence."
        ),
    }


def render_scanner_alignment_root_cause_report(payload: Mapping[str, Any]) -> str:
    return _a53_render.render_scanner_alignment_root_cause_report(payload, facade=sys.modules[__name__])


def _load_day_models_and_evaluations(reports_root: Path, day: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    root = reports_root / "evaluation" / "trades" / day
    models: list[dict[str, Any]] = []
    evaluations: list[dict[str, Any]] = []
    if not root.exists():
        return models, evaluations
    for trade_dir in sorted(path for path in root.iterdir() if path.is_dir()):
        model = _read_json(trade_dir / "trade_read_model.json")
        evaluation = _read_json(trade_dir / "trade_evaluation.json")
        if model:
            models.append(model)
        if evaluation:
            evaluations.append(evaluation)
    return models, evaluations


def build_scanner_alignment_root_cause_range(
    *,
    reports_root: Path = Path("reports"),
    start: str,
    end: str,
) -> dict[str, Any]:
    from datetime import date, timedelta

    reports_root = Path(reports_root)
    cursor = date.fromisoformat(start)
    final = date.fromisoformat(end)
    daily_payloads: list[dict[str, Any]] = []
    while cursor <= final:
        day = cursor.isoformat()
        selection_authority = _read_json(
            reports_root / "evaluation" / "daily" / day / "selection_authority_audit.json"
        )
        models, evaluations = _load_day_models_and_evaluations(reports_root, day)
        if selection_authority or models or evaluations:
            daily_payloads.append(
                build_scanner_alignment_root_cause_report(
                    day=day,
                    models=models,
                    evaluations=evaluations,
                    selection_authority=selection_authority,
                )
            )
        cursor += timedelta(days=1)

    all_rows = [row for payload in daily_payloads for row in payload.get("rows") or []]
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in all_rows:
        grouped[str(row.get("root_cause") or "Missing Evidence")].append(row)
    cause_summary: list[dict[str, Any]] = []
    for cause in ROOT_CAUSES:
        cause_rows = grouped.get(cause, [])
        returns = [
            float(row["net_return_pct"])
            for row in cause_rows
            if row.get("net_return_pct") is not None
        ]
        metrics = performance_metrics(returns)
        cause_summary.append(
            {
                "root_cause": cause,
                "diagnostic_kind": _diagnostic_kind(cause),
                "causal_eligible": _diagnostic_kind(cause) == "structural",
                "trade_count": len(cause_rows),
                "return_observation_count": len(returns),
                "win_rate": metrics["win_rate"],
                "avg_return_pct": metrics["average_return_pct"],
                "profit_factor": metrics["profit_factor"],
                "max_drawdown_pct": metrics["maximum_drawdown_pct"],
                "negative_impact_pct": _impact_score(returns),
            }
        )
    largest = _largest_cause(cause_summary)
    largest_behavior = _largest_cause(
        cause_summary,
        excluded={"Missing Evidence", "Aligned / No Alignment Issue"},
    )
    largest_structural = _largest_cause(
        cause_summary,
        excluded=OUTCOME_CONDITIONED_CAUSES | EVIDENCE_GAP_CAUSES,
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
        "outcome_conditioned_causes": sorted(OUTCOME_CONDITIONED_CAUSES),
        "measurement_contract_version": "q14_structural_causality.v2",
        "q15_behavior_patch_candidate": _patch_candidate(str(largest_structural.get("root_cause") or "")),
        "daily_rows": [
            {
                "day": payload.get("day"),
                "trade_count": payload.get("trade_count"),
                "largest_root_cause": _mapping(payload.get("largest_root_cause")).get("root_cause") or "",
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


def write_scanner_alignment_root_cause_range(
    *,
    reports_root: Path = Path("reports"),
    start: str,
    end: str,
) -> dict[str, str]:
    reports_root = Path(reports_root)
    payload = build_scanner_alignment_root_cause_range(
        reports_root=reports_root,
        start=start,
        end=end,
    )
    out_dir = reports_root / "evaluation" / "range" / f"{start}_{end}"
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / "scanner_alignment_root_cause_report.json"
    md_path = out_dir / "scanner_alignment_root_cause_report.md"
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(render_scanner_alignment_root_cause_report(payload), encoding="utf-8")
    return {"json": str(json_path), "markdown": str(md_path)}


__all__ = [
    "build_scanner_alignment_root_cause_report",
    "render_scanner_alignment_root_cause_report",
    "build_scanner_alignment_root_cause_range",
    "write_scanner_alignment_root_cause_range",
]
