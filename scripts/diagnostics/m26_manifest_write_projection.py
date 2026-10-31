from pathlib import Path
from typing import Any
def _write_text(path: Path, content: str, *, facade: Any) -> None:
 path.parent.mkdir(parents=True,exist_ok=True);path.write_text(content,encoding="utf-8")
