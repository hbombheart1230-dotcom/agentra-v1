"""operator_visibility: ``_safe_int`` body (moved verbatim from ``operator_visibility``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Dict, Iterable, List, Mapping, Optional, Tuple


def _safe_int(v: Any, default: int = 0, *, facade: Any) -> int:
    try:
        return int(float(v))
    except Exception:
        return int(default)
