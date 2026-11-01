"""operator_period_summary: ``_truth_surface_candidate_paths`` body (moved verbatim from ``operator_period_summary``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple


def _truth_surface_candidate_paths(row: Dict[str, Any], reports_root: Path, *, facade: Any) -> List[Path]:
    candidates: List[facade.Path] = []
    for key in ("trade_root_path",):
        raw = str(row.get(key) or "").strip()
        if raw:
            candidates.append(facade.Path(raw) / "reports" / "ai_trade_summary.json")
            candidates.append(facade.Path(raw) / "reports" / "ai_trade_summary_input.json")
    report_path = str(row.get("report_path") or "").strip()
    if report_path:
        report_dir = facade.Path(report_path).parent
        candidates.append(report_dir / "ai_trade_summary.json")
        candidates.append(report_dir / "ai_trade_summary_input.json")
    lifecycle_path = str(row.get("lifecycle_bundle_path") or "").strip()
    if lifecycle_path:
        trade_root = facade.Path(lifecycle_path).parent
        candidates.append(trade_root / "reports" / "ai_trade_summary.json")
        candidates.append(trade_root / "reports" / "ai_trade_summary_input.json")
    trade_id = str(row.get("trade_id") or "").strip()
    day = str(row.get("date") or row.get("day") or "").strip()[:10]
    if trade_id and day:
        trade_root = facade.find_trade_dir(facade.canonical_trade_day_root(facade.Path(reports_root), day), trade_id)
        if trade_root is None:
            trade_root = facade.Path(reports_root) / "trades" / day / trade_id
        candidates.append(trade_root / "reports" / "ai_trade_summary.json")
        candidates.append(trade_root / "reports" / "ai_trade_summary_input.json")
    out: List[facade.Path] = []
    seen: set[str] = set()
    for path in candidates:
        key = str(path)
        if key in seen:
            continue
        seen.add(key)
        out.append(path)
    return out
