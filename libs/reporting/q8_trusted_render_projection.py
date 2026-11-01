"""q8_trusted_reaggregation projections (moved verbatim from q8_trusted_reaggregation).

Module globals and helpers are resolved on ``facade`` (the q8_trusted_reaggregation module) at call time; this module never imports it.
"""
from __future__ import annotations

from typing import Any, Mapping


def render_q8_trusted_reaggregation_markdown(payload: Mapping[str, Any], *, facade: Any) -> str:
    date_range = payload.get("range") if isinstance(payload.get("range"), facade.Mapping) else {}
    aggregate = payload.get("aggregate") if isinstance(payload.get("aggregate"), facade.Mapping) else {}
    daily = list(payload.get("daily") or [])
    lines = [
        f"# Q8 Trusted Reaggregation ({date_range.get('start') or '-'} ~ {date_range.get('end') or '-'})",
        "",
        "This report is evaluation-only. It does not change trading behavior.",
        "",
        "## Summary",
        "",
        f"- raw candidates: **{facade._fmt_num(aggregate.get('candidate_count'))}**",
        f"- deduped candidates: **{facade._fmt_num(aggregate.get('deduped_candidate_count'))}**",
        f"- duplicate count/rate: **{facade._fmt_num(aggregate.get('duplicate_candidate_count'))} / {facade._fmt_pct(aggregate.get('duplicate_rate'))}**",
        f"- trusted forward: **{facade._fmt_num(aggregate.get('forward_outcome_available_count'))} / {facade._fmt_pct(aggregate.get('trusted_forward_coverage'))}**",
        f"- promotion allowed days: **{facade._fmt_num(aggregate.get('promotion_allowed_day_count'))}**",
        f"- cumulative trust gate: **`{aggregate.get('cumulative_trust_gate_status') or 'not_available'}`**",
        f"- cumulative promotion allowed: **`{bool(aggregate.get('cumulative_promotion_allowed'))}`**",
        f"- cumulative block reasons: **{', '.join(str(x) for x in list(aggregate.get('cumulative_trust_reasons') or [])) or '-'}**",
        "",
        "## Daily Trust Gate",
        "",
        "| Day | Raw | Deduped | Dup Rate | Trusted Forward | Trust Gate | Promotion | Reasons |",
        "|---|---:|---:|---:|---:|---|---|---|",
    ]
    for row in daily:
        reasons = ", ".join(str(x) for x in list(row.get("trust_reasons") or [])) or "-"
        lines.append(
            "| {day} | {raw} | {deduped} | {dup_rate} | {forward} ({coverage}) | `{gate}` | `{allowed}` | {reasons} |".format(
                day=row.get("day") or "-",
                raw=facade._fmt_num(row.get("candidate_count")),
                deduped=facade._fmt_num(row.get("deduped_candidate_count")),
                dup_rate=facade._fmt_pct(row.get("duplicate_rate")),
                forward=facade._fmt_num(row.get("trusted_forward_count")),
                coverage=facade._fmt_pct(row.get("trusted_forward_coverage")),
                gate=row.get("trust_gate_status") or "-",
                allowed=bool(row.get("promotion_allowed")),
                reasons=reasons,
            )
        )
    lines += [
        "",
        "## Promotion Watchlist",
        "",
        "| Day | Candidate | Observed | Days | +5m | +15m | MAE5 | State |",
        "|---|---|---:|---:|---:|---:|---:|---|",
    ]
    watch_count = 0
    for item in list(aggregate.get("promotion_watchlist") or []):
        if not isinstance(item, facade.Mapping):
            continue
        watch_count += 1
        lines.append(
            "| {day} | `{name}` | {obs}/{count} | {days} | {ret5} | {ret15} | {mae5} | `{state}` |".format(
                day="cumulative",
                name=item.get("name") or "-",
                obs=facade._fmt_num(item.get("observed_count")),
                count=facade._fmt_num(item.get("candidate_count")),
                days=facade._fmt_num(item.get("observed_day_count")),
                ret5=f"{float(item.get('avg_return_5m_pct')):.4f}%" if item.get("avg_return_5m_pct") is not None else "-",
                ret15=f"{float(item.get('avg_return_15m_pct')):.4f}%" if item.get("avg_return_15m_pct") is not None else "-",
                mae5=f"{float(item.get('avg_mae_5m_pct')):.4f}%" if item.get("avg_mae_5m_pct") is not None else "-",
                state=item.get("review_state") or "-",
            )
        )
    for row in daily:
        for item in list(row.get("promotion_watchlist") or []):
            if not isinstance(item, facade.Mapping):
                continue
            watch_count += 1
            lines.append(
                "| {day} | `{name}` | {obs}/{count} | {days} | {ret5} | {ret15} | {mae5} | `{state}` |".format(
                    day=row.get("day") or "-",
                    name=item.get("name") or "-",
                    obs=facade._fmt_num(item.get("observed_count")),
                    count=facade._fmt_num(item.get("candidate_count")),
                    days=facade._fmt_num(item.get("observed_day_count")),
                    ret5=f"{float(item.get('avg_return_5m_pct')):.4f}%" if item.get("avg_return_5m_pct") is not None else "-",
                    ret15=f"{float(item.get('avg_return_15m_pct')):.4f}%" if item.get("avg_return_15m_pct") is not None else "-",
                    mae5=f"{float(item.get('avg_mae_5m_pct')):.4f}%" if item.get("avg_mae_5m_pct") is not None else "-",
                    state=item.get("review_state") or "-",
                )
            )
    if watch_count <= 0:
        lines.append("| - | - | 0/0 | 0 | - | - | - | no_watchlist |")
    lines += [
        "",
        "## Decision Rule",
        "",
        "- PROMOTE is not allowed unless the daily trust gate has `promotion_allowed=true`.",
        f"- A day is promotion-review eligible only when trusted forward count >= {facade.TRUSTED_FORWARD_MIN_COUNT}, "
        f"trusted coverage >= {facade.TRUSTED_FORWARD_MIN_COVERAGE:.0%}, and duplicate rate <= {facade.DUPLICATE_RATE_MAX:.0%}.",
        f"- Candidate-level promotion requires at least {facade.PROMOTION_CANDIDATE_MIN_OBSERVED} trusted observations "
        f"across at least {facade.PROMOTION_CANDIDATE_MIN_DAYS} observed days.",
        "- Cross-day or stale forward observations are excluded from trusted forward counts.",
        "- Duplicate candidates are removed before forward performance is averaged.",
    ]
    return "\n".join(lines)
