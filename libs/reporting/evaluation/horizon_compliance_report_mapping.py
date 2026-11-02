"""horizon_compliance_report: ``_mapping`` body (moved verbatim from ``horizon_compliance_report``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Mapping


def _mapping(value: Any, *, facade: Any) -> Mapping[str, Any]:
    return value if isinstance(value, facade.Mapping) else {}
