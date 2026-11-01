"""operator_period_summary: ``_closeout_broker_skip_for_row`` body (moved verbatim from ``operator_period_summary``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple


def _closeout_broker_skip_for_row(row: Dict[str, Any], reports_root: Path, *, facade: Any) -> Dict[str, Any]:
    day = str(row.get("date") or row.get("day") or "").strip()[:10]
    trade_id = str(row.get("trade_id") or "").strip()
    if not day or not trade_id:
        return {}
    closeout = facade._read_json(facade.Path(reports_root) / "operator_summary" / "daily" / day / "closeout_maintenance.json")
    if not isinstance(closeout, dict):
        return {}
    steps = closeout.get("steps") if isinstance(closeout.get("steps"), dict) else {}
    broker = (
        steps.get("broker_closed_trade_reconciliation")
        if isinstance(steps.get("broker_closed_trade_reconciliation"), dict)
        else {}
    )
    for skipped in broker.get("skipped") or []:
        if not isinstance(skipped, dict):
            continue
        if str(skipped.get("trade_id") or "") != trade_id:
            continue
        return {
            "broker_reconciliation_status": "skipped_unresolved",
            "broker_reconciliation_reason": str(skipped.get("reason") or ""),
            "broker_reconciliation_snapshot_path": str(broker.get("snapshot_path") or ""),
        }
    return {}
