"""operator_summary_refresh: ``_summary_ref`` body (moved verbatim from ``operator_summary_refresh``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple


def _summary_ref(md_path: Path, json_path: Path, payload: Dict[str, Any] | None = None, *, facade: Any) -> Dict[str, Any]:
    metrics = {}
    if isinstance(payload, dict) and isinstance(payload.get("metrics"), dict):
        metrics = dict(payload.get("metrics") or {})
    return {
        "status": "ok",
        "md_path": str(md_path),
        "json_path": str(json_path),
        "metrics": metrics,
    }
