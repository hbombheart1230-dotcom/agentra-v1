"""Pure task-name resolver owner."""
from __future__ import annotations

from typing import Any


def _resolve_task(raw: str, prefix: str | None, *, facade: Any) -> tuple[str | None, str]:
    if facade.re.fullmatch(r"[A-Za-z0-9_.-]+", raw):
        return raw, "LITERAL"
    match = facade.re.fullmatch(r"%TASK_PREFIX%(-[A-Za-z0-9_.-]+)", raw, facade.re.I)
    if match and prefix is not None:
        return prefix + match.group(1), "PREFIX_RESOLVED"
    return None, "UNRESOLVED"
