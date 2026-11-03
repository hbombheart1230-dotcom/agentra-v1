"""full_chain_component_review: ``build_full_chain_component_review`` body (moved verbatim from ``full_chain_component_review``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any


def build_full_chain_component_review(
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
        drop_q9_row_keys=facade.Q9_ROW_KEYS_UNUSED_BY_FULL_CHAIN,  # never read below; ~80% of the q9 rows' bytes
    )
    candidates = facade._candidate_rows(payloads)
    all_models = facade._load_trade_models(reports_root, start, end)
    models = [model for model in all_models if facade._behavior_metric_eligible(model)]
    profile = facade.load_broker_cost_profile(cost_profile_path)
    cost_pct = float(
        profile.get("conservative_round_trip_cost_pct")
        or profile.get("ema_round_trip_cost_pct")
        or 0.009
    ) * 100.0
    slippage_pct = max(
        0.0,
        float(facade.os.getenv("Q9_EVALUATION_SLIPPAGE_PCT", str(facade.DEFAULT_Q9_SLIPPAGE_PCT)) or facade.DEFAULT_Q9_SLIPPAGE_PCT),
    )
    scanner_quality = facade.build_scanner_quality_review(
        payloads,
        cost_pct=cost_pct,
        slippage_pct=slippage_pct,
    )
    role_metrics = [
        facade._role_metrics(candidates, role=role, horizon=horizon, cost_pct=cost_pct)
        for role in ("top_pick", "runner_up_evaluated")
        for horizon in facade.HORIZONS
    ]
    paired = [facade._paired_role_deltas(candidates, horizon=horizon) for horizon in facade.HORIZONS]
    availability = facade._selection_availability(models)
    decision_attribution = facade._decision_window_attribution(payloads, cost_pct=cost_pct)
    entry = facade._entry_timing_summary(models, candidates)
    exit_hold = facade._exit_hold_summary(models)
    realized = facade._realized_trade_summary(models)
    problem_segment = facade._classify_root_cause(
        scanner_quality=scanner_quality,
        attribution=decision_attribution,
        entry=entry,
        exit_hold=exit_hold,
    )
    scanner = facade._scanner_decision(role_metrics=role_metrics, paired=paired)
    entry_count = int(entry.get("matched_trade_count") or 0)
    entry_days = int(entry.get("matched_day_count") or 0)
    entry_enough = entry_count >= facade.DIRECTIONAL_MIN_OBSERVATIONS and entry_days >= facade.DIRECTIONAL_MIN_DAYS
    entry_average = facade._number(entry.get("average_entry_price_delta_pct"))
    entry_median = facade._number(entry.get("median_entry_price_delta_pct"))
    entry_decision = (
        facade.DecisionClass.RETAIN.value
        if entry_enough
        and entry_average is not None
        and entry_median is not None
        and entry_average <= 0.30
        and entry_median <= 0.30
        else facade.DecisionClass.ADJUST_AND_RETEST.value
        if entry_enough
        else facade.DecisionClass.INSUFFICIENT_EVIDENCE.value
    )
    exit_count = int(exit_hold.get("observed_trade_count") or 0)
    exit_days = int(exit_hold.get("observed_day_count") or 0)
    exit_enough = exit_count >= facade.DIRECTIONAL_MIN_OBSERVATIONS and exit_days >= facade.DIRECTIONAL_MIN_DAYS
    five_minute = next(
        (row for row in exit_hold.get("by_hold_offset") or [] if row.get("offset") == "+5m"),
        {},
    )
    exit_decision = (
        facade.DecisionClass.ADJUST_AND_RETEST.value
        if exit_enough and float(five_minute.get("average_improvement_pct") or 0.0) >= 0.30
        else facade.DecisionClass.RETAIN.value
        if exit_enough
        else facade.DecisionClass.INSUFFICIENT_EVIDENCE.value
    )
    realized_performance = realized.get("performance") or {}
    realized_count = int(realized_performance.get("count") or 0)
    realized_days = len(
        {
            str(model.get("day") or "")[:10]
            for model in models
            if (model.get("outcome") or {}).get("net_return_pct") is not None
        }
    )
    full_system_enough = (
        realized_count >= facade.DIRECTIONAL_MIN_OBSERVATIONS
        and realized_days >= facade.DIRECTIONAL_MIN_DAYS
    )
    full_system_decision = (
        facade.DecisionClass.RETAIN.value
        if full_system_enough
        and float(realized_performance.get("expectancy_pct") or 0.0) > 0.0
        else facade.DecisionClass.REJECT.value
        if full_system_enough
        else facade.DecisionClass.INSUFFICIENT_EVIDENCE.value
    )
    components = {
        "scanner": {
            **scanner,
            "role_cost_adjusted_metrics": role_metrics,
            "paired_role_comparisons": paired,
            "evidence_class": "TRUSTED_SHADOW",
            "behavior_change_authorized": False,
        },
        "strategist": facade._attribution_component(
            attribution=decision_attribution,
            component="strategist",
            question="Does the strategy ranking overlay improve the same-universe intrinsic Scanner ranking?",
            missing_comparison="same-universe intrinsic and strategy-weighted Scanner outcomes",
            availability=availability,
        ),
        "commander": facade._attribution_component(
            attribution=decision_attribution,
            component="commander",
            question="Does Commander selection or veto improve the Strategist-selected outcome?",
            missing_comparison="explicit Commander alternative or veto joined to forward outcomes",
            availability=availability,
        ),
        "monitor_entry": {
            "decision": entry_decision,
            "question": "Does Monitor improve entry timing relative to the selected candidate baseline?",
            "finding": (
                "Actual entries were not systematically later or more expensive than the nearby "
                "same-symbol shadow baseline; entry timing is not the first demonstrated loss source."
                if entry_decision == facade.DecisionClass.RETAIN.value
                else "Entry timing requires adjustment."
                if entry_decision == facade.DecisionClass.ADJUST_AND_RETEST.value
                else "The minimum directional comparison count was not reached."
            ),
            "evidence_class": "RECONSTRUCTED",
            "metrics": entry,
            "missing_comparison": (
                None
                if entry_enough
                else "at least 20 actual-entry versus selected-baseline matches across 2 days"
            ),
            "behavior_change_authorized": False,
        },
        "monitor_exit": {
            "decision": exit_decision,
            "question": "Does Monitor exit too early or surrender material value?",
            "finding": (
                "Observed post-exit improvement is too small to identify exit timing as the primary "
                "loss source."
                if exit_decision == facade.DecisionClass.RETAIN.value
                else "Post-exit improvement is large enough to justify a bounded exit-policy review."
                if exit_decision == facade.DecisionClass.ADJUST_AND_RETEST.value
                else "Only 16 exits have post-exit observations; this is below the fixed 20-observation threshold."
            ),
            "evidence_class": "REALIZED_PLUS_POST_EXIT_SHADOW",
            "metrics": exit_hold,
            "missing_comparison": (
                None
                if exit_enough
                else "at least 20 exits with observed post-exit checkpoints across 2 days"
            ),
            "behavior_change_authorized": False,
        },
        "full_system": {
            "decision": full_system_decision,
            "question": "Does the integrated system currently produce positive broker-net value?",
            "finding": (
                "The integrated system produced positive broker-net expectancy for the analyzed range."
                if full_system_decision == facade.DecisionClass.RETAIN.value
                else "The current positive-edge hypothesis is rejected for the analyzed range."
                if full_system_decision == facade.DecisionClass.REJECT.value
                else "The fixed realized-trade and day minimum has not been reached."
            ),
            "evidence_class": "REALIZED",
            "metrics": realized,
            "missing_comparison": (
                None
                if full_system_enough
                else "at least 20 realized trades across 2 days"
            ),
            "behavior_change_authorized": False,
        },
    }
    components["strategist"]["scope"] = "ranking_overlay_only"
    components["strategist"]["full_strategist_contribution"] = facade._unavailable_component(
        question="Does the complete Strategist improve a strategy-neutral Scanner pipeline?",
        missing_comparison="parallel strategy-neutral candidate sourcing and ranking shadow",
        availability=availability,
    )
    refresh_primary = next(
        (
            row
            for row in decision_attribution.get("by_horizon") or []
            if row.get("horizon") == "+30m"
        ),
        {},
    )
    refresh_count = int(refresh_primary.get("post_scanner_refresh_comparison_count") or 0)
    refresh_days = int(refresh_primary.get("post_scanner_refresh_day_count") or 0)
    refresh_delta = facade._number(refresh_primary.get("average_post_scanner_refresh_delta_pct"))
    refresh_positive_rate = facade._number(refresh_primary.get("post_scanner_refresh_positive_delta_rate"))
    refresh_enough = refresh_count >= facade.DIRECTIONAL_MIN_OBSERVATIONS and refresh_days >= facade.DIRECTIONAL_MIN_DAYS
    refresh_material = bool(
        refresh_enough
        and refresh_delta is not None
        and refresh_positive_rate is not None
        and refresh_delta >= facade.MIN_MATERIAL_RANKING_DELTA_PCT
        and refresh_positive_rate >= facade.MIN_POSITIVE_RANKING_DELTA_RATE
    )
    components["strategist"]["post_scanner_refresh"] = {
        "decision": (
            facade.DecisionClass.PROMOTION_CANDIDATE.value
            if refresh_material
            else facade.DecisionClass.ADJUST_AND_RETEST.value
            if refresh_enough
            else facade.DecisionClass.INSUFFICIENT_EVIDENCE.value
        ),
        "question": "Does the optional post-Scanner Strategist refresh improve the first Scanner result?",
        "finding": (
            f"Observed {refresh_count} paired +30m refresh windows across {refresh_days} day(s)."
        ),
        "missing_comparison": (
            None
            if refresh_count >= facade.DIRECTIONAL_MIN_OBSERVATIONS and refresh_days >= facade.DIRECTIONAL_MIN_DAYS
            else f"at least {facade.DIRECTIONAL_MIN_OBSERVATIONS} refresh pairs across {facade.DIRECTIONAL_MIN_DAYS} days"
        ),
        "metrics": {
            key: value
            for key, value in refresh_primary.items()
            if "post_scanner_refresh" in key or key == "horizon"
        },
        "behavior_change_authorized": False,
    }
    return {
        "schema_version": "q9_full_chain_component_review.v1",
        "contract_version": facade.CONTRACT_VERSION,
        "behavior_effect": "evaluation_only",
        "range": {"start": start[:10], "end": end[:10]},
        "cost_model": {
            "source": str(profile.get("source") or "fallback"),
            "sample_count": int(profile.get("sample_count") or 0),
            "conservative_round_trip_cost_pct": round(cost_pct, 4),
            "evaluation_slippage_pct": round(slippage_pct, 4),
        },
        "evidence": {
            "shadow_payload_count": len(payloads),
            "deduped_shadow_candidate_count": len(candidates),
            "trade_model_count": len(models),
            "total_trade_model_count": len(all_models),
            "excluded_trade_model_count": len(all_models) - len(models),
            "selection_availability": availability,
            "decision_window_attribution": decision_attribution,
            "scanner_quality": scanner_quality,
        },
        "problem_segment": problem_segment,
        "component_decisions": components,
        "overall_decision": {
            "decision": (
                facade.DecisionClass.ADJUST_AND_RETEST.value
                if full_system_enough
                else facade.DecisionClass.INSUFFICIENT_EVIDENCE.value
            ),
            "first_actionable_component": (
                "scanner_candidate_quality_and_horizon_calibration"
                if full_system_enough
                else "artifact_and_forward_evidence_collection"
            ),
            "reason": (
                "The fixed realized-trade and multi-day thresholds are not complete; continue "
                "the frozen forward window without changing trading behavior."
                if not full_system_enough
                else "Scanner ordering does not show a material relative advantage and selected "
                "candidates remain cost-negative. Monitor entry is not the first demonstrated "
                "failure, and Monitor exit has insufficient observations."
            ),
            "behavior_change_authorized": False,
        },
        "closure": {
            "historical_review_complete": True,
            "open_ended_extension_authorized": False,
            "remaining_forward_requirement": (
                "Persist trusted A/B/C decision snapshots and reach the fixed missing-comparison "
                "thresholds; do not add new diagnostic categories."
            ),
        },
    }
