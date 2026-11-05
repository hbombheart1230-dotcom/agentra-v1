from typing import Any, List, Mapping, Sequence
def _extract_failed_names(rows: Any, *, statuses: Sequence[str], facade: Any) -> List[str]:
    expected={str(x or "").strip().lower() for x in list(statuses or []) if str(x or "").strip()}; out=[]
    for row in list(rows or []):
        if not isinstance(row, Mapping): continue
        if str(row.get("status") or "").strip().lower() in expected: out.append(str(row.get("name") or "").strip())
    return facade._dedupe_non_empty(out,limit=8)
