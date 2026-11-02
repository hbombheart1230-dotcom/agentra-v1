"""entry_timing_attribution: ``_pre_entry_move_pct`` body (moved verbatim from ``entry_timing_attribution``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping, Sequence


def _pre_entry_move_pct(
    *,
    symbol: str,
    decision_epoch: int,
    entry_price: float | None,
    minute_rows_by_symbol: Mapping[str, list[Mapping[str, Any]]],
    facade: Any,
) -> tuple[float | None, dict[str, Any]]:
    if not symbol or decision_epoch <= 0 or entry_price is None or entry_price <= 0:
        return None, {"available": False, "reason": "missing_symbol_time_or_entry_price"}
    rows = list(minute_rows_by_symbol.get(symbol) or [])
    base = facade._row_at_or_before(rows, decision_epoch)
    if not base:
        return None, {"available": False, "reason": "minute_row_before_decision_unavailable"}
    base_price = facade._num(base.get("close") or base.get("price"))
    if base_price is None or base_price <= 0:
        return None, {"available": False, "reason": "decision_base_price_unavailable"}
    return round(((entry_price / base_price) - 1.0) * 100.0, 4), {
        "available": True,
        "decision_base_price": base_price,
        "decision_base_ts": base.get("raw_ts") or base.get("ts"),
    }
