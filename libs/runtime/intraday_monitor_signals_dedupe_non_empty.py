from __future__ import annotations

from typing import Any, Dict, List, Mapping, Sequence


def _dedupe_non_empty(values: Sequence[Any], *, facade: Any):
    seen: set[str] = set()
    out: List[str] = []
    for value in list(values or []):
        text = str(value or "").strip()
        if not text or text in seen:
            continue
        seen.add(text)
        out.append(text)
    return out
