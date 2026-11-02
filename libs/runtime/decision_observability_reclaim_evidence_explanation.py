from typing import Any

def _reclaim_evidence_explanation(*, reclaim_blocked: bool, reclaim_gate_ok: bool | None, vwap_hold_ok: bool | None, vwap_reclaim_ok: bool | None, reclaim_distance_to_ready: Any, reclaim_readiness_tuned: bool, facade: Any) -> str:
    if reclaim_readiness_tuned: return "VWAP reclaim was slightly short of the standard near-ready band, but small_relaxation_v1 allowed the breakout path because supporting evidence stayed intact."
    if bool(reclaim_gate_ok):
        if bool(vwap_reclaim_ok) and not bool(vwap_hold_ok): return "VWAP reclaim confirmation is in place even though the hold check is still marginal."
        return "VWAP hold condition is satisfied." if bool(vwap_hold_ok) else "VWAP reclaim gate is satisfied."
    if reclaim_blocked:
        distance=facade._to_float(reclaim_distance_to_ready)
        return f"VWAP reclaim confirmation is still short of ready state (distance_to_ready={distance:.4f})." if distance else "VWAP reclaim confirmation is still short of ready state."
    return ""
