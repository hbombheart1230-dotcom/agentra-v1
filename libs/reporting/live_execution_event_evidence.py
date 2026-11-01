from __future__ import annotations

import sys
from typing import Any, Dict, Iterable, List, Set, Tuple

from libs.core.symbols import normalize_symbol
from libs.reporting.live_execution_open_monitor import safe_float
from libs.reporting.live_execution_report_context import to_epoch
from libs.reporting.trade_story_pipeline import safe_int
from libs.reporting import live_event_name_projection as _c03_11_a1_owner
from libs.reporting import live_event_symbol_projection as _c03_11_a2_owner
from libs.reporting import live_event_row_name_projection as _c03_11_a3_owner
from libs.reporting import live_event_identity_merge_projection as _c03_11_a4_owner
from libs.reporting import live_event_canonical_filter_projection as _c03_11_a5_owner
from libs.reporting import live_event_strategist_source_ids_projection as _c03_11_a6_owner
from libs.reporting import live_event_expand_run_ids_projection as _c03_11_a7_owner
from libs.reporting import live_event_latest_payload_projection as _c03_11_a8_owner


def row_event_name(row: Dict[str, Any]) -> str:
    return _c03_11_a1_owner.row_event_name(row)


def event_row_symbol(row: Dict[str, Any]) -> str:
    return _c03_11_a2_owner.event_row_symbol(row, facade=sys.modules[__name__])


def event_row_name(row: Dict[str, Any]) -> str:
    return _c03_11_a3_owner.event_row_name(row)


def merge_rows_by_identity(*collections: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return _c03_11_a4_owner.merge_rows_by_identity(*collections, facade=sys.modules[__name__])


def filter_canonical_events(
    rows: List[Dict[str, Any]],
    *,
    run_ids: List[str],
    agent: str,
    event_names: List[str],
) -> List[Dict[str, Any]]:
    return _c03_11_a5_owner.filter_canonical_events(rows, run_ids=run_ids, agent=agent, event_names=event_names, facade=sys.modules[__name__])


def resolve_strategist_source_run_ids(
    *,
    event_rows: List[Dict[str, Any]],
    lifecycle: Dict[str, Any],
) -> Tuple[List[str], Dict[str, str]]:
    return _c03_11_a6_owner.resolve_strategist_source_run_ids(event_rows=event_rows, lifecycle=lifecycle, facade=sys.modules[__name__])


def expand_targeted_run_ids_with_cached_strategist_sources(
    *,
    event_rows: List[Dict[str, Any]],
    targeted_run_ids: Iterable[str],
) -> Set[str]:
    return _c03_11_a7_owner.expand_targeted_run_ids_with_cached_strategist_sources(event_rows=event_rows, targeted_run_ids=targeted_run_ids, facade=sys.modules[__name__])


def latest_event_payload(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    return _c03_11_a8_owner.latest_event_payload(rows)


def headline_count(news_rows: List[Dict[str, Any]]) -> int:
    total = 0
    for row in list(news_rows or []):
        if not isinstance(row, dict):
            continue
        total += safe_int(row.get("headline_count"), 0)
    return total


def hydrate_strategist_payload_from_evidence(
    strategist_payload: Dict[str, Any],
    strategist_evidence: Dict[str, Any],
) -> Dict[str, Any]:
    out = dict(strategist_payload or {})
    snapshot = latest_event_payload(list(strategist_evidence.get("market_context_snapshots") or []))
    decision_frame = latest_event_payload(list(strategist_evidence.get("decision_frames") or []))
    news_ranked = latest_event_payload(list(strategist_evidence.get("news_evidence_ranked") or []))
    llm_saved = latest_event_payload(list(strategist_evidence.get("llm_response_saved") or []))

    global_signal = snapshot.get("global_signal") if isinstance(snapshot.get("global_signal"), dict) else {}
    if not isinstance(out.get("llm_parsed_output"), dict) or not out.get("llm_parsed_output"):
        out["llm_parsed_output"] = dict(decision_frame or {})
    if not str(out.get("market_regime") or "").strip():
        out["market_regime"] = str(decision_frame.get("market_regime") or "")
    if not str(out.get("market_sentiment") or "").strip():
        out["market_sentiment"] = str(decision_frame.get("market_sentiment") or "")
    if not str(out.get("playbook") or "").strip():
        out["playbook"] = str(decision_frame.get("playbook") or "")
    if not list(out.get("themes") or []):
        out["themes"] = [str(x or "") for x in list(decision_frame.get("themes") or []) if str(x or "").strip()]
    existing_global_score = out.get("global_sentiment_score")
    existing_global_status = str(out.get("global_sentiment_status") or "").strip()
    if existing_global_score in (None, "") or (
        safe_float(existing_global_score, None) == 0.0
        and not existing_global_status
        and isinstance(global_signal, dict)
        and global_signal.get("score") not in (None, "")
    ):
        out["global_sentiment_score"] = global_signal.get("score")
    if not str(out.get("global_sentiment_status") or "").strip():
        out["global_sentiment_status"] = str(global_signal.get("status") or "")
    if not str(out.get("global_sentiment_source") or "").strip():
        out["global_sentiment_source"] = str(global_signal.get("source") or "")
    if not isinstance(out.get("fear_index"), dict) or not out.get("fear_index"):
        out["fear_index"] = dict(global_signal.get("fear_index") or {})
    if not isinstance(out.get("global_macro_moves"), dict) or not out.get("global_macro_moves"):
        out["global_macro_moves"] = dict(global_signal.get("macro_moves") or {})
    if not isinstance(out.get("macro_stress_overlay"), dict) or not out.get("macro_stress_overlay"):
        out["macro_stress_overlay"] = dict(snapshot.get("macro_stress_overlay") or {})
    if not str(out.get("news_query_reasoning") or "").strip():
        reasons = list(decision_frame.get("reason_chain") or [])
        out["news_query_reasoning"] = str(reasons[-1] or "") if reasons else ""
    if not list(out.get("news_query_targets") or []):
        out["news_query_targets"] = [str(x or "") for x in list(news_ranked.get("news_query_targets") or []) if str(x or "").strip()]
    if safe_int(out.get("market_news_query_count"), 0) <= 0:
        out["market_news_query_count"] = len(list(news_ranked.get("news_query_targets") or []))
    if safe_int(out.get("market_news_total_headlines"), 0) <= 0:
        ranked_rows = list(news_ranked.get("market_news_ranked") or []) + list(news_ranked.get("candidate_news_ranked") or [])
        out["market_news_total_headlines"] = headline_count(ranked_rows)
    if not str(out.get("llm_provider") or "").strip():
        out["llm_provider"] = str(llm_saved.get("provider") or "OpenRouter")
    if not str(out.get("llm_model") or "").strip():
        out["llm_model"] = str(llm_saved.get("model") or "")
    return out
