"""Pure in-memory intent state summary owner."""
from __future__ import annotations

from typing import Any, Dict, List


def _summary(state_rows: List[Dict[str, Any]], *, now_epoch: int, stuck_executing_sec: int,
             journal_transition_total: Dict[str, int], state_filter: str = "", limit: int = 20,
             facade: Any) -> Dict[str, Any]:
    current_state_total: Dict[str, int] = {}
    latest_rows: List[Dict[str, Any]] = []
    stuck_rows: List[Dict[str, Any]] = []
    active_total = 0
    terminal_total = 0
    selected = state_rows
    if state_filter:
        selected = [r for r in state_rows if str(r.get("state") or "") == state_filter]
    for r in selected:
        st = str(r.get("state") or "")
        current_state_total[st] = int(current_state_total.get(st, 0)) + 1
        age = max(0, int(now_epoch) - int(r.get("updated_ts") or 0))
        row = {**r, "age_sec": age}
        latest_rows.append(row)
        if st in ("executed", "failed", "rejected"):
            terminal_total += 1
        else:
            active_total += 1
        if stuck_executing_sec > 0 and st == "executing" and age >= stuck_executing_sec:
            stuck_rows.append(row)
    lim = max(1, int(limit))
    return {
        "total": int(len(selected)), "active_total": int(active_total), "terminal_total": int(terminal_total),
        "current_state_total": current_state_total, "journal_transition_total": journal_transition_total,
        "stuck_executing_total": int(len(stuck_rows)), "stuck_executing": stuck_rows[:lim],
        "latest_states": latest_rows[:lim],
    }
