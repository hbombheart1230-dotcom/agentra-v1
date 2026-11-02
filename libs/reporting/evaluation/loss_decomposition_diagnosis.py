"""loss_decomposition: ``_diagnosis`` body (moved verbatim from ``loss_decomposition``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any


def _diagnosis(
    *,
    shadow: dict[str, Any],
    candidate_rank: list[dict[str, Any]],
    realized: dict[str, Any],
    entry: dict[str, Any],
    exit_hold: dict[str, Any],
    facade: Any,
) -> list[dict[str, Any]]:
    lane_rows = ((shadow.get("entry_lane_forward_outcomes") or {}).get("by_time_bucket") or [])
    buckets = {row.get("name"): row for row in lane_rows if isinstance(row, facade.Mapping)}
    opening = buckets.get("open_20_60m") or {}
    mid = buckets.get("mid_session") or {}
    findings = [
        {
            "stage": "raw_candidate_edge",
            "status": "CONDITIONAL_EDGE",
            "finding": (
                "Candidate edge is horizon- and time-bucket dependent, not universally absent. "
                f"open_20_60m +30m={opening.get('avg_return_30m_pct')}%, "
                f"+60m={opening.get('avg_return_60m_pct')}%; "
                f"mid_session +30m={mid.get('avg_return_30m_pct')}%, "
                f"+60m={mid.get('avg_return_60m_pct')}%."
            ),
        },
        {
            "stage": "scanner_ranking",
            "status": "PARTIAL_RECONSTRUCTION",
            "finding": (
                "Shadow rank/role outcomes are available, but a true pre-Strategist Scanner "
                "control universe is unavailable. Ranking quality can be diagnosed but not "
                "causally attributed to Strategist yet."
            ),
        },
        {
            "stage": "strategist_commander",
            "status": "MISSING_CONTROL",
            "finding": (
                "Historical raw Scanner and explicit Commander alternatives were not persisted. "
                "No value-add claim is allowed."
            ),
        },
        {
            "stage": "monitor_entry",
            "status": "DIAGNOSTIC",
            "finding": (
                f"{entry.get('matched_trade_count')} trades matched a nearby shadow baseline; "
                f"average entry price delta={entry.get('average_entry_price_delta_pct')}%."
            ),
        },
        {
            "stage": "monitor_exit",
            "status": "DIAGNOSTIC",
            "finding": (
                f"Post-exit hold alternatives were observed for {exit_hold.get('observed_trade_count')} trades."
            ),
        },
        {
            "stage": "realized_system",
            "status": "NEGATIVE",
            "finding": (
                f"Realized count={realized.get('performance', {}).get('count')}, "
                f"expectancy={realized.get('performance', {}).get('expectancy_pct')}%, "
                f"profit_factor={realized.get('performance', {}).get('profit_factor')}."
            ),
        },
    ]
    return findings
