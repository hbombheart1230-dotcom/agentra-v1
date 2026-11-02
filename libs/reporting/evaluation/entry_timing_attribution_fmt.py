"""entry_timing_attribution: ``_fmt`` body (moved verbatim from ``entry_timing_attribution``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping, Sequence


def _fmt(value: Any, suffix: str = "", *, facade: Any) -> str:
    if value in (None, ""):
        return "-"
    try:
        return f"{float(value):.4f}{suffix}"
    except (TypeError, ValueError):
        return str(value)
