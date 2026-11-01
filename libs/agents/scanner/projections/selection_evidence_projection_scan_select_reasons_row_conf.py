"""selection_evidence_projection projections (moved verbatim from selection_evidence_projection).

Module globals and helpers are resolved on ``facade`` (the selection_evidence_projection module) at call time; this module never imports it.
"""
from __future__ import annotations



def scan_select_reasons_row_conf(row, selected_score, selected_confidence, selected_risk, runner_up_reasons, *, facade):
    if True:
            reasons: facade.List[str] = []
            row_score = float(facade._to_float(row.get("score_total") or row.get("score")))
            row_conf = float(facade._to_float(row.get("confidence")))
            row_risk = float(facade._to_float(row.get("risk_score")))
            if row_score < selected_score:
                reasons.append(f"lower total score ({row_score:.3f} vs {selected_score:.3f})")
            if row_conf < selected_confidence:
                reasons.append(f"lower confidence ({row_conf:.2f} vs {selected_confidence:.2f})")
            if row_risk > selected_risk:
                reasons.append(f"higher risk ({row_risk:.2f} vs {selected_risk:.2f})")
            if not reasons:
                reasons.append("lost on tie-break after score, confidence, and risk comparison")
            runner_up_reasons.append(
                {
                    "symbol": str(row.get("symbol") or ""),
                    "why_lost": reasons,
                }
            )
    return (reasons, row_conf, row_risk, row_score)
