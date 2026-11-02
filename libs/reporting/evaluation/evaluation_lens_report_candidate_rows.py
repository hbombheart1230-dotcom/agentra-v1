"""evaluation_lens_report: ``_candidate_rows`` body (moved verbatim from ``evaluation_lens_report``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Iterable, Mapping


def _candidate_rows(payloads: Iterable[Mapping[str, Any]], *, facade: Any) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for payload in payloads:
        generated_at = payload.get("generated_at")
        for raw in payload.get("candidates") or []:
            if not isinstance(raw, facade.Mapping):
                continue
            row = dict(raw)
            row.setdefault("_payload_generated_at", generated_at)
            rows.append(row)
    return facade.attach_forward_outcomes(rows)
