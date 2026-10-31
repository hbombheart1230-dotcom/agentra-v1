"""quant_tactic_evaluation projections (moved verbatim from quant_tactic_evaluation).

Module globals and helpers are resolved on ``facade`` (the quant_tactic_evaluation module) at call time; this module never imports it.
"""
from __future__ import annotations

from typing import Any, Dict, Iterable, List, Mapping


def _evaluation_rows(rows: Iterable[Mapping[str, Any]], *, facade: Any) -> List[Dict[str, Any]]:
    return [dict(row) for row in rows if isinstance(row, facade.Mapping) and facade._closed_or_realized(row)]
