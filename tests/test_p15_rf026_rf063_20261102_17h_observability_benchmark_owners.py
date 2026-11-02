from __future__ import annotations


def test_resolve_check_state_owner_preserves_precedence_and_status_fallback():
    from libs.runtime import decision_observability as obs

    assert obs._resolve_check_state(
        name="volume_ok",
        metrics={"volume_ok": False},
        passed_checks=["volume_ok"],
        failed_checks=[],
        check_status={"required": [{"name": "volume_ok", "status": "pass"}]},
    ) is False
    assert obs._resolve_check_state(
        name="rebound_ok",
        metrics={},
        passed_checks=[],
        failed_checks=[],
        check_status={"required": [{"name": "rebound_ok", "status": "unknown", "actual_state": "marginal"}]},
    ) == "marginal"
    assert obs._resolve_check_state(
        name="missing",
        metrics={}, passed_checks=[], failed_checks=[], check_status={},
    ) is None


def test_resolve_structure_state_owner_preserves_first_match_precedence():
    from libs.runtime import decision_observability as obs

    assert obs._resolve_structure_state(
        {"structure": {"structure_hh_hl": "HH_HL"}, "structure_hh_hl": "direct"},
        {"required": [{"name": "structure_hh_hl", "actual_state": "status"}]},
    ) == "HH_HL"
    assert obs._resolve_structure_state(
        {"structure": {}, "structure_hh_hl": "direct"},
        {"required": [{"name": "structure_hh_hl", "actual_state": "status"}]},
    ) == "direct"


def test_monitor_no_trade_surface_owner_is_read_only_projection():
    from libs.runtime import decision_observability as obs

    result = obs.build_monitor_no_trade_surface(
        {"evaluated": False, "triggered": False, "reason": "volume_confirmation_missing"},
        final_decision="WAIT",
        buy_submitted=False,
        guard_blocked=True,
        guard_reason="synthetic_guard_observation",
    )
    assert result["schema_version"] == "monitor_no_trade_surface.v1"
    assert result["decision_outcome"] == "WAIT"
    assert result["no_trade_stage"] == "guard_block"
    assert result["guard_intervened"] is True
    assert result["no_trade_reason_code"] == "synthetic_guard_observation"
    assert result["dominant_blocker"] == "synthetic_guard_observation"


def test_entry_blocker_surface_owner_preserves_metrics_and_check_status():
    from libs.runtime import decision_observability as obs

    result = obs.build_entry_blocker_surface(
        {
            "reason": "volume_confirmation_missing",
            "metrics": {"confidence_score": 0.89, "confidence_threshold": 0.90, "volume_ok": False},
            "passed_checks": ["rebound_ok"],
            "primary_failure_axis": "volume_confirmation_missing",
        },
        final_decision="WAIT",
        entry_blockers=["volume_confirmation_missing"],
        buy_blocked_open_position=True,
        open_position_count=2,
    )
    assert result["schema_version"] == "entry_blocker_surface.v1"
    assert result["final_decision"] == "WAIT"
    assert result["volume_ok"] is False
    assert result["rebound_ok"] is True
    assert result["open_position_blocked"] is True
    assert result["open_position_count"] == 2
    assert result["confidence_near_miss"] is False


def test_scanner_monitor_handoff_owner_preserves_rank_order_and_projection():
    from libs.runtime import decision_observability as obs

    result = obs.build_scanner_monitor_handoff_surface(
        selected={"symbol": " aapl ", "score_total": 0.9, "score_breakdown": {"trend": 0.4}},
        ranked_candidates=[
            {"symbol": "AAPL", "score_total": 0.9},
            {"symbol": "MSFT", "score_total": 0.8},
        ],
        scanner_output={},
        final_decision="WAIT",
        no_trade_surface={"no_trade_reason_code": "guard_block", "no_trade_stage": "guard_block"},
        entry_info={"policy_interpretation": {"entry_style": "pullback"}},
    )
    assert result["schema_version"] == "scanner_monitor_handoff.v1"
    assert result["scanner_selected_symbol"] == "AAPL"
    assert result["scanner_rank"] == 1
    assert [row["symbol"] for row in result["scanner_top_candidates"]] == ["AAPL", "MSFT"]
    assert result["scanner_vs_monitor_alignment"] == "guard_block"
    assert result["monitor_rejection_after_top_pick"] is True
    assert result["entry_style"] == "pullback"


def test_strategist_policy_resolution_owner_preserves_fallback_projection():
    from libs.runtime import decision_observability as obs

    result = obs.build_strategist_policy_resolution_surface(
        strategist_output={
            "policy_fallback_used": True,
            "policy_source": "synthetic_safe_default",
            "monitor_entry_policy": {"schema_version": "policy.v2", "policy_id": "p-7"},
        },
        strategist_llm={"status": "error", "error": "timeout", "latency_ms": "12", "prompt_ref": "prompts/v1.json"},
        commander_context={"strategist_cache_preferred": False},
    )
    assert result["schema_version"] == "strategist_policy_resolution.v1"
    assert result["llm_attempted"] is True
    assert result["llm_ok"] is False
    assert result["llm_error_type"] == "timeout"
    assert result["fallback_used"] is True
    assert result["fallback_source"] == "synthetic_safe_default"
    assert result["effective_prompt_version"] == "v1.json"
    assert result["effective_schema_version"] == "policy.v2"
    assert result["strategy_generation_mode"] == "fallback"


def test_commander_route_observability_owner_does_not_invoke_strategist():
    from libs.runtime import decision_observability as obs

    result = obs.build_commander_route_observability_surface(
        selected_route="monitor_only",
        route_reason="synthetic read-only route",
        commander_decision={"strategist_invocation": "SKIP"},
        runtime_fast_path={"cache_age_sec": None},
        resilience={"incident_count": "2", "degrade_mode": True, "last_error_type": "timeout"},
        runtime_status="degraded",
        runtime_transition="cooldown",
    )
    assert result["schema_version"] == "commander_route_observability.v1"
    assert result["route_selected"] == "monitor_only"
    assert result["strategist_call_decision"] == "skip"
    assert result["strategy_generation_mode"] == "default_safe"
    assert result["resilience_state"]["incident_count"] == 2
    assert result["resilience_state"]["degrade_mode"] is True
    assert result["monitor_only_reason"] == "synthetic read-only route"


def test_benchmark_peak_ws_owner_uses_only_fake_os_facilities(monkeypatch):
    import ctypes

    from scripts.diagnostics import benchmark_operator_visibility_memory as bench

    monkeypatch.setattr(bench.platform, "system", lambda: "Linux")
    assert bench._self_peak_ws_mb() is None

    monkeypatch.setattr(bench.platform, "system", lambda: "Windows")
    observed = {"ok": True}

    class FakeFunction:
        def __init__(self, call):
            self.call = call
            self.restype = None
            self.argtypes = None

        def __call__(self, *args):
            return self.call(*args)

    class FakeLibrary:
        def __init__(self, name):
            if name == "kernel32":
                self.GetCurrentProcess = FakeFunction(lambda: 123)
            else:
                def get_process_memory_info(_handle, counters, _size):
                    counters._obj.PeakWorkingSetSize = 3 * 1024 * 1024
                    return observed["ok"]
                self.GetProcessMemoryInfo = FakeFunction(get_process_memory_info)

    monkeypatch.setattr(ctypes, "WinDLL", lambda name, **_kwargs: FakeLibrary(name), raising=False)
    assert bench._self_peak_ws_mb() == 3.0
    observed["ok"] = False
    assert bench._self_peak_ws_mb() is None
