"""operator_visibility: ``_compact_blocking_features`` body (moved verbatim from ``operator_visibility``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Dict, Iterable, List, Mapping, Optional, Tuple


def _compact_blocking_features(raw: Any, *, limit: int = 3, facade: Any) -> str:
    values = raw if isinstance(raw, list) else []
    clipped = [str(v or "").strip() for v in values if str(v or "").strip()]
    return ", ".join(clipped[:limit]) if clipped else "-"
