"""scanner_alignment_root_cause: ``_symbol`` body (moved verbatim from ``scanner_alignment_root_cause``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any


def _symbol(value: Any, *, facade: Any) -> str:
    if isinstance(value, facade.Mapping):
        return str(value.get("symbol") or "").strip()
    return str(value or "").strip()
