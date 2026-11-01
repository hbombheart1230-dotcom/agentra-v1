from typing import Any, Dict


def _build_markdown(*, day: str, out: Dict[str, Any], facade: Any) -> str:
    anomalies = out.get("anomaly_examples") if isinstance(out.get("anomaly_examples"), dict) else {}
    stage_event_total = out.get("stage_event_total") if isinstance(out.get("stage_event_total"), dict) else {}
    lines = [f"# Audit Trail Completeness ({day})", "", f"- ok: **{bool(out.get('ok'))}**", f"- events: **{int(out.get('events') or 0)}**", f"- runs: **{int(out.get('run_total') or 0)}**", f"- actionable_decision_run_total: **{int(out.get('actionable_decision_run_total') or 0)}**", f"- linked_complete_run_total: **{int(out.get('linked_complete_run_total') or 0)}**", f"- link_success_rate: **{float(out.get('link_success_rate') or 0.0):.2%}**", "", "## Anomaly Totals", "", f"- missing_execution_start_total: {int(out.get('missing_execution_start_total') or 0)}", f"- missing_execution_resolution_total: {int(out.get('missing_execution_resolution_total') or 0)}", f"- missing_execution_payload_total: {int(out.get('missing_execution_payload_total') or 0)}", f"- missing_terminal_event_total: {int(out.get('missing_terminal_event_total') or 0)}", f"- orphan_execution_run_total: {int(out.get('orphan_execution_run_total') or 0)}", "", "## execute_from_packet stage_event_total", ""]
    for k in ("start", "verdict", "execution", "degrade_policy_block", "end", "error"):
        lines.append(f"- {k}: {int(stage_event_total.get(k) or 0)}")
    lines += ["", "## Anomaly Examples", ""]
    for key in ("missing_execution_start", "missing_execution_resolution", "missing_execution_payload", "missing_terminal_event", "orphan_execution"):
        vals = anomalies.get(key) if isinstance(anomalies.get(key), list) else []
        lines.append(f"- {key}: {', '.join(str(x) for x in vals)}" if vals else f"- {key}: (none)")
    failures = out.get("failures") if isinstance(out.get("failures"), list) else []
    lines += ["", "## Failures", ""]
    lines.extend(f"- {x}" for x in failures) if failures else lines.append("- (none)")
    lines.append("")
    return "\n".join(lines)
