"""loss_decomposition: ``_candidate_rows`` body (moved verbatim from ``loss_decomposition``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any


def _candidate_rows(payloads: list[dict[str, Any]], *, facade: Any) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for payload in payloads:
        generated_at = payload.get("generated_at")
        for raw in payload.get("candidates") or []:
            if not isinstance(raw, facade.Mapping):
                continue
            row = dict(raw)
            row.setdefault("_payload_generated_at", generated_at)
            rows.append(row)
    return facade.dedupe_q8_candidates(facade.attach_forward_outcomes(rows))
