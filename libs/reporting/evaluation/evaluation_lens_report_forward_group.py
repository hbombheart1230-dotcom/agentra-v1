"""evaluation_lens_report: ``_forward_group`` body (moved verbatim from ``evaluation_lens_report``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any


def _forward_group(rows: list[dict[str, Any]], group_key: str, *, cost_floor_pct: float, facade: Any) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = facade.defaultdict(list)
    for row in rows:
        grouped[facade._text(row.get(group_key)) or "unknown"].append(row)
    out: list[dict[str, Any]] = []
    for name, members in grouped.items():
        record: dict[str, Any] = {"name": name, "candidate_count": len(members)}
        days = sorted({facade.candidate_day(row) for row in members if facade.candidate_day(row)})
        record["observed_days"] = days
        for horizon in facade.HORIZONS:
            returns: list[float] = []
            mfes: list[float] = []
            maes: list[float] = []
            cost_reachable = 0
            for row in members:
                ret = facade._checkpoint_return(row, horizon)
                mfe = facade._checkpoint_mfe(row, horizon)
                mae = facade._checkpoint_mae(row, horizon)
                if ret is not None:
                    returns.append(ret)
                if mfe is not None:
                    mfes.append(mfe)
                    if cost_floor_pct > 0 and mfe >= cost_floor_pct:
                        cost_reachable += 1
                if mae is not None:
                    maes.append(mae)
            record[horizon] = {
                "observed_count": len(returns),
                "return": facade.performance_metrics(returns),
                "avg_mfe_pct": round(sum(mfes) / len(mfes), 4) if mfes else None,
                "avg_mae_pct": round(sum(maes) / len(maes), 4) if maes else None,
                "cost_floor_reachable_count": cost_reachable,
                "cost_floor_reachable_rate": round(cost_reachable / len(mfes), 4) if mfes else 0.0,
            }
        out.append(record)
    return sorted(out, key=lambda row: (-max(int(facade._as_dict(row.get(h)).get("observed_count") or 0) for h in facade.HORIZONS), row["name"]))
