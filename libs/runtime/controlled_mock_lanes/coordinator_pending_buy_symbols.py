"""coordinator: ``_pending_buy_symbols`` body (moved verbatim from ``coordinator``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Dict, Iterable, List, Mapping, Optional, Tuple


def _pending_buy_symbols(state: Mapping[str, Any], *, facade: Any) -> set[str]:
    output: set[str] = set()
    containers = (
        state.get("account_orders"),
        facade._mapping(state.get("portfolio_snapshot")).get("orders"),
        facade._mapping(state.get("persisted_state")).get("pending_unfilled_orders"),
    )
    for container in containers:
        rows = container.values() if isinstance(container, Mapping) else container or []
        for raw in rows:
            if not isinstance(raw, Mapping):
                continue
            side = facade._text(raw.get("side") or raw.get("action") or raw.get("ord_dvsn_name")).upper()
            remaining = facade._int(
                raw.get("remaining_qty")
                or raw.get("unfilled_qty")
                or raw.get("rmn_qty")
                or raw.get("qty")
            )
            if "BUY" not in side and "매수" not in side:
                continue
            if remaining <= 0:
                continue
            symbol = facade.normalize_symbol(raw.get("symbol") or raw.get("stk_cd") or raw.get("code"))
            if symbol:
                output.add(symbol)
    return output
