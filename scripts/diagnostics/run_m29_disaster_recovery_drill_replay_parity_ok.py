from __future__ import annotations

from typing import Any, Dict, List, Tuple


def _replay_parity_ok(base: Dict[str, Any], restored: Dict[str, Any], *, facade: object = None) -> Tuple[bool, List[str]]:
    failures: List[str] = []
    for key in (
        "replayed_intent_total",
        "executed_intent_total",
        "blocked_intent_total",
        "pending_intent_total",
        "fill_qty_total",
    ):
        if int(base.get(key) or 0) != int(restored.get(key) or 0):
            failures.append(f"parity_mismatch:{key}")
    b_notional = float(base.get("fill_notional_total") or 0.0)
    r_notional = float(restored.get("fill_notional_total") or 0.0)
    if abs(b_notional - r_notional) > 1e-9:
        failures.append("parity_mismatch:fill_notional_total")
    return len(failures) == 0, failures
