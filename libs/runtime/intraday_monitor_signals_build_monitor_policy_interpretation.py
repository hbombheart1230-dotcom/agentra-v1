from __future__ import annotations

from typing import Any, Dict, List, Mapping

def _build_monitor_policy_interpretation(
    *,
    received_policy: Mapping[str, Any] | MonitorEntryPolicy | None = None,
    effective_policy: Mapping[str, Any] | MonitorEntryPolicy | None = None,
    frame: Mapping[str, Any] | None = None,
    policy_contract: Mapping[str, Any] | None = None,
    facade: Any,
) -> Dict[str, Any]:
    frame_obj = dict(frame or {}) if isinstance(frame, Mapping) else {}
    playbook = str(frame_obj.get("playbook") or "").strip().lower()
    explicit_fields = facade._extract_explicit_policy_interpretation_fields(policy_contract)
    explicit_entry_style = str(explicit_fields.get("entry_style") or "").strip().lower()
    source_mapping = (
        facade.extract_monitor_entry_policy_mapping(received_policy)
        if isinstance(received_policy, Mapping)
        else {}
    )
    policy_obj = (
        effective_policy
        if isinstance(effective_policy, facade.MonitorEntryPolicy)
        else facade.MonitorEntryPolicy.from_mapping(effective_policy)
        if isinstance(effective_policy, Mapping) and effective_policy
        else None
    )
    policy_available = bool(source_mapping) or bool(playbook) or bool(explicit_fields.get("selected_policy"))
    interpretation = facade._empty_monitor_policy_interpretation()
    interpretation["policy_available"] = bool(policy_available)
    interpretation["entry_style"] = explicit_entry_style or playbook or None
    interpretation["contract_source"] = explicit_fields.get("contract_source")
    interpretation["policy_schema_available"] = bool(explicit_fields.get("policy_schema_available"))
    interpretation["policy_schema_version"] = explicit_fields.get("policy_schema_version")
    interpretation["policy_schema_raw_keys"] = list(explicit_fields.get("policy_schema_raw_keys") or [])
    interpretation["explicit_fields_used"] = list(explicit_fields.get("explicit_fields_used") or [])
    interpretation["spec_validation_notes"] = list(explicit_fields.get("spec_validation_notes") or [])
    if not policy_available:
        return interpretation

    required_checks: List[str] = []
    preferred_checks: List[str] = []
    relaxable_checks: List[str] = []
    blockers: List[str] = []
    primary_focus: List[str] = []
    secondary_focus: List[str] = []
    notes: List[str] = []
    volume_ratio_min = 0.68
    policy_enabled = True
    require_vwap_reclaim = False
    require_rebound = False
    interpretation_style = explicit_entry_style or playbook

    if policy_obj is not None:
        volume_ratio_min = float(policy_obj.volume_ratio_min)
        policy_enabled = bool(policy_obj.enabled)
        require_vwap_reclaim = bool(policy_obj.require_vwap_reclaim)
        require_rebound = bool(policy_obj.require_rebound)
        interpretation["policy_source"] = str(policy_obj.policy_source or "") or None
        interpretation["policy_adjustments"] = list(policy_obj.adjustments or [])
    if explicit_fields.get("policy_source"):
        interpretation["policy_source"] = str(explicit_fields.get("policy_source") or "")
    if explicit_fields.get("policy_adjustments"):
        interpretation["policy_adjustments"] = list(explicit_fields.get("policy_adjustments") or [])
    interpretation["priority_hints"] = {
        "volume_priority": facade._volume_priority_hint(volume_ratio_min),
        "reclaim_priority": "high" if require_vwap_reclaim else "normal",
        "breakout_priority": (
            "high" if interpretation_style == "breakout" else "low" if interpretation_style in ("pullback", "reversal") else "normal"
        ),
        "pullback_priority": (
            "high" if interpretation_style in ("pullback", "reversal") else "low" if interpretation_style == "breakout" else "normal"
        ),
    }
    if not policy_enabled:
        blockers.append("policy_disabled")
    if require_vwap_reclaim and interpretation_style != "breakout":
        required_checks.append("reclaim_gate_ok")
        notes.append("vwap_reclaim_required")
    elif require_vwap_reclaim and interpretation_style == "breakout":
        preferred_checks.append("reclaim_gate_ok")
        relaxable_checks.append("reclaim_gate_ok")
        notes.append("vwap_reclaim_near_ready_relaxable_for_breakout_style")
    if require_rebound and interpretation_style in ("pullback", "reversal"):
        required_checks.append("rebound_ok")
        notes.append("rebound_required_for_pullback_style")
    if volume_ratio_min >= 1.0:
        notes.append("volume_threshold_emphasized")
    elif volume_ratio_min <= 0.75:
        notes.append("volume_threshold_relatively_loose")
        relaxable_checks.append("volume_ok")
    if interpretation_style == "breakout":
        preferred_checks.extend(["breakout_ok", "volume_ok", "reclaim_gate_ok"])
        relaxable_checks.extend(["pullback_ok"])
        primary_focus.extend(["breakout_ok", "volume_ok"])
        secondary_focus.extend(["reclaim_gate_ok", "confidence_ok", "structure_hh_hl", "momentum_follow_through"])
    elif interpretation_style in ("pullback", "reversal"):
        preferred_checks.extend(["pullback_ok", "volume_ok", "vwap_reclaim_ok"])
        relaxable_checks.extend(["breakout_ok"])
        primary_focus.extend(["pullback_ok", "volume_ok"])
        secondary_focus.extend(["reclaim_gate_ok", "rebound_ok", "support_holding", "trend_regime"])
    elif interpretation_style == "defensive":
        preferred_checks.extend(["reclaim_gate_ok", "extension_ok", "confidence_ok"])
        relaxable_checks.extend(["breakout_ok", "pullback_ok"])
        primary_focus.extend(["reclaim_gate_ok", "extension_ok"])
        secondary_focus.extend(["volume_ok", "confidence_ok", "failed_breakout", "momentum_decay"])
    else:
        preferred_checks.extend(["reclaim_gate_ok", "confidence_ok"])
        primary_focus.extend(["reclaim_gate_ok"])
        secondary_focus.extend(["volume_ok", "breakout_ok", "pullback_ok", "trend_regime"])

    fallback_used = False
    if explicit_fields.get("required_checks"):
        required_checks = list(explicit_fields.get("required_checks") or [])
    elif required_checks:
        fallback_used = True
    if explicit_fields.get("preferred_checks"):
        preferred_checks = list(explicit_fields.get("preferred_checks") or [])
    elif preferred_checks:
        fallback_used = True
    if explicit_fields.get("relaxable_checks"):
        relaxable_checks = list(explicit_fields.get("relaxable_checks") or [])
    elif relaxable_checks:
        fallback_used = True
    if explicit_fields.get("blockers"):
        blockers = list(explicit_fields.get("blockers") or [])
    elif blockers:
        fallback_used = True
    if (explicit_fields.get("priority_hints") or {}):
        merged_priority_hints = dict(interpretation.get("priority_hints") or {})
        merged_priority_hints.update(dict(explicit_fields.get("priority_hints") or {}))
        interpretation["priority_hints"] = merged_priority_hints
    elif any((interpretation.get("priority_hints") or {}).values()):
        fallback_used = True
    explicit_focus = dict(explicit_fields.get("evidence_focus") or {})
    if explicit_focus.get("primary") or explicit_focus.get("secondary"):
        primary_focus = list(explicit_focus.get("primary") or primary_focus)
        secondary_focus = list(explicit_focus.get("secondary") or secondary_focus)
    elif primary_focus or secondary_focus:
        fallback_used = True
    if explicit_fields.get("notes"):
        notes = list(explicit_fields.get("notes") or [])
    elif notes:
        fallback_used = True

    explicit_fields_used = list(explicit_fields.get("explicit_fields_used") or [])
    if explicit_fields_used and fallback_used:
        interpretation["interpretation_basis"] = "mixed"
    elif explicit_fields_used:
        interpretation["interpretation_basis"] = "explicit_policy"
    elif policy_available and interpretation_style:
        interpretation["interpretation_basis"] = "fallback_playbook"
    else:
        interpretation["interpretation_basis"] = "none"

    interpretation["required_checks"] = facade._dedupe_non_empty(required_checks)
    interpretation["preferred_checks"] = facade._dedupe_non_empty(preferred_checks)
    interpretation["relaxable_checks"] = facade._dedupe_non_empty(relaxable_checks)
    interpretation["blockers"] = facade._dedupe_non_empty(blockers)
    interpretation["evidence_focus"] = {
        "primary": facade._dedupe_non_empty(primary_focus),
        "secondary": facade._dedupe_non_empty(secondary_focus),
    }
    interpretation["notes"] = facade._dedupe_non_empty(notes)
    return interpretation
