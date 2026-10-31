from typing import Any, Dict
def _json_path_get(obj: Dict[str, Any], path: str, default: float = 0.0, *, facade: Any) -> float:
    cur: Any = obj
    for part in path.split("."):
        if not isinstance(cur, dict): return float(default)
        cur = cur.get(part)
    return facade._as_float(cur, default)
