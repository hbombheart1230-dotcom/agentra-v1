from __future__ import annotations
from typing import Any, Dict, List, Mapping

def _extract_explicit_policy_interpretation_fields(policy_contract: Mapping[str, Any] | None, facade: Any) -> Dict[str, Any]:
    contract = dict(policy_contract or {}) if isinstance(policy_contract, Mapping) else {}
    selected_policy = dict(contract.get("selected_policy") or {}) if isinstance(contract.get("selected_policy"), Mapping) else {}
    schema_candidate = dict(contract.get("selected_policy_schema") or {}) if isinstance(contract.get("selected_policy_schema"), Mapping) else facade.normalize_monitor_entry_policy_schema(selected_policy)
    explicit_fields_used: List[str] = list(facade._dedupe_non_empty(schema_candidate.get("explicit_fields_used") or []))
    def _optional_text(value: Any) -> str | None:
        text = str(value or "").strip(); return text or None
    def _optional_list(value: Any) -> List[str]:
        if isinstance(value, str): return facade._dedupe_non_empty([value])
        if isinstance(value, (list, tuple, set)): return facade._dedupe_non_empty(list(value))
        return []
    def _optional_mapping(value: Any) -> Dict[str, Any]: return dict(value or {}) if isinstance(value, Mapping) else {}
    entry_style = _optional_text(schema_candidate.get("entry_style")); required_checks = _optional_list(schema_candidate.get("required_checks")); preferred_checks = _optional_list(schema_candidate.get("preferred_checks")); relaxable_checks = _optional_list(schema_candidate.get("relaxable_checks")); blockers = _optional_list(schema_candidate.get("blockers")); priority_hints = _optional_mapping(schema_candidate.get("priority_hints"))
    if not any(priority_hints.values()): priority_hints = {}
    evidence_focus = _optional_mapping(schema_candidate.get("evidence_focus")); notes = _optional_list(schema_candidate.get("notes")); policy_adjustments = list(schema_candidate.get("policy_adjustments") or []); spec_validation_notes = _optional_list(schema_candidate.get("spec_validation_notes")); policy_source = _optional_text(selected_policy.get("policy_source"))
    return {"contract_source": _optional_text(contract.get("selected_source")), "selected_policy": selected_policy, "policy_schema_available": bool(schema_candidate.get("available")), "policy_schema_version": _optional_text(schema_candidate.get("schema_version")), "policy_schema_raw_keys": _optional_list(schema_candidate.get("raw_keys")), "entry_style": entry_style.lower() if isinstance(entry_style, str) else None, "required_checks": required_checks, "preferred_checks": preferred_checks, "relaxable_checks": relaxable_checks, "blockers": blockers, "priority_hints": priority_hints, "evidence_focus": {"primary": _optional_list(evidence_focus.get("primary")), "secondary": _optional_list(evidence_focus.get("secondary"))}, "notes": notes, "policy_adjustments": policy_adjustments, "policy_source": policy_source, "explicit_fields_used": explicit_fields_used, "spec_validation_notes": spec_validation_notes}
