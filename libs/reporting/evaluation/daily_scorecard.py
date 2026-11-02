from __future__ import annotations

from collections import Counter
from typing import Any
import sys
from . import daily_scorecard_build_daily_scorecard as _a38_build_daily_scorecard

from .contracts import CONTRACT_VERSION, DecisionClass, IntegrityStatus, contract_metadata
from .metrics import performance_metrics


def build_daily_scorecard(
    *,
    day: str,
    inventory: dict[str, Any],
    trade_evaluations: list[dict[str, Any]],
    attributions: list[dict[str, Any]],
    q8_review: dict[str, Any],
    start_gate: dict[str, Any],
    day_validity: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return _a38_build_daily_scorecard.build_daily_scorecard(day=day, inventory=inventory, trade_evaluations=trade_evaluations, attributions=attributions, q8_review=q8_review, start_gate=start_gate, day_validity=day_validity, facade=sys.modules[__name__])
