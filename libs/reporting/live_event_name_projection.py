"""live_execution_event_evidence projections (moved verbatim from live_execution_event_evidence).

Module globals and helpers are resolved on ``facade`` (the live_execution_event_evidence module) at call time; this module never imports it.
"""
from __future__ import annotations

from typing import Any, Dict


def row_event_name(row: Dict[str, Any]) -> str:
    text = str(row.get("event_name") or "").strip()
    if text:
        return text
    stage = str(row.get("stage") or "").strip()
    event = str(row.get("event") or "").strip()
    return ".".join(part for part in (stage, event) if part)
