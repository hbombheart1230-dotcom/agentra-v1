"""quant_tactic_evaluation projections (moved verbatim from quant_tactic_evaluation).

Module globals and helpers are resolved on ``facade`` (the quant_tactic_evaluation module) at call time; this module never imports it.
"""
from __future__ import annotations

from typing import Any, Dict, List


def _invalid_sample_examples(rows: List[Dict[str, Any]], *, limit: int = 5, facade: Any) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for row in rows:
        reason = facade._invalid_sample_reason(row)
        if not reason:
            continue
        out.append(
            {
                "trade_id": facade._text(row.get("trade_id")),
                "symbol": facade._text(row.get("symbol")),
                "reason": reason,
            }
        )
        if len(out) >= limit:
            break
    return out
