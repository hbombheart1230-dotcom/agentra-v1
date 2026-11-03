from __future__ import annotations

import pytest

from libs.llm.llm_router import LLMRouter
from libs.llm.model_catalog import resolve_model_profile
from libs.llm.model_policy import (
    OPERATOR_BRIEF_MODELS,
    REPORTER_FINAL_MODELS,
    STRATEGIST_FALLBACK,
    STRATEGIST_PRIMARY,
    TRADE_REPORT_MODELS,
)


class _Client:
    def __init__(self, failures: int = 0):
        self.failures = failures
        self.payloads: list[dict] = []

    def chat_completions(self, payload):
        self.payloads.append(dict(payload))
        if len(self.payloads) <= self.failures:
            raise TimeoutError("timeout")
        return {"choices": [{"message": {"content": "{}"}}]}

    @staticmethod
    def extract_text(_response):
        return "{}"


def test_primary_and_fallback_profiles_are_verified_models():
    assert resolve_model_profile("balanced")["models"] == [STRATEGIST_PRIMARY, STRATEGIST_FALLBACK]
    assert resolve_model_profile("fast_free")["models"] == list(OPERATOR_BRIEF_MODELS)
    assert resolve_model_profile("trade_report_free")["models"] == list(TRADE_REPORT_MODELS)
    assert resolve_model_profile("strong_reasoning")["models"] == list(REPORTER_FINAL_MODELS)


def test_strategist_primary_route_is_luna():
    assert LLMRouter(None).resolve("strategist").model == STRATEGIST_PRIMARY


@pytest.mark.parametrize(
    ("role", "primary", "fallback"),
    [
        ("operator_ui", *OPERATOR_BRIEF_MODELS),
        ("trade_report", *TRADE_REPORT_MODELS),
        ("reporter_final", *REPORTER_FINAL_MODELS),
    ],
)
def test_reporter_primary_failure_uses_only_free_fallback(role, primary, fallback):
    client = _Client(failures=1)
    assert LLMRouter(client).chat(role, [{"role": "user", "content": "x"}], policy={"model": primary}) == "{}"
    assert [p["model"] for p in client.payloads] == [primary, fallback]
    assert all(p["model"].endswith(":free") for p in client.payloads)


def test_paid_reporter_override_is_fail_closed():
    with pytest.raises(ValueError, match="reporter_model_not_allowed"):
        LLMRouter(None).resolve("trade_report", policy={"model": "openai/gpt-6-luna"})


def test_invalid_reporter_model_does_not_fall_back_to_paid_default():
    with pytest.raises(ValueError, match="reporter_model_not_allowed"):
        LLMRouter(None).resolve("reporter_final", policy={"model": "minimax/minimax-m2.5"})
