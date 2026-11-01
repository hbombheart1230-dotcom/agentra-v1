from __future__ import annotations

from typing import Any, Dict, List, Mapping, Sequence


def _runner_row(trace: Mapping[str, Any], ranked_by_symbol: Mapping[str, Dict[str, Any]], *, facade: Any):
    symbol = facade._symbol(trace)
    base = facade._candidate_context(ranked_by_symbol.get(symbol, {}))
    base.update(
        {
            "symbol": symbol,
            "shadow_role": "runner_up_evaluated",
            "evaluated": True,
            "rank": trace.get("rank") or base.get("rank"),
            "score_total": trace.get("score_total") or base.get("score_total"),
            "triggered": facade._bool(trace.get("triggered")),
            "guard_blocked": facade._bool(trace.get("guard_blocked")),
            "guard_reason": facade._text(trace.get("guard_reason")),
            "intent_submitted": facade._bool(trace.get("intent_submitted")),
            "buy_blocked_open_position": facade._bool(trace.get("buy_blocked_open_position")),
            "buy_blocked_same_symbol": facade._bool(trace.get("buy_blocked_same_symbol")),
            "buy_blocked_pending_buy": facade._bool(trace.get("buy_blocked_pending_buy")),
            "buy_blocked_post_exit_cooldown": facade._bool(trace.get("buy_blocked_post_exit_cooldown")),
            "buy_blocked_closeout_window": facade._bool(trace.get("buy_blocked_closeout_window")),
            "reason": facade._text(trace.get("reason")),
            "primary_failure_axis": facade._text(trace.get("primary_failure_axis")),
            "transition_readiness_score": trace.get("transition_readiness_score"),
            "vwap_distance": trace.get("vwap_distance"),
            "volume_ratio": trace.get("volume_ratio"),
            "breakout_ok": trace.get("breakout_ok"),
            "pullback_ok": trace.get("pullback_ok"),
            "extension_ok": trace.get("extension_ok"),
            "confidence_score": trace.get("confidence_score"),
            "confidence_threshold": trace.get("confidence_threshold"),
            "runner_up_quality_gate": facade._as_dict(trace.get("runner_up_quality_gate")),
            "pullback_evidence_profile": facade._as_dict(trace.get("pullback_evidence_profile")),
            "runner_up_quality_blocked": facade._bool(trace.get("runner_up_quality_blocked")),
            "weak_fallback_blocked": facade._bool(trace.get("weak_fallback_blocked")),
            "entry_cost_filter": facade._as_dict(trace.get("entry_cost_filter")),
            "directional_edge_estimate": facade._as_dict(
                trace.get("directional_edge_estimate")
            ),
        }
    )
    base["would_enter"] = (
        facade._bool(base.get("triggered"))
        and not facade._bool(base.get("guard_blocked"))
        and not facade._bool(base.get("runner_up_quality_blocked"))
        and not facade._bool(base.get("weak_fallback_blocked"))
    )
    return base
