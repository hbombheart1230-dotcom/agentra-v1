from __future__ import annotations

from typing import Any, Dict, List, Mapping, Sequence


def _range_threshold_score(actual: float, minimum: float, maximum: float, *, facade: Any):
    actual_value = float(actual)
    minimum_value = float(minimum)
    maximum_value = float(maximum)
    if minimum_value <= actual_value <= maximum_value:
        return 1.0
    if actual_value < minimum_value:
        return facade._min_threshold_score(actual_value, minimum_value)
    if actual_value <= 0.0:
        return 0.0
    return facade._clamp_score(maximum_value / actual_value if maximum_value > 0.0 else 0.0)
