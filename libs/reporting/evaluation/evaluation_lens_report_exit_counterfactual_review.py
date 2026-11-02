"""evaluation_lens_report: ``_exit_counterfactual_review`` body (moved verbatim from ``evaluation_lens_report``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any


def _exit_counterfactual_review(models: list[dict[str, Any]], *, facade: Any) -> dict[str, Any]:
    by_reason: dict[str, list[dict[str, Any]]] = facade.defaultdict(list)
    for model in models:
        exit_reason = facade._text((facade._as_dict(model.get("exit")).get("reason"))) or facade._text((facade._as_dict(model.get("outcome")).get("exit_reason"))) or "unknown"
        monitor = facade._as_dict(model.get("monitor"))
        shadow = facade._as_dict(model.get("post_exit_shadow")) or facade._as_dict(monitor.get("post_exit"))
        checkpoints = facade._as_dict(shadow.get("checkpoints"))
        actual = facade._num((facade._as_dict(model.get("outcome")).get("net_return_pct"))
                      or (facade._as_dict(model.get("outcome")).get("return_pct")))
        row = {"trade_id": model.get("trade_id"), "symbol": model.get("symbol"), "actual_return_pct": actual}
        for horizon in ("+5m", "+15m", "+30m", "+60m", "EOD"):
            cp = facade._as_dict(checkpoints.get(horizon))
            ret = facade._num(cp.get("return_pct"))
            row[horizon] = ret
            if ret is not None and actual is not None:
                row[f"{horizon}_improvement_pct"] = round(ret - actual, 4)
        by_reason[exit_reason].append(row)
    groups: list[dict[str, Any]] = []
    for reason, rows in by_reason.items():
        group = {"exit_reason": reason, "trade_count": len(rows)}
        for horizon in ("+5m", "+15m", "+30m", "+60m", "EOD"):
            values = [float(row[f"{horizon}_improvement_pct"]) for row in rows if row.get(f"{horizon}_improvement_pct") is not None]
            group[horizon] = facade.performance_metrics(values)
        groups.append(group)
    return {
        "schema_version": "exit_hold_counterfactual_review.v1",
        "behavior_effect": "evaluation_only",
        "trade_count": len(models),
        "by_exit_reason": sorted(groups, key=lambda row: (-int(row["trade_count"]), row["exit_reason"])),
    }
