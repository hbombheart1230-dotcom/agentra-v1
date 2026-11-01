"""operator_period_summary: ``_is_unavailable_pnl`` body (moved verbatim from ``operator_period_summary``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Dict, Iterable, List, Tuple


def _is_unavailable_pnl(value: Any, *, facade: Any) -> bool:
    if value is None:
        return True
    return str(value).strip().lower() in facade._UNAVAILABLE_PNL_VALUES
