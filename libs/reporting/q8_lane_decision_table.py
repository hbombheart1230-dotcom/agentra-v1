from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any, Dict, Iterable, List, Mapping

from libs.reporting.q8_evaluation_contract import TRUSTED_FORWARD_MIN_COVERAGE
from libs.reporting.quant_shadow_candidate_evaluation import (
    build_quant_shadow_candidate_evaluation,
    load_quant_shadow_candidate_payloads,
)
from libs.reporting import q8_lane_text_projection as _o9a1_owner
from libs.reporting import q8_lane_float_projection as _o9a2_owner
from libs.reporting import q8_lane_int_projection as _o9a3_owner
from libs.reporting import q8_lane_rows_projection as _o9a4_owner
from libs.reporting import q8_lane_forward_rows_projection as _o9a5_owner
from libs.reporting import q8_lane_counts_projection as _o9a6_owner
from libs.reporting import q8_lane_reason_summary_projection as _o9a7_owner
from libs.reporting import q8_lane_verdict_projection as _o9a8_owner


def _text(value: Any) -> str:
    return _o9a1_owner._text(value)


def _float(value: Any, default: float = 0.0) -> float:
    return _o9a2_owner._float(value, default)


def _int(value: Any, default: int = 0) -> int:
    return _o9a3_owner._int(value, default)


def _rows(value: Any) -> List[Dict[str, Any]]:
    return _o9a4_owner._rows(value, facade=sys.modules[__name__])


def _forward_rows(evaluation: Mapping[str, Any]) -> List[Dict[str, Any]]:
    return _o9a5_owner._forward_rows(evaluation, facade=sys.modules[__name__])


def _counts_by_name(rows: Iterable[Mapping[str, Any]]) -> Dict[str, int]:
    return _o9a6_owner._counts_by_name(rows, facade=sys.modules[__name__])


def _reason_summary(evaluation: Mapping[str, Any], *, limit: int = 6) -> str:
    return _o9a7_owner._reason_summary(evaluation, limit=limit, facade=sys.modules[__name__])


def _verdict(row: Mapping[str, Any], *, promotion_allowed: bool) -> Dict[str, str]:
    return _o9a8_owner._verdict(row, promotion_allowed=promotion_allowed, facade=sys.modules[__name__])


def build_q8_lane_decision_table(
    *,
    reports_root: Path = Path("reports"),
    day: str,
) -> Dict[str, Any]:
    payloads = load_quant_shadow_candidate_payloads(reports_root=reports_root, days=[str(day)[:10]])
    evaluation = build_quant_shadow_candidate_evaluation(payloads)
    trust_gate = evaluation.get("evaluation_trust_gate") if isinstance(evaluation.get("evaluation_trust_gate"), Mapping) else {}
    promotion_allowed = bool(trust_gate.get("promotion_allowed"))
    lane_observation = evaluation.get("entry_lane_observation")
    lane_counts = _counts_by_name(
        _rows(lane_observation.get("by_primary_lane") if isinstance(lane_observation, Mapping) else [])
    )
    rows: List[Dict[str, Any]] = []
    for row in _forward_rows(evaluation):
        verdict = _verdict(row, promotion_allowed=promotion_allowed)
        lane = _text(row.get("name"))
        rows.append(
            {
                "lane": lane,
                "candidate_count": _int(row.get("candidate_count")),
                "observed_count": _int(row.get("observed_count")),
                "coverage": round(_float(row.get("coverage")), 4),
                "shadow_count": lane_counts.get(lane, _int(row.get("candidate_count"))),
                "avg_return_3m_pct": row.get("avg_return_3m_pct"),
                "avg_return_5m_pct": row.get("avg_return_5m_pct"),
                "avg_return_15m_pct": row.get("avg_return_15m_pct"),
                "avg_return_30m_pct": row.get("avg_return_30m_pct"),
                "avg_return_60m_pct": row.get("avg_return_60m_pct"),
                "avg_mfe_5m_pct": row.get("avg_mfe_5m_pct"),
                "avg_mae_5m_pct": row.get("avg_mae_5m_pct"),
                **verdict,
            }
        )
    order = {
        "TRUST_GATE_BLOCKED": 0,
        "MISSED_OPPORTUNITY": 1,
        "BAD_ENTRY": 2,
        "GOOD_BLOCK": 3,
        "DATA_INCOMPLETE": 4,
    }
    rows.sort(key=lambda item: (order.get(str(item.get("verdict")), 9), -_int(item.get("observed_count"))))
    return {
        "schema_version": "q8_lane_decision_table.v1",
        "day": str(day)[:10],
        "payload_count": _int(evaluation.get("payload_count")),
        "candidate_count": _int(evaluation.get("candidate_count")),
        "deduped_candidate_count": _int(evaluation.get("deduped_candidate_count")),
        "duplicate_candidate_count": _int(evaluation.get("duplicate_candidate_count")),
        "dedupe_key": list(evaluation.get("dedupe_key") or []),
        "evaluated_count": _int(evaluation.get("evaluated_count")),
        "forward_outcome_available_count": _int(evaluation.get("forward_outcome_available_count")),
        "forward_outcome_coverage": round(_float(evaluation.get("forward_outcome_coverage")), 4),
        "evaluation_trust_gate": dict(trust_gate),
        "promotion_allowed": promotion_allowed,
        "would_enter_count": _int(evaluation.get("would_enter_count")),
        "reason_summary": _reason_summary(evaluation),
        "rows": rows,
    }


