from __future__ import annotations

# Direct execution from the deeper scripts package retains repository imports.
import sys as _migration_sys
from pathlib import Path as _MigrationPath
_migration_root = _MigrationPath(__file__).resolve().parents[2]
if str(_migration_root) not in _migration_sys.path:
    _migration_sys.path.insert(0, str(_migration_root))

import argparse
import json
import os
import sqlite3
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional


def _resolve_db_path(*, state_db_path: str, intent_log_path: str) -> Path:
    raw = str(state_db_path or "").strip()
    if raw:
        return Path(raw)
    env_db = str((os.getenv("INTENT_STATE_DB_PATH", "") or "").strip())
    if env_db:
        return Path(env_db)
    return Path(str(intent_log_path or "").strip() or "data/logs/intents.jsonl").with_suffix(".db")


def _load_state_rows(db_path: Path) -> List[Dict[str, Any]]:
    with sqlite3.connect(str(db_path)) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT intent_id, state, updated_ts, version FROM intent_state ORDER BY updated_ts DESC, intent_id ASC"
        ).fetchall()
    out: List[Dict[str, Any]] = []
    for r in rows:
        out.append(
            {
                "intent_id": str(r["intent_id"]),
                "state": str(r["state"] or ""),
                "updated_ts": int(r["updated_ts"] or 0),
                "version": int(r["version"] or 0),
            }
        )
    return out


def _load_journal_transition_total(db_path: Path, *, state_filter: str = "") -> Dict[str, int]:
    with sqlite3.connect(str(db_path)) as conn:
        conn.row_factory = sqlite3.Row
        if state_filter:
            rows = conn.execute(
                """
                SELECT from_state, to_state, COUNT(*) AS total
                FROM intent_journal
                WHERE to_state = ?
                GROUP BY from_state, to_state
                ORDER BY total DESC, from_state ASC, to_state ASC
                """,
                (state_filter,),
            ).fetchall()
        else:
            rows = conn.execute(
                """
                SELECT from_state, to_state, COUNT(*) AS total
                FROM intent_journal
                GROUP BY from_state, to_state
                ORDER BY total DESC, from_state ASC, to_state ASC
                """
            ).fetchall()

    out: Dict[str, int] = {}
    for r in rows:
        from_state = str(r["from_state"] or "")
        to_state = str(r["to_state"] or "")
        key = f"{from_state}->{to_state}"
        out[key] = int(r["total"] or 0)
    return out


def _load_recent_journal(db_path: Path, *, limit: int, state_filter: str = "") -> List[Dict[str, Any]]:
    lim = max(1, int(limit))
    with sqlite3.connect(str(db_path)) as conn:
        conn.row_factory = sqlite3.Row
        if state_filter:
            rows = conn.execute(
                """
                SELECT id, intent_id, ts, from_state, to_state, reason
                FROM intent_journal
                WHERE to_state = ?
                ORDER BY id DESC
                LIMIT ?
                """,
                (state_filter, lim),
            ).fetchall()
        else:
            rows = conn.execute(
                """
                SELECT id, intent_id, ts, from_state, to_state, reason
                FROM intent_journal
                ORDER BY id DESC
                LIMIT ?
                """,
                (lim,),
            ).fetchall()
    out: List[Dict[str, Any]] = []
    for r in rows:
        out.append(
            {
                "id": int(r["id"] or 0),
                "intent_id": str(r["intent_id"]),
                "ts": int(r["ts"] or 0),
                "from_state": str(r["from_state"] or ""),
                "to_state": str(r["to_state"] or ""),
                "reason": str(r["reason"] or ""),
            }
        )
    return out


def _summary(
    state_rows: List[Dict[str, Any]],
    *,
    now_epoch: int,
    stuck_executing_sec: int,
    journal_transition_total: Dict[str, int],
    state_filter: str = "",
    limit: int = 20,
) -> Dict[str, Any]:
    from scripts.diagnostics.query_intent_state_store_summary import _summary as owner
    return owner(state_rows, now_epoch=now_epoch, stuck_executing_sec=stuck_executing_sec,
                 journal_transition_total=journal_transition_total, state_filter=state_filter,
                 limit=limit, facade=_migration_sys.modules[__name__])


def _build_parser() -> argparse.ArgumentParser:
    from scripts.diagnostics.query_intent_state_store_build_parser import _build_parser as owner
    return owner(facade=_migration_sys.modules[__name__])


def main(argv: Optional[List[str]] = None) -> int:
    args = _build_parser().parse_args(argv)
    db_path = _resolve_db_path(state_db_path=str(args.state_db_path), intent_log_path=str(args.intent_log_path))
    if not db_path.exists():
        print(f"ERROR: state db path does not exist: {db_path}", file=sys.stderr)
        return 2

    try:
        now_epoch = int(time.time())
        state_filter = str(args.state or "").strip().lower()
        state_rows = _load_state_rows(db_path)
        journal_transition_total = _load_journal_transition_total(db_path, state_filter=state_filter)
        summary = _summary(
            state_rows,
            now_epoch=now_epoch,
            stuck_executing_sec=max(0, int(args.stuck_executing_sec)),
            journal_transition_total=journal_transition_total,
            state_filter=state_filter,
            limit=max(1, int(args.limit)),
        )
        recent_journal = _load_recent_journal(
            db_path,
            limit=max(1, int(args.limit)),
            state_filter=state_filter,
        )
    except sqlite3.Error as e:
        print(f"ERROR: sqlite query failed: {e}", file=sys.stderr)
        return 2

    out = {
        "ok": True,
        "state_db_path": str(db_path),
        "state_filter": state_filter,
        "summary": summary,
        "recent_journal": recent_journal,
    }

    if args.json:
        print(json.dumps(out, ensure_ascii=False))
    else:
        print(
            f"total={summary['total']} active_total={summary['active_total']} terminal_total={summary['terminal_total']} "
            f"stuck_executing_total={summary['stuck_executing_total']}"
        )

    if bool(args.require_no_stuck) and int(summary.get("stuck_executing_total") or 0) > 0:
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
