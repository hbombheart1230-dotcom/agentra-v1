from __future__ import annotations

import json
from collections import Counter
from datetime import date, timedelta
from pathlib import Path
from typing import Any, Mapping
import sys
from . import attribution_score_range_date_range as _a35_date_range
from . import attribution_score_range_day_trade_count as _a35_day_trade_count
from . import attribution_score_range_render_attribution_score_range as _a35_render_attribution_score_range

from .attribution_score_window import SCORE_KEYS, _mapping, _read_json, _score_value


def _parse_date(value: str) -> date:
    return date.fromisoformat(str(value))


def _date_range(start: str, end: str) -> list[str]:
    return _a35_date_range._date_range(start=start, end=end, facade=sys.modules[__name__])


def _trade_dir_count(reports_root: Path, day: str) -> int:
    trade_dir = reports_root / "trades" / day
    if not trade_dir.exists():
        return 0
    return sum(1 for path in trade_dir.rglob("TRD_*") if path.is_dir())


def _has_source_artifact(reports_root: Path, day: str) -> bool:
    return any(
        path.exists()
        for path in (
            reports_root / "trades" / day,
            reports_root / "operator_summary" / "daily" / day,
            reports_root / "evaluation" / "daily" / day,
        )
    )


def _day_payload(reports_root: Path, day: str) -> dict[str, Any]:
    return _read_json(reports_root / "evaluation" / "daily" / day / "attribution_score_v0.json")


def _day_trade_count(reports_root: Path, day: str) -> int:
    return _a35_day_trade_count._day_trade_count(reports_root=reports_root, day=day, facade=sys.modules[__name__])


def build_attribution_score_range(
    *,
    reports_root: Path = Path("reports"),
    start: str,
    end: str,
    include_empty_days: bool = False,
) -> dict[str, Any]:
    reports_root = Path(reports_root)
    day_rows: list[dict[str, Any]] = []
    for day in _date_range(start, end):
        if not include_empty_days and not _has_source_artifact(reports_root, day):
            continue
        payload = _day_payload(reports_root, day)
        trade_count = _day_trade_count(reports_root, day)
        scores = dict(payload.get("scores") or {}) if payload else {}
        has_score = any(_score_value({"scores": scores}, key) is not None for key in SCORE_KEYS)
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
    for key in SCORE_KEYS:
        values: list[int] = []
        status_counts: Counter[str] = Counter()
        reason_counts: Counter[str] = Counter()
        for row in day_rows:
            item = _mapping(_mapping(row.get("scores")).get(key))
            status = str(item.get("status") or ("MISSING" if not row.get("available") else "MISSING_SCORE"))
            status_counts[status] += 1
            value = _score_value(row, key)
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

    weakest_counts: Counter[str] = Counter()
    for row in scored_rows:
        weakest = str(_mapping(row.get("weakest_observed_axis")).get("name") or "")
        if weakest:
            weakest_counts[weakest] += 1

    daily_table = [
        {
            "day": row.get("day"),
            "available": bool(row.get("available")),
            "scored": bool(row.get("scored")),
            "trade_count": row.get("trade_count"),
            "weakest_axis": _mapping(row.get("weakest_observed_axis")).get("name") or "",
            **{key: _score_value(row, key) for key in SCORE_KEYS},
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


def render_attribution_score_range(payload: Mapping[str, Any]) -> str:
    return _a35_render_attribution_score_range.render_attribution_score_range(payload=payload, facade=sys.modules[__name__])


def write_attribution_score_range(
    *,
    reports_root: Path = Path("reports"),
    start: str,
    end: str,
    include_empty_days: bool = False,
) -> dict[str, str]:
    reports_root = Path(reports_root)
    payload = build_attribution_score_range(
        reports_root=reports_root,
        start=start,
        end=end,
        include_empty_days=include_empty_days,
    )
    out_dir = reports_root / "evaluation" / "range" / f"{start}_{end}"
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / "attribution_score_range.json"
    md_path = out_dir / "attribution_score_range.md"
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(render_attribution_score_range(payload), encoding="utf-8")
    return {"json": str(json_path), "markdown": str(md_path)}


__all__ = [
    "build_attribution_score_range",
    "render_attribution_score_range",
    "write_attribution_score_range",
]
