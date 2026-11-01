"""live_execution_event_evidence projections (moved verbatim from live_execution_event_evidence).

Module globals and helpers are resolved on ``facade`` (the live_execution_event_evidence module) at call time; this module never imports it.
"""
from __future__ import annotations

from typing import Any, Dict


def event_row_name(row: Dict[str, Any]) -> str:
    return str(row.get("event_name") or row.get("name") or row.get("event") or "").strip()
