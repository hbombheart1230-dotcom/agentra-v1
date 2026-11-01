"""operator_visibility: ``_pick_day`` body (moved verbatim from ``operator_visibility``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Dict, Iterable, List, Mapping, Optional, Tuple


def _pick_day(rows: List[Dict[str, Any]], requested_day: Optional[str], *, facade: Any) -> str:
    if requested_day:
        return str(requested_day).strip()
    days = sorted({str(r.get("_day")) for r in rows if r.get("_day")})
    if days:
        return days[-1]
    return facade.date.today().isoformat()
