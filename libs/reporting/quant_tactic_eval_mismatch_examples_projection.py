"""quant_tactic_evaluation projections (moved verbatim from quant_tactic_evaluation).

Module globals and helpers are resolved on ``facade`` (the quant_tactic_evaluation module) at call time; this module never imports it.
"""
from __future__ import annotations

from typing import Any, Dict, List


def _mismatch_examples(rows: List[Dict[str, Any]], *, limit: int = 4, facade: Any) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for row in rows:
        count = facade._int(row.get("quant_tactic_mismatch_count"))
        if count <= 0:
            continue
        out.append(
            {
                "trade_id": facade._text(row.get("trade_id")),
                "symbol": facade._text(row.get("symbol")),
                "tactic_id": facade._text(row.get("quant_tactic_id")),
                "mismatch_count": count,
            }
        )
        if len(out) >= limit:
            break
    return out
