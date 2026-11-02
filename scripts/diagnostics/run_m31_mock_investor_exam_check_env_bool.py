from __future__ import annotations

from typing import Dict


def _env_bool(env: Dict[str, str], key: str, default: bool = False, *, facade: object = None) -> bool:
    raw = str(env.get(key, "")).strip().lower()
    if not raw:
        return bool(default)
    return raw in ("1", "true", "yes", "y", "on")
