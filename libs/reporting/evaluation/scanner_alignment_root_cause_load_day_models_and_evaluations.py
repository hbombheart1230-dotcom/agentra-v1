"""scanner_alignment_root_cause: ``_load_day_models_and_evaluations`` body (moved verbatim from ``scanner_alignment_root_cause``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any


def _load_day_models_and_evaluations(reports_root: Path, day: str, *, facade: Any) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    root = reports_root / "evaluation" / "trades" / day
    models: list[dict[str, Any]] = []
    evaluations: list[dict[str, Any]] = []
    if not root.exists():
        return models, evaluations
    for trade_dir in sorted(path for path in root.iterdir() if path.is_dir()):
        model = facade._read_json(trade_dir / "trade_read_model.json")
        evaluation = facade._read_json(trade_dir / "trade_evaluation.json")
        if model:
            models.append(model)
        if evaluation:
            evaluations.append(evaluation)
    return models, evaluations
