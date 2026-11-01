"""RF-039 existing_evidence_mining: ``discovery_cohorts`` body (moved verbatim from ``analysis``).

``facade`` is the ``analysis`` module; module-level names and helpers are resolved on it at call time so caller
monkeypatching keeps working. This module never imports ``analysis``. Pure, no IO.
"""
from __future__ import annotations

from typing import Any, Iterable, Mapping


def discovery_cohorts(episodes: list[Mapping[str, Any]], *, facade: Any) -> dict[str, Any]:
    cohorts = {
        "opening_all": [row for row in episodes if row.get("time_bucket") == "open_0_20m"],
        "opening_rank1": [
            row
            for row in episodes
            if row.get("time_bucket") == "open_0_20m" and row.get("rank_bucket") == "rank1"
        ],
        "opening_rank2_3": [
            row
            for row in episodes
            if row.get("time_bucket") == "open_0_20m" and row.get("rank_bucket") == "rank2_3"
        ],
    }
    output: dict[str, Any] = {}
    for name, rows in cohorts.items():
        output[name] = {
            "overall": {horizon: facade.summarize_rows(rows, horizon) for horizon in facade.HORIZONS},
            "calibration": {
                horizon: facade.summarize_rows(
                    [row for row in rows if str(row.get("day") or "") <= "2026-07-10"],
                    horizon,
                )
                for horizon in facade.HORIZONS
            },
            "retrospective": {
                horizon: facade.summarize_rows(
                    [row for row in rows if str(row.get("day") or "") >= "2026-07-13"],
                    horizon,
                )
                for horizon in facade.HORIZONS
            },
        }
    return output
