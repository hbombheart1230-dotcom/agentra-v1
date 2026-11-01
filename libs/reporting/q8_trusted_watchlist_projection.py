"""q8_trusted_reaggregation projections (moved verbatim from q8_trusted_reaggregation).

Module globals and helpers are resolved on ``facade`` (the q8_trusted_reaggregation module) at call time; this module never imports it.
"""
from __future__ import annotations

from typing import Any, Dict, List, Mapping


def _watchlist_rows(scorecard: Mapping[str, Any], *, facade: Any) -> List[Dict[str, Any]]:
    return [dict(row) for row in list(scorecard.get("promotion_watchlist") or []) if isinstance(row, facade.Mapping)]
