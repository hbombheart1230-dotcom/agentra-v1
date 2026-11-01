from __future__ import annotations
from typing import Any, Dict, Mapping

def _extract_commander_entry_control(policy: Any, frame: Mapping[str, Any] | None, *, facade: Any) -> Dict[str, Any]:
    candidates=[]
    if isinstance(policy, Mapping):
        raw_policy=facade.extract_monitor_entry_policy_mapping(policy); candidates.extend([raw_policy.get("commander_entry_control"),raw_policy.get("entry_control")])
    if isinstance(frame, Mapping):
        commander_context=frame.get("commander_context")
        if isinstance(commander_context, Mapping): candidates.extend([commander_context.get("commander_entry_control"),commander_context.get("entry_control")])
    for candidate in candidates:
        if isinstance(candidate, Mapping): return dict(candidate or {})
    return {}
