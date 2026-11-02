"""attribution_score_window: ``build_attribution_score_window`` body (moved verbatim from ``attribution_score_window``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any, Iterable, Mapping


def build_attribution_score_window(
    *,
    reports_root: Path = Path("reports"),
    window_id: str = "q9_q10_q11_q12_5d_20260629",
    facade: Any,
) -> dict[str, Any]:
    reports_root = facade.Path(reports_root)
    freeze_root = reports_root / "evaluation" / "freeze_window" / window_id
    ledger_rows = facade._ledger_days(freeze_root)
    day_rows: list[dict[str, Any]] = []
    for ledger in ledger_rows:
        day = str(ledger.get("day") or "")
        payload = facade._day_payload(reports_root, day)
        if not payload:
            day_rows.append({
                "day": day,
                "counts_as_valid_day": bool(ledger.get("counts_as_valid_day")),
                "available": False,
                "reason": "attribution_score_missing",
                "scores": {},
                "weakest_observed_axis": {},
                "trade_count": 0,
            })
            continue
        day_rows.append({
            "day": day,
            "counts_as_valid_day": bool(ledger.get("counts_as_valid_day")),
            "available": True,
            "reason": "",
            "scores": dict(payload.get("scores") or {}),
            "weakest_observed_axis": dict(payload.get("weakest_observed_axis") or {}),
            "trade_count": facade._read_json(
                reports_root / "evaluation" / "daily" / day / "daily_scorecard.json"
            ).get("artifact_integrity", {}).get("trade_count", 0),
        })

    valid_rows = [row for row in day_rows if row.get("counts_as_valid_day")]
    axis_summary: dict[str, Any] = {}
    for key in facade.SCORE_KEYS:
        values: list[int] = []
        status_counts: facade.Counter[str] = facade.Counter()
        reason_counts: facade.Counter[str] = facade.Counter()
        for row in valid_rows:
            item = facade._mapping(facade._mapping(row.get("scores")).get(key))
            status = str(item.get("status") or "MISSING")
            status_counts[status] += 1
            value = facade._score_value(row, key)
            if value is not None:
                values.append(value)
            for reason in item.get("reasons") or []:
                reason_counts[str(reason)] += 1
        axis_summary[key] = {
            "valid_day_count": len(valid_rows),
            "scored_day_count": len(values),
            "insufficient_day_count": status_counts.get("INSUFFICIENT_EVIDENCE", 0),
            "average_score": round(sum(values) / len(values), 2) if values else None,
            "min_score": min(values) if values else None,
            "max_score": max(values) if values else None,
            "status_counts": dict(status_counts),
            "top_reasons": [
                {"reason": reason, "count": count}
                for reason, count in reason_counts.most_common(10)
            ],
        }

    weakest_counts: facade.Counter[str] = facade.Counter()
    for row in valid_rows:
        weakest = str(facade._mapping(row.get("weakest_observed_axis")).get("name") or "")
        if weakest:
            weakest_counts[weakest] += 1

    daily_table = []
    for row in day_rows:
        daily_table.append({
            "day": row.get("day"),
            "valid": bool(row.get("counts_as_valid_day")),
            "available": bool(row.get("available")),
            "trade_count": row.get("trade_count"),
            "weakest_axis": facade._mapping(row.get("weakest_observed_axis")).get("name") or "",
            **{
                key: facade._score_value(row, key)
                for key in facade.SCORE_KEYS
            },
        })

    scored_axis_averages = {
        key: item.get("average_score")
        for key, item in axis_summary.items()
        if item.get("average_score") is not None
    }
    weakest_average_axis = (
        min(scored_axis_averages.items(), key=lambda item: float(item[1]))
        if scored_axis_averages
        else ("", None)
    )
    return {
        "schema_version": "attribution_score_window.v1",
        "evaluation_program_id": "Q13_ATTRIBUTION_SCORE_WINDOW",
        "behavior_effect": "observation_only",
        "window_id": window_id,
        "day_count": len(day_rows),
        "valid_day_count": len(valid_rows),
        "available_day_count": sum(1 for row in day_rows if row.get("available")),
        "total_trade_count_valid_days": sum(int(row.get("trade_count") or 0) for row in valid_rows),
        "axis_summary": axis_summary,
        "weakest_axis_distribution": dict(weakest_counts),
        "weakest_axis_by_average_score": {
            "name": weakest_average_axis[0],
            "average_score": weakest_average_axis[1],
        },
        "daily_rows": daily_table,
        "interpretation_rule": (
            "Use valid days for aggregate conclusions. Invalid days are shown for audit "
            "but excluded from average score and weakest-axis distribution."
        ),
    }
