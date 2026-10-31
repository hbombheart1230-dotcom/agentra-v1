"""quant_tactic_evaluation projections (moved verbatim from quant_tactic_evaluation).

Module globals and helpers are resolved on ``facade`` (the quant_tactic_evaluation module) at call time; this module never imports it.
"""
from __future__ import annotations

from typing import Any, Dict, Iterable, Mapping


def build_quant_tactic_evaluation(rows: Iterable[Mapping[str, Any]], *, facade: Any) -> Dict[str, Any]:
    all_evaluation_rows = facade._evaluation_rows(rows)
    invalid_examples = facade._invalid_sample_examples(all_evaluation_rows)
    evaluation_rows = facade._valid_evaluation_rows(all_evaluation_rows)
    field_gaps = facade._field_gap_rows(evaluation_rows)
    gap_fields = [row["field"] for row in field_gaps if not bool(row.get("coverage_ok"))]
    mismatch_count = sum(facade._int(row.get("quant_tactic_mismatch_count")) for row in evaluation_rows)
    mismatch_trade_count = sum(1 for row in evaluation_rows if facade._int(row.get("quant_tactic_mismatch_count")) > 0)
    exit_drift_count = sum(facade._int(row.get("quant_exit_tactic_drift_count")) for row in evaluation_rows)
    exit_drift_trade_count = sum(1 for row in evaluation_rows if facade._int(row.get("quant_exit_tactic_drift_count")) > 0)
    source_counts = facade.Counter(facade._text(row.get("quant_tactic_id_source")) for row in evaluation_rows)
    source_counts.pop("", None)

    if invalid_examples:
        status = "hold_invalid_truth_samples"
    elif len(evaluation_rows) < facade._MIN_REVIEW_SAMPLE:
        status = "hold_sample_insufficient"
    elif mismatch_trade_count > 0:
        status = "hold_tactic_id_mismatch"
    elif gap_fields:
        status = "hold_field_gaps"
    elif len(evaluation_rows) < facade._TARGET_PROMOTION_SAMPLE:
        status = "review_sample_building"
    else:
        status = "promotion_review_ready"

    return {
        "schema_version": "quant_tactic_evaluation.v1",
        "behavior_effect": "evaluation_only",
        "status": status,
        "live_trade_readiness": status,
        "promotion_action": "hold" if status.startswith("hold_") else "manual_review",
        "closed_or_realized_sample_count": len(evaluation_rows),
        "raw_closed_or_realized_sample_count": len(all_evaluation_rows),
        "invalid_sample_count": max(0, len(all_evaluation_rows) - len(evaluation_rows)),
        "invalid_sample_examples": invalid_examples,
        "review_sample_floor": facade._MIN_REVIEW_SAMPLE,
        "promotion_sample_target": facade._TARGET_PROMOTION_SAMPLE,
        "required_fields": list(facade._REQUIRED_FIELDS),
        "field_coverage_floor": facade._FIELD_COVERAGE_FLOOR,
        "field_gaps": field_gaps,
        "missing_required_fields": gap_fields,
        "tactic_id_mismatch_trade_count": mismatch_trade_count,
        "tactic_id_mismatch_count": mismatch_count,
        "tactic_id_mismatch_examples": facade._mismatch_examples(evaluation_rows),
        "exit_tactic_drift_trade_count": exit_drift_trade_count,
        "exit_tactic_drift_count": exit_drift_count,
        "tactic_id_source_counts": dict(source_counts),
    }
