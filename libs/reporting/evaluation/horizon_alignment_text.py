"""horizon_alignment: ``_text`` body (moved verbatim from ``horizon_alignment``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any


def _text(value: Any, fallback: str = "unknown", *, facade: Any) -> str:
    text = str(value or "").strip()
    return text if text else fallback
