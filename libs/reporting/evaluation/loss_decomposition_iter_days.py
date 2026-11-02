"""loss_decomposition: ``_iter_days`` body (moved verbatim from ``loss_decomposition``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Iterable


def _iter_days(start: str, end: str, *, facade: Any) -> Iterable[str]:
    current = facade.date.fromisoformat(start[:10])
    final = facade.date.fromisoformat(end[:10])
    while current <= final:
        yield current.isoformat()
        current += facade.timedelta(days=1)
