"""entry_timing_attribution: ``_iso`` body (moved verbatim from ``entry_timing_attribution``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping, Sequence


def _iso(epoch: int, *, facade: Any) -> str:
    if epoch <= 0:
        return ""
    return facade.datetime.fromtimestamp(epoch, tz=facade.timezone.utc).isoformat()
