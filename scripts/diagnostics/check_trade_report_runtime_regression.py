from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from libs.reporting.llm_artifacts import trade_artifact_paths
from scripts.diagnostics import trade_artifact_command_projection as trade_commands
from scripts.diagnostics import trade_artifact_validation_read_projection as trade_read
from scripts.diagnostics import trade_artifact_context_projection as trade_context
from scripts.diagnostics import trade_artifact_validation_evidence_projection as trade_evidence
from scripts.diagnostics import trade_artifact_validation_cli as trade_cli


DEFAULT_GOLDEN_CASES: Tuple[Tuple[str, str], ...] = (
    ("2026-04-15", "TRD_20260415_000660_04"),
    ("2026-04-16", "TRD_20260416_000660_01"),
    ("2026-04-16", "TRD_20260416_047040_01"),
)


def _emit_text(text: str) -> None:
    payload = str(text or "")
    try:
        sys.stdout.write(payload)
        if not payload.endswith("\n"):
            sys.stdout.write("\n")
        sys.stdout.flush()
        return
    except UnicodeEncodeError:
        pass
    sys.stdout.buffer.write(payload.encode("utf-8", errors="replace"))
    if not payload.endswith("\n"):
        sys.stdout.buffer.write(b"\n")
    sys.stdout.buffer.flush()


def _read_json(path: Path) -> Dict[str, Any]:
    return trade_read._read_json(path, facade=sys.modules[__name__])


def _safe_int(value: Any, default: int = 0) -> int:
    from scripts.diagnostics import trade_artifact_evidence_predicates as _owner
    return _owner._safe_int(value=value, default=default, facade=sys.modules[__name__])


def _is_closed_trade(lifecycle_bundle: Dict[str, Any], exit_payload: Dict[str, Any]) -> bool:
    from scripts.diagnostics import trade_artifact_evidence_predicates as _owner
    return _owner._is_closed_trade(lifecycle_bundle=lifecycle_bundle, exit_payload=exit_payload, facade=sys.modules[__name__])


def _is_empty_placeholder(value: Any) -> bool:
    from scripts.diagnostics import trade_artifact_evidence_predicates as _owner
    return _owner._is_empty_placeholder(value=value, facade=sys.modules[__name__])


def _has_substantive_entry_evidence(entry_payload: Dict[str, Any]) -> bool:
    from scripts.diagnostics import trade_artifact_evidence_predicates as _owner
    return _owner._has_substantive_entry_evidence(entry_payload=entry_payload, facade=sys.modules[__name__])


def _has_substantive_exit_evidence(exit_payload: Dict[str, Any]) -> bool:
    from scripts.diagnostics import trade_artifact_evidence_predicates as _owner
    return _owner._has_substantive_exit_evidence(exit_payload=exit_payload, facade=sys.modules[__name__])


def _section_provenance_all_fallback(report: Dict[str, Any]) -> bool:
    from scripts.diagnostics import trade_artifact_evidence_predicates as _owner
    return _owner._section_provenance_all_fallback(report=report, facade=sys.modules[__name__])


def _parse_case(raw: str) -> Dict[str, str]:
    from scripts.diagnostics import trade_artifact_case_projection as _owner
    return _owner._parse_case(raw=raw, facade=sys.modules[__name__])


def _normalize_cases(values: List[str]) -> List[Dict[str, str]]:
    from scripts.diagnostics import trade_artifact_case_projection as _owner
    return _owner._normalize_cases(values=values, facade=sys.modules[__name__])


def _resolve_trade_context(reports_root: Path, day: str, trade_id: str) -> Dict[str, Any]:
    return trade_context._resolve_trade_context(reports_root, day, trade_id, facade=sys.modules[__name__])


def _command_to_text(command: List[str]) -> str:
    from scripts.diagnostics import trade_artifact_command_text as _owner
    return _owner._command_to_text(command=command, facade=sys.modules[__name__])


