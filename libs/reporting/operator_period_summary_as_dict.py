"""operator_period_summary: ``_as_dict`` body (moved verbatim from ``operator_period_summary``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple


def _as_dict(value: Any, *, facade: Any) -> Dict[str, Any]:
    return value if isinstance(value, dict) else {}
