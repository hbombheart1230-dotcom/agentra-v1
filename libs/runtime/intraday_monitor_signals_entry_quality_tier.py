from __future__ import annotations

from typing import Any, Dict, List, Mapping, Sequence


def _entry_quality_tier(score: float, *, facade: Any):
    value = facade._clamp_score(score)
    if value >= 0.80:
        return "strong"
    if value >= 0.65:
        return "watch"
    return "weak"
