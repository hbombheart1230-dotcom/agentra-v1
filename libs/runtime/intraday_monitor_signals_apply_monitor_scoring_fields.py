from __future__ import annotations

from typing import Any, Dict, Mapping, Sequence


def _apply_monitor_scoring_fields(
    out: Dict[str, Any], *, scoring_settings: Dict[str, Any],
    hard_filter_passed: bool, hard_filter_fail_reasons: Sequence[str] | None,
    score_breakdown: Mapping[str, Any] | None = None,
    legacy_entry_decision: str = "WAIT", scoring_entry_decision: str = "WAIT",
    facade: Any,
) -> Dict[str, Any]:
    breakdown = dict(score_breakdown or {})
    total_score = round(sum(facade._to_float(v) for v in breakdown.values()), 4) if breakdown else 0.0
    threshold = float(scoring_settings.get("entry_threshold") or 3.0)
    score_passed = bool(hard_filter_passed) and total_score >= threshold
    fail_reasons = [str(x or "").strip() for x in list(hard_filter_fail_reasons or []) if str(x or "").strip()]
    out["hard_filter_passed"] = bool(hard_filter_passed)
    out["hard_filter_fail_reasons"] = fail_reasons
    out["total_score"] = total_score
    out["score_breakdown"] = breakdown
    out["entry_threshold"] = threshold
    out["score_passed"] = bool(score_passed)
    out["scoring_mode"] = str(scoring_settings.get("scoring_mode") or "disabled")
    out["legacy_entry_decision"] = str(legacy_entry_decision or "WAIT")
    out["scoring_entry_decision"] = str(scoring_entry_decision or ("BUY" if score_passed else "WAIT"))
    return out
