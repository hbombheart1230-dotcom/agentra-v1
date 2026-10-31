from __future__ import annotations

from collections import Counter
import sys
from typing import Any, Dict, Iterable, List, Mapping
from libs.reporting import quant_tactic_eval_text_projection as _a1_owner
from libs.reporting import quant_tactic_eval_int_projection as _a2_owner
from libs.reporting import quant_tactic_eval_closed_projection as _a3_owner
from libs.reporting import quant_tactic_eval_rows_projection as _a4_owner
from libs.reporting import quant_tactic_eval_invalid_reason_projection as _a5_owner
from libs.reporting import quant_tactic_eval_valid_rows_projection as _a6_owner
from libs.reporting import quant_tactic_eval_invalid_examples_projection as _a7_owner
from libs.reporting import quant_tactic_eval_field_gaps_projection as _a8_owner


_REQUIRED_FIELDS = (
    "quant_tactic_id",
    "entry_quant_decision",
    "exit_quant_decision",
    "tactic_suitability_tier",
    "entry_quant_cost_floor_state",
)
_MIN_REVIEW_SAMPLE = 8
_TARGET_PROMOTION_SAMPLE = 20
_FIELD_COVERAGE_FLOOR = 0.90


def _text(value: Any) -> str:
    return _a1_owner._text(value)


def _int(value: Any, default: int = 0) -> int:
    return _a2_owner._int(value, default)


def _closed_or_realized(row: Mapping[str, Any]) -> bool:
    return _a3_owner._closed_or_realized(row)


