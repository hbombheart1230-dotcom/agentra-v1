"""attribution_score_v0: ``_score`` body (moved verbatim from ``attribution_score_v0``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping


def _score(status: str, value: int | None, reasons: list[str], evidence: Mapping[str, Any] | None = None, *, facade: Any) -> dict[str, Any]:
    return {
        "status": status,
        "score": value if status != facade.INSUFFICIENT else None,
        "reasons": reasons,
        "evidence": dict(evidence or {}),
    }
