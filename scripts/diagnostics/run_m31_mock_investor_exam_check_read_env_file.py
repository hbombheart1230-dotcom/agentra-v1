from __future__ import annotations

from pathlib import Path
from typing import Dict


def _read_env_file(path: Path, *, facade: object = None) -> Dict[str, str]:
    if not path.exists():
        return {}
    out: Dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        k, v = line.split("=", 1)
        k = k.strip()
        v = v.strip()
        if v and v[0] not in ("'", "\"") and "#" in v:
            v = v.split("#", 1)[0].rstrip()
        if (len(v) >= 2) and ((v[0] == v[-1]) and v[0] in ("'", '"')):
            v = v[1:-1]
        if k:
            out[k] = v
    return out
