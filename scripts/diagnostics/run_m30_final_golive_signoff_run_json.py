from __future__ import annotations
import io, json
from contextlib import redirect_stdout
from typing import Any, Dict, List, Tuple
def _run_json(main_fn, argv: List[str], *, facade: object = None) -> Tuple[int, Dict[str, Any]]:
    buf=io.StringIO()
    with redirect_stdout(buf): rc=main_fn(argv)
    out=buf.getvalue().strip()
    if not out: return int(rc), {}
    try: return int(rc), (facade.json if facade is not None else json).loads(out)
    except Exception: return int(rc), {}
