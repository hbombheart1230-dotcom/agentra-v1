"""RF-039 existing_evidence_mining: ``split_summary`` body (moved verbatim from ``analysis``).

``facade`` is the ``analysis`` module; module-level names and helpers are resolved on it at call time so caller
monkeypatching keeps working. This module never imports ``analysis``. Pure, no IO.
"""
from __future__ import annotations

from typing import Any, Iterable, Mapping


def split_summary(
    episodes: list[Mapping[str, Any]],
    *,
    field: str,
    calibration_end: str,
    retrospective_start: str,
    facade: Any,
) -> dict[str, Any]:
    return {
        "calibration": facade.grouped_horizon_summary(
            [row for row in episodes if str(row.get("day") or "") <= calibration_end],
            field=field,
        ),
        "retrospective": facade.grouped_horizon_summary(
            [row for row in episodes if str(row.get("day") or "") >= retrospective_start],
            field=field,
        ),
    }
