"""quant_tactic_evaluation projections (moved verbatim from quant_tactic_evaluation).

Module globals and helpers are resolved on ``facade`` (the quant_tactic_evaluation module) at call time; this module never imports it.
"""
from __future__ import annotations

from typing import Any, Mapping


def _invalid_sample_reason(row: Mapping[str, Any], *, facade: Any) -> str:
    status = facade._text(row.get("broker_alignment_status")).lower()
    if status and status not in {"ok"}:
        return f"broker_alignment_{status}"
    if facade._int(row.get("broker_alignment_missing_in_local_total")) > 0:
        return "broker_missing_in_local"
    if facade._int(row.get("broker_alignment_missing_in_broker_total")) > 0:
        return "broker_missing_in_broker"
    snapshot_status = facade._text(row.get("broker_account_snapshot_status")).lower()
    if snapshot_status and snapshot_status not in {"ok"}:
        return f"account_snapshot_{snapshot_status}"
    if facade._int(row.get("broker_alignment_account_snapshot_error_count")) > 0:
        return "account_snapshot_partial_errors"
    return ""
