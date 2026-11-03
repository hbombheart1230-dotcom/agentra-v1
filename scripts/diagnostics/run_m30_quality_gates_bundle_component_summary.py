from __future__ import annotations

from typing import Any, Dict


def _component_summary(rc: int, obj: Dict[str, Any], *, facade: object = None) -> Dict[str, Any]:
    return {"rc": int(rc), "ok": bool(obj.get("ok")) if isinstance(obj, dict) else False, "failure_total": int(len(obj.get("failures") or [])) if isinstance(obj, dict) else 0}
