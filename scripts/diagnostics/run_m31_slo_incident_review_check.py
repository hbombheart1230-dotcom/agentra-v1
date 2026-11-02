from __future__ import annotations

# Direct execution from the deeper scripts package retains repository imports.
import sys as _migration_sys
from pathlib import Path as _MigrationPath
_migration_root = _MigrationPath(__file__).resolve().parents[2]
if str(_migration_root) not in _migration_sys.path:
    _migration_sys.path.insert(0, str(_migration_root))

import argparse
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional


def _to_epoch(ts: Any) -> Optional[int]:
    from scripts.diagnostics.run_m31_slo_incident_review_check_to_epoch import _to_epoch as owner

    return owner(ts, facade=_migration_sys.modules[__name__])


def _utc_day(ts: Any) -> Optional[str]:
    from scripts.diagnostics.run_m31_slo_incident_review_check_utc_day import _utc_day as owner

    return owner(ts, facade=_migration_sys.modules[__name__])


def _iter_jsonl(path: Path) -> Iterable[Dict[str, Any]]:
    from scripts.diagnostics.run_m31_slo_incident_review_check_iter_jsonl import _iter_jsonl as owner

    return owner(path, facade=_migration_sys.modules[__name__])


def _read_json(path: Path) -> Dict[str, Any]:
    from scripts.diagnostics.run_m31_slo_incident_review_check_read_json import _read_json as owner

    return owner(path, facade=_migration_sys.modules[__name__])


def _resolve_day_artifact(report_dir: Path, prefix: str, day: str) -> tuple[Path, Dict[str, Any], bool]:
    direct = report_dir / f"{prefix}_{day}.json"
    direct_obj = _read_json(direct)
    if direct_obj:
        return direct, direct_obj, False

    target_day = str(day or "").strip()
    best_day = ""
    best_path = direct
    best_obj: Dict[str, Any] = {}
    pattern = f"{prefix}_*.json"
    for path in sorted(report_dir.glob(pattern)):
        stem = path.stem
        if not stem.startswith(f"{prefix}_"):
            continue
        candidate_day = stem[len(prefix) + 1 :].strip()
        if not candidate_day:
            continue
        if target_day and candidate_day > target_day:
            continue
        obj = _read_json(path)
        if not obj:
            continue
        if not best_day or candidate_day > best_day:
            best_day = candidate_day
            best_path = path
            best_obj = obj
    return best_path, best_obj, bool(best_obj)


def _item(
    *,
    item_id: str,
    title: str,
    passed: bool,
    evidence: str,
    required: bool = True,
) -> Dict[str, Any]:
    from scripts.diagnostics.run_m31_slo_incident_review_check_item import _item as owner

    return owner(item_id=item_id, title=title, passed=passed, evidence=evidence, required=required, facade=_migration_sys.modules[__name__])


def _severity_from_level(level: str) -> str:
    from scripts.diagnostics.run_m31_slo_incident_review_check_severity_from_level import _severity_from_level as owner

    return owner(level, facade=_migration_sys.modules[__name__])


def _ownership_from_level(level: str) -> str:
    from scripts.diagnostics.run_m31_slo_incident_review_check_ownership_from_level import _ownership_from_level as owner

    return owner(level, facade=_migration_sys.modules[__name__])


def _build_markdown(out: Dict[str, Any]) -> str:
    from scripts.diagnostics.run_m31_slo_incident_review_check_build_markdown import _build_markdown as owner

    return owner(out, facade=_migration_sys.modules[__name__])


def _build_parser() -> argparse.ArgumentParser:
    from scripts.diagnostics.run_m31_slo_incident_review_check_build_parser import _build_parser as owner

    return owner(facade=_migration_sys.modules[__name__])


