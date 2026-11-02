"""loss_decomposition: ``_next_action`` body (moved verbatim from ``loss_decomposition``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any


def _next_action(
    *,
    role_rows: list[dict[str, Any]],
    realized: dict[str, Any],
    exit_hold: dict[str, Any],
    facade: Any,
) -> dict[str, Any]:
    roles = {str(row.get("name") or ""): row for row in role_rows}
    top_pick = roles.get("top_pick") or {}
    realized_expectancy = facade._to_float((realized.get("performance") or {}).get("expectancy_pct"))
    five_minute_exit = next(
        (
            row for row in exit_hold.get("by_hold_offset") or []
            if row.get("offset") == "+5m"
        ),
        {},
    )
    return {
        "priority": 1,
        "component": "candidate_edge_and_horizon_alignment",
        "decision": "FIX_BEFORE_ENTRY_OR_EXIT_TUNING",
        "reason": (
            "Top-pick gross forward edge is economically trivial relative to current round-trip "
            "cost, while the realized system is deeply negative. Exit delay improvement is too "
            "small to rescue the deficit."
        ),
        "evidence": {
            "top_pick_15m_pct": top_pick.get("avg_return_15m_pct"),
            "top_pick_30m_pct": top_pick.get("avg_return_30m_pct"),
            "top_pick_60m_pct": top_pick.get("avg_return_60m_pct"),
            "realized_expectancy_pct": realized_expectancy,
            "post_exit_5m_average_improvement_pct": five_minute_exit.get("average_improvement_pct"),
        },
        "required_follow_up": [
            "separate candidate scoring by time bucket and intended holding horizon",
            "treat mid-session candidate generation as a distinct negative-edge segment",
            "evaluate open_20_60m continuation against 30-60 minute holding targets",
            "do not tune exits first",
            "do not attribute the problem to Strategist until a trusted raw Scanner control exists",
        ],
        "behavior_change_authorized": False,
    }
