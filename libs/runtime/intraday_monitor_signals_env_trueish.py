from __future__ import annotations
from typing import Any

def _env_trueish(value: Any, default: bool = False, *, facade: Any) -> bool:
    text = str(value or "").strip().lower()
    if not text:
        return bool(default)
    return text in ("1", "true", "yes", "y", "on")
