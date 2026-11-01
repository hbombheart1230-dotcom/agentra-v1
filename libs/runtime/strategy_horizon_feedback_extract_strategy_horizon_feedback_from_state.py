"""strategy_horizon_feedback: ``extract_strategy_horizon_feedback_from_state`` body (moved verbatim from ``strategy_horizon_feedback``).

``facade`` is the source module; names/helpers resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Dict, Iterable, List, Mapping, Optional, Tuple


def extract_strategy_horizon_feedback_from_state(state: Mapping[str, Any] | None, *, facade: Any) -> dict[str, Any]:
    obj = facade._as_dict(state)
    for key in ("strategist_output", "strategy_policy", "entry_strategy_context"):
        surface = obj.get(key)
        if isinstance(surface, Mapping):
            found = facade.extract_strategy_horizon_feedback(surface)
            if found:
                return found
    return facade.build_strategy_horizon_feedback(
        {},
        playbook=str(obj.get("playbook") or ""),
        monitor_guidance=str(obj.get("monitor_guidance") or ""),
        trade_aggressiveness=str(obj.get("trade_aggressiveness") or ""),
        risk_tone=str(obj.get("risk_tone") or ""),
        source="state_default",
    )