def _run_python_json(command: List[str]) -> Dict[str, Any]:
    proc = subprocess.run(
        command,
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    stdout = str(proc.stdout or "").strip()
    payload: Dict[str, Any] = {}
    if stdout:
        for line in reversed(stdout.splitlines()):
            try:
                candidate = json.loads(line)
            except Exception:
                continue
            if isinstance(candidate, dict):
                payload = candidate
                break
    return {
        "ok": proc.returncode == 0,
        "returncode": proc.returncode,
        "stdout": stdout,
        "stderr": str(proc.stderr or "").strip(),
        "json": payload,
        "command": _command_to_text(command),
    }


def _build_bundle_repair_command(
    *,
    day: str,
    target_run_id: str,
    role: str,
    max_runs: int,
    event_log_path: str,
    evidence_log_path: str,
    report_dir: str,
    reports_root: str,
) -> List[str]:
    return trade_commands._build_bundle_repair_command(
        day=day, target_run_id=target_run_id, role=role, max_runs=max_runs,
        event_log_path=event_log_path, evidence_log_path=evidence_log_path,
        report_dir=report_dir, reports_root=reports_root, facade=sys.modules[__name__],
    )


def _build_report_regen_command(
    *, day: str, trade_id: str, reports_root: str, local_debug: bool,
    hard_timeout_sec: Optional[float], with_llm: bool = False,
) -> List[str]:
    return trade_commands._build_report_regen_command(day=day, trade_id=trade_id, reports_root=reports_root, local_debug=local_debug, hard_timeout_sec=hard_timeout_sec, with_llm=with_llm, facade=sys.modules[__name__])


def validate_trade_artifact_chain(reports_root: Path, day: str, trade_id: str) -> Dict[str, Any]:
    return trade_evidence.validate_trade_artifact_chain(
        reports_root, day, trade_id, facade=sys.modules[__name__]
    )


def _build_parser() -> argparse.ArgumentParser:
    return trade_cli._build_parser(facade=sys.modules[__name__])


def main(argv: Optional[List[str]] = None) -> int:
    args = _build_parser().parse_args(argv)
    reports_root = Path(str(args.reports_root or "reports")).resolve()
    cases = _normalize_cases(args.case)
    rows: List[Dict[str, Any]] = []
    overall_failures = 0

    for case in cases:
        day = str(case.get("day") or "").strip()
        trade_id = str(case.get("trade_id") or "").strip()
        requested_run_id = str(case.get("target_run_id") or "").strip()
        before_ctx = _resolve_trade_context(reports_root, day, trade_id)
        target_run_id = requested_run_id or str(before_ctx.get("target_run_id") or "").strip()

        repair_result: Dict[str, Any] = {"skipped": bool(args.skip_repair), "ok": False, "command": ""}
        if not args.skip_repair and target_run_id:
            repair_command = _build_bundle_repair_command(
                day=day,
                target_run_id=target_run_id,
                role=str(args.role or "manual_repair_bundle"),
                max_runs=int(args.max_runs or 200),
                event_log_path=str(args.event_log_path or "data/logs/events.jsonl"),
                evidence_log_path=str(args.evidence_log_path or "data/evidence_ledger/events.jsonl"),
                report_dir=str(args.report_dir or "reports/dev/analysis/live_execution_bundles"),
                reports_root=str(args.reports_root or "reports"),
            )
            repair_result = _run_python_json(repair_command)
        elif not args.skip_repair:
            repair_result = {
                "skipped": True,
                "ok": False,
                "command": "",
                "stderr": "",
                "stdout": "",
                "json": {},
                "returncode": 0,
                "reason": "target_run_id_missing",
            }

        local_debug_result: Dict[str, Any] = {"skipped": bool(args.skip_local_debug), "ok": False, "command": ""}
        if not args.skip_local_debug:
            local_debug_result = _run_python_json(
                _build_report_regen_command(
                    day=day,
                    trade_id=trade_id,
                    reports_root=str(args.reports_root or "reports"),
                    local_debug=True,
                    with_llm=False,
                    hard_timeout_sec=5.0,
                )
            )

        llm_result: Dict[str, Any] = {"skipped": not bool(args.llm_acceptance), "ok": False, "command": ""}
        if bool(args.llm_acceptance):
            llm_result = _run_python_json(
                _build_report_regen_command(
                    day=day,
                    trade_id=trade_id,
                    reports_root=str(args.reports_root or "reports"),
                    local_debug=False,
                    with_llm=True,
                    hard_timeout_sec=float(args.llm_hard_timeout_sec or 900.0),
                )
            )

        validation = validate_trade_artifact_chain(reports_root, day, trade_id)
        row = {
            "day": day,
            "trade_id": trade_id,
            "requested_target_run_id": requested_run_id,
            "resolved_target_run_id": target_run_id,
            "repair": repair_result,
            "local_debug_regen": local_debug_result,
            "llm_acceptance": llm_result,
            "validation": validation,
        }
        if not validation.get("ok"):
            overall_failures += 1
        rows.append(row)

    payload = {
        "ok": overall_failures == 0,
        "case_count": len(rows),
        "failed_case_count": overall_failures,
        "rows": rows,
    }

    if args.json:
        _emit_text(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        for row in rows:
            validation = row["validation"]
            status = "PASS" if validation.get("ok") else "FAIL"
            _emit_text(f"[{status}] {row['day']} {row['trade_id']}")
            _emit_text(f"  target_run_id={row.get('resolved_target_run_id') or '-'}")
            _emit_text(
                f"  repair={'ok' if row['repair'].get('ok') else 'skip' if row['repair'].get('skipped') else 'fail'} "
                f"local_debug={'ok' if row['local_debug_regen'].get('ok') else 'skip' if row['local_debug_regen'].get('skipped') else 'fail'} "
                f"llm={'ok' if row['llm_acceptance'].get('ok') else 'skip' if row['llm_acceptance'].get('skipped') else 'fail'}"
            )
            _emit_text(
                f"  entry={validation.get('entry_run_id') or '-'} exit={validation.get('exit_run_id') or '-'} "
                f"linked={len(validation.get('linked_run_ids') or [])} selected_rank={validation.get('selected_rank')} "
                f"candidate_count={validation.get('candidate_count')} hold={validation.get('hold_duration') or '-'}"
            )
            if validation.get("failures"):
                _emit_text("  failures: " + ", ".join(str(item) for item in validation["failures"]))
            if validation.get("warnings"):
                _emit_text("  warnings: " + ", ".join(str(item) for item in validation["warnings"]))
        _emit_text(f"[summary] cases={len(rows)} failed={overall_failures}")
    return 0 if overall_failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