def _evaluation_rows(rows: Iterable[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    return _a4_owner._evaluation_rows(rows, facade=sys.modules[__name__])


def _invalid_sample_reason(row: Mapping[str, Any]) -> str:
    return _a5_owner._invalid_sample_reason(row, facade=sys.modules[__name__])


def _valid_evaluation_rows(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return _a6_owner._valid_evaluation_rows(rows, facade=sys.modules[__name__])


def _invalid_sample_examples(rows: List[Dict[str, Any]], *, limit: int = 5) -> List[Dict[str, Any]]:
    return _a7_owner._invalid_sample_examples(rows, limit=limit, facade=sys.modules[__name__])


def _field_gap_rows(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return _a8_owner._field_gap_rows(rows, facade=sys.modules[__name__])


def _mismatch_examples(rows: List[Dict[str, Any]], *, limit: int = 4) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for row in rows:
        count = _int(row.get("quant_tactic_mismatch_count"))
        if count <= 0:
            continue
        out.append(
            {
                "trade_id": _text(row.get("trade_id")),
                "symbol": _text(row.get("symbol")),
                "tactic_id": _text(row.get("quant_tactic_id")),
                "mismatch_count": count,
            }
        )
        if len(out) >= limit:
            break
    return out


def build_quant_tactic_evaluation(rows: Iterable[Mapping[str, Any]]) -> Dict[str, Any]:
    all_evaluation_rows = _evaluation_rows(rows)
    invalid_examples = _invalid_sample_examples(all_evaluation_rows)
    evaluation_rows = _valid_evaluation_rows(all_evaluation_rows)
    field_gaps = _field_gap_rows(evaluation_rows)
    gap_fields = [row["field"] for row in field_gaps if not bool(row.get("coverage_ok"))]
    mismatch_count = sum(_int(row.get("quant_tactic_mismatch_count")) for row in evaluation_rows)
    mismatch_trade_count = sum(1 for row in evaluation_rows if _int(row.get("quant_tactic_mismatch_count")) > 0)
    exit_drift_count = sum(_int(row.get("quant_exit_tactic_drift_count")) for row in evaluation_rows)
    exit_drift_trade_count = sum(1 for row in evaluation_rows if _int(row.get("quant_exit_tactic_drift_count")) > 0)
    source_counts = Counter(_text(row.get("quant_tactic_id_source")) for row in evaluation_rows)
    source_counts.pop("", None)

    if invalid_examples:
        status = "hold_invalid_truth_samples"
    elif len(evaluation_rows) < _MIN_REVIEW_SAMPLE:
        status = "hold_sample_insufficient"
    elif mismatch_trade_count > 0:
        status = "hold_tactic_id_mismatch"
    elif gap_fields:
        status = "hold_field_gaps"
    elif len(evaluation_rows) < _TARGET_PROMOTION_SAMPLE:
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
        "review_sample_floor": _MIN_REVIEW_SAMPLE,
        "promotion_sample_target": _TARGET_PROMOTION_SAMPLE,
        "required_fields": list(_REQUIRED_FIELDS),
        "field_coverage_floor": _FIELD_COVERAGE_FLOOR,
        "field_gaps": field_gaps,
        "missing_required_fields": gap_fields,
        "tactic_id_mismatch_trade_count": mismatch_trade_count,
        "tactic_id_mismatch_count": mismatch_count,
        "tactic_id_mismatch_examples": _mismatch_examples(evaluation_rows),
        "exit_tactic_drift_trade_count": exit_drift_trade_count,
        "exit_tactic_drift_count": exit_drift_count,
        "tactic_id_source_counts": dict(source_counts),
    }


def render_quant_tactic_evaluation_lines(payload: Mapping[str, Any] | None) -> List[str]:
    evaluation = dict(payload or {})
    if not evaluation:
        return []
    missing = list(evaluation.get("missing_required_fields") or [])
    missing_text = ", ".join(str(field) for field in missing) if missing else "none"
    source_counts = dict(evaluation.get("tactic_id_source_counts") or {})
    source_text = ", ".join(f"{key}={value}" for key, value in source_counts.items()) if source_counts else "none"
    lines = [
        "- Quant Q8 readiness: "
        f"`{evaluation.get('status') or 'not_available'}` / action `{evaluation.get('promotion_action') or 'hold'}` "
        f"/ sample {evaluation.get('closed_or_realized_sample_count') or 0}"
        f" valid, invalid {evaluation.get('invalid_sample_count') or 0}"
        f"/{evaluation.get('promotion_sample_target') or _TARGET_PROMOTION_SAMPLE}",
        "- Quant Q8 live-trade readiness: "
        f"`{evaluation.get('live_trade_readiness') or evaluation.get('status') or 'not_available'}` "
        "(actual closed-trade performance only)",
        f"- Quant Q8 missing fields: {missing_text}",
        "- Quant Q8 tactic ID integrity: "
        f"mismatch trades {evaluation.get('tactic_id_mismatch_trade_count') or 0}, "
        f"mismatch rows {evaluation.get('tactic_id_mismatch_count') or 0}, "
        f"exit drift trades {evaluation.get('exit_tactic_drift_trade_count') or 0}, "
        f"exit drift rows {evaluation.get('exit_tactic_drift_count') or 0}, "
        f"sources {source_text}",
    ]
    invalid_examples = [row for row in list(evaluation.get("invalid_sample_examples") or []) if isinstance(row, Mapping)]
    if invalid_examples:
        rendered = []
        for row in invalid_examples[:5]:
            trade_id = _text(row.get("trade_id")) or "-"
            symbol = _text(row.get("symbol")) or "-"
            reason = _text(row.get("reason")) or "unknown"
            rendered.append(f"{trade_id}/{symbol}:{reason}")
        lines.append(f"- Quant Q8 invalid samples: {', '.join(rendered)}")
    mismatch_examples = [row for row in list(evaluation.get("tactic_id_mismatch_examples") or []) if isinstance(row, Mapping)]
    if mismatch_examples:
        rendered = []
        for row in mismatch_examples[:4]:
            trade_id = _text(row.get("trade_id")) or "-"
            symbol = _text(row.get("symbol")) or "-"
            count = _int(row.get("mismatch_count"))
            rendered.append(f"{trade_id}/{symbol}:{count}")
        lines.append(f"- Quant Q8 tactic mismatch examples: {', '.join(rendered)}")
    return lines
