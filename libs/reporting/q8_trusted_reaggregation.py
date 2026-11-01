from __future__ import annotations

import json
from datetime import date, timedelta
from pathlib import Path
import sys
from typing import Any, Dict, Iterable, List, Mapping

from libs.reporting.q8_evaluation_contract import (
    DUPLICATE_RATE_MAX,
    PROMOTION_CANDIDATE_MIN_DAYS,
    PROMOTION_CANDIDATE_MIN_OBSERVED,
    TRUSTED_FORWARD_MIN_COUNT,
    TRUSTED_FORWARD_MIN_COVERAGE,
)
from libs.reporting.quant_shadow_candidate_evaluation import (
    build_quant_shadow_candidate_evaluation,
    load_quant_shadow_candidate_payloads,
)
from libs.reporting import q8_trusted_day_projection as _c03_10_a3_owner
from libs.reporting import q8_trusted_pct_projection as _c03_10_a4_owner
from libs.reporting import q8_trusted_num_projection as _c03_10_a5_owner
from libs.reporting import q8_trusted_watchlist_projection as _c03_10_a6_owner
from libs.reporting import q8_trusted_render_projection as _c03_10_a7_owner


def _iter_days(start: str, end: str) -> Iterable[str]:
    yield from _c03_10_a3_owner._iter_days(start, end, facade=sys.modules[__name__])


def _fmt_pct(value: Any) -> str:
    return _c03_10_a4_owner._fmt_pct(value)


def _fmt_num(value: Any) -> str:
    return _c03_10_a5_owner._fmt_num(value)


def _watchlist_rows(scorecard: Mapping[str, Any]) -> List[Dict[str, Any]]:
    return _c03_10_a6_owner._watchlist_rows(scorecard, facade=sys.modules[__name__])


def build_q8_trusted_reaggregation(*, reports_root: Path, start: str, end: str) -> Dict[str, Any]:
    daily: List[Dict[str, Any]] = []
    all_payloads: List[Dict[str, Any]] = []
    promotion_allowed_day_count = 0
    for day in _iter_days(start, end):
        payloads = load_quant_shadow_candidate_payloads(reports_root=reports_root, days=[day])
        if not payloads:
            continue
        all_payloads.extend(payloads)
        evaluation = build_quant_shadow_candidate_evaluation(payloads)
        scorecard = (
            evaluation.get("no_trade_scorecard")
            if isinstance(evaluation.get("no_trade_scorecard"), Mapping)
            else {}
        )
        trust_gate = (
            evaluation.get("evaluation_trust_gate")
            if isinstance(evaluation.get("evaluation_trust_gate"), Mapping)
            else {}
        )
        row = {
            "day": day,
            "payload_count": int(evaluation.get("payload_count") or 0),
            "candidate_count": int(evaluation.get("candidate_count") or 0),
            "deduped_candidate_count": int(evaluation.get("deduped_candidate_count") or 0),
            "duplicate_candidate_count": int(evaluation.get("duplicate_candidate_count") or 0),
            "duplicate_rate": float(trust_gate.get("duplicate_rate") or 0.0),
            "trusted_forward_count": int(evaluation.get("forward_outcome_available_count") or 0),
            "trusted_forward_coverage": float(evaluation.get("forward_outcome_coverage") or 0.0),
            "scorecard_status": scorecard.get("status") or "not_available",
            "trust_gate_status": trust_gate.get("status") or "not_available",
            "promotion_allowed": bool(trust_gate.get("promotion_allowed")),
            "trust_reasons": list(trust_gate.get("block_reasons") or trust_gate.get("reasons") or []),
            "promotion_watchlist": _watchlist_rows(scorecard),
        }
        daily.append(row)
        if row["promotion_allowed"]:
            promotion_allowed_day_count += 1

    cumulative_evaluation = build_quant_shadow_candidate_evaluation(all_payloads) if all_payloads else {}
    cumulative_scorecard = (
        cumulative_evaluation.get("no_trade_scorecard")
        if isinstance(cumulative_evaluation.get("no_trade_scorecard"), Mapping)
        else {}
    )
    cumulative_trust_gate = (
        cumulative_evaluation.get("evaluation_trust_gate")
        if isinstance(cumulative_evaluation.get("evaluation_trust_gate"), Mapping)
        else {}
    )
    aggregate = {
        "candidate_count": int(cumulative_evaluation.get("candidate_count") or 0),
        "deduped_candidate_count": int(cumulative_evaluation.get("deduped_candidate_count") or 0),
        "duplicate_candidate_count": int(cumulative_evaluation.get("duplicate_candidate_count") or 0),
        "duplicate_rate": float(cumulative_trust_gate.get("duplicate_rate") or 0.0),
        "forward_outcome_available_count": int(cumulative_evaluation.get("forward_outcome_available_count") or 0),
        "trusted_forward_coverage": float(cumulative_evaluation.get("forward_outcome_coverage") or 0.0),
        "promotion_allowed_day_count": promotion_allowed_day_count,
        "cumulative_trust_gate_status": cumulative_trust_gate.get("status") or "not_available",
        "cumulative_promotion_allowed": bool(cumulative_trust_gate.get("promotion_allowed")),
        "cumulative_trust_reasons": list(
            cumulative_trust_gate.get("block_reasons") or cumulative_trust_gate.get("reasons") or []
        ),
        "promotion_watchlist": _watchlist_rows(cumulative_scorecard),
    }
    return {
        "schema_version": "q8_trusted_reaggregation.v2",
        "behavior_effect": "evaluation_only",
        "generated_with": "same_day_max_delay_forward_outcomes_deduped_candidates_and_trust_gate",
        "range": {"start": str(start)[:10], "end": str(end)[:10], "days_with_payloads": len(daily)},
        "aggregate": aggregate,
        "daily": daily,
        "important_note": (
            "Promotion decisions must use trusted same-day forward outcomes, deduped candidates, "
            "and promotion_allowed=true trust-gate rows only."
        ),
    }


def render_q8_trusted_reaggregation_markdown(payload: Mapping[str, Any]) -> str:
    return _c03_10_a7_owner.render_q8_trusted_reaggregation_markdown(payload, facade=sys.modules[__name__])


def write_q8_trusted_reaggregation(
    *,
    reports_root: Path,
    start: str,
    end: str,
    output_dir: Path,
) -> Dict[str, Path]:
    payload = build_q8_trusted_reaggregation(reports_root=reports_root, start=start, end=end)
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = f"q8_trusted_reaggregation_{str(start)[:10]}_to_{str(end)[:10]}"
    json_path = output_dir / f"{stem}.json"
    md_path = output_dir / f"{stem}.md"
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(render_q8_trusted_reaggregation_markdown(payload), encoding="utf-8")
    return {"json": json_path, "markdown": md_path}
