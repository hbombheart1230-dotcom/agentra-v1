from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def _to_epoch(ts: Any) -> Optional[int]:
    from scripts.diagnostics import audit_trail_epoch_projection as _c03_10_b1_owner
    return _c03_10_b1_owner._to_epoch(ts,facade=sys.modules[__name__])


def _utc_day(ts: Any) -> str:
    from scripts.diagnostics import audit_trail_utc_day_projection as _c03_10_b2_owner
    return _c03_10_b2_owner._utc_day(ts,facade=sys.modules[__name__])


def _extract_ts(row: Dict[str, Any]) -> Any:
    from scripts.diagnostics import audit_trail_extract_ts_projection as _c03_10_b3_owner
    return _c03_10_b3_owner._extract_ts(row,facade=sys.modules[__name__])


def _iter_rows(path: Path) -> List[Dict[str, Any]]:
    from scripts.diagnostics import audit_trail_rows_projection as owner
    return owner._iter_rows(path, facade=sys.modules[__name__])


def _extract_decision_action(row: Dict[str, Any]) -> str:
    from scripts.diagnostics import audit_trail_decision_action_projection as _c03_10_b4_owner
    return _c03_10_b4_owner._extract_decision_action(row,facade=sys.modules[__name__])


def _extract_allowed(row: Dict[str, Any]) -> Optional[bool]:
    from scripts.diagnostics import audit_trail_allowed_projection as _c03_10_b5_owner
    return _c03_10_b5_owner._extract_allowed(row,facade=sys.modules[__name__])


def _latest_day(rows: List[Dict[str, Any]]) -> str:
    from scripts.diagnostics import audit_trail_latest_day_projection as _c03_10_b6_owner
    return _c03_10_b6_owner._latest_day(rows,facade=sys.modules[__name__])


def analyze_day_rows(day_rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    from scripts.diagnostics import audit_trail_analysis_projection as owner
    return owner.analyze_day_rows(day_rows, facade=sys.modules[__name__])


def _build_markdown(*, day: str, out: Dict[str, Any]) -> str:
    from scripts.diagnostics import audit_trail_markdown_projection as _c03_11_k1_owner
    return _c03_11_k1_owner._build_markdown(day=day, out=out, facade=sys.modules[__name__])


def _build_parser() -> argparse.ArgumentParser:
    from scripts.diagnostics import audit_trail_parser_projection as _c03_11_k2_owner
    return _c03_11_k2_owner._build_parser(facade=sys.modules[__name__])


def main(argv: Optional[List[str]] = None) -> int:
    args = _build_parser().parse_args(argv)
    events_path = Path(str(args.event_log_path).strip())
    report_dir = Path(str(args.report_dir).strip())
    report_dir.mkdir(parents=True, exist_ok=True)

    rows = _iter_rows(events_path)
    prepared: List[Dict[str, Any]] = []
    for row in rows:
        ts = _extract_ts(row)
        prepared.append({**row, "_day": _utc_day(ts)})

    day = str(args.day or "").strip()
    if not day:
        day = _latest_day(prepared)

    day_rows = [r for r in prepared if str(r.get("_day") or "") == day]
    analysis = analyze_day_rows(day_rows)

    failures: List[str] = []
    if int(analysis.get("missing_execution_start_total") or 0) > 0:
        failures.append("missing_execution_start_total > 0")
    if int(analysis.get("missing_execution_resolution_total") or 0) > 0:
        failures.append("missing_execution_resolution_total > 0")
    if int(analysis.get("missing_execution_payload_total") or 0) > 0:
        failures.append("missing_execution_payload_total > 0")
    if int(analysis.get("missing_terminal_event_total") or 0) > 0:
        failures.append("missing_terminal_event_total > 0")
    if int(analysis.get("orphan_execution_run_total") or 0) > 0:
        failures.append("orphan_execution_run_total > 0")
    if bool(args.require_actionable) and int(analysis.get("actionable_decision_run_total") or 0) < 1:
        failures.append("actionable_decision_run_total < 1")

    out: Dict[str, Any] = {
        "ok": len(failures) == 0,
        "day": day,
        "event_log_path": str(events_path),
        "events": int(len(day_rows)),
        **analysis,
        "failures": failures,
    }

    js_path = report_dir / f"audit_trail_{day}.json"
    md_path = report_dir / f"audit_trail_{day}.md"
    out["report_json_path"] = str(js_path)
    out["report_md_path"] = str(md_path)

    js_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(_build_markdown(day=day, out=out), encoding="utf-8")

    if bool(args.json):
        print(json.dumps(out, ensure_ascii=False))
    else:
        print(
            f"ok={out['ok']} day={day} actionable={out['actionable_decision_run_total']} "
            f"linked={out['linked_complete_run_total']} missing={len(failures)}"
        )
        for msg in failures:
            print(msg)

    return 0 if len(failures) == 0 else 3


if __name__ == "__main__":
    raise SystemExit(main())
