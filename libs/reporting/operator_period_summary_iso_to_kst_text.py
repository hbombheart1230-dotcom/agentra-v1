"""operator_period_summary: ``_iso_to_kst_text`` body (moved verbatim from ``operator_period_summary``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Dict, Iterable, List, Tuple


def _iso_to_kst_text(value: Any, *, facade: Any) -> str:
    dt = facade._iso_to_kst_dt(value)
    if dt is None:
        return ""
    return dt.strftime("%Y-%m-%d %H:%M:%S KST")
