"""strategy_horizon_feedback: ``extract_commander_horizon_policy_from_state`` body (moved verbatim from ``strategy_horizon_feedback``).

``facade`` is the source module; names/helpers resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Dict, Iterable, List, Mapping, Optional, Tuple


def extract_commander_horizon_policy_from_state(state: Mapping[str, Any] | None, *, facade: Any) -> dict[str, Any]:
    obj = facade._as_dict(state)
    direct = facade.extract_commander_horizon_policy(obj)
    if direct:
        return direct
    for key in (
        "commander_decision",
        "strategist_output",
        "strategy_policy",
        "entry_strategy_context",
        "monitor_policy",
        "applied_policy",
    ):
        surface = obj.get(key)
        if isinstance(surface, Mapping):
            found = facade.extract_commander_horizon_policy(surface)
            if found:
                return found
    return {}
