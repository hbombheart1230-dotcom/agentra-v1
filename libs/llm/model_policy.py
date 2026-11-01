"""Verified OpenRouter model policy for runtime LLM roles.

Keep role allow-lists here so an environment or applied-policy override cannot
silently route reporting data to a paid model.
"""
from __future__ import annotations

from typing import Dict, Tuple

STRATEGIST_PRIMARY = "openai/gpt-6-luna"
STRATEGIST_FALLBACK = "anthropic/claude-haiku-5.5"
OPERATOR_BRIEF_MODELS = ("nvidia/nemotron-3.5-lightning:free", "google/gemma-4-26b-a4b-it:free")
TRADE_REPORT_MODELS = ("google/gemma-4-26b-a4b-it:free", "nvidia/nemotron-3.5-lightning:free")
REPORTER_FINAL_MODELS = ("nvidia/nemotron-3-ultra-550b-a55b:free", "google/gemma-4-26b-a4b-it:free")

ROLE_MODELS: Dict[str, Tuple[str, ...]] = {
    "strategist": (STRATEGIST_PRIMARY, STRATEGIST_FALLBACK),
    "operator_ui": OPERATOR_BRIEF_MODELS,
    "reporter_intraday": OPERATOR_BRIEF_MODELS,
    "trade_report": TRADE_REPORT_MODELS,
    "reporter_final": REPORTER_FINAL_MODELS,
    "daily_report": REPORTER_FINAL_MODELS,
}


def is_reporter_role(role: str) -> bool:
    return str(role or "").strip().lower() in {
        "operator_ui", "reporter_intraday", "trade_report", "reporter_final", "daily_report"
    }


def is_allowed_model(role: str, model: str) -> bool:
    normalized_role = str(role or "").strip().lower()
    normalized_model = str(model or "").strip().lower()
    allowed = ROLE_MODELS.get(normalized_role)
    return bool(allowed and normalized_model in allowed)


def fallback_model(role: str, primary: str) -> str:
    allowed = ROLE_MODELS.get(str(role or "").strip().lower(), ())
    for model in allowed:
        if model != str(primary or "").strip().lower():
            return model
    return ""
