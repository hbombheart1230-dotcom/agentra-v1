"""live_session_watch: ``_build_markdown`` body (moved verbatim from ``live_session_watch``).

``facade`` is the source module; names/helpers resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Dict, Iterable, List, Mapping, Optional, Tuple


def _build_markdown(snapshot: Dict[str, Any], *, facade: Any) -> str:
    health = snapshot.get("health") if isinstance(snapshot.get("health"), dict) else {}
    metrics = health.get("metrics") if isinstance(health.get("metrics"), dict) else {}
    reasons = health.get("reasons") if isinstance(health.get("reasons"), list) else []
    actions = health.get("recommended_actions") if isinstance(health.get("recommended_actions"), list) else []
    summary = snapshot.get("summary") if isinstance(snapshot.get("summary"), dict) else {}
    decision = summary.get("decision") if isinstance(summary.get("decision"), dict) else {}
    action_counts = decision.get("action_counts") if isinstance(decision.get("action_counts"), dict) else {}

    lines = [
        f"# Live Session Watch ({snapshot.get('ts_kst')})",
        "",
        f"- status: **{health.get('status', 'UNKNOWN')}**",
        f"- loop_alive: **{bool(snapshot.get('loop_alive'))}** (pid={int(snapshot.get('loop_pid') or 0)})",
        f"- event_lag_sec: **{snapshot.get('event_lag_sec')}**",
        f"- summary_rc: **{int(snapshot.get('summary_rc') or 0)}**",
        "",
        "## Metrics",
        "",
        f"- window_total: **{int(metrics.get('window_total') or 0)}**",
        f"- decision action_counts: `{facade.json.dumps(action_counts, ensure_ascii=False)}`",
        f"- llm_error_rate: **{float(metrics.get('llm_error_rate') or 0.0):.2%}**",
        f"- blocked_rate: **{float(metrics.get('blocked_rate') or 0.0):.2%}**",
        f"- executed_broker_fail_total: **{int(metrics.get('executed_broker_fail_total') or 0)}**",
        "",
        "## Reasons",
        "",
    ]
    if reasons:
        for r in reasons:
            lines.append(f"- {str(r)}")
    else:
        lines.append("- none")
    lines.extend(["", "## Recommended Actions", ""])
    if actions:
        for a in actions:
            lines.append(f"- {str(a)}")
    else:
        lines.append("- none")
    lines.extend(
        [
            "",
            "## Artifacts",
            "",
            f"- summary_report_json_path: `{snapshot.get('summary_report_json_path')}`",
            f"- summary_report_md_path: `{snapshot.get('summary_report_md_path')}`",
            f"- watch_jsonl_path: `{snapshot.get('watch_jsonl_path')}`",
        ]
    )
    return "\n".join(lines)
