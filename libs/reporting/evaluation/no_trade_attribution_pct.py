"""no_trade_attribution: ``_pct`` body (moved verbatim from ``no_trade_attribution``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any


def _pct(value: Any, *, facade: Any) -> str:
    number = facade._num(value)
    if number is None:
        return "-"
    return f"{number:.4f}%"
