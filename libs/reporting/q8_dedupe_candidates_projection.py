"""q8_evaluation_contract projections (moved verbatim from q8_evaluation_contract).

Module globals and helpers are resolved on ``facade`` (the q8_evaluation_contract module) at call time; this module never imports it.
"""
from __future__ import annotations

from typing import Any, Dict, List, Mapping, Sequence


def dedupe_q8_candidates(rows: Sequence[Mapping[str, Any]], *, facade: Any) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    seen: set[tuple[str, str, int, str]] = set()
    for row in rows:
        key = facade.canonical_dedupe_key(row)
        if key in seen:
            continue
        seen.add(key)
        out.append(dict(row))
    return out
