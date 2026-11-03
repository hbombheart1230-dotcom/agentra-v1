from __future__ import annotations

from typing import Any, Dict


def _gate_status(components: Dict[str, Dict[str, Any]], *, facade: object = None) -> Dict[str, Any]:
    pass_total = 0
    fail_total = 0
    for c in components.values():
        if bool(c.get("ok")) and int(c.get("rc") or 0) == 0:
            pass_total += 1
        else:
            fail_total += 1
    return {"ok": fail_total == 0, "pass_total": int(pass_total), "fail_total": int(fail_total), "components": components}
