from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any, Mapping
from . import agent_effectiveness_scorecard_mapping as _a33_mapping
from . import agent_effectiveness_scorecard_number as _a33_number
from . import agent_effectiveness_scorecard_delta_state as _a33_delta_state
from . import agent_effectiveness_scorecard_decision_state as _a33_decision_state
from . import agent_effectiveness_scorecard_build_agent_effectiveness_scorecard as _a33_build_agent_effectiveness_scorecard
from . import agent_effectiveness_scorecard_render_agent_effectiveness_scorecard as _a33_render_agent_effectiveness_scorecard

from .contracts import (
    CONTRACT_VERSION,
    DIRECTIONAL_MIN_DAYS,
    DIRECTIONAL_MIN_OBSERVATIONS,
)
from .full_chain_component_review import build_full_chain_component_review


MIN_MATERIAL_DELTA_PCT = 0.30
MIN_POSITIVE_RATE = 0.55
MAX_DEGRADING_POSITIVE_RATE = 0.45


def _mapping(value: Any) -> dict[str, Any]:
    return _a33_mapping._mapping(value=value, facade=sys.modules[__name__])


def _number(value: Any) -> float | None:
    return _a33_number._number(value=value, facade=sys.modules[__name__])


def _delta_state(
    metrics: Mapping[str, Any],
    *,
    prefix: str,
    missing_control: str,
) -> dict[str, Any]:
    return _a33_delta_state._delta_state(metrics=metrics, prefix=prefix, missing_control=missing_control, facade=sys.modules[__name__])


def _decision_state(component: Mapping[str, Any]) -> str:
    return _a33_decision_state._decision_state(component=component, facade=sys.modules[__name__])


def build_agent_effectiveness_scorecard(
    full_chain_review: Mapping[str, Any],
) -> dict[str, Any]:
    return _a33_build_agent_effectiveness_scorecard.build_agent_effectiveness_scorecard(full_chain_review=full_chain_review, facade=sys.modules[__name__])


def render_agent_effectiveness_scorecard(payload: Mapping[str, Any]) -> str:
    return _a33_render_agent_effectiveness_scorecard.render_agent_effectiveness_scorecard(payload=payload, facade=sys.modules[__name__])


def write_agent_effectiveness_scorecard(
    *,
    reports_root: Path,
    start: str,
    end: str,
    output_dir: Path,
) -> dict[str, Any]:
    review = build_full_chain_component_review(
        reports_root=Path(reports_root),
        start=start,
        end=end,
    )
    payload = build_agent_effectiveness_scorecard(review)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "agent_effectiveness_scorecard.json"
    md_path = output_dir / "agent_effectiveness_scorecard.md"
    json_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    md_path.write_text(render_agent_effectiveness_scorecard(payload), encoding="utf-8")
    return {
        "json_path": str(json_path),
        "markdown_path": str(md_path),
        "range": payload.get("range"),
    }
