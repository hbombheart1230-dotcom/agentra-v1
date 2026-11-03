from __future__ import annotations

from typing import Any, Dict, List


def _count_by(items: List[Dict[str, Any]], key: str, *, facade: object = None) -> Dict[str, int]:
    out: Dict[str, int] = {}
    for it in items:
        k = str(it.get(key) or "")
        if not k:
            continue
        out[k] = int(out.get(k) or 0) + 1
    return out
