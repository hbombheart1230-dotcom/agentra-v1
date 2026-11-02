"""loss_decomposition: ``render_loss_decomposition`` body (moved verbatim from ``loss_decomposition``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Mapping


def render_loss_decomposition(payload: Mapping[str, Any], *, facade: Any) -> str:
    date_range = payload.get("range") or {}
    evidence = payload.get("evidence") or {}
    realized = payload.get("realized_system") or {}
    performance = realized.get("performance") or {}
    lines = [
        f"# Full-Chain Loss Decomposition ({date_range.get('start')} ~ {date_range.get('end')})",
        "",
        "This report is evaluation-only and does not change trading behavior.",
        "",
        "## Evidence",
        "",
        f"- shadow payloads: {evidence.get('shadow_payload_count')}",
        f"- raw/deduped candidates: {evidence.get('raw_shadow_candidate_count')} / {evidence.get('deduped_shadow_candidate_count')}",
        f"- trusted forward: {evidence.get('trusted_forward_count')} ({float(evidence.get('trusted_forward_coverage') or 0):.1%})",
        f"- trusted forward observed days: {', '.join(evidence.get('trusted_forward_observed_days') or []) or '-'}",
        f"- trade models: {evidence.get('trade_model_count')}",
        "",
        "## Stage Diagnosis",
        "",
        "| Stage | Status | Finding |",
        "|---|---|---|",
    ]
    for row in payload.get("diagnosis") or []:
        lines.append(f"| {row.get('stage')} | `{row.get('status')}` | {row.get('finding')} |")
    lines += [
        "",
        "## Candidate Edge By Time Bucket",
        "",
        "| Bucket | Observed | +5m | +15m | +30m | +60m |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for row in (payload.get("raw_candidate_edge") or {}).get("by_time_bucket") or []:
        lines.append(
            f"| {row.get('name')} | {row.get('observed_count')} | "
            f"{row.get('avg_return_5m_pct')} | {row.get('avg_return_15m_pct')} | "
            f"{row.get('avg_return_30m_pct')} | {row.get('avg_return_60m_pct')} |"
        )
    lines += [
        "",
        "## Shadow Rank Buckets",
        "",
        "| Rank | Observed | +5m | +15m | +30m | +60m |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for row in (payload.get("scanner_ranking") or {}).get("by_rank_bucket") or []:
        lines.append(
            f"| {row.get('name')} | {row.get('observed_count')} | "
            f"{row.get('avg_return_5m_pct')} | {row.get('avg_return_15m_pct')} | "
            f"{row.get('avg_return_30m_pct')} | {row.get('avg_return_60m_pct')} |"
        )
    lines += [
        "",
        "## Realized System",
        "",
        f"- count: {performance.get('count')}",
        f"- win rate: {performance.get('win_rate')}",
        f"- average return: {performance.get('average_return_pct')}%",
        f"- expectancy: {performance.get('expectancy_pct')}%",
        f"- profit factor: {performance.get('profit_factor')}",
        f"- maximum drawdown: {performance.get('maximum_drawdown_pct')}%",
        "",
        "## Monitor Entry",
        "",
        f"- matched trades: {(payload.get('monitor_entry') or {}).get('matched_trade_count')}",
        f"- average entry price delta: {(payload.get('monitor_entry') or {}).get('average_entry_price_delta_pct')}%",
        f"- late entries over +0.3%: {(payload.get('monitor_entry') or {}).get('late_entry_count')}",
        "",
        "## Monitor Exit Hold Alternatives",
        "",
        "| Offset | Count | Average improvement | Improved | Worsened |",
        "|---|---:|---:|---:|---:|",
    ]
    for row in (payload.get("monitor_exit") or {}).get("by_hold_offset") or []:
        lines.append(
            f"| {row.get('offset')} | {row.get('count')} | "
            f"{row.get('average_improvement_pct')}% | {row.get('improved_count')} | "
            f"{row.get('worsened_count')} |"
        )
    lines += [
        "",
        "## Fixed Interpretation",
        "",
        "- Do not patch every component at once.",
        "- Fix the first stage with a demonstrated loss of edge.",
        "- Strategist and Commander remain unjudged until trusted controls exist.",
        "- Reconstructed evidence is diagnostic and cannot promote behavior.",
        "",
        "## Next Action",
        "",
        f"- component: `{(payload.get('next_action') or {}).get('component')}`",
        f"- decision: **{(payload.get('next_action') or {}).get('decision')}**",
        f"- reason: {(payload.get('next_action') or {}).get('reason')}",
        "- behavior change authorized: **False**",
    ]
    return "\n".join(lines) + "\n"
