"""evaluation_lens_report: ``_num`` body (moved verbatim from ``evaluation_lens_report``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any


def _num(value: Any, default: float | None = None, *, facade: Any) -> float | None:
    try:
        if value in (None, ""):
            return default
        return float(value)
    except Exception:
        return default
