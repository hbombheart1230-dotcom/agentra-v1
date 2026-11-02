from __future__ import annotations

from typing import Any
import sys
from . import counterfactuals_build_selection_attribution as _a38_build_selection_attribution

from .contracts import EvidenceClass


def build_selection_attribution(trade_model: dict[str, Any]) -> dict[str, Any]:
    return _a38_build_selection_attribution.build_selection_attribution(trade_model=trade_model, facade=sys.modules[__name__])
