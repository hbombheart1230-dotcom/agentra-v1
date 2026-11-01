"""strategy_horizon_feedback: ``extract_strategy_horizon_feedback`` body (moved verbatim from ``strategy_horizon_feedback``).

``facade`` is the source module; names/helpers resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Dict, Iterable, List, Mapping, Optional, Tuple


def extract_strategy_horizon_feedback(surface: Mapping[str, Any] | None, *, facade: Any) -> dict[str, Any]:
    obj = facade._as_dict(surface)
    if isinstance(obj.get("strategy_horizon_feedback"), Mapping):
        return dict(obj.get("strategy_horizon_feedback") or {})
    strategy_policy = facade._as_dict(obj.get("strategy_policy"))
    if not strategy_policy and isinstance(obj.get("monitor_policy"), Mapping):
        strategy_policy = dict(obj)
    monitor_policy = facade._as_dict(strategy_policy.get("monitor_policy"))
    if isinstance(monitor_policy.get("strategy_horizon_feedback"), Mapping):
        return dict(monitor_policy.get("strategy_horizon_feedback") or {})
    if obj.get("strategy_horizon") not in (None, ""):
        return facade.build_strategy_horizon_feedback(
            {
                "strategy_horizon": obj.get("strategy_horizon"),
                "expected_hold_window": facade._as_dict(obj.get("expected_hold_window")),
                "exit_guidance": facade._as_dict(obj.get("exit_guidance")),
                "invalidation_conditions": obj.get("invalidation_conditions"),
                "monitor_handoff": facade._as_dict(obj.get("monitor_handoff")),
            },
            playbook=str(obj.get("playbook") or ""),
            monitor_guidance=str(obj.get("monitor_guidance") or ""),
            trade_aggressiveness=str(obj.get("trade_aggressiveness") or ""),
            risk_tone=str(obj.get("risk_tone") or ""),
            source="extracted_surface",
        )
    return {}
