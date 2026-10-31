"""quant_tactic_evaluation projections (moved verbatim from quant_tactic_evaluation).

Module globals and helpers are resolved on ``facade`` (the quant_tactic_evaluation module) at call time; this module never imports it.
"""
from __future__ import annotations

from typing import Any, Mapping


def _closed_or_realized(row: Mapping[str, Any]) -> bool:
    status = str(row.get("status") or row.get("last_status") or "").strip().lower()
    action = str(row.get("last_action") or row.get("action") or "").strip().upper()
    origin = str(row.get("trade_origin") or "").strip().lower()
    partial = status == "partial" or origin == "recovered_partial"
    return bool(
        row.get("is_closed_trade")
        or row.get("is_realized_nonclosed_exit")
        or (status == "closed" and not partial)
        or (action == "SELL" and partial)
    )
