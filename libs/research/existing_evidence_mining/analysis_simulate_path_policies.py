"""RF-039 existing_evidence_mining: ``simulate_path_policies`` body (moved verbatim from ``analysis``).

``facade`` is the ``analysis`` module; module-level names and helpers are resolved on it at call time so caller
monkeypatching keeps working. This module never imports ``analysis``. Pure, no IO.
"""
from __future__ import annotations

from typing import Any, Iterable, Mapping


def simulate_path_policies(
    episodes: list[Mapping[str, Any]],
    *,
    minute_rows_by_symbol: Mapping[str, list[Mapping[str, Any]]],
    facade: Any,
) -> dict[str, Any]:
    policy_returns: dict[str, list[float]] = facade.defaultdict(list)
    policy_reasons: dict[str, dict[str, int]] = facade.defaultdict(lambda: facade.defaultdict(int))
    for episode in episodes:
        symbol = str(episode.get("symbol") or "")
        day = str(episode.get("day") or "")
        baseline_epoch = int(episode.get("baseline_epoch") or 0)
        baseline_price = float(episode.get("baseline_price") or 0.0)
        rows = [
            row
            for row in minute_rows_by_symbol.get(symbol) or []
            if baseline_epoch <= int(row.get("ts") or 0) <= baseline_epoch + 30 * 60
            and str(row.get("raw_ts") or "")[:8] in ("", day.replace("-", ""))
        ]
        if not rows or baseline_price <= 0.0:
            continue
        for policy in facade.PATH_POLICIES:
            target = baseline_price * (1.0 + float(policy["target_pct"]) / 100.0)
            stop = baseline_price * (1.0 - float(policy["stop_pct"]) / 100.0)
            exit_price = float(rows[-1].get("close") or baseline_price)
            reason = "time_exit"
            for bar in rows:
                low_hit = float(bar.get("low") or exit_price) <= stop
                high_hit = float(bar.get("high") or exit_price) >= target
                if low_hit:
                    exit_price = stop
                    reason = "stop"
                    break
                if high_hit:
                    exit_price = target
                    reason = "target"
                    break
            net = (exit_price / baseline_price - 1.0) * 100.0 - facade.LIVE_COST_PCT
            policy_id = str(policy["policy_id"])
            policy_returns[policy_id].append(net)
            policy_reasons[policy_id][reason] += 1
    return {
        policy_id: {
            "metrics": facade.performance_metrics(values),
            "exit_reasons": dict(policy_reasons[policy_id]),
            "conservative_same_bar_rule": "stop_before_target",
        }
        for policy_id, values in sorted(policy_returns.items())
    }
