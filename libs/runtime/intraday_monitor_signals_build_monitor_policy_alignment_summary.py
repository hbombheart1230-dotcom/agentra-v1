from __future__ import annotations
from typing import Any, Dict, List, Mapping, Sequence

def _build_monitor_policy_alignment_summary(*, policy_interpreter_trace: Mapping[str, Any] | None = None, facade: Any) -> Dict[str, Any]:
    trace = dict(policy_interpreter_trace or {}) if isinstance(policy_interpreter_trace, Mapping) else {}; summary = facade._empty_monitor_policy_alignment_summary(); available = bool(trace.get("available")); summary["policy_available"] = bool(trace.get("policy_available")); summary["entry_style"] = trace.get("entry_style")
    if not available: return summary
    check_status = dict(trace.get("check_status") or {}) if isinstance(trace.get("check_status"), Mapping) else {}; alignment_summary = dict(trace.get("alignment_summary") or {}) if isinstance(trace.get("alignment_summary"), Mapping) else {}; focus_alignment = dict(trace.get("focus_alignment") or {}) if isinstance(trace.get("focus_alignment"), Mapping) else {}
    def _failed(rows: Any, *, statuses: Sequence[str] = ("fail",)) -> List[str]:
        out=[]; expected={str(x).strip().lower() for x in list(statuses or [])}
        for row in list(rows or []):
            if isinstance(row, Mapping) and str(row.get("status") or "").strip().lower() in expected: out.append(str(row.get("name") or "").strip())
        return facade._dedupe_non_empty(out)
    primary_focus=facade._dedupe_non_empty(focus_alignment.get("primary_focus") or []); secondary_focus=facade._dedupe_non_empty(focus_alignment.get("secondary_focus") or []); failed_required=_failed(check_status.get("required")); failed_preferred=_failed(check_status.get("preferred")); failed_relaxable=_failed(check_status.get("relaxable")); active_blockers=_failed(check_status.get("blockers"), statuses=("active",)); focus_mismatch=facade._dedupe_non_empty([*(n for n in primary_focus if n in failed_required or n in failed_preferred or n in failed_relaxable), *(n for n in secondary_focus if n in failed_required or n in failed_preferred)])
    summary.update({"available": True, "alignment_state": alignment_summary.get("policy_alignment_state"), "primary_blocker": alignment_summary.get("primary_blocker"), "secondary_blockers": facade._dedupe_non_empty([*list(alignment_summary.get("secondary_blockers") or []), *active_blockers]), "focus_mismatch": focus_mismatch, "top_failed_required_checks": failed_required[:3], "top_failed_preferred_checks": failed_preferred[:3], "top_relaxable_gaps": failed_relaxable[:3]})
    summary_notes=list(trace.get("notes") or []); high_level=any(str((row or {}).get("feature_level") or "")=="high_level_feature" and str((row or {}).get("status") or "") in {"fail","active"} for section in ("required","preferred","relaxable","blockers") for row in list(check_status.get(section) or []) if isinstance(row, Mapping))
    if high_level: summary_notes.append("higher_level_feature_mismatch_present")
    summary["summary_notes"]=facade._dedupe_non_empty(summary_notes); return summary
