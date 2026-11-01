"""q8_lane_decision_table projections (moved verbatim from q8_lane_decision_table).

Module globals and helpers are resolved on ``facade`` (the q8_lane_decision_table module) at call time; this module never imports it.
"""
from __future__ import annotations

from typing import Any, Dict, Mapping


def _verdict(row: Mapping[str, Any], *, promotion_allowed: bool, facade: Any) -> Dict[str, str]:
    observed = facade._int(row.get("observed_count"))
    coverage = facade._float(row.get("coverage"))
    ret5 = facade._float(row.get("avg_return_5m_pct"))
    ret15 = facade._float(row.get("avg_return_15m_pct"))
    mfe5 = facade._float(row.get("avg_mfe_5m_pct"))
    mae5 = facade._float(row.get("avg_mae_5m_pct"))
    lane = facade._text(row.get("name"))

    if not promotion_allowed:
        return {
            "verdict": "TRUST_GATE_BLOCKED",
            "decision": "retain under observation",
            "rationale": "Q8 trust gate blocked promotion review; lane signal is diagnostic only.",
        }
    if observed < 10 or coverage < facade.TRUSTED_FORWARD_MIN_COVERAGE:
        return {
            "verdict": "DATA_INCOMPLETE",
            "decision": "observe",
            "rationale": "sample or trusted forward coverage is insufficient.",
        }
    if lane == "vwap_reclaim" and ret5 < 0.0 and ret15 < 0.0:
        return {
            "verdict": "GOOD_BLOCK",
            "decision": "keep blocked",
            "rationale": "VWAP reclaim lane showed weak short/mid forward returns.",
        }
    if ret5 >= 0.50 or ret15 >= 0.80 or mfe5 >= 1.50:
        risk_note = " MAE is high, so only small probe or rule review is allowed." if mae5 <= -1.50 else ""
        return {
            "verdict": "MISSED_OPPORTUNITY",
            "decision": "relaxation candidate",
            "rationale": f"Blocked candidates showed positive forward potential.{risk_note}".strip(),
        }
    if ret5 <= 0.0 and ret15 <= 0.0:
        return {
            "verdict": "GOOD_BLOCK",
            "decision": "keep blocked",
            "rationale": "Blocked candidates showed weak forward returns.",
        }
    return {
        "verdict": "DATA_INCOMPLETE",
        "decision": "observe",
        "rationale": "Signal direction is not decisive enough for a policy review.",
    }
