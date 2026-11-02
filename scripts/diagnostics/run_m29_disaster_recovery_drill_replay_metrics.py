from __future__ import annotations

from typing import Any, Dict


def _replay_metrics(obj: Dict[str, Any], *, facade: object = None) -> Dict[str, Any]:
    return {
        "replayed_intent_total": int(obj.get("replayed_intent_total") or 0),
        "executed_intent_total": int(obj.get("executed_intent_total") or 0),
        "blocked_intent_total": int(obj.get("blocked_intent_total") or 0),
        "pending_intent_total": int(obj.get("pending_intent_total") or 0),
        "fill_qty_total": int(obj.get("fill_qty_total") or 0),
        "fill_notional_total": float(obj.get("fill_notional_total") or 0.0),
    }
