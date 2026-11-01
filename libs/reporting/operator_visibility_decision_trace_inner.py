"""operator_visibility: ``_decision_trace_inner`` body (moved verbatim from ``operator_visibility``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Dict, Iterable, List, Mapping, Optional, Tuple


def _decision_trace_inner(payload: Dict[str, Any], *, facade: Any) -> Dict[str, Any]:
    inner = payload.get("payload") if isinstance(payload.get("payload"), dict) else {}
    return inner if isinstance(inner, dict) else {}
