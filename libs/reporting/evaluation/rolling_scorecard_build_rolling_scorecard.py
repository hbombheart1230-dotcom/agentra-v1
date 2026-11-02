"""rolling_scorecard: ``build_rolling_scorecard`` body (moved verbatim from ``rolling_scorecard``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from collections import Counter
from typing import Any


def build_rolling_scorecard(scorecards: list[dict[str, Any]], *, window_days: int, facade: Any) -> dict[str, Any]:
    selected = sorted(scorecards, key=lambda row: str(row.get("day") or ""))[-window_days:]
    eligible_days = [
        row for row in selected
        if (
            str((((row.get("evaluation_phase") or {}).get("q9_day_validity") or {}).get("status")) or "")
            == "VALID"
            or (
                not ((row.get("evaluation_phase") or {}).get("q9_day_validity"))
                and str(
                    (((row.get("evaluation_phase") or {}).get("full_chain_start_gate") or {}).get("status"))
                    or ""
                )
                == "READY"
            )
        )
    ]
    returns: list[float] = []
    status_counts: Counter[str] = facade.Counter()
    for row in eligible_days:
        performance = row.get("realized_performance") if isinstance(row.get("realized_performance"), dict) else {}
        samples = performance.get("return_samples_pct")
        if isinstance(samples, list):
            returns.extend(float(value) for value in samples)
        status_counts.update((row.get("artifact_integrity") or {}).get("status_counts") or {})
    valid_days = len(eligible_days)
    if len(returns) < facade.DIRECTIONAL_MIN_OBSERVATIONS or valid_days < facade.DIRECTIONAL_MIN_DAYS:
        decision = facade.DecisionClass.INSUFFICIENT_EVIDENCE.value
    elif sum(returns) / len(returns) < 0:
        decision = facade.DecisionClass.ADJUST_AND_RETEST.value
    else:
        decision = facade.DecisionClass.RETAIN.value
    realized_performance = facade.performance_metrics(returns)
    realized_performance["return_samples_pct"] = returns
    return {
        "schema_version": "rolling_scorecard.v1",
        "contract_version": facade.CONTRACT_VERSION,
        "window_days": window_days,
        "start_day": selected[0].get("day") if selected else "",
        "end_day": selected[-1].get("day") if selected else "",
        "valid_day_count": valid_days,
        "decision_class": decision,
        "realized_performance": realized_performance,
        "integrity_status_counts": dict(status_counts),
        "source_days": [row.get("day") for row in selected],
        "forward_window_eligible_days": [row.get("day") for row in eligible_days],
        "excluded_pre_start_gate_days": [
            row.get("day") for row in selected if row not in eligible_days
        ],
    }
