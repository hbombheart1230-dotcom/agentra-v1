"""q8_evaluation_contract projections (moved verbatim from q8_evaluation_contract).

Module globals and helpers are resolved on ``facade`` (the q8_evaluation_contract module) at call time; this module never imports it.
"""
from __future__ import annotations

from typing import Any, Dict, Mapping


def forward_base(row: Mapping[str, Any], *, facade: Any) -> Dict[str, Any]:
    base = row.get("shadow_forward_base")
    return dict(base) if isinstance(base, facade.Mapping) else {}
