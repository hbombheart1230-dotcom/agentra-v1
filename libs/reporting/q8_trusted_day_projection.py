"""q8_trusted_reaggregation projections (moved verbatim from q8_trusted_reaggregation).

Module globals and helpers are resolved on ``facade`` (the q8_trusted_reaggregation module) at call time; this module never imports it.
"""
from __future__ import annotations

from typing import Any, Iterable


def _iter_days(start: str, end: str, *, facade: Any) -> Iterable[str]:
    current = facade.date.fromisoformat(str(start)[:10])
    final = facade.date.fromisoformat(str(end)[:10])
    while current <= final:
        yield current.isoformat()
        current += facade.timedelta(days=1)
