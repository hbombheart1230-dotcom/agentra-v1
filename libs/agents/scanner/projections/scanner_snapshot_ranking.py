"""output_snapshots projections (moved verbatim from output_snapshots).

Module globals and helpers are resolved on ``facade`` (the output_snapshots module) at call time; this module never imports it.
"""
from __future__ import annotations

from typing import Any, Dict, List


def ranking_table_rows(rows: List[Dict[str, Any]], *, max_rows: int = 5, facade: Any) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for idx, row in enumerate(list(rows or [])[: max(0, int(max_rows))], start=1):
        candidate = row.get("candidate") if isinstance(row.get("candidate"), dict) else {}
        out.append(
            {
                "rank": int(idx),
                "symbol": str(row.get("symbol") or ""),
                "score_total": float(facade.to_float(row.get("score_total") or row.get("score"))),
                "score_breakdown": dict(row.get("score_breakdown") or {}),
                "sources": list(candidate.get("sources") or [])[:8],
                "source_scores": dict(candidate.get("source_scores") or {}),
                "source_observations": dict(candidate.get("source_observations") or {}),
                "candidate_source": str(candidate.get("source_why") or ""),
                "rank_score": float(facade.to_float(candidate.get("rank_score"))),
                "universe_score": float(facade.to_float(candidate.get("universe_score"))),
                "risk_score": float(facade.to_float(row.get("risk_score"))),
                "confidence": float(facade.to_float(row.get("confidence"))),
                "bias_adjustment": float(facade.to_float(row.get("bias_adjustment"))),
                "bias_adjustments": list(row.get("bias_adjustments") or []),
                "bias_summary": dict(row.get("bias_summary") or {}),
                "entry_compatibility_score": float(facade.to_float(row.get("entry_compatibility_score"))),
                "compatibility_bias": float(facade.to_float(row.get("compatibility_bias"))),
                "compatibility_components": dict(row.get("compatibility_components") or {}),
                "scanner_chart_fit_score": float(facade.to_float(row.get("scanner_chart_fit_score"))),
                "scanner_chart_fit_authority": str(row.get("scanner_chart_fit_authority") or ""),
                "scanner_chart_fit_components": dict(row.get("scanner_chart_fit_components") or {}),
                "scanner_macro_chart_fit_score": float(facade.to_float(row.get("scanner_macro_chart_fit_score"), 0.5)),
                "scanner_macro_chart_fit_bias": float(facade.to_float(row.get("scanner_macro_chart_fit_bias"))),
                "scanner_macro_chart_fit_authority": str(row.get("scanner_macro_chart_fit_authority") or ""),
                "scanner_macro_chart_fit_components": dict(row.get("scanner_macro_chart_fit_components") or {}),
                "expected_monitor_block_reason": str(row.get("expected_monitor_block_reason") or ""),
                "dominant_block_reason": str(row.get("dominant_block_reason") or ""),
                "dominant_block_reason_ratio": float(facade.to_float(row.get("dominant_block_reason_ratio"))),
                "bias_scale": float(facade.to_float(row.get("bias_scale"))),
                "soft_penalty": float(facade.to_float(row.get("soft_penalty"))),
                "compatibility_score_pre_penalty": float(facade.to_float(row.get("compatibility_score_pre_penalty"))),
                "compatibility_score_post_penalty": float(facade.to_float(row.get("compatibility_score_post_penalty"))),
                "pre_adjust_score_total": float(facade.to_float(row.get("pre_adjust_score_total"))),
                "post_adjust_score_total": float(facade.to_float(row.get("post_adjust_score_total") or row.get("score_total") or row.get("score"))),
                "theme_match": facade.candidate_theme_match(row),
                "feature_coverage": facade.feature_coverage_summary(row),
                "status": "selected" if idx == 1 else "runner_up",
                "exclusion_reason": str(row.get("exclusion_reason") or ""),
                "compact_feature_snapshot": facade.compact_feature_snapshot(row),
                "quant_factor_snapshot": facade.build_factor_snapshot_from_candidate(
                    row,
                    tactic_id=str(row.get("tactical_strategy") or ""),
                    playbook=str(row.get("playbook") or ""),
                ),
                "tactic_suitability": dict(row.get("tactic_suitability") or {}),
            }
        )
    return out
