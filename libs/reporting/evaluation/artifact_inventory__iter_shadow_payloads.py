"""artifact_inventory: ``_iter_shadow_payloads`` body (moved verbatim from ``artifact_inventory``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable, Mapping


def _iter_shadow_payloads(reports_root: Path, day: str, *, facade: Any):
    """Yield each non-empty shadow payload of `day` one at a time, in file-name order.

    Streaming (rather than collecting a list) keeps only one parsed payload alive at a
    time; a trading day's full list was ~300 MiB of parsed objects and, loaded twice
    here, was a large part of the closeout peak that OOM-killed the 1 GiB container.
    """
    shadow_root = facade.Path(reports_root).parent / "data" / "logs" / "quant_shadow_candidates" / day
    if not shadow_root.exists():
        return
    for shadow_path in sorted(shadow_root.glob("*.json")):
        if shadow_path.name == "latest.json":
            continue
        shadow = facade.read_json(shadow_path)
        if shadow:
            yield shadow
