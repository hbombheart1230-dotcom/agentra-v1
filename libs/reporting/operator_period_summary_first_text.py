"""operator_period_summary: ``_first_text`` body (moved verbatim from ``operator_period_summary``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Dict, Iterable, List, Tuple


def _first_text(*values: Any, facade: Any) -> str:
    for value in values:
        text = facade._text_value(value)
        if text:
            return text
    return ""
