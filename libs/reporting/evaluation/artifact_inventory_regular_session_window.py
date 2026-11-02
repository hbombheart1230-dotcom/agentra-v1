"""artifact_inventory: ``_regular_session_window`` body (moved verbatim from ``artifact_inventory``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable, Mapping


def _regular_session_window(row: dict[str, Any], *, facade: Any) -> bool:
    parsed = facade._parse_window_kst(row.get("generated_at"))
    if parsed is None:
        return True
    return (9, 0) <= (parsed.hour, parsed.minute) <= (15, 30)
