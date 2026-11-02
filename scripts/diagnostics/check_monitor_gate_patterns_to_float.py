"""Pure float coercion owner for monitor gate diagnostics."""
from __future__ import annotations

from typing import Any, Optional


def _to_float(value: Any, *, facade: Any) -> Optional[float]:
    try:
        out = float(value)
    except Exception:
        return None
    if out != out:
        return None
    return out
