from __future__ import annotations

from typing import Any, Dict


def _build_markdown(out: Dict[str, Any], *, facade: object = None) -> str:
    slo = out.get("slo") if isinstance(out.get("slo"), dict) else {}
    inc = out.get("incident") if isinstance(out.get("incident"), dict) else {}
    policy = out.get("policy") if isinstance(out.get("policy"), dict) else {}
    checklist = out.get("checklist") if isinstance(out.get("checklist"), list) else []

    lines = [
        f"# M31-1 SLO and Incident Review Check ({out.get('day')})",
        "",
        f"- ok: **{bool(out.get('ok'))}**",
        f"- required_pass_total: **{int(out.get('required_pass_total') or 0)}**",
        f"- required_fail_total: **{int(out.get('required_fail_total') or 0)}**",
        "",
        "## SLO Snapshot",
        "",
        f"- run_total: **{int(slo.get('run_total') or 0)}**",
        f"- success_run_total: **{int(slo.get('success_run_total') or 0)}**",
        f"- availability_rate: **{float(slo.get('availability_rate') or 0.0):.2%}**",
        f"- event_total: **{int(slo.get('event_total') or 0)}**",
        f"- error_total: **{int(slo.get('error_total') or 0)}**",
        f"- error_rate: **{float(slo.get('error_rate') or 0.0):.2%}**",
        "",
        "## Incident and Ownership",
        "",
        f"- escalation_level: **{policy.get('escalation_level')}**",
        f"- severity: **{policy.get('severity')}**",
        f"- ownership: **{policy.get('ownership')}**",
        f"- cooldown_transition_total: **{int(inc.get('cooldown_transition_total') or 0)}**",
        f"- intervention_total: **{int(inc.get('intervention_total') or 0)}**",
        "",
        "## Checklist",
        "",
    ]
    for item in checklist:
        mark = "x" if bool(item.get("passed")) else " "
        lines.append(f"- [{mark}] {item.get('title')} | evidence={item.get('evidence')}")

    failures = out.get("failures") if isinstance(out.get("failures"), list) else []
    lines += ["", "## Failures", ""]
    if failures:
        for msg in failures:
            lines.append(f"- {msg}")
    else:
        lines.append("- (none)")
    lines.append("")
    return "\n".join(lines)
