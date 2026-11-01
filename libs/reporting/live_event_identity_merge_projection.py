"""live_execution_event_evidence projections (moved verbatim from live_execution_event_evidence).

Module globals and helpers are resolved on ``facade`` (the live_execution_event_evidence module) at call time; this module never imports it.
"""
from __future__ import annotations

from typing import Any, Dict, Iterable, List


def merge_rows_by_identity(*collections: Iterable[Dict[str, Any]], facade: Any) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    seen: set[tuple[str, str, str, str]] = set()
    for rows in collections:
        for row in list(rows or []):
            if not isinstance(row, dict):
                continue
            key = (
                str(row.get("ts") or row.get("timestamp") or ""),
                str(row.get("run_id") or ""),
                facade.event_row_name(row),
                facade.event_row_symbol(row),
            )
            if key in seen:
                continue
            seen.add(key)
            out.append(row)
    return out
