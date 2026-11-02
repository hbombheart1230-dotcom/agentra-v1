"""loss_decomposition: ``_exit_hold_summary`` body (moved verbatim from ``loss_decomposition``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any


def _exit_hold_summary(models: list[dict[str, Any]], *, facade: Any) -> dict[str, Any]:
    improvements: dict[str, list[float]] = facade.defaultdict(list)
    examples: list[dict[str, Any]] = []
    observed_trade_count = 0
    observed_days: set[str] = set()
    for model in models:
        realized = facade._to_float((model.get("outcome") or {}).get("net_return_pct"))
        post_exit = (model.get("monitor") or {}).get("post_exit")
        post_exit = post_exit if isinstance(post_exit, facade.Mapping) else {}
        checkpoints = post_exit.get("checkpoints")
        checkpoints = checkpoints if isinstance(checkpoints, facade.Mapping) else {}
        trade_values: dict[str, float] = {}
        for label in ("+5m", "+15m", "+30m", "+60m"):
            row = checkpoints.get(label)
            if not isinstance(row, facade.Mapping) or row.get("status") != "observed":
                continue
            ratio = facade._to_float(row.get("return_pct"))
            if ratio is None:
                continue
            delta_pct = ratio * 100.0
            improvements[label].append(delta_pct)
            trade_values[label] = round(delta_pct, 4)
        if trade_values:
            observed_trade_count += 1
            observed_days.add(str(model.get("day") or "")[:10])
            examples.append({
                "trade_id": model.get("trade_id"),
                "symbol": model.get("symbol"),
                "realized_net_return_pct": realized,
                "hold_improvement_pct": trade_values,
            })
    return {
        "observed_trade_count": observed_trade_count,
        "observed_day_count": len({day for day in observed_days if day}),
        "by_hold_offset": [
            {
                "offset": label,
                "count": len(values),
                "average_improvement_pct": round(sum(values) / len(values), 4),
                "improved_count": sum(1 for value in values if value > 0),
                "worsened_count": sum(1 for value in values if value < 0),
            }
            for label, values in improvements.items()
        ],
        "examples": examples[:20],
        "limitation": "price delta after actual exit; realized fees remain fixed and re-entry is not assumed",
    }
