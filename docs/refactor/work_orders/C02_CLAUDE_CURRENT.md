# C02 — Claude A | A-20261101-12 | RF-DONE-FIRST / RF-014 8 VERIFIED BODY MOVEs + bounded G2 closeout seam

**ONE-FILE ENTRY / PIN:** At start record CANONICAL_HEAD, C02 ORDER_FILE_BLOB_SHA, A_OWNER_REMOTE_SHA and ORDER_ID=A-20261101-12. Read only THIS C02 and the named source/target/test code. No D00/RF/queue/C03/CURRENT/HANDOFF read or RF self-selection. Previous A-20261101-11 8/8 REMOTE_DONE at A remote `b4504878e80786a95a28e13178de89cdf30567c6`, normal 8/8 exit0 (#11 6552247540); do not repeat or rename. New C02 changes next start only, not an in-flight pinned order.

**DIRECT PRIORITY CHANGE:** RF-035 is already 05_DONE; no more RF-035 development assigned. This order targets unfinished **RF-014 (03_PEER_REVIEW, CLAUDE_A exclusive)**. Aim to advance G1/G2 toward C04 scoped integration and C05 new RF DONE; **8 actual SOURCE BODY MOVEs are supply requirement, not 8 RF DONE**. RF-014 G1 remains PARTIAL on Scanner→RF-009 repeat/risk/NOOP consumer; G2 partial; G3 pending. Do not claim whole-RF DONE from the eight projections or the bounded seam smoke.

**SOURCE BLOBS / OWNERSHIP:** `libs/agents/scanner/projections/output_snapshots.py` `02ef48a408338fcb010e82241ef2c694b039979e`, `libs/agents/scanner/projections/selection_evidence_projection.py` `bf20e9af5ec4988e7fef831b0cbb3e44644f6914`, `libs/agents/scanner/projections/output_payloads.py` `fe5e34d58aecb7972adc02e0faa8c89eeb8555f0`; same exact blob on A branch and integration at issuance. All A1–A8 target paths 404/absent on both refs at issuance; only `libs/agents/scanner/` RF-014 code plus new RF-014 targeted tests writable. RF-009 `graphs/nodes/scanner_node.py` and any other RF owner are **READ ONLY**. Do not alter policy thresholds, broker/Guard/Step5C/UEF, operational state, RunLab, real orders/network/files, CI/frozen tests, D00/RF/STATUS/C04/C05, or other actor branches. All fixture tests in-memory, no scanner pipeline execution.

**BODY MOVE CONTRACT:** For each A1–A8, move the entire exact executable function BODY below into the specified *single* new Owner module; remove it from original SOURCE leaving original signature with a thin local-import delegation wrapper. No copy-only move or duplicate calculation. For SOURCE functions without existing `facade`, Owner accepts extra keyword-only `facade` and all original global lookups resolve through `facade.NAME` at call time; SOURCE adds `import sys` and passes `facade=sys.modules[__name__]`. For selection_evidence functions **already accepting facade**, forward that same facade (do not inject another). Preserve signature, kwargs/defaults, order, exception types, mutation/copy, module-level monkeypatch, and external imports. Owner never imports SOURCE. Use unique aliases `_c03_12_aN_owner`. Before editing capture exact golden result/exception for each fixture from original SOURCE, then compare original vs wrapper vs Owner and AST assert original calculation is gone. If any effect or monkeypatch seam cannot be safely preserved, mark that item SAFETY_BLOCKED and continue the next.

**TEST / PUSH:** Add `tests/test_p15_rf014_20261101_12h_projection_owners.py` with one independent `test_aN_*` per item, normal `python -m unittest tests/test_p15_rf014_20261101_12h_projection_owners.py -v` expected 8/8 exit0 **NOT_RUN at issuance**. Add optional bounded G2 closeout test C0 below as a separate test, never count it as BODY MOVE. Commit only A-owned source/new Owner/tests on A branch, normal non-force push, re-fetch A HEAD and all source/target/test blobs, report A1–A8 plus C0, exact exit, SHA and actually measured START/END to #11. Git auth failure=PUSH_BLOCKED only; continue safe local items; pytest missing does not block stdlib unittest. C04 integrates exact code/test SHA, C05 alone moves RF/STATUS.

## C0 — RF-014 CLOSEOUT G2 SEAM (not BODY MOVE, do after A1–A8 or independently if blocked)
Create `tests/test_p15_rf014_scanner_repeat_risk_noop_20261101_12h.py` with fake-only normal unittest for read-only `libs/agents/scanner/candidate_risk.py::resolve_candidate_base_risk` (SOURCE blob `8dea30aebd811d8d9f214c8bca7bef8ea41fa3f9`): scanner_row={'risk_score':0.25} -> risk_score=0.25/source='scanner_row'; empty inputs -> original deterministic fallback. Read-only `libs/agents/scanner/policy/repeat_guard.py::_normalize_scanner_blocker_family_r3_impl` (blob `5f794e544dd0597d36c1f2dee8f474b386df120c`): 'risk_blocked' -> 'risk_guard', 'none' -> ''. Read-only `libs/agents/scanner/projections/control_eligibility.py::build_full_strategist_control_eligibility` (blob `d47013045a37b97a6a1b5d50e067934b628d3251`): {} -> behavior_effect='observation_only', eligible=False; no action/order/noop effect. Command `python -m unittest tests/test_p15_rf014_scanner_repeat_risk_noop_20261101_12h.py -v` expected exit0 with 3 scoped tests (NOT_RUN at issuance). These are bounded pure-function evidence, **not** proof of the entire RF-009 caller or actual runtime NOOP. Record precise remaining caller seam as G1_FIRST_UNMET for C04/C05; never edit RF-009. Do not rerun unchanged existing PASS.

## A1 | RF-014 CLAUDE_A | SOURCE `libs/agents/scanner/projections/output_snapshots.py::to_float` @ L9 | CURRENT_BLOB `02ef48a408338fcb010e82241ef2c694b039979e`
**TARGET (404 both refs):** `libs/agents/scanner/projections/scanner_snapshot_numeric.py::to_float`. Move this actual original BODY (not KEEP/copy) into target:
```python
def to_float(v: Any, default: float = 0.0) -> float:
    try:
        return float(v)
    except Exception:
        return float(default)
```
**THIN WRAPPER / CALL-TIME:** keep exact source signature and delegate via unique alias `_c03_12_a1_owner` to target `to_float`; pass facade=sys.modules[__name__] as an extra target-only kwarg. Globals/seams: none; direct float/exception. Preserve original callers, original exception and any mutation/copy/iteration behavior; never call operational pipeline.
**TARGETED `test_a1_to_float`:** '2.5' -> 2.5; 'bad',default=7 -> 7.0; nonnumeric object matches original exception fallback. Compare exact original golden + wrapper + Owner, patched SOURCE globals and AST body removal. Normal expected exit0; no test run at publication. **BLOCKED→NEXT:** #11 exact error/SHA, continue A2.

## A2 | RF-014 CLAUDE_A | SOURCE `libs/agents/scanner/projections/output_snapshots.py::compact_selected_snapshot` @ L16 | CURRENT_BLOB `02ef48a408338fcb010e82241ef2c694b039979e`
**TARGET (404 both refs):** `libs/agents/scanner/projections/scanner_snapshot_selected.py::compact_selected_snapshot`. Move this actual original BODY (not KEEP/copy) into target:
```python
def compact_selected_snapshot(selected: Dict[str, Any] | None) -> Dict[str, Any]:
    if not isinstance(selected, dict):
        return {}
    candidate = selected.get("candidate") if isinstance(selected.get("candidate"), dict) else {}
    features = selected.get("features") if isinstance(selected.get("features"), dict) else {}
    components = selected.get("components") if isinstance(selected.get("components"), dict) else {}
    return {
        "symbol": str(selected.get("symbol") or ""),
        "why": str(selected.get("why") or ""),
        "asset_class_detected": str(selected.get("asset_class_detected") or ""),
        "detection_source": str(selected.get("detection_source") or ""),
        "detection_field": str(selected.get("detection_field") or ""),
        "sources": list(candidate.get("sources") or [])[:8],
        "source_scores": dict(candidate.get("source_scores") or {}),
        "source_observations": dict(candidate.get("source_observations") or {}),
        "rank_score": to_float(candidate.get("rank_score") or 0.0),
        "universe_score": to_float(candidate.get("universe_score") or 0.0),
        "score_total": to_float(selected.get("score_total") or selected.get("score") or 0.0),
        "risk_score": to_float(selected.get("risk_score") or 0.0),
        "confidence": to_float(selected.get("confidence") or 0.0),
        "best_bid": features.get("quote_best_bid"),
        "best_ask": features.get("quote_best_ask"),
        "spread_bps": features.get("quote_spread_bps"),
        "score_breakdown": dict(selected.get("score_breakdown") or {}),
        "feature_snapshot": {
            "quote_trading_value": features.get("quote_trading_value"),
            "quote_volume": features.get("quote_volume"),
            "intraday_change_pct": features.get("intraday_change_pct"),
            "skill_quote_price": features.get("skill_quote_price"),
            "quote_best_bid": features.get("quote_best_bid"),
            "quote_best_ask": features.get("quote_best_ask"),
            "quote_spread_bps": features.get("quote_spread_bps"),
            "quote_payload_available": features.get("quote_payload_available"),
            "quote_source": features.get("quote_source"),
            "quote_evidence_status": features.get("quote_evidence_status"),
            "entry_compatibility_score": features.get("entry_compatibility_score"),
            "compatibility_bias": features.get("compatibility_bias"),
            "compatibility_source": features.get("compatibility_source"),
            "compat_vwap_distance_abs": features.get("compat_vwap_distance_abs"),
            "compat_is_below_vwap": features.get("compat_is_below_vwap"),
            "compat_reclaim_proximity": features.get("compat_reclaim_proximity"),
            "compat_volume_ratio": features.get("compat_volume_ratio"),
            "compat_breakout_gap_pct": features.get("compat_breakout_gap_pct"),
            "engine_ma20_gap": features.get("engine_ma20_gap"),
            "engine_close_last": features.get("engine_close_last"),
            "engine_ma60": features.get("engine_ma60"),
            "engine_ma120": features.get("engine_ma120"),
            "engine_adx14": features.get("engine_adx14"),
            "engine_trend_strength": features.get("engine_trend_strength"),
            "engine_volume_spike20": features.get("engine_volume_spike20"),
            "engine_volatility20": features.get("engine_volatility20"),
            "engine_vwap_distance": features.get("engine_vwap_distance"),
            "engine_sector_relative_strength": features.get("engine_sector_relative_strength"),
            "engine_cross_section_rank": features.get("engine_cross_section_rank"),
            "engine_regime": features.get("engine_regime"),
            "engine_signal_score": features.get("engine_signal_score"),
        },
        "component_snapshot": {
            "news_sentiment": components.get("news_sentiment"),
            "global_sentiment": components.get("global_sentiment"),
            "trading_value_component": components.get("trading_value_component"),
            "momentum_component": components.get("momentum_component"),
            "trend_component": components.get("trend_component"),
            "volume_surge_component": components.get("volume_surge_component"),
            "intraday_strength_component": components.get("intraday_strength_component"),
            "theme_boost_component": components.get("theme_boost_component"),
            "sentiment_component": components.get("sentiment_component"),
            "volatility_penalty_component": components.get("volatility_penalty_component"),
            "gap_penalty_component": components.get("gap_penalty_component"),
            "avoid_theme_penalty_component": components.get("avoid_theme_penalty_component"),
        },
        "quant_factor_snapshot": build_factor_snapshot_from_candidate(
            selected,
            tactic_id=str(selected.get("tactical_strategy") or ""),
            playbook=str(selected.get("playbook") or ""),
        ),
        "tactic_suitability": dict(selected.get("tactic_suitability") or {}),
    }
```
**THIN WRAPPER / CALL-TIME:** keep exact source signature and delegate via unique alias `_c03_12_a2_owner` to target `compact_selected_snapshot`; pass facade=sys.modules[__name__] as an extra target-only kwarg. Globals/seams: facade.to_float, facade.build_factor_snapshot_from_candidate. Preserve original callers, original exception and any mutation/copy/iteration behavior; never call operational pipeline.
**TARGETED `test_a2_compact_selected_snapshot`:** None -> {}; selected={'symbol':'005930','candidate':{}} -> result['symbol']=='005930'; patch facade.build_factor_snapshot_from_candidate to return {} and verify golden. Compare exact original golden + wrapper + Owner, patched SOURCE globals and AST body removal. Normal expected exit0; no test run at publication. **BLOCKED→NEXT:** #11 exact error/SHA, continue A3.

## A3 | RF-014 CLAUDE_A | SOURCE `libs/agents/scanner/projections/output_snapshots.py::feature_coverage_summary` @ L96 | CURRENT_BLOB `02ef48a408338fcb010e82241ef2c694b039979e`
**TARGET (404 both refs):** `libs/agents/scanner/projections/scanner_snapshot_coverage.py::feature_coverage_summary`. Move this actual original BODY (not KEEP/copy) into target:
```python
def feature_coverage_summary(row: Dict[str, Any]) -> Dict[str, Any]:
    features = row.get("features") if isinstance(row.get("features"), dict) else {}
    if not isinstance(features, dict):
        return {
            "present": 0,
            "total": 0,
            "coverage_ratio": 0.0,
            "quality": "missing",
            "present_keys": [],
            "missing_keys": [],
        }
    interesting_keys = [
        "engine_ma20_gap",
        "engine_ma60",
        "engine_ma120",
        "engine_adx14",
        "engine_trend_strength",
        "engine_atr14",
        "engine_volume_spike20",
        "engine_volatility20",
        "engine_vwap_distance",
        "engine_sector_relative_strength",
        "engine_cross_section_rank",
        "engine_regime",
        "engine_signal_score",
    ]
    present_keys = [key for key in interesting_keys if features.get(key) not in (None, "")]
    missing_keys = [key for key in interesting_keys if features.get(key) in (None, "")]
    total = len(interesting_keys)
    present = len(present_keys)
    ratio = float(present) / float(total) if total else 0.0
    if ratio >= 0.75:
        quality = "strong"
    elif ratio >= 0.5:
        quality = "partial"
    else:
        quality = "weak"
    return {
        "present": int(present),
        "total": int(total),
        "coverage_ratio": float(ratio),
        "quality": quality,
        "present_keys": present_keys,
        "missing_keys": missing_keys,
    }
```
**THIN WRAPPER / CALL-TIME:** keep exact source signature and delegate via unique alias `_c03_12_a3_owner` to target `feature_coverage_summary`; pass facade=sys.modules[__name__] as an extra target-only kwarg. Globals/seams: no mutable module globals. Preserve original callers, original exception and any mutation/copy/iteration behavior; never call operational pipeline.
**TARGETED `test_a3_feature_coverage_summary`:** {'features':{}} -> present=0; a row with one present feature compared to original golden, no mutation. Compare exact original golden + wrapper + Owner, patched SOURCE globals and AST body removal. Normal expected exit0; no test run at publication. **BLOCKED→NEXT:** #11 exact error/SHA, continue A4.

## A4 | RF-014 CLAUDE_A | SOURCE `libs/agents/scanner/projections/output_snapshots.py::compact_feature_snapshot` @ L143 | CURRENT_BLOB `02ef48a408338fcb010e82241ef2c694b039979e`
**TARGET (404 both refs):** `libs/agents/scanner/projections/scanner_snapshot_features.py::compact_feature_snapshot`. Move this actual original BODY (not KEEP/copy) into target:
```python
def compact_feature_snapshot(row: Dict[str, Any]) -> Dict[str, Any]:
    features = row.get("features") if isinstance(row.get("features"), dict) else {}
    if not isinstance(features, dict):
        return {}
    return {
        "skill_quote_price": features.get("skill_quote_price"),
        "quote_trading_value": features.get("quote_trading_value"),
        "quote_volume": features.get("quote_volume"),
        "quote_best_bid": features.get("quote_best_bid"),
        "quote_best_ask": features.get("quote_best_ask"),
        "quote_spread_bps": features.get("quote_spread_bps"),
        "quote_payload_available": features.get("quote_payload_available"),
        "quote_source": features.get("quote_source"),
        "quote_evidence_status": features.get("quote_evidence_status"),
        "intraday_change_pct": features.get("intraday_change_pct"),
        "entry_compatibility_score": features.get("entry_compatibility_score"),
        "compatibility_bias": features.get("compatibility_bias"),
        "compatibility_source": features.get("compatibility_source"),
        "compat_vwap_distance_abs": features.get("compat_vwap_distance_abs"),
        "compat_is_below_vwap": features.get("compat_is_below_vwap"),
        "compat_reclaim_proximity": features.get("compat_reclaim_proximity"),
        "compat_volume_ratio": features.get("compat_volume_ratio"),
        "compat_breakout_gap_pct": features.get("compat_breakout_gap_pct"),
        "engine_ma20_gap": features.get("engine_ma20_gap"),
        "engine_close_last": features.get("engine_close_last"),
        "engine_ma60": features.get("engine_ma60"),
        "engine_ma120": features.get("engine_ma120"),
        "engine_adx14": features.get("engine_adx14"),
        "engine_trend_strength": features.get("engine_trend_strength"),
        "engine_atr14": features.get("engine_atr14"),
        "engine_volume_spike20": features.get("engine_volume_spike20"),
        "engine_volatility20": features.get("engine_volatility20"),
        "engine_vwap_distance": features.get("engine_vwap_distance"),
        "engine_sector_relative_strength": features.get("engine_sector_relative_strength"),
        "engine_cross_section_rank": features.get("engine_cross_section_rank"),
        "engine_regime": features.get("engine_regime"),
        "engine_signal_score": features.get("engine_signal_score"),
    }
```
**THIN WRAPPER / CALL-TIME:** keep exact source signature and delegate via unique alias `_c03_12_a4_owner` to target `compact_feature_snapshot`; pass facade=sys.modules[__name__] as an extra target-only kwarg. Globals/seams: no mutable module globals. Preserve original callers, original exception and any mutation/copy/iteration behavior; never call operational pipeline.
**TARGETED `test_a4_compact_feature_snapshot`:** {'features':{'skill_quote_price':101}} -> output['skill_quote_price']==101; {} -> original golden; input unchanged. Compare exact original golden + wrapper + Owner, patched SOURCE globals and AST body removal. Normal expected exit0; no test run at publication. **BLOCKED→NEXT:** #11 exact error/SHA, continue A5.

## A5 | RF-014 CLAUDE_A | SOURCE `libs/agents/scanner/projections/output_snapshots.py::ranking_table_rows` @ L183 | CURRENT_BLOB `02ef48a408338fcb010e82241ef2c694b039979e`
**TARGET (404 both refs):** `libs/agents/scanner/projections/scanner_snapshot_ranking.py::ranking_table_rows`. Move this actual original BODY (not KEEP/copy) into target:
```python
def ranking_table_rows(rows: List[Dict[str, Any]], *, max_rows: int = 5) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for idx, row in enumerate(list(rows or [])[: max(0, int(max_rows))], start=1):
        candidate = row.get("candidate") if isinstance(row.get("candidate"), dict) else {}
        out.append(
            {
                "rank": int(idx),
                "symbol": str(row.get("symbol") or ""),
                "score_total": float(to_float(row.get("score_total") or row.get("score"))),
                "score_breakdown": dict(row.get("score_breakdown") or {}),
                "sources": list(candidate.get("sources") or [])[:8],
                "source_scores": dict(candidate.get("source_scores") or {}),
                "source_observations": dict(candidate.get("source_observations") or {}),
                "candidate_source": str(candidate.get("source_why") or ""),
                "rank_score": float(to_float(candidate.get("rank_score"))),
                "universe_score": float(to_float(candidate.get("universe_score"))),
                "risk_score": float(to_float(row.get("risk_score"))),
                "confidence": float(to_float(row.get("confidence"))),
                "bias_adjustment": float(to_float(row.get("bias_adjustment"))),
                "bias_adjustments": list(row.get("bias_adjustments") or []),
                "bias_summary": dict(row.get("bias_summary") or {}),
                "entry_compatibility_score": float(to_float(row.get("entry_compatibility_score"))),
                "compatibility_bias": float(to_float(row.get("compatibility_bias"))),
                "compatibility_components": dict(row.get("compatibility_components") or {}),
                "scanner_chart_fit_score": float(to_float(row.get("scanner_chart_fit_score"))),
                "scanner_chart_fit_authority": str(row.get("scanner_chart_fit_authority") or ""),
                "scanner_chart_fit_components": dict(row.get("scanner_chart_fit_components") or {}),
                "scanner_macro_chart_fit_score": float(to_float(row.get("scanner_macro_chart_fit_score"), 0.5)),
                "scanner_macro_chart_fit_bias": float(to_float(row.get("scanner_macro_chart_fit_bias"))),
                "scanner_macro_chart_fit_authority": str(row.get("scanner_macro_chart_fit_authority") or ""),
                "scanner_macro_chart_fit_components": dict(row.get("scanner_macro_chart_fit_components") or {}),
                "expected_monitor_block_reason": str(row.get("expected_monitor_block_reason") or ""),
                "dominant_block_reason": str(row.get("dominant_block_reason") or ""),
                "dominant_block_reason_ratio": float(to_float(row.get("dominant_block_reason_ratio"))),
                "bias_scale": float(to_float(row.get("bias_scale"))),
                "soft_penalty": float(to_float(row.get("soft_penalty"))),
                "compatibility_score_pre_penalty": float(to_float(row.get("compatibility_score_pre_penalty"))),
                "compatibility_score_post_penalty": float(to_float(row.get("compatibility_score_post_penalty"))),
                "pre_adjust_score_total": float(to_float(row.get("pre_adjust_score_total"))),
                "post_adjust_score_total": float(to_float(row.get("post_adjust_score_total") or row.get("score_total") or row.get("score"))),
                "theme_match": candidate_theme_match(row),
                "feature_coverage": feature_coverage_summary(row),
                "status": "selected" if idx == 1 else "runner_up",
                "exclusion_reason": str(row.get("exclusion_reason") or ""),
                "compact_feature_snapshot": compact_feature_snapshot(row),
                "quant_factor_snapshot": build_factor_snapshot_from_candidate(
                    row,
                    tactic_id=str(row.get("tactical_strategy") or ""),
                    playbook=str(row.get("playbook") or ""),
                ),
                "tactic_suitability": dict(row.get("tactic_suitability") or {}),
            }
        )
    return out
```
**THIN WRAPPER / CALL-TIME:** keep exact source signature and delegate via unique alias `_c03_12_a5_owner` to target `ranking_table_rows`; pass facade=sys.modules[__name__] as an extra target-only kwarg. Globals/seams: facade.to_float, facade.candidate_theme_match, facade.feature_coverage_summary, facade.compact_feature_snapshot, facade.build_factor_snapshot_from_candidate. Preserve original callers, original exception and any mutation/copy/iteration behavior; never call operational pipeline.
**TARGETED `test_a5_ranking_table_rows`:** [] -> []; any rows with max_rows=0 -> []; one fake row with patched facade.candidate_theme_match=lambda _:False and factor snapshot=lambda *a,**kw:{} -> one output row, exact original golden and order. Compare exact original golden + wrapper + Owner, patched SOURCE globals and AST body removal. Normal expected exit0; no test run at publication. **BLOCKED→NEXT:** #11 exact error/SHA, continue A6.

## A6 | RF-014 CLAUDE_A | SOURCE `libs/agents/scanner/projections/selection_evidence_projection.py::scan_select_value_state_scanner_skill` @ L188 | CURRENT_BLOB `bf20e9af5ec4988e7fef831b0cbb3e44644f6914`
**TARGET (404 both refs):** `libs/agents/scanner/projections/scanner_selection_skill.py::scan_select_value_state_scanner_skill`. Move this actual original BODY (not KEEP/copy) into target:
```python
def scan_select_value_state_scanner_skill(fallback_reasons, skill_quotes, skill_order_counts, skill_order_rows, quote_meta, order_meta, *, facade):
    return (
{
        "contract_version": facade.SKILL_CONTRACT_VERSION,
        "used": bool(skill_quotes) or bool(skill_order_counts),
        "quote_symbols": len(skill_quotes),
        "account_open_order_symbols": len(skill_order_counts),
        "account_order_rows": int(skill_order_rows),
        "quote_present": bool(quote_meta.get("present")),
        "account_orders_present": bool(order_meta.get("present")),
        "fallback": bool(fallback_reasons),
        "fallback_reasons": fallback_reasons,
        "error_count": len(fallback_reasons),
    }
    )
```
**THIN WRAPPER / CALL-TIME:** keep exact source signature and delegate via unique alias `_c03_12_a6_owner` to target `scan_select_value_state_scanner_skill`; forward the existing facade argument unchanged. Globals/seams: EXISTING facade parameter; preserve same facade, facade.SKILL_CONTRACT_VERSION. Preserve original callers, original exception and any mutation/copy/iteration behavior; never call operational pipeline.
**TARGETED `test_a6_scan_select_value_state_scanner_skill`:** fallback_reasons=[], skill_quotes={}, skill_order_counts={}, skill_order_rows=[], quote_meta={},order_meta={},facade=SimpleNamespace(SKILL_CONTRACT_VERSION='fixture') -> first returned dict contract_version='fixture', used=False; compare full original tuple. Compare exact original golden + wrapper + Owner, patched SOURCE globals and AST body removal. Normal expected exit0; no test run at publication. **BLOCKED→NEXT:** #11 exact error/SHA, continue A7.

## A7 | RF-014 CLAUDE_A | SOURCE `libs/agents/scanner/projections/selection_evidence_projection.py::scan_select_reasons_row_conf` @ L231 | CURRENT_BLOB `bf20e9af5ec4988e7fef831b0cbb3e44644f6914`
**TARGET (404 both refs):** `libs/agents/scanner/projections/selection_evidence_projection_scan_select_reasons_row_conf.py::scan_select_reasons_row_conf`. Move this actual original BODY (not KEEP/copy) into target:
```python
def scan_select_reasons_row_conf(row, selected_score, selected_confidence, selected_risk, runner_up_reasons, *, facade):
    if True:
            reasons: facade.List[str] = []
            row_score = float(facade._to_float(row.get("score_total") or row.get("score")))
            row_conf = float(facade._to_float(row.get("confidence")))
            row_risk = float(facade._to_float(row.get("risk_score")))
            if row_score < selected_score:
                reasons.append(f"lower total score ({row_score:.3f} vs {selected_score:.3f})")
            if row_conf < selected_confidence:
                reasons.append(f"lower confidence ({row_conf:.2f} vs {selected_confidence:.2f})")
            if row_risk > selected_risk:
                reasons.append(f"higher risk ({row_risk:.2f} vs {selected_risk:.2f})")
            if not reasons:
                reasons.append("lost on tie-break after score, confidence, and risk comparison")
            runner_up_reasons.append(
                {
                    "symbol": str(row.get("symbol") or ""),
                    "why_lost": reasons,
                }
            )
    return (reasons, row_conf, row_risk, row_score)
```
**THIN WRAPPER / CALL-TIME:** keep exact source signature and delegate via unique alias `_c03_12_a7_owner` to target `scan_select_reasons_row_conf`; forward the existing facade argument unchanged. Globals/seams: EXISTING facade parameter; preserve facade._to_float and facade.List at call time; mutation of runner_up_reasons. Preserve original callers, original exception and any mutation/copy/iteration behavior; never call operational pipeline.
**TARGETED `test_a7_scan_select_reasons_row_conf`:** row={'symbol':'005930','score_total':0.5,'confidence':0.3,'risk_score':0.9}, selected_score=0.8,selected_confidence=0.6,selected_risk=0.2,runner_up_reasons=[],facade=SimpleNamespace(_to_float=float,List=list) -> 3 lower/confidence/higher-risk reasons and appended symbol='005930'; tuple and list match golden. Compare exact original golden + wrapper + Owner, patched SOURCE globals and AST body removal. Normal expected exit0; no test run at publication. **BLOCKED→NEXT:** #11 exact error/SHA, continue A8.

## A8 | RF-014 CLAUDE_A | SOURCE `libs/agents/scanner/projections/output_payloads.py::_to_float` @ L8 | CURRENT_BLOB `fe5e34d58aecb7972adc02e0faa8c89eeb8555f0`
**TARGET (404 both refs):** `libs/agents/scanner/projections/scanner_output_numeric.py::_to_float`. Move this actual original BODY (not KEEP/copy) into target:
```python
def _to_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except Exception:
        return float(default)
```
**THIN WRAPPER / CALL-TIME:** keep exact source signature and delegate via unique alias `_c03_12_a8_owner` to target `_to_float`; pass facade=sys.modules[__name__] as an extra target-only kwarg. Globals/seams: none; direct float/exception. Preserve original callers, original exception and any mutation/copy/iteration behavior; never call operational pipeline.
**TARGETED `test_a8__to_float`:** '3.25' -> 3.25; 'bad',default=9 -> 9.0; exception fallback identical. Compare exact original golden + wrapper + Owner, patched SOURCE globals and AST body removal. Normal expected exit0; no test run at publication. **BLOCKED→NEXT:** #11 exact error/SHA, continue C0 and reserve (design-only).

## FUTURE RESERVE — RF-014 CLAUDE_A VERIFIED 6/6, DESIGN_ONLY / NOT EXECUTABLE
All SOURCE blobs same A/integration; targets absent on both refs; all RF-014 exclusive, no external real effects. These are NOT part of A-12 order; C03 must revalidate before promotion:
- **R1 VERIFIED DESIGN ONLY:** `libs/agents/scanner/candidate_risk.py::_optional_float` L6 blob `8dea30aebd811d8d9f214c8bca7bef8ea41fa3f9` → `libs/agents/scanner/scanner_candidate_risk_numeric.py::_optional_float` (404 both refs). Actual original BODY confirmed (7 lines, first executable `if value in (None, ""):`), original source is not a thin wrapper. Candidate extraction only after call-time facade and original-golden parity. Fixture: '0.2' -> 0.2, None -> None; no IO. No network/operational IO; any transitive factor builder must be fake patched. NOT ASSIGNED.
- **R2 VERIFIED DESIGN ONLY:** `libs/agents/scanner/candidate_risk.py::_clamp` L15 blob `8dea30aebd811d8d9f214c8bca7bef8ea41fa3f9` → `libs/agents/scanner/scanner_candidate_risk_clamp.py::_clamp` (404 both refs). Actual original BODY confirmed (2 lines, first executable `return max(lower, min(upper, float(value)))`), original source is not a thin wrapper. Candidate extraction only after call-time facade and original-golden parity. Fixture: -0.2 -> 0.0, 1.4 -> 1.0; no IO. No network/operational IO; any transitive factor builder must be fake patched. NOT ASSIGNED.
- **R3 VERIFIED DESIGN ONLY:** `libs/agents/scanner/candidate_risk.py::_first_number` L19 blob `8dea30aebd811d8d9f214c8bca7bef8ea41fa3f9` → `libs/agents/scanner/scanner_candidate_risk_first_number.py::_first_number` (404 both refs). Actual original BODY confirmed (6 lines, first executable `for key in keys:`), original source is not a thin wrapper. Candidate extraction only after call-time facade and original-golden parity. Fixture: {'a':None,'b':'0.4'},'a','b' -> 0.4; fake mapping. No network/operational IO; any transitive factor builder must be fake patched. NOT ASSIGNED.
- **R4 VERIFIED DESIGN ONLY:** `libs/agents/scanner/candidate_risk.py::resolve_candidate_base_risk` L27 blob `8dea30aebd811d8d9f214c8bca7bef8ea41fa3f9` → `libs/agents/scanner/scanner_candidate_base_risk_projection.py::resolve_candidate_base_risk` (404 both refs). Actual original BODY confirmed (86 lines, first executable `*,`), original source is not a thin wrapper. Candidate extraction only after call-time facade and original-golden parity. Fixture: scanner_row risk 0.25 -> risk_score 0.25/source scanner_row; pure no order. No network/operational IO; any transitive factor builder must be fake patched. NOT ASSIGNED.
- **R5 VERIFIED DESIGN ONLY:** `libs/agents/scanner/projections/output_payloads.py::build_candidate_ranking_table_payload` L15 blob `fe5e34d58aecb7972adc02e0faa8c89eeb8555f0` → `libs/agents/scanner/projections/scanner_ranking_payload_projection.py::build_candidate_ranking_table_payload` (404 both refs). Actual original BODY confirmed (80 lines, first executable `ranking_table: List[Dict[str, Any]],`), original source is not a thin wrapper. Candidate extraction only after call-time facade and original-golden parity. Fixture: fake ranking [] -> original golden; sorted fake rows, patch source numeric helper; no IO. No network/operational IO; any transitive factor builder must be fake patched. NOT ASSIGNED.
- **R6 VERIFIED DESIGN ONLY:** `libs/agents/scanner/projections/output_payloads.py::build_candidate_selection_reason_payload` L97 blob `fe5e34d58aecb7972adc02e0faa8c89eeb8555f0` → `libs/agents/scanner/projections/scanner_selection_reason_payload_projection.py::build_candidate_selection_reason_payload` (404 both refs). Actual original BODY confirmed (134 lines, first executable `*,`), original source is not a thin wrapper. Candidate extraction only after call-time facade and original-golden parity. Fixture: fake selected/empty reasons + patched factor snapshot, golden payload; no IO. No network/operational IO; any transitive factor builder must be fake patched. NOT ASSIGNED.

**COUNT/DELIVERY:** A-11 8/8 REMOTE_DONE; A-12 NEW_READY=8 real BODY MOVEs RF-014, C0 scoped test=1 non-MOVE, RESERVE_VERIFIED=6/6 design only. G1/G2/G3 new evidence NOT_RUN until A actor; C03 DOC_ONLY, RF_DONE_DELTA=0. FIRST_BLOCKER: RF-014 Scanner→RF-009 actual consumer NOOP seam not yet established; C04/C05 must judge exact new evidence. RunLab Exited(255), RUN_SOURCE_SHA UNKNOWN, operational HOLD.
