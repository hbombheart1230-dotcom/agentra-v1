from __future__ import annotations

def _resolve_check_state(*, name: str, metrics: facade.Mapping[str, facade.Any], passed_checks: facade.Sequence[facade.Any], failed_checks: facade.Sequence[facade.Any], check_status: facade.Mapping[str, facade.Any], facade: facade.Any) -> facade.Any:
    if name in metrics:
        value = metrics.get(name)
        if isinstance(value, bool):
            return value
        if value not in (None, ''):
            return value
    for candidate in list(passed_checks or []):
        text = str(candidate or '').strip()
        if not text:
            continue
        if text == name or text.startswith(f'{name}='):
            return True
    for candidate in list(failed_checks or []):
        text = str(candidate or '').strip()
        if not text:
            continue
        if text == name or text.startswith(f'{name}='):
            return False
    for rows in list(check_status.values()):
        for row in list(rows or []):
            if not isinstance(row, facade.Mapping):
                continue
            row_name = str(row.get('name') or '').strip()
            if row_name != name and (not row_name.startswith(f'{name}=')):
                continue
            status = str(row.get('status') or '').strip().lower()
            if status == 'pass':
                return True
            if status == 'fail':
                return False
            actual_state = row.get('actual_state')
            if actual_state not in (None, ''):
                return actual_state
    return None
