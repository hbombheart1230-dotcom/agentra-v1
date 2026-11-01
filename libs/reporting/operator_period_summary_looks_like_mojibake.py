"""operator_period_summary: ``_looks_like_mojibake`` body (moved verbatim from ``operator_period_summary``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple


def _looks_like_mojibake(text: str, *, facade: Any) -> bool:
    if not text:
        return False
    if "\ufffd" in text:
        return True
    compatibility_count = sum(1 for ch in text if "\uf900" <= ch <= "\ufaff")
    if compatibility_count:
        return True
    question_count = text.count("?")
    return question_count >= 2 and any(ord(ch) > 127 for ch in text)
