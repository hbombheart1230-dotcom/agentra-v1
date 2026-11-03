from __future__ import annotations
from pathlib import Path
def _gitignore_has_env(root: Path, *, facade: object = None) -> bool:
    p=root/".gitignore"
    if not p.exists(): return False
    try: return any(line.strip()==".env" for line in p.read_text(encoding="utf-8").splitlines())
    except Exception: return False
