from __future__ import annotations

from typing import Any, Dict


def _item(*, item_id: str, title: str, passed: bool, evidence: str, required: bool = True, facade: object = None) -> Dict[str, Any]:
    return {
        "id": item_id,
        "title": title,
        "required": bool(required),
        "passed": bool(passed),
        "evidence": str(evidence),
    }
