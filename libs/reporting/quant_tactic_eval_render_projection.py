"""quant_tactic_evaluation projections (moved verbatim from quant_tactic_evaluation).

Module globals and helpers are resolved on ``facade`` (the quant_tactic_evaluation module) at call time; this module never imports it.
"""
from __future__ import annotations

from typing import Any, List, Mapping


def render_quant_tactic_evaluation_lines(payload: Mapping[str, Any] | None, *, facade: Any) -> List[str]:
    evaluation = dict(payload or {})
    if not evaluation:
        return []
    missing = list(evaluation.get("missing_required_fields") or [])
    missing_text = ", ".join(str(field) for field in missing) if missing else "none"
    source_counts = dict(evaluation.get("tactic_id_source_counts") or {})
    source_text = ", ".join(f"{key}={value}" for key, value in source_counts.items()) if source_counts else "none"
    lines = [
        "- Quant Q8 readiness: "
        f"`{evaluation.get('status') or 'not_available'}` / action `{evaluation.get('promotion_action') or 'hold'}` "
        f"/ sample {evaluation.get('closed_or_realized_sample_count') or 0}"
        f" valid, invalid {evaluation.get('invalid_sample_count') or 0}"
        f"/{evaluation.get('promotion_sample_target') or facade._TARGET_PROMOTION_SAMPLE}",
        "- Quant Q8 live-trade readiness: "
        f"`{evaluation.get('live_trade_readiness') or evaluation.get('status') or 'not_available'}` "
        "(actual closed-trade performance only)",
        f"- Quant Q8 missing fields: {missing_text}",
        "- Quant Q8 tactic ID integrity: "
        f"mismatch trades {evaluation.get('tactic_id_mismatch_trade_count') or 0}, "
        f"mismatch rows {evaluation.get('tactic_id_mismatch_count') or 0}, "
        f"exit drift trades {evaluation.get('exit_tactic_drift_trade_count') or 0}, "
        f"exit drift rows {evaluation.get('exit_tactic_drift_count') or 0}, "
        f"sources {source_text}",
    ]
    invalid_examples = [row for row in list(evaluation.get("invalid_sample_examples") or []) if isinstance(row, facade.Mapping)]
    if invalid_examples:
        rendered = []
        for row in invalid_examples[:5]:
            trade_id = facade._text(row.get("trade_id")) or "-"
            symbol = facade._text(row.get("symbol")) or "-"
            reason = facade._text(row.get("reason")) or "unknown"
            rendered.append(f"{trade_id}/{symbol}:{reason}")
        lines.append(f"- Quant Q8 invalid samples: {', '.join(rendered)}")
    mismatch_examples = [row for row in list(evaluation.get("tactic_id_mismatch_examples") or []) if isinstance(row, facade.Mapping)]
    if mismatch_examples:
        rendered = []
        for row in mismatch_examples[:4]:
            trade_id = facade._text(row.get("trade_id")) or "-"
            symbol = facade._text(row.get("symbol")) or "-"
            count = facade._int(row.get("mismatch_count"))
            rendered.append(f"{trade_id}/{symbol}:{count}")
        lines.append(f"- Quant Q8 tactic mismatch examples: {', '.join(rendered)}")
    return lines
