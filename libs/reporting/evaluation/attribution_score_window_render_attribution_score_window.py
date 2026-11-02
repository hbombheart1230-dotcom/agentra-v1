"""attribution_score_window: ``render_attribution_score_window`` body (moved verbatim from ``attribution_score_window``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any, Iterable, Mapping


def render_attribution_score_window(payload: Mapping[str, Any], *, facade: Any) -> str:
    lines = [
        f"# Q13 Attribution Score Window - {payload.get('window_id', '')}",
        "",
        f"- Behavior effect: `{payload.get('behavior_effect', '')}`",
        f"- Days: {payload.get('day_count', 0)} total / {payload.get('valid_day_count', 0)} valid",
        f"- Available attribution days: {payload.get('available_day_count', 0)}",
        f"- Valid-day trades: {payload.get('total_trade_count_valid_days', 0)}",
        f"- Weakest by average score: `{facade._mapping(payload.get('weakest_axis_by_average_score')).get('name') or '-'}` "
        f"({facade._mapping(payload.get('weakest_axis_by_average_score')).get('average_score')})",
        "",
        "## Axis Summary",
        "",
        "| Axis | Avg Score | Min | Max | Scored Days | Insufficient Days | Top Reasons |",
        "| --- | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for key, item in facade._mapping(payload.get("axis_summary")).items():
        obj = facade._mapping(item)
        reasons = ", ".join(
            f"{row.get('reason')} ({row.get('count')})"
            for row in obj.get("top_reasons") or []
        ) or "-"
        lines.append(
            f"| {key} | {obj.get('average_score')} | {obj.get('min_score')} | "
            f"{obj.get('max_score')} | {obj.get('scored_day_count')} | "
            f"{obj.get('insufficient_day_count')} | {reasons} |"
        )
    lines.extend([
        "",
        "## Weakest Axis Distribution",
        "",
    ])
    distribution = facade._mapping(payload.get("weakest_axis_distribution"))
    if distribution:
        for key, count in sorted(distribution.items(), key=lambda item: (-int(item[1]), item[0])):
            lines.append(f"- `{key}`: {count}")
    else:
        lines.append("- No valid scored days.")
    lines.extend([
        "",
        "## Daily Rows",
        "",
        "| Day | Valid | Trades | Weakest | Selection | Scanner | Entry | Exit/Horizon | Evidence |",
        "| --- | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |",
    ])
    for row in payload.get("daily_rows") or []:
        if not isinstance(row, facade.Mapping):
            continue
        lines.append(
            f"| {row.get('day')} | {row.get('valid')} | {row.get('trade_count')} | "
            f"{row.get('weakest_axis') or '-'} | "
            f"{row.get('selection_integrity_score')} | "
            f"{row.get('scanner_alignment_score')} | "
            f"{row.get('entry_timing_score')} | "
            f"{row.get('exit_horizon_score')} | "
            f"{row.get('evidence_quality_score')} |"
        )
    lines.extend([
        "",
        "## Interpretation Rule",
        "",
        f"- {payload.get('interpretation_rule', '')}",
        "",
    ])
    return "\n".join(lines)
