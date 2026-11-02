"""scanner_score_decomposition: ``_first_num`` body (moved verbatim from ``scanner_score_decomposition``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Mapping


def _first_num(row: Mapping[str, Any], keys: tuple[str, ...], *, facade: Any) -> float | None:
    for key in keys:
        value = facade._num(row.get(key))
        if value is not None:
            return value
    return None
