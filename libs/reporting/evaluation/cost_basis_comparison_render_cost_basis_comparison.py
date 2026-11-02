"""cost_basis_comparison: ``render_cost_basis_comparison`` body (moved verbatim from ``cost_basis_comparison``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Mapping


def render_cost_basis_comparison(payload: Mapping[str, Any], *, facade: Any) -> str:
    date_range = payload.get("range") or {}
    bases = payload.get("cost_bases") or {}
    mock = bases.get("mock_observed") or {}
    live = bases.get("live_deployment_equity") or {}
    lines = [
        f"# Cost Basis Comparison ({date_range.get('start')} ~ {date_range.get('end')})",
        "",
        "Evaluation-only. Runtime entry, exit, and broker accounting are unchanged.",
        f"Forward data source: `{payload.get('forward_data_source') or 'unknown'}`.",
        f"Cohort scope: `{payload.get('cohort_scope') or 'unknown'}`.",
        "",
        "## Cost Assumptions",
        "",
        "| Basis | Round Trip | Slippage | Total Drag | Purpose |",
        "|---|---:|---:|---:|---|",
        f"| Mock observed | {float(mock.get('round_trip_cost_pct') or 0):.4f}% | "
        f"{float(bases.get('slippage_pct') or 0):.4f}% | "
        f"{float(mock.get('total_drag_with_slippage_pct') or 0):.4f}% | Mock PnL/cash truth |",
        f"| Live equity assumption | {float(live.get('round_trip_cost_pct') or 0):.4f}% | "
        f"{float(bases.get('slippage_pct') or 0):.4f}% | "
        f"{float(live.get('total_drag_with_slippage_pct') or 0):.4f}% | Deployment evaluation |",
        "",
        "## Pre-Strategist Scanner Top-K",
        "",
        "| Top-K | Horizon | Windows/Days | Gross | Mock Net | Live Net | Live-Mock Delta |",
        "|---:|---|---:|---:|---:|---:|---:|",
    ]
    for row in payload.get("rows") or []:
        gross = row.get("gross") or {}
        mock_net = row.get("mock_net") or {}
        live_net = row.get("live_net") or {}
        lines.append(
            f"| {row.get('top_k')} | {row.get('horizon')} | "
            f"{row.get('window_count')}/{row.get('observed_day_count')} | "
            f"{float(gross.get('expectancy_pct') or 0):.4f}% | "
            f"{float(mock_net.get('expectancy_pct') or 0):.4f}% | "
            f"{float(live_net.get('expectancy_pct') or 0):.4f}% | "
            f"{float(row.get('expectancy_delta_live_minus_mock_pct') or 0):+.4f}% |"
        )
    lines += [
        "",
        "## Interpretation",
        "",
        "- Mock net answers whether the signal beats the mock account's observed friction.",
        "- Live net answers whether it beats the explicit 2026 KRX equity assumption.",
        "- ETF/ETN tax treatment requires instrument classification and is not inferred here.",
        "- This report does not authorize a trading-policy change.",
    ]
    return "\n".join(lines) + "\n"
