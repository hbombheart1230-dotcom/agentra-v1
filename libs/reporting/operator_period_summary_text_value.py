"""operator_period_summary: ``_text_value`` body (moved verbatim from ``operator_period_summary``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Dict, Iterable, List, Tuple


def _text_value(value: Any, *, facade: Any) -> str:
    text = str(value or "").strip()
    if text.lower() in {"", "-", "none", "null", "unknown", "not_captured"}:
        return ""
    return text
