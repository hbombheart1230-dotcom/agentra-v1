from __future__ import annotations

from pathlib import Path

from libs.llm.model_catalog_store import (
    build_model_cards_payload,
    get_model_card,
    list_models_by_tag,
    load_model_cards,
    load_openrouter_models,
    save_model_cards,
    save_openrouter_models,
    sync_openrouter_model_catalog,
)


def _sample_openrouter_payload() -> dict:
    return {
        "fetched_at": "2026-04-09T06:00:00+00:00",
        "source": "openrouter",
        "source_url": "https://openrouter.ai/api/v1/models",
        "fetch_status": "ok",
        "model_count": 3,
        "data": [
            {
                "id": "minimax/minimax-m2.5",
                "name": "MiniMax M2.5",
                "context_length": 1_000_000,
                "pricing": {"prompt": "0", "completion": "0"},
                "supported_parameters": ["response_format", "structured_outputs", "temperature", "max_tokens"],
            },
            {
                "id": "deepseek/deepseek-v3.2",
                "name": "DeepSeek V3.2",
                "context_length": 131_072,
                "pricing": {"prompt": "0.000001", "completion": "0.000004"},
                "supported_parameters": ["response_format", "temperature", "max_tokens"],
            },
            {
                "id": "moonshotai/kimi-k2.5",
                "name": "Kimi K2.5",
                "context_length": 262_144,
                "pricing": {"prompt": "0.000004", "completion": "0.000012"},
                "supported_parameters": ["response_format", "structured_outputs", "temperature", "max_tokens"],
            },
        ],
    }


def test_build_model_cards_payload_generates_expected_fields() -> None:
    payload = build_model_cards_payload(_sample_openrouter_payload())

    assert payload["card_count"] == 3
    first = get_model_card("minimax/minimax-m2.5", cards_payload=payload)
    assert first["provider"] == "minimax"
    assert first["context_window"] == 1_000_000
    assert first["cost_tier"] == "free"
    assert first["latency_tier"] == "fast"
    assert "recommended_roles" in first
    assert "strengths" in first
    assert "weaknesses" in first
    assert isinstance(first["recommended_roles"], list)
    assert isinstance(first["strengths"], list)
    assert isinstance(first["weaknesses"], list)
    assert isinstance(first["json_stability_note"], str)
    assert isinstance(first["latency_note"], str)
    assert isinstance(first["cost_note"], str)
    assert isinstance(first["long_context_note"], str)


def test_manual_model_cards_do_not_prescribe_removed_operational_models() -> None:
    payload = build_model_cards_payload(_sample_openrouter_payload())
    for model_id in ("minimax/minimax-m2.5", "deepseek/deepseek-v3.2", "moonshotai/kimi-k2.5"):
        assert get_model_card(model_id, cards_payload=payload)["recommended_roles"] == []


def test_list_models_by_tag_filters_expected_models() -> None:
    payload = build_model_cards_payload(_sample_openrouter_payload())

    reasoning = list_models_by_tag("reasoning", cards_payload=payload)
    model_ids = {row["model_id"] for row in reasoning}

    assert "moonshotai/kimi-k2.5" in model_ids
    assert "minimax/minimax-m2.5" not in model_ids


def test_save_and_load_catalog_files_round_trip(tmp_path: Path) -> None:
    raw_path = tmp_path / "openrouter_models.json"
    cards_path = tmp_path / "model_cards.json"
    raw_payload = _sample_openrouter_payload()
    cards_payload = build_model_cards_payload(raw_payload)

    save_openrouter_models(raw_payload, raw_path)
    save_model_cards(cards_payload, cards_path)

    assert load_openrouter_models(raw_path)["model_count"] == 3
    loaded_cards = load_model_cards(cards_path)
    assert loaded_cards["card_count"] == 3
    assert get_model_card("deepseek/deepseek-v3.2", cards_payload=loaded_cards)["provider"] == "deepseek"


def test_sync_openrouter_model_catalog_uses_cached_fallback(monkeypatch, tmp_path: Path) -> None:
    raw_path = tmp_path / "openrouter_models.json"
    save_openrouter_models(_sample_openrouter_payload(), raw_path)

    def _boom(*args, **kwargs):
        raise RuntimeError("network down")

    monkeypatch.setattr("libs.llm.model_catalog_store.fetch_openrouter_models", _boom)

    result = sync_openrouter_model_catalog(catalog_dir=tmp_path, allow_cached_fallback=True)

    assert result["fetch_source"] == "cached_fallback"
    assert Path(result["openrouter_models_path"]).exists()
    assert Path(result["model_cards_path"]).exists()
    cards = load_model_cards(result["model_cards_path"])
    assert cards["card_count"] == 3