def main(argv: Optional[List[str]] = None) -> int:
    args = _build_parser().parse_args(argv)
    day = str(args.day or "2026-02-21").strip()
    event_log_path = Path(str(args.event_log_path).strip())
    policy_report_dir = Path(str(args.policy_report_dir).strip())
    signoff_report_dir = Path(str(args.signoff_report_dir).strip())
    report_dir = Path(str(args.report_dir).strip())
    min_availability_rate = max(0.0, min(1.0, float(args.min_availability_rate)))
    max_error_rate = max(0.0, min(1.0, float(args.max_error_rate)))
    inject_fail = bool(args.inject_fail)

    report_dir.mkdir(parents=True, exist_ok=True)

    event_total = 0
    error_total = 0
    run_total_set: set[str] = set()
    error_run_set: set[str] = set()
    cooldown_transition_total = 0
    intervention_total = 0
    stage_error_total: Counter[str] = Counter()

    for row in _iter_jsonl(event_log_path):
        row_day = _utc_day(row.get("ts"))
        if row_day != day:
            continue

        event_total += 1
        run_id = str(row.get("run_id") or "").strip()
        if run_id:
            run_total_set.add(run_id)

        stage = str(row.get("stage") or "").strip()
        event = str(row.get("event") or "").strip()
        payload = row.get("payload") if isinstance(row.get("payload"), dict) else {}

        if event == "error":
            error_total += 1
            if run_id:
                error_run_set.add(run_id)
            stage_error_total[stage or "unknown"] += 1

        if stage == "commander_router" and event == "transition":
            transition = str(payload.get("transition") or "").strip().lower()
            if transition == "cooldown":
                cooldown_transition_total += 1

        if stage == "commander_router" and event == "intervention":
            intervention_total += 1

    run_total = int(len(run_total_set))
    success_run_total = int(max(0, run_total - len(error_run_set)))
    availability_rate = float(success_run_total) / float(run_total) if run_total > 0 else 0.0
    error_rate = float(error_total) / float(event_total) if event_total > 0 else 0.0

    policy_path, policy_obj, policy_fallback_used = _resolve_day_artifact(
        policy_report_dir,
        "m30_post_golive_policy",
        day,
    )
    signoff_path, signoff_obj, signoff_fallback_used = _resolve_day_artifact(
        signoff_report_dir,
        "m30_final_golive_signoff",
        day,
    )

    escalation_level = str(policy_obj.get("escalation_level") or "").strip().lower()
    policy = policy_obj.get("policy") if isinstance(policy_obj.get("policy"), dict) else {}
    manual_approval_only = bool(policy.get("manual_approval_only"))
    oncall_escalation = str(policy.get("oncall_escalation") or "").strip().lower()
    severity = _severity_from_level(escalation_level)
    expected_ownership = _ownership_from_level(escalation_level)
    ownership_ok = (oncall_escalation == expected_ownership) or (not escalation_level)

    checklist: List[Dict[str, Any]] = [
        _item(
            item_id="policy_artifact_presence",
            title="M30 post-go-live policy artifact exists",
            passed=bool(policy_obj),
            evidence=(
                f"path={policy_path}, exists={bool(policy_obj)}, "
                f"fallback_used={policy_fallback_used}"
            ),
        ),
        _item(
            item_id="signoff_artifact_presence",
            title="M30 final signoff artifact exists",
            passed=bool(signoff_obj),
            evidence=(
                f"path={signoff_path}, exists={bool(signoff_obj)}, "
                f"fallback_used={signoff_fallback_used}"
            ),
        ),
        _item(
            item_id="slo_probe_measurable",
            title="Daily SLO probes are measurable from artifacts",
            passed=(event_total > 0 and run_total > 0),
            evidence=f"event_total={event_total}, run_total={run_total}",
        ),
        _item(
            item_id="slo_availability_guard",
            title="Availability rate meets threshold",
            passed=availability_rate >= min_availability_rate,
            evidence=f"availability_rate={availability_rate:.4f}, threshold={min_availability_rate:.4f}",
        ),
        _item(
            item_id="slo_error_budget_guard",
            title="Error rate stays within threshold",
            passed=error_rate <= max_error_rate,
            evidence=f"error_rate={error_rate:.4f}, threshold={max_error_rate:.4f}",
        ),
        _item(
            item_id="severity_ownership_deterministic",
            title="Severity ladder and on-call ownership are deterministic from policy level",
            passed=ownership_ok,
            evidence=(
                f"escalation_level={escalation_level or '(none)'}, severity={severity}, "
                f"oncall_escalation={oncall_escalation or '(none)'}, expected={expected_ownership or '(none)'}"
            ),
        ),
        _item(
            item_id="incident_manual_approval_guard",
            title="Incident level enforces manual approval",
            passed=(escalation_level != "incident") or manual_approval_only,
            evidence=f"escalation_level={escalation_level or '(none)'}, manual_approval_only={manual_approval_only}",
        ),
    ]

    failures: List[str] = []
    for item in checklist:
        if bool(item.get("required")) and not bool(item.get("passed")):
            failures.append(f"check_failed:{item.get('id')}")
    if inject_fail:
        failures.append("inject_fail forced red-path for operator drill")

    required_total = int(sum(1 for x in checklist if bool(x.get("required"))))
    required_pass_total = int(sum(1 for x in checklist if bool(x.get("required")) and bool(x.get("passed"))))
    required_fail_total = int(required_total - required_pass_total)
    ok = (len(failures) == 0) and (not inject_fail)

    out: Dict[str, Any] = {
        "ok": bool(ok),
        "inject_fail": inject_fail,
        "day": day,
        "event_log_path": str(event_log_path),
        "policy_report_dir": str(policy_report_dir),
        "signoff_report_dir": str(signoff_report_dir),
        "report_dir": str(report_dir),
        "thresholds": {
            "min_availability_rate": min_availability_rate,
            "max_error_rate": max_error_rate,
        },
        "slo": {
            "event_total": int(event_total),
            "error_total": int(error_total),
            "error_rate": float(error_rate),
            "run_total": int(run_total),
            "success_run_total": int(success_run_total),
            "availability_rate": float(availability_rate),
            "stage_error_top": dict(stage_error_total.most_common(5)),
        },
        "incident": {
            "cooldown_transition_total": int(cooldown_transition_total),
            "intervention_total": int(intervention_total),
        },
        "policy": {
            "path": str(policy_path),
            "exists": bool(policy_obj),
            "fallback_used": bool(policy_fallback_used),
            "escalation_level": escalation_level,
            "severity": severity,
            "ownership": expected_ownership,
            "manual_approval_only": manual_approval_only,
            "oncall_escalation": oncall_escalation,
        },
        "signoff": {
            "path": str(signoff_path),
            "exists": bool(signoff_obj),
            "fallback_used": bool(signoff_fallback_used),
            "approved": bool(signoff_obj.get("approved")),
            "go_live_decision": str(signoff_obj.get("go_live_decision") or ""),
        },
        "checklist": checklist,
        "required_total": required_total,
        "required_pass_total": required_pass_total,
        "required_fail_total": required_fail_total,
        "failure_total": int(len(failures)),
        "failures": failures,
    }

    js_path = report_dir / f"m31_slo_incident_{day}.json"
    md_path = report_dir / f"m31_slo_incident_{day}.md"
    out["report_json_path"] = str(js_path)
    out["report_md_path"] = str(md_path)
    js_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(_build_markdown(out), encoding="utf-8")

    if bool(args.json):
        print(json.dumps(out, ensure_ascii=False))
    else:
        print(
            f"ok={out['ok']} day={day} availability_rate={out['slo']['availability_rate']:.2%} "
            f"error_rate={out['slo']['error_rate']:.2%} severity={out['policy']['severity']} "
            f"failure_total={out['failure_total']}"
        )
        for msg in failures:
            print(msg)
    return 0 if bool(ok) else 3


if __name__ == "__main__":
    raise SystemExit(main())
