from typing import Any

def _blocker_family(*, code: str, primary_failure_axis: str, guard_blocked: bool, facade: Any) -> str:
    reason=str(code or "").strip().lower(); axis=str(primary_failure_axis or "").strip().lower()
    if guard_blocked: return "guard_intervention"
    if axis in {"vwap_relationship","pullback_structure","volume_confirmation","breakout_readiness","entry_confirmation","overextension","chart_structure_support","chart_structure_continuation"}: return axis
    if "chart_structure" in reason: return "chart_structure_guard"
    if "volume" in reason: return "volume_confirmation"
    if "reclaim" in reason or "vwap" in reason: return "vwap_relationship"
    if "pullback" in reason: return "pullback_structure"
    if "breakout" in reason: return "breakout_readiness"
    if "extend" in reason: return "overextension"
    if "confirmation" in reason: return "entry_confirmation"
    return "unknown"
