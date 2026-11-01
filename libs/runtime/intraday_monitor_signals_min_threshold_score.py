from __future__ import annotations

from typing import Any, Dict, List, Mapping, Sequence


def _min_threshold_score(actual: float, threshold: float, *, facade: Any):
    actual_value = float(actual)
    threshold_value = float(threshold)
    if threshold_value <= 0.0:
        return 1.0 if actual_value > 0.0 else 0.0
    return facade._clamp_score(actual_value / threshold_value)
