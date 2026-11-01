"""operator_period_summary: ``_first_dict`` body (moved verbatim from ``operator_period_summary``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Dict, Iterable, List, Tuple


def _first_dict(*values: Any, facade: Any) -> Dict[str, Any]:
    for value in values:
        if isinstance(value, dict) and value:
            return dict(value)
    return {}
