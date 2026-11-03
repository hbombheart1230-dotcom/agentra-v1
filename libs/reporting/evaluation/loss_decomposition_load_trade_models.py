"""loss_decomposition: ``_load_trade_models`` body (moved verbatim from ``loss_decomposition``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any


def _load_trade_models(reports_root: Path, start: str, end: str, *, facade: Any) -> list[dict[str, Any]]:
    models: list[dict[str, Any]] = []
    for day in facade._iter_days(start, end):
        models.extend(facade.build_q9_trade_read_model(path) for path in facade.iter_trade_dirs(reports_root, day))
    return models
