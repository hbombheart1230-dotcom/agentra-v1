"""quant_tactic_evaluation projections (moved verbatim from quant_tactic_evaluation).

Module globals and helpers are resolved on ``facade`` (the quant_tactic_evaluation module) at call time; this module never imports it.
"""
from __future__ import annotations

from typing import Any, Dict, List


def _field_gap_rows(rows: List[Dict[str, Any]], *, facade: Any) -> List[Dict[str, Any]]:
    count = len(rows)
    out: List[Dict[str, Any]] = []
    for field in facade._REQUIRED_FIELDS:
        captured = sum(1 for row in rows if facade._text(row.get(field)))
        coverage = float(captured) / float(count) if count else 0.0
        out.append(
            {
                "field": field,
                "captured_count": captured,
                "missing_count": max(0, count - captured),
                "coverage": coverage,
                "coverage_ok": coverage >= facade._FIELD_COVERAGE_FLOOR,
            }
        )
    return out
