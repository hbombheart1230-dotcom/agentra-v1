"""operator_visibility: ``_safe_float`` body (moved verbatim from ``operator_visibility``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Dict, Iterable, List, Mapping, Optional, Tuple


def _safe_float(v: Any, default: float = 0.0, *, facade: Any) -> float:
    try:
        return float(v)
    except Exception:
        return float(default)
