from __future__ import annotations

def _resolve_structure_state(chart_features: facade.Mapping[str, facade.Any], check_status: facade.Mapping[str, facade.Any], *, facade: facade.Any) -> str:
    structure = chart_features.get('structure')
    if isinstance(structure, facade.Mapping):
        state = str(structure.get('structure_hh_hl') or '').strip()
        if state:
            return state
    direct_state = str(chart_features.get('structure_hh_hl') or '').strip()
    if direct_state:
        return direct_state
    for rows in list(check_status.values()):
        for row in list(rows or []):
            if not isinstance(row, facade.Mapping):
                continue
            row_name = str(row.get('name') or '').strip()
            if row_name != 'structure_hh_hl' and (not row_name.startswith('structure_hh_hl=')):
                continue
            actual_state = str(row.get('actual_state') or '').strip()
            if actual_state:
                return actual_state
            if '=' in row_name:
                return row_name.split('=', 1)[1].strip()
    return ''
