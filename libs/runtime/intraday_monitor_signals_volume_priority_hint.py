from __future__ import annotations

from typing import Any, Dict, List, Mapping, Sequence


def _volume_priority_hint(volume_ratio_min: float, *, facade: Any):
    if float(volume_ratio_min) >= 1.0:
        return "high"
    if float(volume_ratio_min) <= 0.75:
        return "low"
    return "normal"
