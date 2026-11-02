"""evaluation_lens_report: ``_as_dict`` body (moved verbatim from ``evaluation_lens_report``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any


def _as_dict(value: Any, *, facade: Any) -> dict[str, Any]:
    return dict(value) if isinstance(value, facade.Mapping) else {}
