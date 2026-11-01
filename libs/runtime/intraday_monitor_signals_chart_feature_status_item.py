from __future__ import annotations
from typing import Any, Dict, Mapping

def _chart_feature_status_item(*, spec: Mapping[str, Any], chart_states: Mapping[str, Any], blocker: bool=False, facade: Any) -> Dict[str, Any] | None:
    name=str(spec.get("name") or "").strip(); expected_state=str(spec.get("expected_state") or "").strip() or None
    feature=dict(chart_states.get(name) or {}) if isinstance(chart_states.get(name), Mapping) else {}
    if not feature: return None
    actual_state=str(feature.get("state") or "").strip() or None; source=feature.get("source"); status="unknown"
    if expected_state is not None:
        if actual_state is None: status="unknown"
        elif blocker: status="active" if actual_state == expected_state else "inactive"
        else: status="pass" if actual_state == expected_state else "fail"
    else:
        rules=facade._CHART_FEATURE_STATUS_RULES.get(name) or {}
        active_states={str(v).strip() for v in list(rules.get("blocker_active") or set()) if str(v).strip()}; inactive_states={str(v).strip() for v in list(rules.get("blocker_inactive") or set()) if str(v).strip()}; pass_states={str(v).strip() for v in list(rules.get("pass") or set()) if str(v).strip()}; fail_states={str(v).strip() for v in list(rules.get("fail") or set()) if str(v).strip()}
        if blocker:
            if actual_state in active_states: status="active"
            elif actual_state in inactive_states: status="inactive"
        else:
            if actual_state in pass_states: status="pass"
            elif actual_state in fail_states: status="fail"
    return {"name":name,"expected_state":expected_state,"actual_state":actual_state,"status":status,"source":source,"feature_level":"high_level_feature","spec_valid":bool(spec.get("is_valid", True)),"validation_notes":list(spec.get("validation_notes") or [])}
