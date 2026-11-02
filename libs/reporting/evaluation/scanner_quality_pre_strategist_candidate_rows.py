"""scanner_quality: ``pre_strategist_candidate_rows`` body (moved verbatim from ``scanner_quality``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Mapping


def pre_strategist_candidate_rows(
    payloads: list[dict[str, Any]],
    *,
    minute_rows_by_symbol: Mapping[str, list[Mapping[str, Any]]] | None = None,
    facade: Any,
) -> list[dict[str, Any]]:
    rows = facade.extract_pre_strategist_candidate_rows(payloads)
    if minute_rows_by_symbol is None:
        return facade.attach_forward_outcomes(rows)
    return facade.attach_forward_outcomes(
        rows,
        minute_rows_by_symbol=minute_rows_by_symbol,
    )
