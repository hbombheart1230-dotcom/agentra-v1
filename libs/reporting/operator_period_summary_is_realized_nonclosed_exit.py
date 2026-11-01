"""operator_period_summary: ``_is_realized_nonclosed_exit`` body (moved verbatim from ``operator_period_summary``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Dict, Iterable, List, Tuple


def _is_realized_nonclosed_exit(row: Dict[str, Any], *, facade: Any) -> bool:
    if str(row.get("broker_reconciliation_status") or "") == "skipped_unresolved":
        return False
    if facade._is_closed_trade(row) or facade._trade_action(row) != "SELL":
        return False
    return facade._is_recovered_partial_marker(row)
