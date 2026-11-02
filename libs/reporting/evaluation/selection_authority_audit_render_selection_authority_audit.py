"""selection_authority_audit: ``render_selection_authority_audit`` body (moved verbatim from ``selection_authority_audit``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Mapping


def render_selection_authority_audit(payload: Mapping[str, Any], *, facade: Any) -> str:
    lines = [
        "# Selection Authority Audit",
        "",
        f"- Behavior effect: `{payload.get('behavior_effect', '')}`",
        f"- Trades: {payload.get('trade_count', 0)}",
        "",
        "## Summary",
        "",
    ]
    summary = facade._mapping(payload.get("summary"))
    if summary:
        for key in sorted(summary):
            lines.append(f"- `{key}`: {summary[key]}")
    else:
        lines.append("- No rows.")
    lines.extend([
        "",
        "## Rows",
        "",
        "| Trade | Raw Top1 | Post-Strategy Top1 | Selected | Monitor | Commander Candidate | Commander Selected | Executed |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ])
    for row in payload.get("rows") or []:
        if not isinstance(row, facade.Mapping):
            continue
        lines.append(
            "| "
            + " | ".join(
                str(row.get(key) or "-")
                for key in (
                    "trade_id",
                    "raw_scanner_top1",
                    "post_strategy_top1",
                    "selected_symbol",
                    "monitor_symbol",
                    "commander_candidate_symbol",
                    "commander_selected_symbol",
                    "executed_symbol",
                )
            )
            + " |"
        )
    lines.append("")
    return "\n".join(lines)
