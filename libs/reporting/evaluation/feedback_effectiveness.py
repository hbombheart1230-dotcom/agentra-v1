from __future__ import annotations

from typing import Any
import sys

from .contracts import CONTRACT_VERSION, DecisionClass
from . import feedback_effectiveness_build_feedback_effectiveness as _a48_build_feedback_effectiveness


def build_feedback_effectiveness(
    trade_models: list[dict[str, Any]],
    q9_windows: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    return _a48_build_feedback_effectiveness.build_feedback_effectiveness(trade_models, q9_windows, facade=sys.modules[__name__])
