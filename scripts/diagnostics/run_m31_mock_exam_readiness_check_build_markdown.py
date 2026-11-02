from __future__ import annotations

from typing import Any, Dict


def _build_markdown(out: Dict[str, Any], *, facade: object = None) -> str:
    stage = out.get("stage_checks") if isinstance(out.get("stage_checks"), dict) else {}
    runtime = out.get("runtime_profile") if isinstance(out.get("runtime_profile"), dict) else {}
    guard = out.get("guardrails") if isinstance(out.get("guardrails"), dict) else {}
    checklist = out.get("checklist") if isinstance(out.get("checklist"), list) else []
    missing = out.get("missing_prerequisites") if isinstance(out.get("missing_prerequisites"), list) else []
    lines = [
        f"# M31 Mock Exam Readiness Check ({out.get('day')})", "",
        f"- ok: **{bool(out.get('ok'))}**",
        f"- required_pass_total: **{int(out.get('required_pass_total') or 0)}**",
        f"- required_fail_total: **{int(out.get('required_fail_total') or 0)}**", "",
        "## Stage Checks", "",
        f"- m30_final_signoff: rc={int(stage.get('m30_final_signoff_rc') or 0)} ok={bool(stage.get('m30_final_signoff_ok'))}",
        f"- m30_post_golive_policy: rc={int(stage.get('m30_post_golive_policy_rc') or 0)} ok={bool(stage.get('m30_post_golive_policy_ok'))}",
        f"- m31_slo_incident: rc={int(stage.get('m31_slo_incident_rc') or 0)} ok={bool(stage.get('m31_slo_incident_ok'))}",
        f"- m31_mock_exam: rc={int(stage.get('m31_mock_exam_rc') or 0)} ok={bool(stage.get('m31_mock_exam_ok'))}", "",
        "## Runtime Profile", "",
        f"- RUNTIME_PROFILE: **{runtime.get('RUNTIME_PROFILE')}**", f"- KIWOOM_MODE: **{runtime.get('KIWOOM_MODE')}**",
        f"- APPROVAL_MODE: **{runtime.get('APPROVAL_MODE')}**", f"- EXECUTION_ENABLED: **{bool(runtime.get('EXECUTION_ENABLED'))}**",
        f"- ALLOW_REAL_EXECUTION: **{bool(runtime.get('ALLOW_REAL_EXECUTION'))}**", "", "## Guardrails", "",
        f"- allowlist_size: **{int(guard.get('allowlist_size') or 0)}**",
        "- SYMBOL_ALLOWLIST policy: **optional operational guard (recommended but not mandatory)**",
        f"- max_notional_key: **{guard.get('max_notional_key')}**", f"- max_notional: **{float(guard.get('max_notional') or 0.0):.2f}**",
        f"- daily_loss_limit: **{float(guard.get('daily_loss_limit') or 0.0):.6f}**", "", "## Checklist", "",
    ]
    for item in checklist:
        mark = "x" if bool(item.get("passed")) else " "
        lines.append(f"- [{mark}] {item.get('title')} | evidence={item.get('evidence')}")
    lines += ["", "## Missing Prerequisites", ""]
    if missing:
        for row in missing:
            lines.append(f"- {row}")
    else:
        lines.append("- (none)")
    lines.append("")
    return "\n".join(lines)
