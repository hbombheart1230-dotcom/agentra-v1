"""strategy_horizon_feedback: ``extract_commander_horizon_policy`` body (moved verbatim from ``strategy_horizon_feedback``).

``facade`` is the source module; names/helpers resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Dict, Iterable, List, Mapping, Optional, Tuple


def extract_commander_horizon_policy(surface: Mapping[str, Any] | None, *, facade: Any) -> dict[str, Any]:
    obj = facade._as_dict(surface)
    for key in ("commander_horizon_policy", "horizon_policy"):
        if isinstance(obj.get(key), Mapping):
            found = dict(obj.get(key) or {})
            if str(found.get("owner") or "").strip().lower() == "commander" or str(
                found.get("schema_version") or ""
            ).startswith("commander_horizon_policy"):
                return found
    applied_policy = facade._as_dict(obj.get("applied_policy"))
    for key in ("horizon", "commander_horizon_policy"):
        if isinstance(applied_policy.get(key), Mapping):
            found = dict(applied_policy.get(key) or {})
            if str(found.get("owner") or "").strip().lower() == "commander" or str(
                found.get("schema_version") or ""
            ).startswith("commander_horizon_policy"):
                return found
    strategy_policy = facade._as_dict(obj.get("strategy_policy"))
    if strategy_policy:
        found = facade.extract_commander_horizon_policy(strategy_policy)
        if found:
            return found
    monitor_policy = facade._as_dict(obj.get("monitor_policy"))
    if monitor_policy:
        found = facade.extract_commander_horizon_policy(monitor_policy)
        if found:
            return found
    commander_context = facade._as_dict(obj.get("commander_context"))
    if commander_context:
        found = facade.extract_commander_horizon_policy(commander_context)
        if found:
            return found
    commander_context_ref = facade._as_dict(obj.get("commander_context_ref"))
    if commander_context_ref:
        found = facade.extract_commander_horizon_policy(commander_context_ref)
        if found:
            return found
    return {}
