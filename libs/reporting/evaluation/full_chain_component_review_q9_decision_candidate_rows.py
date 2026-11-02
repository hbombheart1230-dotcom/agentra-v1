"""full_chain_component_review: ``_q9_decision_candidate_rows`` body (moved verbatim from ``full_chain_component_review``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any


def _q9_decision_candidate_rows(payloads: list[dict[str, Any]], *, facade: Any) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for payload in payloads:
        for raw in payload.get("q9_decision_candidates") or []:
            if not isinstance(raw, facade.Mapping):
                continue
            row = dict(raw)
            row.setdefault("_payload_generated_at", payload.get("generated_at"))
            rows.append(row)
    return facade.attach_forward_outcomes(rows)
