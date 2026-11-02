"""artifact_inventory: ``iter_trade_dirs`` body (moved verbatim from ``artifact_inventory``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable, Mapping


def iter_trade_dirs(reports_root: Path, day: str, *, facade: Any) -> list[Path]:
    root = facade.Path(reports_root) / "trades" / day
    if not root.exists():
        return []
    return sorted({path.parent for path in root.rglob("lifecycle_bundle.json")})
