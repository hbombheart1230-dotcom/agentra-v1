"""artifact_inventory: ``load_q9_pre_strategist_rows`` body (moved verbatim from ``artifact_inventory``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable, Mapping


def load_q9_pre_strategist_rows(reports_root: Path, day: str, *, facade: Any) -> list[dict[str, Any]]:
    pre_rows: list[dict[str, Any]] = []
    for shadow in facade._iter_shadow_payloads(reports_root, day):
        generated_at = str(shadow.get("generated_at") or "")
        for raw in shadow.get("q9_decision_candidates") or []:
            if (
                not isinstance(raw, dict)
                or str(raw.get("q9_decision_role") or "")
                != "P_SCANNER_PRE_STRATEGIST_UNIVERSE"
            ):
                continue
            row = dict(raw)
            row.setdefault("_payload_generated_at", generated_at)
            if facade._synthetic_identity(row) or not facade._regular_session_window(
                {"generated_at": generated_at}
            ):
                continue
            pre_rows.append(row)
    return pre_rows
