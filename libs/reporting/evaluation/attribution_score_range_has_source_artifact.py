"""attribution_score_range: ``_has_source_artifact`` body (moved verbatim from ``attribution_score_range``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any, Iterable, Mapping


def _has_source_artifact(reports_root: Path, day: str, *, facade: Any) -> bool:
    return any(
        path.exists()
        for path in (
            reports_root / "trades" / day,
            reports_root / "operator_summary" / "daily" / day,
            reports_root / "evaluation" / "daily" / day,
        )
    )