def _fmt_pct(value: Any) -> str:
    if value in (None, ""):
        return "-"
    return f"{_float(value):.4f}%"


def render_q8_lane_decision_table_markdown(payload: Mapping[str, Any]) -> str:
    gate = payload.get("evaluation_trust_gate") if isinstance(payload.get("evaluation_trust_gate"), Mapping) else {}
    lines = [
        f"# Q8 Lane Decision Table - {payload.get('day')}",
        "",
        "## Summary",
        "",
        f"- payloads: {payload.get('payload_count')}",
        f"- candidates: {payload.get('candidate_count')}",
        f"- deduped candidates: {payload.get('deduped_candidate_count')}",
        f"- duplicates: {payload.get('duplicate_candidate_count')}",
        f"- dedupe_key: `{', '.join(list(payload.get('dedupe_key') or []))}`",
        f"- evaluated: {payload.get('evaluated_count')}",
        f"- forward observed: {payload.get('forward_outcome_available_count')} "
        f"({float(payload.get('forward_outcome_coverage') or 0.0):.1%})",
        f"- trust_gate: `{gate.get('status') or '-'}`",
        f"- promotion_allowed: `{bool(gate.get('promotion_allowed'))}`",
        f"- trust_block_reasons: `{', '.join(list(gate.get('block_reasons') or gate.get('reasons') or [])) or '-'}`",
        f"- would-enter: {payload.get('would_enter_count')}",
        f"- top reasons: {payload.get('reason_summary') or '-'}",
        "",
        "## Lane Verdicts",
        "",
        "| Lane | Verdict | Decision | n | obs | +5m | +15m | +30m | MFE5 | MAE5 | Rationale |",
        "|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in _rows(payload.get("rows")):
        lines.append(
            "| "
            + " | ".join(
                [
                    _text(row.get("lane")) or "-",
                    _text(row.get("verdict")) or "-",
                    _text(row.get("decision")) or "-",
                    str(row.get("candidate_count") or 0),
                    str(row.get("observed_count") or 0),
                    _fmt_pct(row.get("avg_return_5m_pct")),
                    _fmt_pct(row.get("avg_return_15m_pct")),
                    _fmt_pct(row.get("avg_return_30m_pct")),
                    _fmt_pct(row.get("avg_mfe_5m_pct")),
                    _fmt_pct(row.get("avg_mae_5m_pct")),
                    _text(row.get("rationale")) or "-",
                ]
            )
            + " |"
        )
    lines += [
        "",
        "## Operating Interpretation",
        "",
        "- `TRUST_GATE_BLOCKED`: lane signal is visible, but Q8 evidence is not eligible for policy promotion.",
        "- `MISSED_OPPORTUNITY`: blocked candidates rose afterward. This is a review target, not direct permission to buy.",
        "- `GOOD_BLOCK`: blocked candidates underperformed after the block. Keep the gate under observation.",
        "- `DATA_INCOMPLETE`: sample or coverage is insufficient for a policy conclusion.",
        "",
        "## Current Action",
        "",
        "No new behavior patch is implied by this table unless the Q8 trust gate allows promotion review.",
        "",
    ]
    return "\n".join(lines)


def write_q8_lane_decision_table(
    *,
    reports_root: Path = Path("reports"),
    docs_root: Path = Path("docs/tactics"),
    day: str,
) -> Dict[str, Any]:
    payload = build_q8_lane_decision_table(reports_root=reports_root, day=day)
    docs_root.mkdir(parents=True, exist_ok=True)
    md_path = docs_root / f"q8_lane_decision_table_{str(day)[:10]}.md"
    json_dir = reports_root / "dev" / "analysis" / "q8_lane_decision_table"
    json_dir.mkdir(parents=True, exist_ok=True)
    json_path = json_dir / f"q8_lane_decision_table_{str(day)[:10]}.json"
    md_path.write_text(render_q8_lane_decision_table_markdown(payload), encoding="utf-8")
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    return {"ok": True, "payload": payload, "md_path": str(md_path), "json_path": str(json_path)}


__all__ = [
    "build_q8_lane_decision_table",
    "render_q8_lane_decision_table_markdown",
    "write_q8_lane_decision_table",
]
