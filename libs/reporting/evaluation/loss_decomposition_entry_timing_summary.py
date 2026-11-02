"""loss_decomposition: ``_entry_timing_summary`` body (moved verbatim from ``loss_decomposition``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any


def _entry_timing_summary(
    models: list[dict[str, Any]],
    candidates: list[dict[str, Any]],
    *,
    facade: Any,
) -> dict[str, Any]:
    by_symbol: dict[str, list[dict[str, Any]]] = facade.defaultdict(list)
    for row in candidates:
        base = row.get("shadow_forward_base")
        base = base if isinstance(base, facade.Mapping) else {}
        epoch = int(facade._to_float(base.get("baseline_epoch")) or 0)
        price = facade._to_float(base.get("baseline_price"))
        if epoch > 0 and price and price > 0:
            by_symbol[str(row.get("symbol") or "")].append(row)
    for rows in by_symbol.values():
        rows.sort(key=lambda row: int((row.get("shadow_forward_base") or {}).get("baseline_epoch") or 0))

    deltas: list[float] = []
    matched: list[dict[str, Any]] = []
    matched_days: set[str] = set()
    for model in models:
        entry = model.get("entry") or {}
        entry_ts = facade._parse_ts(entry.get("timestamp"))
        entry_price = facade._to_float(entry.get("price"))
        symbol = str(model.get("symbol") or "")
        if entry_ts is None or entry_price is None or entry_price <= 0:
            continue
        epoch = int(entry_ts.timestamp())
        eligible = []
        for row in by_symbol.get(symbol, []):
            base = row.get("shadow_forward_base") or {}
            base_epoch = int(base.get("baseline_epoch") or 0)
            if 0 <= epoch - base_epoch <= 15 * 60:
                eligible.append(row)
        if not eligible:
            continue
        candidate = eligible[-1]
        base = candidate.get("shadow_forward_base") or {}
        baseline_price = facade._to_float(base.get("baseline_price"))
        if baseline_price is None or baseline_price <= 0:
            continue
        delta = ((entry_price / baseline_price) - 1.0) * 100.0
        deltas.append(delta)
        matched_days.add(str(model.get("day") or "")[:10])
        matched.append({
            "trade_id": model.get("trade_id"),
            "symbol": symbol,
            "baseline_epoch": base.get("baseline_epoch"),
            "baseline_price": baseline_price,
            "entry_price": entry_price,
            "entry_price_delta_pct": round(delta, 4),
            "candidate_reason": candidate.get("reason"),
        })
    return {
        "matched_trade_count": len(matched),
        "matched_day_count": len({day for day in matched_days if day}),
        "average_entry_price_delta_pct": round(sum(deltas) / len(deltas), 4) if deltas else None,
        "median_entry_price_delta_pct": round(facade.median(deltas), 4) if deltas else None,
        "late_entry_count": sum(1 for value in deltas if value > 0.3),
        "better_entry_count": sum(1 for value in deltas if value < -0.3),
        "examples": matched[:20],
        "limitation": "matched to nearest same-symbol shadow baseline within 15 minutes; diagnostic only",
    }
