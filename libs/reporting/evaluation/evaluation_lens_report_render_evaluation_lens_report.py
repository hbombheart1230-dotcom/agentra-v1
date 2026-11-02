"""evaluation_lens_report: ``render_evaluation_lens_report`` body (moved verbatim from ``evaluation_lens_report``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Mapping


def render_evaluation_lens_report(payload: Mapping[str, Any], *, facade: Any) -> str:
    rng = facade._as_dict(payload.get("range"))
    evidence = facade._as_dict(payload.get("evidence"))
    lines = [
        f"# Evaluation Lens Report ({rng.get('start')} ~ {rng.get('end')})",
        "",
        "Behavior effect: evaluation_only. This report does not change trading behavior or reset the freeze window.",
        "",
        "## Evidence",
        f"- shadow payloads: {evidence.get('shadow_payload_count')}",
        f"- shadow candidates: {evidence.get('candidate_count')}",
        f"- Q9 candidates: {evidence.get('q9_candidate_count')}",
        f"- trade models: {evidence.get('trade_model_count')}",
        "",
        "## Blocker Forward Review",
        "| Blocker | Candidates | +5m avg | +15m avg | +30m avg | +30m MFE | +30m cost reachable |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    blocker = facade._as_dict(payload.get("blocker_forward_review"))
    for row in blocker.get("by_blocker") or []:
        h5 = facade._as_dict(row.get("+5m"))
        h15 = facade._as_dict(row.get("+15m"))
        h30 = facade._as_dict(row.get("+30m"))
        lines.append(
            f"| {row.get('name')} | {row.get('candidate_count')} | "
            f"{facade._metric_avg(facade._as_dict(h5.get('return')))} | "
            f"{facade._metric_avg(facade._as_dict(h15.get('return')))} | "
            f"{facade._metric_avg(facade._as_dict(h30.get('return')))} | "
            f"{h30.get('avg_mfe_pct')} | {h30.get('cost_floor_reachable_rate')} |"
        )
    lines += [
        "",
        "## Strategist Delta",
        "| Horizon | Best role | Strategist delta avg | Commander delta avg |",
        "|---|---|---:|---:|",
    ]
    strat = facade._as_dict(payload.get("strategist_delta_review"))
    best_by = {row.get("horizon"): row.get("best_role") for row in strat.get("best_role_by_horizon") or []}
    for row in strat.get("deltas_by_horizon") or []:
        horizon = row.get("horizon")
        sd = facade._as_dict(row.get("strategist_minus_scanner_control"))
        cd = facade._as_dict(row.get("commander_minus_strategist"))
        lines.append(
            f"| {horizon} | {best_by.get(horizon) or ''} | "
            f"{facade._metric_avg(sd)} | {facade._metric_avg(cd)} |"
        )
    lines += [
        "",
        "## Exit Hold Counterfactual",
        "| Exit reason | Trades | +5m improvement | +15m improvement | +30m improvement | EOD improvement |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    exit_review = facade._as_dict(payload.get("exit_hold_counterfactual_review"))
    for row in exit_review.get("by_exit_reason") or []:
        lines.append(
            f"| {row.get('exit_reason')} | {row.get('trade_count')} | "
            f"{facade._metric_avg(facade._as_dict(row.get('+5m')))} | "
            f"{facade._metric_avg(facade._as_dict(row.get('+15m')))} | "
            f"{facade._metric_avg(facade._as_dict(row.get('+30m')))} | "
            f"{facade._metric_avg(facade._as_dict(row.get('EOD')))} |"
        )
    lines += [
        "",
        "## Rules",
        "- This report can be regenerated for past days without resetting evaluation.",
        "- It adds observability only; entry, exit, scanner, strategist, commander, and monitor behavior are unchanged.",
        "- Promotion decisions still require the promotion framework and enough comparable days.",
    ]
    return "\n".join(lines) + "\n"
