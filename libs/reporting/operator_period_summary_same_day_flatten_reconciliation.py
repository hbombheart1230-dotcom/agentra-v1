"""operator_period_summary: ``_same_day_flatten_reconciliation`` body (moved verbatim from ``operator_period_summary``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple


def _same_day_flatten_reconciliation(
    *,
    reports_root: Path,
    day: str | None,
    symbol: str,
    qty: int,
    avg_price: Any,
    facade: Any,
) -> Dict[str, Any]:
    normalized_day = str(day or "").strip()
    normalized_symbol = str(symbol or "").strip().upper()
    if not normalized_day or not normalized_symbol or qty <= 0:
        return {}
    day_root = facade.Path(reports_root) / "trades" / normalized_day
    if not day_root.exists():
        return {}

    day_token = normalized_day.replace("-", "")
    pattern = f"TRD_{day_token}_{normalized_symbol}_*/lifecycle_bundle.json"
    for path in sorted(day_root.rglob(pattern)):
        payload = facade._read_json(path)
        if not isinstance(payload, dict):
            continue
        entry = payload.get("entry") if isinstance(payload.get("entry"), dict) else {}
        exit_row = payload.get("exit") if isinstance(payload.get("exit"), dict) else {}
        if str(exit_row.get("action") or "").strip().upper() != "SELL":
            continue
        entry_qty = facade._safe_int(entry.get("qty"))
        exit_qty = facade._safe_int(exit_row.get("qty"))
        if entry_qty < qty or exit_qty < qty:
            continue
        entry_price = entry.get("price")
        if facade._safe_float(avg_price) is not None and not facade._price_matches(avg_price, entry_price):
            continue
        return {
            "symbol": normalized_symbol,
            "trade_id": str(payload.get("trade_id") or path.parent.name),
            "lifecycle_bundle_path": str(path),
            "reason": "same_day_lifecycle_full_sell_after_flatten_decision",
            "exit_reason": str(exit_row.get("reason_human") or ""),
            "exit_ts": str(exit_row.get("ts") or ""),
            "exit_qty": exit_qty,
        }
    return {}
