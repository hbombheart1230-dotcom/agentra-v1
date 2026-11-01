from __future__ import annotations
from typing import Any, Dict, Mapping

def _flatten_chart_structure_feature_states(chart_structure_features: Mapping[str, Any] | None, *, facade: Any) -> Dict[str, Dict[str, Any]]:
    payload = dict(chart_structure_features or {}) if isinstance(chart_structure_features, Mapping) else {}
    if not bool(payload.get("available")): return {}
    out: Dict[str, Dict[str, Any]] = {}
    for name, group in facade._CHART_FEATURE_GROUP_PATHS.items():
        group_payload = dict(payload.get(group) or {}) if isinstance(payload.get(group), Mapping) else {}
        state = group_payload.get(name)
        if state is None: continue
        state_text = str(state or "").strip()
        if not state_text: continue
        out[name] = {"state":state_text,"group":group,"source":f"chart_structure_features.{group}.{name}"}
    return out
