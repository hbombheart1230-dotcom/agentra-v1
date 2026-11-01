"""live_execution_event_evidence projections (moved verbatim from live_execution_event_evidence).

Module globals and helpers are resolved on ``facade`` (the live_execution_event_evidence module) at call time; this module never imports it.
"""
from __future__ import annotations

from typing import Any, Dict, List


def latest_event_payload(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not rows:
        return {}
    payload = rows[-1].get("payload") if isinstance(rows[-1], dict) else {}
    return dict(payload or {}) if isinstance(payload, dict) else {}
