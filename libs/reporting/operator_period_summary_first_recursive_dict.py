"""operator_period_summary: ``_first_recursive_dict`` body (moved verbatim from ``operator_period_summary``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple


def _first_recursive_dict(*roots: Any, key: str, facade: Any) -> Dict[str, Any]:
    for root in roots:
        found = facade._find_key_recursive(root, key)
        if isinstance(found, dict) and found:
            return dict(found)
    return {}
