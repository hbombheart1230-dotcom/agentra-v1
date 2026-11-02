"""loss_decomposition: ``_realized_trade_summary`` body (moved verbatim from ``loss_decomposition``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any


def _realized_trade_summary(models: list[dict[str, Any]], *, facade: Any) -> dict[str, Any]:
    returns: list[float] = []
    by_rank: dict[str, list[float]] = facade.defaultdict(list)
    selection_mismatch = 0
    for model in models:
        value = facade._to_float((model.get("outcome") or {}).get("net_return_pct"))
        if value is None:
            continue
        returns.append(value)
        selection = model.get("selection") or {}
        by_rank[facade._rank_bucket(selection.get("selected_rank"))].append(value)
        scanner_top1 = selection.get("scanner_top1")
        scanner_top1 = scanner_top1 if isinstance(scanner_top1, facade.Mapping) else {}
        if scanner_top1.get("symbol") and selection.get("selected_symbol") != scanner_top1.get("symbol"):
            selection_mismatch += 1
    return {
        "performance": facade.performance_metrics(returns),
        "by_executed_rank": [
            {"rank_bucket": name, **facade.performance_metrics(values)}
            for name, values in sorted(by_rank.items())
        ],
        "scanner_top1_execution_mismatch_count": selection_mismatch,
        "comparable_trade_count": len(returns),
    }
