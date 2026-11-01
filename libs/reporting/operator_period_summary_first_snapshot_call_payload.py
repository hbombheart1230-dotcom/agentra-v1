"""operator_period_summary: ``_first_snapshot_call_payload`` body (moved verbatim from ``operator_period_summary``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple


def _first_snapshot_call_payload(snapshot: Dict[str, Any], api_id: str, *, facade: Any) -> Dict[str, Any]:
    for call in list(snapshot.get("calls") or []):
        if not isinstance(call, dict):
            continue
        if str(call.get("api_id") or "").strip() != api_id:
            continue
        payload = call.get("payload")
        return payload if isinstance(payload, dict) else {}
    return {}
