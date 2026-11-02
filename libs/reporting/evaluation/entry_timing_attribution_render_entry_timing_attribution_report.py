"""entry_timing_attribution: ``render_entry_timing_attribution_report`` body (moved verbatim from ``entry_timing_attribution``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping, Sequence


def render_entry_timing_attribution_report(payload: Mapping[str, Any], *, facade: Any) -> str:
    lines = [
        f"# Q13 Entry Timing Attribution - {payload.get('day', '')}",
        "",
        f"- Behavior effect: `{payload.get('behavior_effect', '')}`",
        f"- Trades: {payload.get('trade_count', 0)}",
        "",
        "## Label Summary",
        "",
        "| Label | Trades | Win Rate | Avg Return | Avg Delay Sec | Avg 5m MFE | Avg 5m MAE |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in payload.get("label_summary") or []:
        if not isinstance(row, facade.Mapping):
            continue
        perf = facade._mapping(row.get("performance"))
        lines.append(
            f"| {row.get('label')} | {row.get('trade_count')} | "
            f"{facade._fmt(float(perf.get('win_rate') or 0.0) * 100.0, '%')} | "
            f"{facade._fmt(perf.get('average_return_pct'), '%')} | "
            f"{facade._fmt(row.get('avg_scanner_to_entry_delay_sec'))} | "
            f"{facade._fmt(row.get('avg_5m_mfe_pct'), '%')} | "
            f"{facade._fmt(row.get('avg_5m_mae_pct'), '%')} |"
        )
    lines.extend([
        "",
        "## Trade Rows",
        "",
        "| Trade | Symbol | Label | Delay Sec | Pre-entry Move | +5m Return | +5m MFE | +5m MAE | Realized | Reasons |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ])
    for row in payload.get("rows") or []:
        if not isinstance(row, facade.Mapping):
            continue
        quality = facade._mapping(row.get("entry_forward_quality"))
        lines.append(
            f"| {row.get('trade_id')} | {row.get('symbol')} | {row.get('label')} | "
            f"{facade._fmt(row.get('scanner_to_entry_delay_sec'))} | "
            f"{facade._fmt(row.get('pre_entry_move_pct'), '%')} | "
            f"{facade._fmt(quality.get('+5m_return_pct'), '%')} | "
            f"{facade._fmt(quality.get('+5m_mfe_pct'), '%')} | "
            f"{facade._fmt(quality.get('+5m_mae_pct'), '%')} | "
            f"{facade._fmt(row.get('entry_return_pct'), '%')} | "
            f"{', '.join(row.get('label_reasons') or []) or '-'} |"
        )
    lines.extend([
        "",
        "## Limitations",
        "",
    ])
    for item in payload.get("limitations") or []:
        lines.append(f"- {item}")
    lines.append("")
    return "\n".join(lines)
