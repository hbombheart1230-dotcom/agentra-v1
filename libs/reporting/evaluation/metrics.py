from __future__ import annotations

from typing import Iterable
import sys
from . import metrics_performance_metrics as _a41_performance_metrics


def performance_metrics(values: Iterable[float]) -> dict[str, float | int]:
    return _a41_performance_metrics.performance_metrics(values, facade=sys.modules[__name__])
