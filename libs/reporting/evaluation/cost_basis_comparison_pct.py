"""cost_basis_comparison: ``_pct`` body (moved verbatim from ``cost_basis_comparison``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any


def _pct(value: float, *, facade: Any) -> float:
    return round(float(value) * 100.0, 6)
