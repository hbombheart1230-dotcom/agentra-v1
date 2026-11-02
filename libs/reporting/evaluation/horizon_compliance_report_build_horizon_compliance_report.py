"""horizon_compliance_report: ``build_horizon_compliance_report`` body (moved verbatim from ``horizon_compliance_report``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from collections import Counter
from typing import Any, Mapping, Sequence


def build_horizon_compliance_report(
    evaluations: Sequence[Mapping[str, Any]],
    *,
    facade: Any,
) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    grouped: dict[tuple[str, str], dict[str, Any]] = facade.defaultdict(
        lambda: {
            "count": 0,
            "returns": [],
            "before_min": 0,
            "before_target": 0,
            "beyond_max": 0,
            "target_improve": 0,
            "violation": 0,
            "hard_or_allowed": 0,
            "actual_hold_sec": [],
        }
    )
    horizon_counts: Counter[str] = facade.Counter()
    excluded_count = 0
    exit_incident_excluded_count = 0
    for evaluation in evaluations:
        integrity = facade._mapping(evaluation.get("integrity"))
        if integrity.get("promotion_metric_eligible") is False:
            excluded_count += 1
            continue
        if integrity.get("exit_metric_eligible") is False:
            exit_incident_excluded_count += 1
            continue
        horizon = facade._mapping(evaluation.get("horizon_alignment"))
        outcome = facade._mapping(evaluation.get("realized_outcome"))
        strategy_horizon = str(horizon.get("strategy_horizon") or "unknown")
        exit_quality = facade._mapping(evaluation.get("exit_quality"))
        exit_reason = str(exit_quality.get("reason") or "unknown")
        actual_hold = facade._num(horizon.get("actual_hold_sec") or outcome.get("holding_seconds"))
        net_return = facade._num(outcome.get("net_return_pct"))
        row = {
            "trade_id": evaluation.get("trade_id"),
            "symbol": evaluation.get("symbol"),
            "strategy_horizon": strategy_horizon,
            "exit_reason": exit_reason,
            "bucket": str(horizon.get("bucket") or "unknown"),
            "actual_hold_sec": actual_hold,
            "expected_hold_window": facade._mapping(horizon.get("expected_hold_window")),
            "net_return_pct": net_return,
            "exited_before_min_hold": bool(horizon.get("exited_before_min_hold")),
            "exited_before_target_hold": bool(horizon.get("exited_before_target_hold")),
            "exited_beyond_max_hold": bool(horizon.get("exited_beyond_max_hold")),
            "horizon_violation_candidate": bool(horizon.get("horizon_violation_candidate")),
            "target_hold_would_improve_exit": bool(horizon.get("target_hold_would_improve_exit")),
            "valid_early_exit": bool(horizon.get("valid_early_exit")),
            "early_exit_allowed_match": list(horizon.get("early_exit_allowed_match") or []),
            "target_checkpoint": facade._mapping(horizon.get("target_checkpoint")),
            "max_post_exit_upside_pct": horizon.get("max_post_exit_upside_pct"),
            "max_post_exit_drawdown_pct": horizon.get("max_post_exit_drawdown_pct"),
        }
        rows.append(row)
        horizon_counts[strategy_horizon] += 1
        group = grouped[facade._bucket_key(evaluation)]
        group["count"] += 1
        if net_return is not None:
            group["returns"].append(float(net_return))
        if actual_hold is not None:
            group["actual_hold_sec"].append(float(actual_hold))
        if row["exited_before_min_hold"]:
            group["before_min"] += 1
        if row["exited_before_target_hold"]:
            group["before_target"] += 1
        if row["exited_beyond_max_hold"]:
            group["beyond_max"] += 1
        if row["target_hold_would_improve_exit"]:
            group["target_improve"] += 1
        if row["horizon_violation_candidate"]:
            group["violation"] += 1
        if row["valid_early_exit"] or row["early_exit_allowed_match"]:
            group["hard_or_allowed"] += 1

    group_rows: list[dict[str, Any]] = []
    for (strategy_horizon, exit_reason), group in sorted(grouped.items()):
        hold_values = group["actual_hold_sec"]
        metrics = facade.performance_metrics(group["returns"])
        group_rows.append({
            "strategy_horizon": strategy_horizon,
            "exit_reason": exit_reason,
            "count": group["count"],
            "average_hold_sec": round(sum(hold_values) / len(hold_values), 2) if hold_values else None,
            "exit_before_min_hold_count": group["before_min"],
            "exit_before_target_hold_count": group["before_target"],
            "exit_beyond_max_hold_count": group["beyond_max"],
            "horizon_violation_candidate_count": group["violation"],
            "target_hold_would_improve_exit_count": group["target_improve"],
            "valid_or_allowed_early_exit_count": group["hard_or_allowed"],
            "performance": metrics,
        })

    return {
        "schema_version": "horizon_compliance_report.v1",
        "behavior_effect": "observation_only",
        "trade_count": len(rows),
        "excluded_trade_count": excluded_count,
        "exit_incident_excluded_trade_count": exit_incident_excluded_count,
        "horizon_counts": dict(horizon_counts),
        "group_rows": group_rows,
        "rows": rows,
        "policy_warning": (
            "Do not convert this into delayed exits directly. Promotion requires "
            "target-hold improvement by horizon and exit reason."
        ),
    }
