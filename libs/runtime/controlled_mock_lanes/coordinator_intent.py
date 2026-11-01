"""coordinator: ``_intent`` body (moved verbatim from ``coordinator``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Dict, Iterable, List, Mapping, Optional, Tuple


def _intent(candidate: Mapping[str, Any], *, facade: Any) -> dict[str, Any]:
    lane_id = facade._text(candidate.get("lane_id"))
    return {
        "symbol": facade.normalize_symbol(candidate.get("symbol")),
        "side": "BUY",
        "qty": facade.DEFAULT_ORDER_QTY,
        "price": candidate.get("price"),
        "risk_score": 0.0,
        "confidence": 1.0,
        "thesis": f"controlled mock validation lane: {lane_id}",
        "meta": {
            "entry_signal_source": "monitor_intraday_entry",
            "entry_lane": f"controlled_mock:{lane_id}",
            "entry_reason": "controlled_mock_lane_signal_confirmed",
            "controlled_mock_lane": {
                "schema_version": facade.SCHEMA_VERSION,
                **dict(candidate),
                "daily_limit": 1,
                "submission_state": "PENDING_BROKER_RESULT",
            },
            "position_strategy_snapshot": facade._strategy_snapshot(candidate),
            "price": candidate.get("price"),
            "current_price": candidate.get("price"),
            "order_price_source": "controlled_mock_lane_artifact",
        },
    }
