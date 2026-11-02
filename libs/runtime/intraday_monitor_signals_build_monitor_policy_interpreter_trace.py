from __future__ import annotations

from typing import Any, Dict, List, Mapping

def _build_monitor_policy_interpreter_trace(
    *,
    policy_interpretation: Mapping[str, Any] | None = None,
    signal_evidence: Mapping[str, Any] | None = None,
    chart_structure_features: Mapping[str, Any] | None = None,
    facade: Any,
) -> Dict[str, Any]:
    interpretation = dict(policy_interpretation or {}) if isinstance(policy_interpretation, Mapping) else {}
    evidence = dict(signal_evidence or {}) if isinstance(signal_evidence, Mapping) else {}
    chart_states = facade._flatten_chart_structure_feature_states(chart_structure_features)
    trace = facade._empty_monitor_policy_interpreter_trace()

    policy_available = bool(interpretation.get("policy_available"))
    trace["policy_available"] = policy_available
    trace["entry_style"] = interpretation.get("entry_style")
    trace["focus_alignment"] = {
        "primary_focus": facade._dedupe_non_empty(((interpretation.get("evidence_focus") or {}).get("primary")) or []),
        "secondary_focus": facade._dedupe_non_empty(((interpretation.get("evidence_focus") or {}).get("secondary")) or []),
    }
    if not policy_available:
        return trace

    checks = dict(evidence.get("checks") or {}) if isinstance(evidence.get("checks"), Mapping) else {}
    derived = dict(evidence.get("derived") or {}) if isinstance(evidence.get("derived"), Mapping) else {}
    scores = dict(evidence.get("scores") or {}) if isinstance(evidence.get("scores"), Mapping) else {}

    def _status_item(spec_value: Any, *, blocker: bool = False) -> Dict[str, Any]:
        spec = facade._parse_policy_signal_spec(spec_value)
        name = str(spec.get("name") or "").strip()
        if name in checks:
            return {
                "name": str(name),
                "expected_state": None,
                "actual_state": None,
                "status": ("active" if not bool(checks.get(name)) else "inactive") if blocker else ("pass" if bool(checks.get(name)) else "fail"),
                "source": f"signal_evidence.checks.{name}",
                "feature_level": "low_level_signal",
                "spec_valid": bool(spec.get("is_valid", True)),
                "validation_notes": list(spec.get("validation_notes") or []),
            }
        if name in derived:
            value = derived.get(name)
            if isinstance(value, bool):
                return {
                    "name": str(name),
                    "expected_state": None,
                    "actual_state": None,
                    "status": ("active" if bool(value) else "inactive") if blocker else ("pass" if bool(value) else "fail"),
                    "source": f"signal_evidence.derived.{name}",
                    "feature_level": "low_level_signal",
                    "spec_valid": bool(spec.get("is_valid", True)),
                    "validation_notes": list(spec.get("validation_notes") or []),
                }
        feature_item = facade._chart_feature_status_item(spec=spec, chart_states=chart_states, blocker=blocker)
        if feature_item is not None:
            return feature_item
        return {
            "name": str(name),
            "expected_state": spec.get("expected_state"),
            "actual_state": None,
            "status": "unknown",
            "source": None,
            "feature_level": spec.get("feature_level") or "unknown",
            "spec_valid": bool(spec.get("is_valid")),
            "validation_notes": list(spec.get("validation_notes") or []),
        }

    required_rows = [_status_item(name) for name in facade._dedupe_non_empty(interpretation.get("required_checks") or [])]
    preferred_rows = [_status_item(name) for name in facade._dedupe_non_empty(interpretation.get("preferred_checks") or [])]
    relaxable_rows = [_status_item(name) for name in facade._dedupe_non_empty(interpretation.get("relaxable_checks") or [])]
    blocker_names = facade._dedupe_non_empty([
        *(interpretation.get("blockers") or []),
        "too_extended" if "too_extended" in derived else "",
    ])
    blocker_rows = [_status_item(name, blocker=True) for name in blocker_names]

    trace["available"] = True
    trace["check_status"] = {
        "required": required_rows,
        "preferred": preferred_rows,
        "relaxable": relaxable_rows,
        "blockers": blocker_rows,
    }

    failed_required = [row["name"] for row in required_rows if row.get("status") == "fail"]
    active_blockers = [row["name"] for row in blocker_rows if row.get("status") == "active"]
    failed_preferred = [row["name"] for row in preferred_rows if row.get("status") == "fail"]

    alignment_state: str | None
    if active_blockers or failed_required:
        alignment_state = "misaligned"
    elif failed_preferred:
        alignment_state = "partial"
    elif required_rows or preferred_rows or relaxable_rows:
        alignment_state = "aligned"
    else:
        alignment_state = "unknown"

    primary_blocker = None
    secondary_blockers: List[str] = []
    blocker_order = [*active_blockers, *failed_required, *failed_preferred]
    if blocker_order:
        primary_blocker = blocker_order[0]
        secondary_blockers = blocker_order[1:]

    trace["alignment_summary"] = {
        "policy_alignment_state": alignment_state,
        "primary_blocker": primary_blocker,
        "secondary_blockers": facade._dedupe_non_empty(secondary_blockers),
    }
    higher_level_used = any(
        str((row or {}).get("feature_level") or "") == "high_level_feature"
        for row in [*required_rows, *preferred_rows, *relaxable_rows, *blocker_rows]
        if isinstance(row, Mapping)
    )
    notes = list(interpretation.get("notes") or [])
    if higher_level_used:
        notes.append("chart_structure_features_consumed")
    trace["notes"] = facade._dedupe_non_empty(notes)
    return trace
