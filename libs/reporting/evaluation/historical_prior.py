from __future__ import annotations

import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable
import sys

from .artifact_inventory import read_json
from .counterfactuals import build_selection_attribution
from .metrics import performance_metrics
from .trade_evaluator import evaluate_trade
from .trade_read_model import build_q9_trade_read_model
from . import historical_prior_rank_bucket as _a55_hp_rank_bucket
from . import historical_prior_day_from_trade_dir as _a56_hp_day
from . import historical_prior_net_return as _a56_hp_net
from . import historical_prior_group_metrics as _a56_hp_group
from . import historical_prior_summarize_historical_prior as _a56_hp_summarize
from . import historical_prior_render_historical_prior_markdown as _a56_hp_render
from . import historical_prior_iter_historical_trade_dirs as _a56_hp_iter


DEFAULT_BEFORE_DAY = "2026-06-29"


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _day_from_trade_dir(trade_dir: Path) -> str:
    return _a56_hp_day._day_from_trade_dir(trade_dir, facade=sys.modules[__name__])


def iter_historical_trade_dirs(
    reports_root: Path,
    *,
    from_day: str = "",
    before_day: str = DEFAULT_BEFORE_DAY,
) -> list[Path]:
    return _a56_hp_iter.iter_historical_trade_dirs(reports_root, from_day=from_day, before_day=before_day, facade=sys.modules[__name__])


def _net_return(evaluation: dict[str, Any]) -> float | None:
    return _a56_hp_net._net_return(evaluation, facade=sys.modules[__name__])


def _rank_bucket(value: Any) -> str:
    return _a55_hp_rank_bucket._rank_bucket(value, facade=sys.modules[__name__])


def _group_metrics(rows: Iterable[tuple[str, float]]) -> dict[str, Any]:
    return _a56_hp_group._group_metrics(rows, facade=sys.modules[__name__])


def summarize_historical_prior(
    *,
    models: list[dict[str, Any]],
    evaluations: list[dict[str, Any]],
    attributions: list[dict[str, Any]],
    errors: list[dict[str, Any]],
    from_day: str,
    before_day: str,
) -> dict[str, Any]:
    return _a56_hp_summarize.summarize_historical_prior(models=models, evaluations=evaluations, attributions=attributions, errors=errors, from_day=from_day, before_day=before_day, facade=sys.modules[__name__])


def render_historical_prior_markdown(payload: dict[str, Any]) -> str:
    return _a56_hp_render.render_historical_prior_markdown(payload, facade=sys.modules[__name__])


def build_historical_q9_prior(
    reports_root: Path,
    *,
    from_day: str = "",
    before_day: str = DEFAULT_BEFORE_DAY,
) -> dict[str, Any]:
    reports_root = Path(reports_root)
    output_root = reports_root / "evaluation" / "historical_q9_prior"
    trade_dirs = iter_historical_trade_dirs(reports_root, from_day=from_day, before_day=before_day)
    models: list[dict[str, Any]] = []
    evaluations: list[dict[str, Any]] = []
    attributions: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []

    for trade_dir in trade_dirs:
        try:
            model = build_q9_trade_read_model(trade_dir)
            evaluation = evaluate_trade(model)
            attribution = build_selection_attribution(model)
        except Exception as exc:
            errors.append({
                "trade_dir": str(trade_dir),
                "day": _day_from_trade_dir(trade_dir),
                "error": f"{type(exc).__name__}: {exc}",
            })
            continue
        models.append(model)
        evaluations.append(evaluation)
        attributions.append(attribution)

    summary = summarize_historical_prior(
        models=models,
        evaluations=evaluations,
        attributions=attributions,
        errors=errors,
        from_day=from_day,
        before_day=before_day,
    )
    _write_json(output_root / "historical_q9_trade_read_models.json", {
        "schema_version": "historical_q9_trade_read_models.v1",
        "behavior_effect": "read_only_historical_prior",
        "rows": models,
    })
    _write_json(output_root / "historical_q9_trade_evaluations.json", {
        "schema_version": "historical_q9_trade_evaluations.v1",
        "behavior_effect": "read_only_historical_prior",
        "rows": evaluations,
    })
    _write_json(output_root / "historical_q9_selection_attributions.json", {
        "schema_version": "historical_q9_selection_attributions.v1",
        "behavior_effect": "read_only_historical_prior",
        "rows": attributions,
    })
    _write_json(output_root / "historical_q9_prior_summary.json", summary)
    _write_text(output_root / "historical_q9_prior_report.md", render_historical_prior_markdown(summary))
    return {
        "ok": True,
        "trade_count": len(models),
        "error_count": len(errors),
        "output_dir": str(output_root),
        "summary": str(output_root / "historical_q9_prior_summary.json"),
        "report": str(output_root / "historical_q9_prior_report.md"),
    }


__all__ = [
    "DEFAULT_BEFORE_DAY",
    "build_historical_q9_prior",
    "iter_historical_trade_dirs",
    "render_historical_prior_markdown",
    "summarize_historical_prior",
]
