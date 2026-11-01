from __future__ import annotations
from typing import Any, Dict

def _parse_policy_signal_spec(spec: Any, *, facade: Any) -> Dict[str, Any]:
    normalized = facade.normalize_policy_check_spec(spec)
    return {"name":str(normalized.get("feature_name") or normalized.get("raw") or "").strip(),"expected_state":normalized.get("expected_state"),"raw":str(normalized.get("raw") or "").strip(),"feature_level":normalized.get("feature_level"),"is_valid":bool(normalized.get("is_valid")),"validation_notes":list(normalized.get("validation_notes") or [])}
