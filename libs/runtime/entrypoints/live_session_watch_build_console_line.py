"""live_session_watch: ``_build_console_line`` body (moved verbatim from ``live_session_watch``).

``facade`` is the source module; names/helpers resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Dict, Iterable, List, Mapping, Optional, Tuple


def _build_console_line(snapshot: Dict[str, Any], *, facade: Any) -> str:
    health = snapshot.get("health") if isinstance(snapshot.get("health"), dict) else {}
    metrics = health.get("metrics") if isinstance(health.get("metrics"), dict) else {}
    summary = snapshot.get("summary") if isinstance(snapshot.get("summary"), dict) else {}
    decision = summary.get("decision") if isinstance(summary.get("decision"), dict) else {}
    actions = decision.get("action_counts") if isinstance(decision.get("action_counts"), dict) else {}
    return (
        f"[{snapshot.get('ts_kst')}] status={health.get('status')} "
        f"loop_alive={bool(snapshot.get('loop_alive'))} "
        f"lag_sec={snapshot.get('event_lag_sec')} "
        f"window={int(metrics.get('window_total') or 0)} "
        f"buy={int(actions.get('BUY') or 0)} "
        f"sell={int(actions.get('SELL') or 0)} "
        f"noop={int(actions.get('NOOP') or 0)} "
        f"llm_error_rate={float(metrics.get('llm_error_rate') or 0.0):.2%} "
        f"blocked_rate={float(metrics.get('blocked_rate') or 0.0):.2%}"
    )
