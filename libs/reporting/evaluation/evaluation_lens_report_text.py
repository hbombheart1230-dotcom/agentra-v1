"""evaluation_lens_report: ``_text`` body (moved verbatim from ``evaluation_lens_report``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any


def _text(value: Any, *, facade: Any) -> str:
    return str(value or "").strip()
