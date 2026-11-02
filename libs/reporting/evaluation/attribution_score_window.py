from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Mapping, Sequence
import sys
from . import attribution_score_window_mapping as _a33_mapping
from . import attribution_score_window_score_value as _a33_score_value
from . import attribution_score_window_ledger_days as _a36_ledger_days
from . import attribution_score_window_build_attribution_score_window as _a36_build_attribution_score_window
from . import attribution_score_window_render_attribution_score_window as _a36_render_attribution_score_window


SCORE_KEYS = (
    "selection_integrity_score",
    "scanner_alignment_score",
    "entry_timing_score",
    "exit_horizon_score",
    "evidence_quality_score",
)


def _read_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        return payload if isinstance(payload, dict) else {}
    except Exception:
        return {}


def _mapping(value: Any) -> Mapping[str, Any]:
    return _a33_mapping._mapping(value=value, facade=sys.modules[__name__])


def _score_value(row: Mapping[str, Any], key: str) -> int | None:
    return _a33_score_value._score_value(row=row, key=key, facade=sys.modules[__name__])


def _ledger_days(freeze_root: Path) -> list[dict[str, Any]]:
    return _a36_ledger_days._ledger_days(freeze_root=freeze_root, facade=sys.modules[__name__])


def _day_payload(reports_root: Path, day: str) -> dict[str, Any]:
    return _read_json(reports_root / "evaluation" / "daily" / day / "attribution_score_v0.json")


def build_attribution_score_window(
    *,
    reports_root: Path = Path("reports"),
    window_id: str = "q9_q10_q11_q12_5d_20260629",
) -> dict[str, Any]:
    return _a36_build_attribution_score_window.build_attribution_score_window(reports_root=reports_root, window_id=window_id, facade=sys.modules[__name__])


def render_attribution_score_window(payload: Mapping[str, Any]) -> str:
    return _a36_render_attribution_score_window.render_attribution_score_window(payload=payload, facade=sys.modules[__name__])


def write_attribution_score_window(
    *,
    reports_root: Path = Path("reports"),
    window_id: str = "q9_q10_q11_q12_5d_20260629",
) -> dict[str, str]:
    reports_root = Path(reports_root)
    payload = build_attribution_score_window(reports_root=reports_root, window_id=window_id)
    out_dir = reports_root / "evaluation" / "freeze_window" / window_id
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / "attribution_score_window.json"
    md_path = out_dir / "attribution_score_window.md"
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(render_attribution_score_window(payload), encoding="utf-8")
    return {"json": str(json_path), "markdown": str(md_path)}


__all__ = [
    "build_attribution_score_window",
    "render_attribution_score_window",
    "write_attribution_score_window",
]
