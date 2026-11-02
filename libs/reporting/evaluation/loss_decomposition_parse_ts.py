"""loss_decomposition: ``_parse_ts`` body (moved verbatim from ``loss_decomposition``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any


def _parse_ts(value: Any, *, facade: Any) -> datetime | None:
    try:
        return facade.datetime.fromisoformat(str(value or "").replace("Z", "+00:00"))
    except ValueError:
        return None
