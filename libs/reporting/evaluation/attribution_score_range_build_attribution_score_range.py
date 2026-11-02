"""attribution_score_range: ``build_attribution_score_range`` body (moved verbatim from ``attribution_score_range``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any, Iterable, Mapping


def build_attribution_score_range(
    *,
    reports_root: Path = Path("reports"),
    start: str,
    end: str,
    include_empty_days: bool = False,
    facade: Any,
) -> dict[str, Any]:
    reports_root = facade.Path(reports_root)
    day_rows: list[dict[str, Any]] = []
    for day in facade._date_range(start, end):
        if not include_empty_days and not facade._has_source_artifact(reports_root, day):
            continue
        payload = facade._day_payload(reports_root, day)
        trade_count = facade._day_trade_count(reports_root, day)
        scores = dict(payload.get("scores") or {}) if payload else {}
        has_score = any(facade._score_value({"scores": scores}, key) is not None for key in facade.SCORE_KEYS)
        day_rows.append(
            {
                "day": day,
                "available": bool(payload),
                "scored": has_score,
                "reason": "" if payload else "attribution_score_missing",
                "trade_count": trade_count,
                "scores": scores,
                "weakest_observed_axis": dict(payload.get("weakest_observed_axis") or {}) if payload else {},
            }
        )

    scored_rows = [row for row in day_rows if row.get("scored")]
    axis_summary: dict[str, Any] = {}
    for key in facade.SCORE_KEYS:
        values: list[int] = []
        status_counts: facade.Counter[str] = facade.Counter()
        reason_counts: facade.Counter[str] = facade.Counter()
        for row in day_rows:
            item = facade._mapping(facade._mapping(row.get("scores")).get(key))
            status = str(item.get("status") or ("MISSING" if not row.get("available") else "MISSING_SCORE"))
            status_counts[status] += 1
            value = facade._score_value(row, key)
            if value is not None:
                values.append(value)
            for reason in item.get("reasons") or []:
                reason_counts[str(reason)] += 1
        axis_summary[key] = {
            "day_count": len(day_rows),
            "scored_day_count": len(values),
            "missing_day_count": status_counts.get("MISSING", 0),
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
    for row in scored_rows:
        weakest = str(facade._mapping(row.get("weakest_observed_axis")).get("name") or "")
        if weakest:
            weakest_counts[weakest] += 1

    daily_table = [
        {
            "day": row.get("day"),
            "available": bool(row.get("available")),
            "scored": bool(row.get("scored")),
            "trade_count": row.get("trade_count"),
            "weakest_axis": facade._mapping(row.get("weakest_observed_axis")).get("name") or "",
            **{key: facade._score_value(row, key) for key in facade.SCORE_KEYS},
        }
        for row in day_rows
    ]
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
        "schema_version": "attribution_score_range.v1",
        "evaluation_program_id": "Q13_ATTRIBUTION_SCORE_RANGE",
        "behavior_effect": "observation_only",
        "start": start,
        "end": end,
        "include_empty_days": include_empty_days,
        "day_count": len(day_rows),
        "available_day_count": sum(1 for row in day_rows if row.get("available")),
        "scored_day_count": len(scored_rows),
        "trade_day_count": sum(1 for row in day_rows if int(row.get("trade_count") or 0) > 0),
        "total_trade_count": sum(int(row.get("trade_count") or 0) for row in day_rows),
        "scored_trade_count": sum(int(row.get("trade_count") or 0) for row in scored_rows),
        "axis_summary": axis_summary,
        "weakest_axis_distribution": dict(weakest_counts),
        "weakest_axis_by_average_score": {
            "name": weakest_average_axis[0],
            "average_score": weakest_average_axis[1],
        },
        "daily_rows": daily_table,
        "interpretation_rule": (
            "Use scored days for attribution conclusions. Missing or insufficient days are "
            "shown for audit but excluded from average score and weakest-axis distribution."
        ),
    }
