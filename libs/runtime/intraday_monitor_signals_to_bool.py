from __future__ import annotations

from typing import Any, Dict, List, Mapping, Sequence


def _to_bool(value: Any, default: bool = False, *, facade: Any):
    if value is None:
        return bool(default)
    if isinstance(value, bool):
        return bool(value)
    text = str(value or "").strip().lower()
    if not text:
        return bool(default)
    return text in {"1", "true", "yes", "y", "on"}
