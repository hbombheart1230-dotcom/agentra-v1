"""scanner_alignment_root_cause: ``_largest_cause`` body (moved verbatim from ``scanner_alignment_root_cause``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Mapping, Sequence


def _largest_cause(
    cause_summary: Sequence[Mapping[str, Any]],
    *,
    excluded: set[str] | None = None,
    facade: Any,
) -> dict[str, Any]:
    excluded = excluded or set()
    observed = [
        row
        for row in cause_summary
        if int(row.get("trade_count") or 0) > 0 and str(row.get("root_cause") or "") not in excluded
    ]
    return dict(
        max(
            observed,
            key=lambda row: (
                int(row.get("trade_count") or 0),
                abs(float(row.get("negative_impact_pct") or 0.0)),
            ),
            default={},
        )
    )
