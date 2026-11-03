from libs.llm.llm_router import LLMRouter
from libs.llm.model_catalog import resolve_model_profile


class _Client:
    def __init__(self): self.calls = []
    def chat(self, **payload): self.calls.append(payload); return "ok"


def test_profiles_use_verified_primary_and_fallback_models():
    strategist = resolve_model_profile("balanced")
    reporter = resolve_model_profile("fast_free")
    final = resolve_model_profile("strong_reasoning")
    assert strategist["models"] == ["openai/gpt-6-luna", "anthropic/claude-haiku-5.5"]
    assert reporter["models"] == ["nvidia/nemotron-3.5-lightning:free", "google/gemma-4-26b-a4b-it:free"]
    assert final["models"] == ["nvidia/nemotron-3-ultra-550b-a55b:free", "google/gemma-4-26b-a4b-it:free"]


def test_strategist_policy_can_select_haiku_fallback():
    route = LLMRouter(None).resolve("strategist", policy={"model": "anthropic/claude-haiku-5.5"})
    assert route.model == "anthropic/claude-haiku-5.5"


def test_reporter_rejects_paid_or_unknown_policy_and_never_calls_client():
    client = _Client()
    router = LLMRouter(client)
    assert router.resolve("trade_report", policy={"model": "minimax/minimax-m2.5"}).model == ""
    assert router.chat("trade_report", [{"role": "user", "content": "x"}], policy={"model": "minimax/minimax-m2.5"}) == ""
    assert client.calls == []


def test_reporter_defaults_are_free_and_valid():
    assert LLMRouter(None).resolve("operator_ui").model == "nvidia/nemotron-3.5-lightning:free"
    assert LLMRouter(None).resolve("trade_report").model == "google/gemma-4-26b-a4b-it:free"
    assert LLMRouter(None).resolve("reporter_final").model == "nvidia/nemotron-3-ultra-550b-a55b:free"
