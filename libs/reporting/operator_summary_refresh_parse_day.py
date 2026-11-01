"""operator_summary_refresh: ``_parse_day`` body (moved verbatim from ``operator_summary_refresh``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple


def _parse_day(value: Any, *, facade: Any) -> date | None:
    text = str(value or "").strip()[:10]
    if not text:
        return None
    try:
        return facade.date.fromisoformat(text)
    except Exception:
        return None
