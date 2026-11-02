"""scanner_alignment_root_cause: ``render_scanner_alignment_root_cause_report`` body (moved verbatim from ``scanner_alignment_root_cause``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Mapping


def render_scanner_alignment_root_cause_report(payload: Mapping[str, Any], *, facade: Any) -> str:
    lines = [
        f"# Q14 Scanner Alignment Root Cause - {payload.get('day', '')}",
        "",
        f"- Behavior effect: `{payload.get('behavior_effect', '')}`",
        f"- Trades: {payload.get('trade_count', 0)}",
        f"- Largest observed root cause: `{facade._mapping(payload.get('largest_observed_root_cause') or payload.get('largest_root_cause')).get('root_cause') or '-'}`",
        f"- Largest behavior root cause: `{facade._mapping(payload.get('largest_behavior_root_cause')).get('root_cause') or '-'}`",
        f"- Largest structural root cause: `{facade._mapping(payload.get('largest_structural_root_cause')).get('root_cause') or '-'}`",
        "- Outcome-conditioned labels are descriptive and are not independent causal proof.",
        f"- Q15 candidate: {payload.get('q15_behavior_patch_candidate') or '-'}",
        "",
        "## Root Cause Summary",
        "",
        "| Root Cause | Kind | Causal | Trades | Return Obs | Win Rate | Avg Return | Profit Factor | MDD | Negative Impact |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in payload.get("cause_summary") or []:
        if not isinstance(row, facade.Mapping):
            continue
        lines.append(
            f"| {row.get('root_cause')} | {row.get('diagnostic_kind') or '-'} | "
            f"{bool(row.get('causal_eligible'))} | {row.get('trade_count')} | "
            f"{row.get('return_observation_count')} | {float(row.get('win_rate') or 0):.1%} | "
            f"{float(row.get('avg_return_pct') or 0):.4f}% | {row.get('profit_factor')} | "
            f"{float(row.get('max_drawdown_pct') or 0):.4f}% | "
            f"{float(row.get('negative_impact_pct') or 0):.4f}% |"
        )
    lines.extend(
        [
            "",
            "## Rows",
            "",
            "| Trade | Symbol | Raw Top1 | Post Top1 | Selected | Rank | Return | Root Cause | Reasons |",
            "| --- | --- | --- | --- | --- | ---: | ---: | --- | --- |",
        ]
    )
    for row in payload.get("rows") or []:
        if not isinstance(row, facade.Mapping):
            continue
        reasons = ", ".join(str(reason) for reason in row.get("reasons") or []) or "-"
        value = row.get("net_return_pct")
        lines.append(
            f"| {row.get('trade_id')} | {row.get('symbol') or '-'} | "
            f"{row.get('raw_scanner_top1') or '-'} | {row.get('post_strategy_top1') or '-'} | "
            f"{row.get('selected_symbol') or '-'} | {row.get('selected_rank') or '-'} | "
            f"{'-' if value is None else f'{float(value):.4f}%'} | "
            f"{row.get('root_cause')} | {reasons} |"
        )
    lines.extend(["", "## Interpretation", "", f"- {payload.get('interpretation_rule', '')}", ""])
    return "\n".join(lines)
