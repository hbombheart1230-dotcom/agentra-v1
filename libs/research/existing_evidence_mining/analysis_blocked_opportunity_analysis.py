"""RF-039 existing_evidence_mining: ``blocked_opportunity_analysis`` body (moved verbatim from ``analysis``).

``facade`` is the ``analysis`` module; module-level names and helpers are resolved on it at call time so caller
monkeypatching keeps working. This module never imports ``analysis``. Pure, no IO.
"""
from __future__ import annotations

from typing import Any, Iterable, Mapping


def blocked_opportunity_analysis(samples: list[Mapping[str, Any]], *, facade: Any) -> dict[str, Any]:
    def checkpoint_for(row: Mapping[str, Any], horizon: str) -> Mapping[str, Any] | None:
        direct = row.get("checkpoints") if isinstance(row.get("checkpoints"), Mapping) else {}
        checkpoint = direct.get(horizon)
        if isinstance(checkpoint, Mapping):
            return checkpoint
        shadow = row.get("shadow_forward_outcome")
        shadow = shadow if isinstance(shadow, Mapping) else {}
        checkpoints = shadow.get("checkpoints") if isinstance(shadow.get("checkpoints"), Mapping) else {}
        checkpoint = checkpoints.get(horizon)
        return checkpoint if isinstance(checkpoint, Mapping) else None

    def classify(field: str) -> dict[str, Any]:
        grouped: dict[str, list[Mapping[str, Any]]] = facade.defaultdict(list)
        for row in samples:
            grouped[str(row.get(field) or "missing")].append(row)
        result: dict[str, Any] = {}
        for key, rows in sorted(grouped.items()):
            horizons: dict[str, Any] = {}
            for horizon in facade.HORIZONS[:-1]:
                observed = []
                for row in rows:
                    checkpoint = checkpoint_for(row, horizon)
                    if isinstance(checkpoint, Mapping) and checkpoint.get("status") == "observed":
                        gross = float(
                            checkpoint.get("gross_return_pct")
                            if checkpoint.get("gross_return_pct") is not None
                            else checkpoint.get("return_pct") or 0.0
                        )
                        observed.append(
                            {
                                "net": gross - facade.LIVE_COST_PCT,
                                "gross": gross,
                                "mfe": float(checkpoint.get("mfe_pct") or 0.0),
                                "mae": float(checkpoint.get("mae_pct") or 0.0),
                                "day": str(row.get("q16_day") or ""),
                                "symbol": str(row.get("symbol") or ""),
                            }
                        )
                day_counts = facade.Counter(item["day"] for item in observed)
                symbol_counts = facade.Counter(item["symbol"] for item in observed)
                horizons[horizon] = {
                    "population_count": len(rows),
                    "observed_count": len(observed),
                    "coverage": round(len(observed) / len(rows), 4) if rows else 0.0,
                    "net_metrics": facade.performance_metrics(item["net"] for item in observed),
                    "gross_metrics": facade.performance_metrics(item["gross"] for item in observed),
                    "average_mfe_pct": round(sum(item["mfe"] for item in observed) / len(observed), 4)
                    if observed
                    else None,
                    "average_mae_pct": round(sum(item["mae"] for item in observed) / len(observed), 4)
                    if observed
                    else None,
                    "blocked_net_winner_rate": round(
                        sum(1 for item in observed if item["net"] > 0.0) / len(observed),
                        4,
                    )
                    if observed
                    else 0.0,
                    "day_count": len(day_counts),
                    "symbol_count": len(symbol_counts),
                    "largest_day_share": round(
                        max(day_counts.values(), default=0) / len(observed), 4
                    )
                    if observed
                    else 0.0,
                    "largest_symbol_share": round(
                        max(symbol_counts.values(), default=0) / len(observed), 4
                    )
                    if observed
                    else 0.0,
                }
            result[key] = horizons
        return result

    return {
        "sample_count": len(samples),
        "by_disposition": classify("opportunity_disposition"),
        "by_reason": classify("reason"),
        "by_primary_failure_axis": classify("primary_failure_axis"),
        "by_entry_lane": classify("entry_lane"),
        "by_cost_floor_state": classify("entry_quant_cost_floor_state"),
    }
