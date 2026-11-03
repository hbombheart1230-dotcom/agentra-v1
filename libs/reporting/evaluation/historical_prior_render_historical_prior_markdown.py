"""historical_prior: ``render_historical_prior_markdown`` body (moved verbatim from ``historical_prior``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any


def render_historical_prior_markdown(payload: dict[str, Any], *, facade: Any) -> str:
    coverage = payload.get("coverage") or {}
    performance = payload.get("performance") or {}
    eligible = performance.get("eligible") or {}
    all_realized = performance.get("all_realized") or {}
    scope = payload.get("scope") or {}
    breakdowns = payload.get("breakdowns") or {}
    lines = [
        "# Historical Q9 Prior",
        "",
        f"- Scope: `{scope.get('from_day') or 'beginning'}` to before `{scope.get('before_day')}`",
        "- Behavior effect: read-only historical prior",
        "- Official Q9 freeze sample: **False**",
        "- Usage: prior evidence only, not promotion evidence by itself",
        "",
        "## Coverage",
        "",
        f"- Source days: {coverage.get('source_day_count', 0)}",
        f"- Trades: {coverage.get('trade_count', 0)} total / {coverage.get('eligible_trade_count', 0)} eligible",
        f"- Build errors: {coverage.get('build_error_count', 0)}",
        f"- Integrity counts: {coverage.get('integrity_status_counts', {})}",
        "",
        "## Performance",
        "",
        f"- Eligible count: {eligible.get('count', 0)}",
        f"- Eligible win rate: {float(eligible.get('win_rate') or 0) * 100:.1f}%",
        f"- Eligible average return: {float(eligible.get('average_return_pct') or 0):.4f}%",
        f"- Eligible profit factor: {eligible.get('profit_factor', 0)}",
        f"- Eligible maximum drawdown: {float(eligible.get('maximum_drawdown_pct') or 0):.4f}%",
        f"- All-realized count: {all_realized.get('count', 0)}",
        f"- All-realized average return: {float(all_realized.get('average_return_pct') or 0):.4f}%",
        "",
        "## Key Breakdowns",
        "",
    ]
    for name in ("selected_rank_bucket", "strategist_playbook", "horizon_bucket"):
        lines.append(f"### {name}")
        rows = breakdowns.get(name) if isinstance(breakdowns.get(name), dict) else {}
        if not rows:
            lines.append("- No comparable rows")
            lines.append("")
            continue
        for key, metrics in rows.items():
            lines.append(
                f"- {key}: count {metrics.get('count', 0)}, "
                f"win {float(metrics.get('win_rate') or 0) * 100:.1f}%, "
                f"avg {float(metrics.get('average_return_pct') or 0):.4f}%, "
                f"PF {metrics.get('profit_factor', 0)}"
            )
        lines.append("")
    lines.extend([
        "## Guardrails",
        "",
        "- This does not reopen Q8.",
        "- This does not extend the Q9 five-valid-day freeze.",
        "- Monday Q9 close remains the authoritative decision point; this report is a tie-breaker and root-cause prior.",
        "",
    ])
    return "\n".join(lines)
