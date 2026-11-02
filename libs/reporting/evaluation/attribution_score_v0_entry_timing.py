"""attribution_score_v0: ``_entry_timing`` body (moved verbatim from ``attribution_score_v0``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping


def _entry_timing(entry_timing_report: Mapping[str, Any], *, facade: Any) -> dict[str, Any]:
    rows = facade._as_rows(entry_timing_report.get("rows"))
    sufficient = [row for row in rows if str(row.get("label") or "") != facade.INSUFFICIENT]
    if not sufficient:
        return facade._score(facade.INSUFFICIENT, None, ["entry_timing_rows_missing_or_insufficient"])
    label_scores = {
        "ENTRY_APPROPRIATE": 100.0,
        "ENTRY_TOO_EARLY": 35.0,
        "ENTRY_TOO_LATE": 35.0,
    }
    scores: list[float] = []
    reasons: list[str] = []
    for row in sufficient:
        label = str(row.get("label") or "")
        scores.append(label_scores.get(label, 50.0))
        if label != "ENTRY_APPROPRIATE":
            reasons.append(f"{row.get('trade_id')}:{label}")
    return facade._score(
        facade.OK,
        facade._clamp_score(sum(scores) / len(scores)),
        reasons or ["entry_timing_not_primary_failure_in_observed_rows"],
        {"classified_trade_count": len(sufficient), "total_trade_count": len(rows)},
    )
