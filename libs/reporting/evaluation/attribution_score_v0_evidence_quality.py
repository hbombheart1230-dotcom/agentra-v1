"""attribution_score_v0: ``_evidence_quality`` body (moved verbatim from ``attribution_score_v0``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable, Mapping


def _evidence_quality(
    *,
    daily_scorecard: Mapping[str, Any],
    selection_authority: Mapping[str, Any],
    horizon_report: Mapping[str, Any],
    entry_timing_report: Mapping[str, Any],
    ledger_day: Mapping[str, Any],
    facade: Any,
) -> dict[str, Any]:
    integrity = facade._mapping(daily_scorecard.get("artifact_integrity"))
    counts = facade._mapping(integrity.get("status_counts"))
    total = sum(int(value or 0) for value in counts.values())
    if total <= 0:
        return facade._score(facade.INSUFFICIENT, None, ["artifact_integrity_counts_missing"])
    selection_summary = facade._mapping(selection_authority.get("summary"))
    explicitly_excluded = sum(
        int(value or 0)
        for key, value in selection_summary.items()
        if str(key).startswith("excluded:")
    )
    if explicitly_excluded >= total:
        return facade._score(
            facade.OK,
            100,
            ["all_trade_rows_explicitly_excluded_from_behavior_metrics"],
            {
                "integrity_status_counts": dict(counts),
                "explicitly_excluded_trade_count": explicitly_excluded,
                "ledger_day_present": bool(ledger_day),
                "ledger_evidence_status": ledger_day.get("evidence_status") if ledger_day else "",
            },
        )
    pass_count = int(counts.get("PASS") or 0)
    watch_count = int(counts.get("WATCH") or 0)
    score = ((pass_count + (0.7 * watch_count)) / total) * 100.0
    reasons: list[str] = []
    if int(counts.get("FAIL") or 0) > 0:
        reasons.append("fail_integrity_rows_present")
    if int(counts.get("BLOCKER") or 0) > 0:
        reasons.append("blocker_integrity_rows_present")
    if not facade._as_rows(selection_authority.get("rows")):
        score -= 10.0
        reasons.append("selection_authority_rows_missing")
    if not facade._as_rows(horizon_report.get("rows")):
        score -= 10.0
        reasons.append("horizon_rows_missing")
    if not facade._as_rows(entry_timing_report.get("rows")):
        score -= 10.0
        reasons.append("entry_timing_rows_missing")
    if ledger_day:
        evidence_status = str(ledger_day.get("evidence_status") or "")
        if evidence_status and evidence_status.upper() != "COMPLETE":
            score -= 15.0
            reasons.append(f"ledger_evidence_status:{evidence_status}")
    return facade._score(
        facade.OK,
        facade._clamp_score(score),
        reasons or ["evidence_surfaces_available"],
        {
            "integrity_status_counts": dict(counts),
            "ledger_day_present": bool(ledger_day),
            "ledger_evidence_status": ledger_day.get("evidence_status") if ledger_day else "",
        },
    )
