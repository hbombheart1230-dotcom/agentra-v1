from __future__ import annotations

from typing import Any


def normalize_openrouter_model_name(model: Any) -> str:
    """Normalize OpenRouter aliases while preserving direct provider/model names.

    Examples:
    - auto -> openrouter/auto
    - free -> openrouter/free
    - openrouter/free -> openrouter/free
    - provider/model -> provider/model
    """
    raw = str(model or "").strip()
    lowered = raw.lower()
    if lowered == "auto":
        return "openrouter/auto"
    if lowered == "free":
        return "openrouter/free"
    return raw

