"""horizon_alignment: ``render_horizon_alignment_review`` body (moved verbatim from ``horizon_alignment``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Mapping


def render_horizon_alignment_review(payload: Mapping[str, Any], *, facade: Any) -> str:
    date_range = payload.get("range") or {}
    cost = payload.get("cost_model") or {}
    lines = [
        f"# Horizon Alignment Review ({date_range.get('start')} ~ {date_range.get('end')})",
        "",
        "This report is evaluation-only. It does not change runtime behavior.",
        "",
        "## Cost Basis",
        "",
        f"- source: `{cost.get('source')}`",
        f"- samples: {cost.get('sample_count')}",
        f"- EMA round-trip cost: {float(cost.get('ema_round_trip_cost_pct') or 0):.4f}%",
        f"- conservative round-trip cost: {float(cost.get('conservative_round_trip_cost_pct') or 0):.4f}%",
        "",
        f"## Decision: **{payload.get('decision')}**",
        "",
        "## Time x Tactic x Horizon",
        "",
        "| Time | Tactic | Horizon | Obs/Days | Gross | Net | Net Win | PF | Day Max | Symbol Max | Decision |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in payload.get("time_tactic") or []:
        dimensions = row.get("dimensions") or {}
        lines.append(
            f"| {dimensions.get('time_bucket')} | {dimensions.get('tactic')} | {row.get('horizon')} | "
            f"{row.get('observed_count')}/{row.get('observed_day_count')} | "
            f"{row.get('average_gross_return_pct')}% | {row.get('average_net_return_pct')}% | "
            f"{float(row.get('net_win_rate') or 0):.1%} | {row.get('net_profit_factor')} | "
            f"{float(row.get('maximum_day_share') or 0):.1%} | "
            f"{float(row.get('maximum_symbol_share') or 0):.1%} | `{row.get('decision')}` |"
        )
    lines += [
        "",
        "## Controlled-Adoption Candidates",
        "",
    ]
    adoption = payload.get("controlled_adoption_candidates") or []
    if not adoption:
        lines.append("- None")
    else:
        for row in adoption:
            dimensions = row.get("dimensions") or {}
            lines.append(
                f"- `{dimensions.get('time_bucket')} | {dimensions.get('tactic')} | {row.get('horizon')}`: "
                f"net {row.get('average_net_return_pct')}%, PF {row.get('net_profit_factor')}, "
                f"{row.get('observed_count')} observations across {row.get('observed_day_count')} days"
            )
    lines += [
        "",
        "## Observation Candidates",
        "",
    ]
    observation = payload.get("observation_candidates") or []
    if not observation:
        lines.append("- None")
    else:
        for row in observation:
            dimensions = row.get("dimensions") or {}
            lines.append(
                f"- `{dimensions.get('time_bucket')} | {dimensions.get('tactic')} | {row.get('horizon')}`: "
                f"net {row.get('average_net_return_pct')}%, PF {row.get('net_profit_factor')}, "
                f"worst leave-one-day-out {row.get('worst_leave_one_day_out_net_return_pct')}%, "
                f"robust={row.get('robust_across_days')}"
            )
    lines += [
        "",
        "## Next Action",
        "",
        f"- decision: **{(payload.get('next_action') or {}).get('decision')}**",
        f"- reason: {(payload.get('next_action') or {}).get('reason')}",
        "- behavior change authorized: **False**",
    ]
    return "\n".join(lines) + "\n"
