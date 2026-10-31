from typing import Any, Dict, Tuple
from pathlib import Path
def _run_scorecard_json(*, dataset_root: Path, day: str, facade: Any) -> Tuple[int, Dict[str, Any]]:
    argv = ["--dataset-root", str(dataset_root), "--json"]
    if day: argv.extend(["--day", day])
    buf = facade.io.StringIO()
    with facade.redirect_stdout(buf): rc = facade.scorecard_main(argv)
    out = buf.getvalue().strip()
    if not out: return int(rc), {}
    try: return int(rc), facade.json.loads(out)
    except Exception: return int(rc), {}
