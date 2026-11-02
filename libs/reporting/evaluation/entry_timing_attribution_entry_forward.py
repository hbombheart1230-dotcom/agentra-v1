"""entry_timing_attribution: ``_entry_forward`` body (moved verbatim from ``entry_timing_attribution``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping, Sequence


def _entry_forward(
    *,
    trade_id: str,
    symbol: str,
    entry_epoch: int,
    entry_price: float | None,
    minute_rows_by_symbol: Mapping[str, list[Mapping[str, Any]]],
    facade: Any,
) -> dict[str, Any]:
    if not symbol or entry_epoch <= 0 or entry_price is None or entry_price <= 0:
        return {"available": False, "reason": "entry_baseline_unavailable", "checkpoints": {}}
    rows = facade.attach_forward_outcomes(
        [{
            "symbol": symbol,
            "trade_id": trade_id,
            "generated_at": facade._iso(entry_epoch),
            "shadow_forward_base": {
                "available": True,
                "baseline_epoch": entry_epoch,
                "baseline_price": entry_price,
                "source": "actual_entry",
            },
        }],
        minute_rows_by_symbol=minute_rows_by_symbol,
    )
    outcome = facade._mapping((rows[0] if rows else {}).get("shadow_forward_outcome"))
    checkpoints = facade._mapping(outcome.get("checkpoints"))
    return {
        "available": bool(outcome.get("available")),
        "reason": outcome.get("reason"),
        "observed_checkpoint_count": outcome.get("observed_checkpoint_count"),
        "checkpoints": {
            horizon: dict(checkpoints.get(horizon) or {"status": "pending"})
            for horizon in facade.HORIZONS
        },
    }
