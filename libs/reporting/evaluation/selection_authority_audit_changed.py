"""selection_authority_audit: ``_changed`` body (moved verbatim from ``selection_authority_audit``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any


def _changed(a: str, b: str, *, facade: Any) -> bool | None:
    if not a or not b:
        return None
    return a != b
