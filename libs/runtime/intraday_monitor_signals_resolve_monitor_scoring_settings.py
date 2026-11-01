from __future__ import annotations

from typing import Any, Dict, List, Mapping, Sequence


def _resolve_monitor_scoring_settings(scoring: Mapping[str, Any] | None = None, *, facade: Any):
    raw = dict(scoring or {}) if isinstance(scoring, Mapping) else {}
    enabled = facade._env_trueish(raw.get("enabled"), False)
    shadow_mode = facade._env_trueish(raw.get("shadow_mode"), False)
    threshold = facade._to_float(raw.get("threshold") if raw.get("threshold") not in (None, "") else raw.get("entry_threshold"), 3.0)
    threshold = float(threshold if threshold > 0.0 else 3.0)
    if enabled:
        mode = "enabled"
    elif shadow_mode:
        mode = "shadow"
    else:
        mode = "disabled"
    return {
        "enabled": bool(enabled),
        "shadow_mode": bool(shadow_mode),
        "entry_threshold": threshold,
        "scoring_mode": mode,
    }
