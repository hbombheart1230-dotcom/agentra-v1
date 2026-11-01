from __future__ import annotations

ROLE_CATALOG = (
    {
        "role": "strategist",
        "label": "전략가",
        "configured_model": "openai/gpt-6-luna",
        "fallback_model": "anthropic/claude-haiku-5.5",
        "configuration_source": "strategist balanced policy",
    },
    {
        "role": "trade_report",
        "label": "거래 리포트·요약",
        "configured_model": "google/gemma-4-26b-a4b-it:free",
        "fallback_model": "nvidia/nemotron-3.5-lightning:free",
        "configuration_source": "live report generation path",
    },
    {
        "role": "operator_ui",
        "label": "장중 운영 브리프",
        "configured_model": "nvidia/nemotron-3.5-lightning:free",
        "fallback_model": "google/gemma-4-26b-a4b-it:free",
        "configuration_source": "operator UI route",
    },
    {
        "role": "reporter_intraday",
        "label": "장중 리포터",
        "configured_model": "nvidia/nemotron-3.5-lightning:free",
        "fallback_model": "google/gemma-4-26b-a4b-it:free",
        "configuration_source": "intraday reporter route",
    },
    {
        "role": "reporter_final",
        "label": "장후 최종 리뷰",
        "configured_model": "nvidia/nemotron-3-ultra-550b-a55b:free",
        "fallback_model": "google/gemma-4-26b-a4b-it:free",
        "configuration_source": "final reporter route",
    },
    {
        "role": "daily_report",
        "label": "일일 LLM 요약",
        "configured_model": "nvidia/nemotron-3-ultra-550b-a55b:free",
        "fallback_model": "google/gemma-4-26b-a4b-it:free",
        "configuration_source": "daily report route",
    },
)

ROUTING_ISSUES: tuple[str, ...] = ()
