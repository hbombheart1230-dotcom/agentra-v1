"""quant_tactic_evaluation projections (moved verbatim from quant_tactic_evaluation).

Module globals and helpers are resolved on ``facade`` (the quant_tactic_evaluation module) at call time; this module never imports it.
"""
from __future__ import annotations

from typing import Any, Dict, List


def _valid_evaluation_rows(rows: List[Dict[str, Any]], *, facade: Any) -> List[Dict[str, Any]]:
    return [row for row in rows if not facade._invalid_sample_reason(row)]
