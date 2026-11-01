"""operator_period_summary: ``_state_snapshot_candidate_paths`` body (moved verbatim from ``operator_period_summary``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple


def _state_snapshot_candidate_paths(reports_root: Path, *, facade: Any) -> List[Path]:
    candidates: List[facade.Path] = []
    raw = str(facade.os.getenv("STATE_STORE_PATH") or "").strip()
    if raw:
        candidates.append(facade.Path(raw))
    candidates.append(facade.Path(reports_root).parent / "data" / "state.json")
    out: List[facade.Path] = []
    seen: set[str] = set()
    for path in candidates:
        try:
            key = str(path.resolve())
        except Exception:
            key = str(path)
        if key in seen:
            continue
        seen.add(key)
        out.append(path)
    return out
