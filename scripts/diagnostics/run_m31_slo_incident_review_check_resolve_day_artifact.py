from __future__ import annotations

from pathlib import Path
from typing import Any, Dict


def _resolve_day_artifact(report_dir: Path, prefix: str, day: str, *, facade: object = None) -> tuple[Path, Dict[str, Any], bool]:
    reader = facade._read_json if facade is not None else None
    if reader is None:
        from scripts.diagnostics.run_m31_slo_incident_review_check_read_json import _read_json as reader
    direct = report_dir / f"{prefix}_{day}.json"
    direct_obj = reader(direct)
    if direct_obj:
        return direct, direct_obj, False
    target_day = str(day or "").strip()
    best_day = ""
    best_path = direct
    best_obj: Dict[str, Any] = {}
    pattern = f"{prefix}_*.json"
    for path in sorted(report_dir.glob(pattern)):
        stem = path.stem
        if not stem.startswith(f"{prefix}_"):
            continue
        candidate_day = stem[len(prefix) + 1 :].strip()
        if not candidate_day:
            continue
        if target_day and candidate_day > target_day:
            continue
        obj = reader(path)
        if not obj:
            continue
        if not best_day or candidate_day > best_day:
            best_day = candidate_day
            best_path = path
            best_obj = obj
    return best_path, best_obj, bool(best_obj)
