"""scanner_quality: ``extract_pre_strategist_candidate_rows`` body (moved verbatim from ``scanner_quality``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any


def extract_pre_strategist_candidate_rows(
    payloads: list[dict[str, Any]],
    *,
    facade: Any,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    seen: set[tuple[str, str, int]] = set()
    for payload in payloads:
        generated_at = str(payload.get("generated_at") or "")
        for raw in payload.get("q9_decision_candidates") or []:
            if not isinstance(raw, facade.Mapping):
                continue
            if str(raw.get("q9_decision_role") or "") != "P_SCANNER_PRE_STRATEGIST_UNIVERSE":
                continue
            row = dict(raw)
            decision_id = str(row.get("q9_decision_id") or "")
            symbol = str(row.get("symbol") or "")
            rank = int(facade._number(row.get("rank")) or 0)
            key = (decision_id, symbol, rank)
            if not decision_id or not symbol or rank <= 0 or key in seen:
                continue
            seen.add(key)
            row.setdefault("_payload_generated_at", generated_at)
            rows.append(row)
    return rows
