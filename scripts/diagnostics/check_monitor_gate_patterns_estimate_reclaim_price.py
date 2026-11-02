"""Pure reclaim-price calculation owner for monitor gate diagnostics."""
from __future__ import annotations

from typing import Any, Optional


def _estimate_reclaim_price(current_price: Any, vwap_distance: Any, reclaim_tolerance_pct: Any, *, facade: Any) -> Optional[float]:
    price = facade._to_float(current_price)
    dist = facade._to_float(vwap_distance)
    tol = facade._to_float(reclaim_tolerance_pct)
    if price is None or dist is None or tol is None:
        return None
    denom = 1.0 + dist
    if abs(denom) < 1e-9:
        return None
    est_vwap = price / denom
    return est_vwap * (1.0 - tol)
