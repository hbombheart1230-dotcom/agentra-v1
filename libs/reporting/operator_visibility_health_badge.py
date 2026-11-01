"""operator_visibility: ``_health_badge`` body (moved verbatim from ``operator_visibility``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Dict, Iterable, List, Mapping, Optional, Tuple


def _health_badge(level: str, *, facade: Any) -> str:
    lv = str(level or "").strip().upper()
    if lv not in ("GREEN", "YELLOW", "RED"):
        return f"[{lv or 'UNKNOWN'}]"
    return f"[{lv}]"
