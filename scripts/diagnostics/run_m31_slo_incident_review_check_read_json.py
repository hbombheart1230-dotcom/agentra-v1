from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


def _read_json(path: Path, *, facade: object = None) -> Dict[str, Any]:
    if not path.exists():
        return {}
    try:
        obj = (facade.json if facade is not None else json).loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return obj if isinstance(obj, dict) else {}
