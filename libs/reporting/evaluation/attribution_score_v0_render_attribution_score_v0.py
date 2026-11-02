"""attribution_score_v0: ``render_attribution_score_v0`` body (moved verbatim from ``attribution_score_v0``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable, Mapping


def render_attribution_score_v0(payload: Mapping[str, Any], *, facade: Any) -> str:
    lines = [
        f"# Q13 Attribution Score v0 - {payload.get('day', '')}",
        "",
        f"- Behavior effect: `{payload.get('behavior_effect', '')}`",
        f"- Weakest observed axis: `{facade._mapping(payload.get('weakest_observed_axis')).get('name') or '-'}` "
        f"({facade._mapping(payload.get('weakest_observed_axis')).get('score')})",
        "",
        "## Scores",
        "",
        "| Axis | Status | Score | Reasons |",
        "| --- | --- | ---: | --- |",
    ]
    for key, item in facade._mapping(payload.get("scores")).items():
        obj = facade._mapping(item)
        score = obj.get("score")
        reasons = ", ".join(str(reason) for reason in obj.get("reasons") or []) or "-"
        lines.append(
            f"| {key} | {obj.get('status')} | "
            f"{'-' if score is None else int(score)} | {reasons} |"
        )
    lines.extend([
        "",
        "## Interpretation",
        "",
        f"- {payload.get('interpretation_rule', '')}",
        "",
        "## Limitations",
        "",
    ])
    for item in payload.get("limitations") or []:
        lines.append(f"- {item}")
    lines.append("")
    return "\n".join(lines)
