"""strategy_horizon_feedback: ``_epoch_seconds`` body (moved verbatim from ``strategy_horizon_feedback``).

``facade`` is the source module; names/helpers resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Dict, Iterable, List, Mapping, Optional, Tuple


def _epoch_seconds(value: Any, *, facade: Any) -> float | None:
    if value in (None, ""):
        return None
    if isinstance(value, (int, float)):
        raw = float(value)
        return raw / 1000.0 if raw > 10_000_000_000 else raw
    text = str(value or "").strip()
    if not text:
        return None
    try:
        if text.isdigit():
            if len(text) == 14:
                return facade.datetime.strptime(text, "%Y%m%d%H%M%S").replace(tzinfo=facade.timezone.utc).timestamp()
            raw = float(text)
            return raw / 1000.0 if raw > 10_000_000_000 else raw
        normalized = text.replace("Z", "+00:00")
        dt = facade.datetime.fromisoformat(normalized)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=facade.timezone.utc)
        return dt.timestamp()
    except Exception:
        return None
