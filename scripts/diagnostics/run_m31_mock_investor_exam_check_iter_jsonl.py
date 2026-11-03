from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable


def _iter_jsonl(path: Path, *, facade: object = None) -> Iterable[Dict[str, Any]]:
    if not path.exists():
        return []

    def _gen() -> Iterable[Dict[str, Any]]:
        with path.open("r", encoding="utf-8") as f:
            for raw in f:
                line = raw.strip()
                if not line:
                    continue
                try:
                    obj = (facade.json if facade is not None else json).loads(line)
                except Exception:
                    continue
                if isinstance(obj, dict):
                    yield obj

    return _gen()
