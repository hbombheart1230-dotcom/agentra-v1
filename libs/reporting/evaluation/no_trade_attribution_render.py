"""no_trade_attribution: ``render_no_trade_attribution_report`` body (moved verbatim from ``no_trade_attribution``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Mapping


def render_no_trade_attribution_report(payload: Mapping[str, Any], *, facade: Any) -> str:
    lines = [
        "# No-Trade Attribution Report",
        "",
        f"- Behavior effect: `{payload.get('behavior_effect', '')}`",
        f"- Day: `{payload.get('day', '')}`",
        f"- Trades: {payload.get('trade_count', 0)}",
        f"- Q9 windows: {payload.get('q9_window_count', 0)}",
        f"- No-trade class: `{payload.get('no_trade_class', '')}`",
        f"- Primary issue: `{payload.get('primary_issue', '')}`",
        f"- Commander approve + Monitor NOOP: {payload.get('commander_approve_monitor_noop_count', 0)}",
        "",
        "## Q9 Decision Surface",
        "",
    ]
    for title, key in (
        ("Commander Decisions", "commander_decisions"),
        ("Commander Reasons", "commander_reasons"),
        ("Commander Details", "commander_details"),
        ("Monitor Intents", "monitor_intents"),
        ("Monitor NOOP Reasons", "monitor_noop_reasons"),
        ("Scanner Top1", "scanner_top1"),
        ("Strategist Selected", "strategist_selected"),
    ):
        lines.extend([f"### {title}", ""])
        rows = payload.get(key) if isinstance(payload.get(key), list) else []
        if not rows:
            lines.append("- None")
        else:
            for row in rows:
                if isinstance(row, facade.Mapping):
                    lines.append(f"- `{row.get('name', '')}`: {row.get('count', 0)}")
        lines.append("")

    q11 = facade._mapping(payload.get("q11_opening_opportunity"))
    lines.extend([
        "## Shadow Opportunity",
        "",
        f"- Status: `{payload.get('shadow_opportunity_status', '')}`",
        f"- Q11 available: {bool(q11.get('available'))}",
        f"- Q11 signal rows: {q11.get('signal_rows', 0)}",
        f"- Q11 probe candidates: {q11.get('probe_candidates', 0)}",
        f"- Q11 probe near-misses: {q11.get('probe_near_misses', 0)}",
        f"- Q11 virtual trades: {q11.get('virtual_trades', 0)}",
        f"- Q11 win rate: {q11.get('win_rate') if q11.get('win_rate') is not None else '-'}",
        f"- Q11 avg net: {facade._pct(q11.get('avg_net_return_pct'))}",
        f"- Q11 avg MFE: {facade._pct(q11.get('avg_mfe_pct'))}",
        f"- Q11 avg MAE: {facade._pct(q11.get('avg_mae_pct'))}",
        "",
        "## Baseline Summary",
        "",
        "| Baseline | Horizon | Trades | Win Rate | Avg Net | PF |",
        "| --- | --- | ---: | ---: | ---: | ---: |",
    ])
    for baseline_key, label in (
        ("q10_samsung_hynix", "Q10 Samsung/Hynix"),
        ("q12_btc_woori", "Q12 BTC/Woori"),
    ):
        baseline = facade._mapping(payload.get(baseline_key))
        rows = baseline.get("horizons") if isinstance(baseline.get("horizons"), list) else []
        if not rows:
            lines.append(f"| {label} | - | 0 | - | - | - |")
            continue
        for row in rows:
            if not isinstance(row, facade.Mapping):
                continue
            lines.append(
                "| "
                + " | ".join(
                    [
                        label,
                        str(row.get("horizon") or "-"),
                        str(row.get("trade_count") or 0),
                        str(row.get("win_rate") if row.get("win_rate") is not None else "-"),
                        facade._pct(row.get("avg_net_return_pct")),
                        str(row.get("profit_factor") if row.get("profit_factor") is not None else "-"),
                    ]
                )
                + " |"
            )
    lines.extend([
        "",
        "## Interpretation",
        "",
        "- This report does not change trading behavior.",
        "- If trades are zero, Q13/Q14 trade attribution is insufficient; this report decides whether the absence itself is an over-filtering signal.",
    ])
    return "\n".join(lines) + "\n"
