"""cumulative_improvement_review: ``_candidate_rows`` body (moved verbatim from ``cumulative_improvement_review``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Mapping


def _candidate_rows(
    *,
    episode_review: Mapping[str, Any],
    reentry_review: Mapping[str, Any],
    post_reclaim_review: Mapping[str, Any],
    strategist_review: Mapping[str, Any],
    facade: Any,
) -> list[dict[str, Any]]:
    rank1 = facade._rank_row(episode_review, bucket="rank1", horizon="+30m")
    rank23 = facade._rank_row(episode_review, bucket="rank2_3", horizon="+30m")
    rank1_live = float(
        (rank1.get("live_net") or {}).get("expectancy_pct") or 0.0
    )
    rank23_live = float(
        (rank23.get("live_net") or {}).get("expectancy_pct") or 0.0
    )
    strategist_30 = next(
        (
            row
            for row in strategist_review.get("rows") or []
            if isinstance(row, facade.Mapping) and row.get("horizon") == "+30m"
        ),
        {},
    )
    return [
        {
            "priority": 1,
            "candidate": "same_symbol_loss_reentry_control",
            "class": "damage_reduction",
            "status": (
                "APPLIED_2026_07_29"
                if reentry_review.get("behavior_candidate_eligible")
                else "INSUFFICIENT_EVIDENCE"
            ),
            "evidence": {
                "repeat_count": (reentry_review.get("repeat_entry") or {}).get("count"),
                "repeat_expectancy_pct": (
                    reentry_review.get("repeat_entry") or {}
                ).get("expectancy_pct"),
                "repeat_minus_first_expectancy_pct": reentry_review.get(
                    "repeat_minus_first_expectancy_pct"
                ),
                "repeat_after_loss": reentry_review.get("repeat_after_loss"),
                "repeat_after_non_loss": reentry_review.get(
                    "repeat_after_non_loss"
                ),
            },
        },
        {
            "priority": 2,
            "candidate": "confirmed_post_reclaim_pullback_subtype",
            "class": "alpha_research",
            "status": post_reclaim_review.get("promotion_status"),
            "evidence": {
                "observed_count": post_reclaim_review.get("observed_count"),
                "observed_day_count": post_reclaim_review.get("observed_day_count"),
                "horizon_rows": post_reclaim_review.get("rows"),
            },
        },
        {
            "priority": 3,
            "candidate": "scanner_rank_ordering_component_review",
            "class": "ranking_diagnosis",
            "status": (
                "DIAGNOSTIC_CANDIDATE"
                if rank1_live <= 0 and rank23_live <= 0
                and (episode_review.get("score_component_review") or {}).get(
                    "status"
                )
                == "READY"
                else "OBSERVABILITY_NOT_READY"
                if (episode_review.get("score_component_review") or {}).get(
                    "status"
                )
                != "READY"
                else "RETAIN_UNDER_OBSERVATION"
            ),
            "evidence": {
                "rank1_live_net_30m_pct": rank1_live,
                "rank2_3_live_net_30m_pct": rank23_live,
                "rank1_minus_rank2_3_gross_30m_pct": episode_review.get(
                    "rank1_minus_rank2_3_gross_30m_pct"
                ),
                "score_component_review": episode_review.get(
                    "score_component_review"
                ),
            },
        },
        {
            "priority": 4,
            "candidate": "strategist_ranking_weight_guard",
            "class": "strategist_effectiveness",
            "status": (
                "DIAGNOSTIC_CANDIDATE"
                if float(
                    strategist_30.get("avg_strategist_minus_scanner_pct") or 0.0
                )
                < 0
                else "RETAIN_UNDER_OBSERVATION"
            ),
            "evidence": dict(strategist_30),
        },
    ]
