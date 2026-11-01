"""q8_lane_decision_table projections (moved verbatim from q8_lane_decision_table).

Module globals and helpers are resolved on ``facade`` (the q8_lane_decision_table module) at call time; this module never imports it.
"""
from __future__ import annotations

from typing import Any, Mapping


def render_q8_lane_decision_table_markdown(payload: Mapping[str, Any], *, facade: Any) -> str:
    gate = payload.get("evaluation_trust_gate") if isinstance(payload.get("evaluation_trust_gate"), facade.Mapping) else {}
    lines = [
        f"# Q8 Lane Decision Table - {payload.get('day')}",
        "",
        "## Summary",
        "",
        f"- payloads: {payload.get('payload_count')}",
        f"- candidates: {payload.get('candidate_count')}",
        f"- deduped candidates: {payload.get('deduped_candidate_count')}",
        f"- duplicates: {payload.get('duplicate_candidate_count')}",
        f"- dedupe_key: `{', '.join(list(payload.get('dedupe_key') or []))}`",
        f"- evaluated: {payload.get('evaluated_count')}",
        f"- forward observed: {payload.get('forward_outcome_available_count')} "
        f"({float(payload.get('forward_outcome_coverage') or 0.0):.1%})",
        f"- trust_gate: `{gate.get('status') or '-'}`",
        f"- promotion_allowed: `{bool(gate.get('promotion_allowed'))}`",
        f"- trust_block_reasons: `{', '.join(list(gate.get('block_reasons') or gate.get('reasons') or [])) or '-'}`",
        f"- would-enter: {payload.get('would_enter_count')}",
        f"- top reasons: {payload.get('reason_summary') or '-'}",
        "",
        "## Lane Verdicts",
        "",
        "| Lane | Verdict | Decision | n | obs | +5m | +15m | +30m | MFE5 | MAE5 | Rationale |",
        "|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in facade._rows(payload.get("rows")):
        lines.append(
            "| "
            + " | ".join(
                [
                    facade._text(row.get("lane")) or "-",
                    facade._text(row.get("verdict")) or "-",
                    facade._text(row.get("decision")) or "-",
                    str(row.get("candidate_count") or 0),
                    str(row.get("observed_count") or 0),
                    facade._fmt_pct(row.get("avg_return_5m_pct")),
                    facade._fmt_pct(row.get("avg_return_15m_pct")),
                    facade._fmt_pct(row.get("avg_return_30m_pct")),
                    facade._fmt_pct(row.get("avg_mfe_5m_pct")),
                    facade._fmt_pct(row.get("avg_mae_5m_pct")),
                    facade._text(row.get("rationale")) or "-",
                ]
            )
            + " |"
        )
    lines += [
        "",
        "## Operating Interpretation",
        "",
        "- `TRUST_GATE_BLOCKED`: lane signal is visible, but Q8 evidence is not eligible for policy promotion.",
        "- `MISSED_OPPORTUNITY`: blocked candidates rose afterward. This is a review target, not direct permission to buy.",
        "- `GOOD_BLOCK`: blocked candidates underperformed after the block. Keep the gate under observation.",
        "- `DATA_INCOMPLETE`: sample or coverage is insufficient for a policy conclusion.",
        "",
        "## Current Action",
        "",
        "No new behavior patch is implied by this table unless the Q8 trust gate allows promotion review.",
        "",
    ]
    return "\n".join(lines)
