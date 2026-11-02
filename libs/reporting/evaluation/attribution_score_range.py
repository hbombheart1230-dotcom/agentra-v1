from __future__ import annotations

import json
from collections import Counter
from datetime import date, timedelta
from pathlib import Path
from typing import Any, Mapping
import sys
from . import attribution_score_range_date_range as _a35_date_range
from . import attribution_score_range_day_trade_count as _a35_day_trade_count
from . import attribution_score_range_render_attribution_score_range as _a35_render_attribution_score_range
from . import attribution_score_range_parse_date as _a36_parse_date
from . import attribution_score_range_trade_dir_count as _a36_trade_dir_count
from . import attribution_score_range_has_source_artifact as _a36_has_source_artifact
from . import attribution_score_range_build_attribution_score_range as _a36_build_attribution_score_range

from .attribution_score_window import SCORE_KEYS, _mapping, _read_json, _score_value


def _parse_date(value: str) -> date:
    return _a36_parse_date._parse_date(value=value, facade=sys.modules[__name__])


def _date_range(start: str, end: str) -> list[str]:
    return _a35_date_range._date_range(start=start, end=end, facade=sys.modules[__name__])


def _trade_dir_count(reports_root: Path, day: str) -> int:
    return _a36_trade_dir_count._trade_dir_count(reports_root=reports_root, day=day, facade=sys.modules[__name__])


def _has_source_artifact(reports_root: Path, day: str) -> bool:
    return _a36_has_source_artifact._has_source_artifact(reports_root=reports_root, day=day, facade=sys.modules[__name__])


def _day_payload(reports_root: Path, day: str) -> dict[str, Any]:
    return _read_json(reports_root / "evaluation" / "daily" / day / "attribution_score_v0.json")


def _day_trade_count(reports_root: Path, day: str) -> int:
    return _a35_day_trade_count._day_trade_count(reports_root=reports_root, day=day, facade=sys.modules[__name__])


def build_attribution_score_range(
    *,
    reports_root: Path = Path("reports"),
    start: str,
    end: str,
    include_empty_days: bool = False,
) -> dict[str, Any]:
    return _a36_build_attribution_score_range.build_attribution_score_range(reports_root=reports_root, start=start, end=end, include_empty_days=include_empty_days, facade=sys.modules[__name__])


def render_attribution_score_range(payload: Mapping[str, Any]) -> str:
    return _a35_render_attribution_score_range.render_attribution_score_range(payload=payload, facade=sys.modules[__name__])


def write_attribution_score_range(
    *,
    reports_root: Path = Path("reports"),
    start: str,
    end: str,
    include_empty_days: bool = False,
) -> dict[str, str]:
    reports_root = Path(reports_root)
    payload = build_attribution_score_range(
        reports_root=reports_root,
        start=start,
        end=end,
        include_empty_days=include_empty_days,
    )
    out_dir = reports_root / "evaluation" / "range" / f"{start}_{end}"
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / "attribution_score_range.json"
    md_path = out_dir / "attribution_score_range.md"
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(render_attribution_score_range(payload), encoding="utf-8")
    return {"json": str(json_path), "markdown": str(md_path)}


__all__ = [
    "build_attribution_score_range",
    "render_attribution_score_range",
    "write_attribution_score_range",
]
