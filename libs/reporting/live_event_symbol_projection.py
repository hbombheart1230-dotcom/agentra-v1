"""live_execution_event_evidence projections (moved verbatim from live_execution_event_evidence).

Module globals and helpers are resolved on ``facade`` (the live_execution_event_evidence module) at call time; this module never imports it.
"""
from __future__ import annotations

from typing import Any, Dict


def event_row_symbol(row: Dict[str, Any], *, facade: Any) -> str:
    payload = row.get("payload") if isinstance(row.get("payload"), dict) else {}
    return facade.normalize_symbol(
        row.get("symbol")
        or payload.get("symbol")
        or payload.get("selected_symbol")
        or payload.get("position_symbol")
        or "",
        allow_test_symbols=True,
    )
