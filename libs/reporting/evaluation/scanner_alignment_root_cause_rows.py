"""scanner_alignment_root_cause: ``_rows`` body (moved verbatim from ``scanner_alignment_root_cause``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Mapping


def _rows(value: Any, *, facade: Any) -> list[Mapping[str, Any]]:
    return [row for row in (value or []) if isinstance(row, facade.Mapping)]
