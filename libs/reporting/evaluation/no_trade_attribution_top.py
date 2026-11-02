"""no_trade_attribution: ``_top`` body (moved verbatim from ``no_trade_attribution``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from collections import Counter
from typing import Any


def _top(counter: Counter[str], limit: int = 10, *, facade: Any) -> list[dict[str, Any]]:
    return [
        {"name": key, "count": int(value)}
        for key, value in counter.most_common(limit)
        if key
    ]
