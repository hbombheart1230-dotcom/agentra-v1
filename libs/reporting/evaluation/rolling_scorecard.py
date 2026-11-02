from __future__ import annotations

from collections import Counter
from typing import Any
import sys

from .contracts import CONTRACT_VERSION, DecisionClass, DIRECTIONAL_MIN_DAYS, DIRECTIONAL_MIN_OBSERVATIONS
from .metrics import performance_metrics
from . import rolling_scorecard_build_rolling_scorecard as _a47_build_rolling_scorecard


def build_rolling_scorecard(scorecards: list[dict[str, Any]], *, window_days: int) -> dict[str, Any]:
    return _a47_build_rolling_scorecard.build_rolling_scorecard(scorecards, window_days=window_days, facade=sys.modules[__name__])
