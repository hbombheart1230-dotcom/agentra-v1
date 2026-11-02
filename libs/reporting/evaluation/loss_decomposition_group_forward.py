"""loss_decomposition: ``_group_forward`` body (moved verbatim from ``loss_decomposition``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any


def _group_forward(rows: list[dict[str, Any]], key_fn: Any, *, facade: Any) -> list[dict[str, Any]]:
    groups: dict[str, list[dict[str, Any]]] = facade.defaultdict(list)
    for row in rows:
        groups[str(key_fn(row) or "unknown")].append(row)
    out: list[dict[str, Any]] = []
    for name, members in groups.items():
        result: dict[str, Any] = {
            "name": name,
            "candidate_count": len(members),
        }
        observed_any: set[int] = set()
        for label in ("+5m", "+15m", "+30m", "+60m"):
            values: list[float] = []
            for index, row in enumerate(members):
                value = facade._checkpoint_return(row, label)
                if value is None:
                    continue
                observed_any.add(index)
                values.append(value)
            result[f"observed_{label[1:-1]}m"] = len(values)
            result[f"avg_return_{label[1:-1]}m_pct"] = (
                round(sum(values) / len(values), 4) if values else None
            )
        result["observed_count"] = len(observed_any)
        result["coverage"] = round(len(observed_any) / len(members), 4) if members else 0.0
        out.append(result)
    return sorted(out, key=lambda row: (-int(row["observed_count"]), row["name"]))
