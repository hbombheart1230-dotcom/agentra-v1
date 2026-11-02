"""horizon_compliance_report: ``render_horizon_compliance_report`` body (moved verbatim from ``horizon_compliance_report``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Mapping


def render_horizon_compliance_report(payload: Mapping[str, Any], *, facade: Any) -> str:
    lines = [
        "# Horizon Compliance Report",
        "",
        f"- Behavior effect: `{payload.get('behavior_effect', '')}`",
        f"- Trades: {payload.get('trade_count', 0)}",
        f"- Policy warning: {payload.get('policy_warning', '')}",
        "",
        "## Horizon Counts",
        "",
    ]
    counts = facade._mapping(payload.get("horizon_counts"))
    if counts:
        for key in sorted(counts):
            lines.append(f"- `{key}`: {counts[key]}")
    else:
        lines.append("- No observed horizons.")
    lines.extend([
        "",
        "## By Horizon And Exit Reason",
        "",
        "| Horizon | Exit Reason | Count | Avg Hold Sec | Before Min | Before Target | Target Hold Better | Avg Return |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ])
    for row in payload.get("group_rows") or []:
        if not isinstance(row, facade.Mapping):
            continue
        perf = facade._mapping(row.get("performance"))
        avg_return = perf.get("average_return_pct")
        lines.append(
            f"| {row.get('strategy_horizon')} | {row.get('exit_reason')} | "
            f"{row.get('count')} | {row.get('average_hold_sec')} | "
            f"{row.get('exit_before_min_hold_count')} | "
            f"{row.get('exit_before_target_hold_count')} | "
            f"{row.get('target_hold_would_improve_exit_count')} | "
            f"{'-' if avg_return is None else f'{float(avg_return):.4f}%'} |"
        )
    lines.append("")
    return "\n".join(lines)
