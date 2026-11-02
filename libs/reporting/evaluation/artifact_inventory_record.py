"""artifact_inventory: ``_record`` body (moved verbatim from ``artifact_inventory``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any, Iterable, Mapping


def _record(path: Path, *, required: bool, facade: Any) -> dict[str, Any]:
    exists = path.exists()
    payload = facade.read_json(path) if exists and path.suffix.lower() == ".json" else {}
    return {
        "path": str(path),
        "required": required,
        "exists": exists,
        "size_bytes": path.stat().st_size if exists else 0,
        "modified_epoch": path.stat().st_mtime if exists else None,
        "schema_version": str(payload.get("schema_version") or ""),
        "evidence_status": str(payload.get("evidence_status") or ""),
        "forward_windows_complete": bool(payload.get("forward_windows_complete")),
        "missing_reason": "" if exists else "artifact_not_found",
    }
