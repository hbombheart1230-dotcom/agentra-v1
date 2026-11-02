"""horizon_alignment: ``build_horizon_alignment_review`` body (moved verbatim from ``horizon_alignment``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any


def build_horizon_alignment_review(
    *,
    reports_root: Path,
    start: str,
    end: str,
    cost_profile_path: Path | None = None,
    facade: Any,
) -> dict[str, Any]:
    payloads = facade.load_quant_shadow_candidate_payloads_for_range(
        reports_root=reports_root,
        start=start,
        end=end,
    )
    candidates = facade._candidate_rows(payloads)
    profile = facade.load_broker_cost_profile(cost_profile_path)
    cost_ratio = float(
        profile.get("conservative_round_trip_cost_pct")
        or profile.get("ema_round_trip_cost_pct")
        or 0.009
    )
    cost_pct = cost_ratio * 100.0
    time_tactic = facade._combo_rows(
        candidates,
        dimensions=("time_bucket", "tactic"),
        cost_pct=cost_pct,
    )
    time_lane = facade._combo_rows(
        candidates,
        dimensions=("time_bucket", "primary_lane"),
        cost_pct=cost_pct,
    )
    time_tactic_rail = facade._combo_rows(
        candidates,
        dimensions=("time_bucket", "tactic", "market_regime_rail"),
        cost_pct=cost_pct,
    )
    candidates_for_adoption = [
        row for row in time_tactic
        if row.get("cost_positive")
    ]
    observation_candidates = [
        row for row in time_tactic
        if row.get("decision") == "RETAIN_UNDER_OBSERVATION"
    ]
    decision = (
        "CONTROLLED_ADOPTION_CANDIDATE_FOUND"
        if candidates_for_adoption
        else "RETAIN_UNDER_OBSERVATION"
        if observation_candidates
        else "NO_COST_POSITIVE_COMBINATION"
    )
    return {
        "schema_version": "horizon_alignment_review.v2",
        "behavior_effect": "evaluation_only",
        "range": {"start": start[:10], "end": end[:10]},
        "cost_model": {
            "source": str(profile.get("source") or "fallback"),
            "sample_count": int(profile.get("sample_count") or 0),
            "ema_round_trip_cost_pct": float(profile.get("ema_round_trip_cost_pct") or 0.0) * 100.0,
            "conservative_round_trip_cost_pct": cost_pct,
            "profile_path": str(cost_profile_path or "data/state/broker_cost_profile.json"),
        },
        "eligibility_contract": {
            "minimum_observations": facade.MIN_OBSERVATIONS,
            "minimum_days": facade.MIN_DAYS,
            "maximum_day_share": facade.MAX_DAY_SHARE,
            "maximum_symbol_share": facade.MAX_SYMBOL_SHARE,
            "net_profit_factor_min": facade.MIN_NET_PROFIT_FACTOR,
            "average_net_return_min_pct": facade.MIN_AVERAGE_NET_RETURN_PCT,
            "leave_one_day_out_net_return_positive": True,
        },
        "candidate_count": len(candidates),
        "decision": decision,
        "controlled_adoption_candidates": candidates_for_adoption,
        "observation_candidates": observation_candidates,
        "time_tactic": time_tactic,
        "time_lane": time_lane,
        "time_tactic_market_rail": time_tactic_rail,
        "next_action": {
            "behavior_change_authorized": False,
            "decision": (
                "PREPARE_SHADOW_POLICY_SPEC"
                if candidates_for_adoption
                else "KEEP_FIXED_SHADOW_OBSERVATION"
                if observation_candidates
                else "REJECT_CURRENT_HYPOTHESIS_AND_RESEARCH_NEW_ALPHA"
            ),
            "reason": (
                "At least one time/tactic/horizon combination remains materially positive after "
                "observed costs, concentration checks, and leave-one-day-out validation."
                if candidates_for_adoption
                else "A combination is marginally positive after cost but fails the fixed robustness "
                "contract; it is not eligible for controlled adoption."
                if observation_candidates
                else "No time/tactic/horizon combination survives observed cost and robustness checks."
            ),
        },
    }
