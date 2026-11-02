"""Pure module-path conversion owner for the target-tree audit."""
from __future__ import annotations

from typing import Any


def _module_path(path: str, *, facade: Any) -> str:
    if not path.startswith("scripts/") or not path.endswith(".py"):
        raise ValueError(f"not a Python script path: {path}")
    return path[:-3].replace("/", ".")
