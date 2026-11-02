"""agent_effectiveness_scorecard: ``render_agent_effectiveness_scorecard`` body (moved verbatim from ``agent_effectiveness_scorecard``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping, Sequence


def render_agent_effectiveness_scorecard(payload: Mapping[str, Any], *, facade: Any) -> str:
    date_range = facade._mapping(payload.get("range"))
    components = facade._mapping(payload.get("components"))
    strategist = facade._mapping(components.get("strategist"))
    lines = [
        f"# Agent Effectiveness Scorecard ({date_range.get('start')} ~ {date_range.get('end')})",
        "",
        "Evaluation-only. This report does not change trading behavior.",
        "",
        "## Component States",
        "",
        "| Component | State | Meaning |",
        "|---|---|---|",
        f"| Scanner relative ranking | `{facade._mapping(components.get('scanner')).get('relative_ranking_state')}` | Strategy-conditioned rank precision |",
        f"| Scanner absolute edge | `{facade._mapping(components.get('scanner')).get('absolute_edge_state')}` | Cost-adjusted candidate edge |",
        f"| Strategist full contribution | `{facade._mapping(strategist.get('full_contribution')).get('state')}` | Requires strategy-neutral source control |",
        f"| Strategist ranking overlay | `{facade._mapping(strategist.get('ranking_overlay')).get('state')}` | Same-universe intrinsic vs strategy-weighted |",
        f"| Strategist post-Scanner refresh | `{facade._mapping(strategist.get('post_scanner_refresh')).get('state')}` | First Scanner vs refreshed Scanner |",
        f"| Commander | `{facade._mapping(components.get('commander')).get('state')}` | Presented candidate vs approve/veto |",
        f"| Monitor Entry | `{facade._mapping(components.get('monitor_entry')).get('state')}` | Selected baseline vs entry/block |",
        f"| Monitor Exit/Horizon | `{facade._mapping(components.get('monitor_exit_horizon')).get('state')}` | Actual exit vs strategy-valid alternatives |",
        f"| Full system | `{facade._mapping(components.get('full_system')).get('state')}` | Broker-net result |",
        "",
        "## Strategist Control Boundary",
        "",
        "- `A_SCANNER_CONTROL` is a same-candidate-universe intrinsic ranking control.",
        "- It is not a fully raw pre-Strategist Scanner because Strategist runs first.",
        "- Full Strategist value remains `NOT_MEASURABLE` until a strategy-neutral candidate-source shadow exists.",
        "- Ranking overlay and post-Scanner refresh are evaluated separately.",
        "",
        "## Evidence Shortfalls",
        "",
    ]
    for name, row in (
        ("Strategist full", facade._mapping(strategist.get("full_contribution"))),
        ("Strategist scenario", facade._mapping(strategist.get("scenario_quality"))),
        ("Strategist overlay", facade._mapping(strategist.get("ranking_overlay"))),
        ("Strategist refresh", facade._mapping(strategist.get("post_scanner_refresh"))),
        ("Commander", facade._mapping(components.get("commander"))),
    ):
        if row.get("state") == "NOT_MEASURABLE":
            lines.append(f"- {name}: {row.get('missing_control') or row.get('reason')}")
    return "\n".join(lines) + "\n"
