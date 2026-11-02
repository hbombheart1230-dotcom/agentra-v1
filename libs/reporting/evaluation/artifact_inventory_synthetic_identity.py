"""artifact_inventory: ``_synthetic_identity`` body (moved verbatim from ``artifact_inventory``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable, Mapping


def _synthetic_identity(row: dict[str, Any], *, facade: Any) -> bool:
    identity = " ".join(
        str(row.get(key) or "").lower()
        for key in ("decision_id", "q9_decision_id", "run_id", "candidate_pool_id")
    )
    if any(marker in identity for marker in ("test", "fixture", "synthetic")):
        return True
    symbols: list[str] = []

    def collect(value: Any, *, path: tuple[str, ...] = ()) -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                child_path = (*path, str(key))
                if key in {
                    "symbol",
                    "ticker",
                    "selected_symbol",
                    "top1_symbol",
                    "candidate_symbol",
                } and not any(
                    part == "layer_packet_ids" or part.endswith("_packet_ids")
                    for part in path
                ):
                    text = str(child or "").strip()
                    if text:
                        symbols.append(text)
                elif isinstance(child, (dict, list)):
                    collect(child, path=child_path)
        elif isinstance(value, list):
            for child in value:
                collect(child, path=path)

    collect(row)
    return any(not facade._KRX_SYMBOL_RE.fullmatch(symbol) for symbol in symbols)
