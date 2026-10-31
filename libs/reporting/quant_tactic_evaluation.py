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
from libs.reporting import quant_tactic_eval_mismatch_examples_projection as _o6a1_owner
from libs.reporting import quant_tactic_eval_builder_projection as _o6a2_owner
from libs.reporting import quant_tactic_eval_render_projection as _o6a3_owner


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
    return _o6a1_owner._mismatch_examples(rows, limit=limit, facade=sys.modules[__name__])


def build_quant_tactic_evaluation(rows: Iterable[Mapping[str, Any]]) -> Dict[str, Any]:
    return _o6a2_owner.build_quant_tactic_evaluation(rows, facade=sys.modules[__name__])


def render_quant_tactic_evaluation_lines(payload: Mapping[str, Any] | None) -> List[str]:
    return _o6a3_owner.render_quant_tactic_evaluation_lines(payload, facade=sys.modules[__name__])
