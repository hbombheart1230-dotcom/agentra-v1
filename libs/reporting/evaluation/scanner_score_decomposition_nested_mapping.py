"""scanner_score_decomposition: ``_nested_mapping`` body (moved verbatim from ``scanner_score_decomposition``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Mapping


def _nested_mapping(row: Mapping[str, Any], key: str, *, facade: Any) -> Mapping[str, Any]:
    value = row.get(key)
    return value if isinstance(value, facade.Mapping) else {}
