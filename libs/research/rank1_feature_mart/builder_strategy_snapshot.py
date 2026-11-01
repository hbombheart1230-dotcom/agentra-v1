from typing import Any, Mapping


def _strategy_snapshot(row: Mapping[str, Any], window: Mapping[str, Any]) -> dict[str, Any]:
    strategist = window.get("strategist_selection") if isinstance(window.get("strategist_selection"), Mapping) else {}
    canonical = window.get("_canonical_strategist")
    canonical = canonical if isinstance(canonical, Mapping) else {}
    policy = canonical.get("policy_selected")
    policy = policy if isinstance(policy, Mapping) else {}
    strategy_policy = policy.get("strategy_policy")
    strategy_policy = strategy_policy if isinstance(strategy_policy, Mapping) else {}
    market_policy = strategy_policy.get("market_policy")
    market_policy = market_policy if isinstance(market_policy, Mapping) else {}
    theme_policy = market_policy.get("theme_policy")
    theme_policy = theme_policy if isinstance(theme_policy, Mapping) else {}
    return {
        "scenario": str(row.get("strategist_scenario") or strategist.get("scenario") or canonical.get("market_regime") or "MISSING"),
        "playbook": str(row.get("playbook") or row.get("strategist_playbook") or strategist.get("playbook") or canonical.get("playbook") or "MISSING"),
        "market_playbook": str(canonical.get("final_playbook") or canonical.get("playbook") or strategist.get("playbook") or "MISSING"),
        "tactical_strategy": str(canonical.get("tactical_strategy") or row.get("tactic_id") or "MISSING"),
        "tactical_subtype": str(canonical.get("tactical_subtype") or "MISSING"),
        "tactic_id": str(row.get("tactic_id") or canonical.get("tactical_strategy") or "MISSING"),
        "entry_horizon": str(row.get("strategy_horizon") or canonical.get("strategy_horizon") or strategist.get("strategy_horizon") or strategist.get("horizon") or "MISSING"),
        "strategy_scores": dict(canonical.get("strategy_scores") or {}),
        "preferred_themes": [str(value) for value in theme_policy.get("preferred_themes") or []],
        "theme_strength": dict(theme_policy.get("theme_strength") or canonical.get("theme_strength") or {}),
        "canonical_evidence_status": "OBSERVED" if canonical else "MISSING",
    }
