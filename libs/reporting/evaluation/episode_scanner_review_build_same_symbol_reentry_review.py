"""episode_scanner_review: ``build_same_symbol_reentry_review`` body (moved verbatim from ``episode_scanner_review``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Mapping, Sequence


def build_same_symbol_reentry_review(
    rows: Sequence[Mapping[str, Any]],
    *,
    facade: Any,
) -> dict[str, Any]:
    unique: dict[str, Mapping[str, Any]] = {}
    for row in rows:
        trade_id = str(row.get("trade_id") or "")
        if trade_id:
            unique[trade_id] = row

    grouped: dict[tuple[str, str], list[tuple[int, float, str]]] = facade.defaultdict(list)
    for trade_id, row in unique.items():
        parts = trade_id.split("_")
        if len(parts) < 4 or not parts[1].isdigit():
            continue
        value = facade._number(row.get("net_return_pct"))
        symbol = str(row.get("symbol") or "")
        if value is None or not symbol:
            continue
        try:
            sequence = int(parts[-1])
        except ValueError:
            sequence = 0
        grouped[(parts[1], symbol)].append((sequence, value, trade_id))

    first_values: list[float] = []
    repeat_values: list[float] = []
    repeat_after_loss_values: list[float] = []
    repeat_after_non_loss_values: list[float] = []
    repeated_groups = 0
    for values in grouped.values():
        ordered = sorted(values)
        first_values.append(ordered[0][1])
        for index, (_, value, _) in enumerate(ordered[1:], start=1):
            repeat_values.append(value)
            prior_value = ordered[index - 1][1]
            if prior_value < 0.0:
                repeat_after_loss_values.append(value)
            else:
                repeat_after_non_loss_values.append(value)
        if len(ordered) > 1:
            repeated_groups += 1

    first_metrics = facade.performance_metrics(first_values)
    repeat_metrics = facade.performance_metrics(repeat_values)
    repeat_after_loss_metrics = facade.performance_metrics(repeat_after_loss_values)
    repeat_after_non_loss_metrics = facade.performance_metrics(repeat_after_non_loss_values)
    return {
        "schema_version": "same_symbol_reentry_review.v1",
        "behavior_effect": "evaluation_only",
        "day_symbol_group_count": len(grouped),
        "repeated_day_symbol_group_count": repeated_groups,
        "first_entry": first_metrics,
        "repeat_entry": repeat_metrics,
        "repeat_after_loss": repeat_after_loss_metrics,
        "repeat_after_non_loss": repeat_after_non_loss_metrics,
        "repeat_minus_first_expectancy_pct": round(
            float(repeat_metrics.get("expectancy_pct") or 0.0)
            - float(first_metrics.get("expectancy_pct") or 0.0),
            4,
        ),
        "behavior_candidate_eligible": bool(
            len(repeat_after_loss_values) >= 20
            and float(repeat_after_loss_metrics.get("expectancy_pct") or 0.0)
            < float(first_metrics.get("expectancy_pct") or 0.0) - 0.20
            and float(repeat_after_loss_metrics.get("win_rate") or 0.0)
            < float(first_metrics.get("win_rate") or 0.0)
        ),
        "limitations": [
            "This is an observational prior-outcome-conditioned comparison.",
            "It supports damage reduction, not a claim that a cooldown creates alpha.",
        ],
    }
