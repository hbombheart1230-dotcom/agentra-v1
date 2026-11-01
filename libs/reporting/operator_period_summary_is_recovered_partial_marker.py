"""operator_period_summary: ``_is_recovered_partial_marker`` body (moved verbatim from ``operator_period_summary``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple


def _is_recovered_partial_marker(row: Dict[str, Any], *, facade: Any) -> bool:
    return facade._has_partial_lifecycle_marker(row)
