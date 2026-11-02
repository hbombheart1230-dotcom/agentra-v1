from typing import Any, Iterable, List
def _dedupe_non_empty(values: Iterable[Any], *, limit: int|None=None, facade: Any) -> List[str]:
    out=[]; seen=set()
    for value in values:
        text=str(value or "").strip()
        if not text or text in seen: continue
        seen.add(text); out.append(text)
        if limit is not None and len(out)>=int(limit): break
    return out
