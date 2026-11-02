from libs.runtime import intraday_monitor_signals as signals


def test_numeric_owner_facades_keep_conversion_and_clamp_contracts():
    assert signals._to_float("1.25") == 1.25
    assert signals._to_float("bad", 2.5) == 2.5
    assert signals._to_int("2.9") == 2
    assert signals._to_int(None, 7) == 7
    assert signals._clamp_score(-2) == 0.0
    assert signals._clamp_score(2) == 1.0
    assert signals._clamp_score("bad") == 0.0


def test_scoring_fields_owner_preserves_dict_identity_and_helper_patch():
    out = {}
    original = signals._to_float
    signals._to_float = lambda value: 1.5
    try:
        result = signals._apply_monitor_scoring_fields(
            out, scoring_settings={"entry_threshold": 3, "scoring_mode": "x"},
            hard_filter_passed=True, hard_filter_fail_reasons=["", "reason"],
            score_breakdown={"a": "ignored", "b": "ignored"},
        )
    finally:
        signals._to_float = original
    assert result is out
    assert out["total_score"] == 3.0
    assert out["hard_filter_fail_reasons"] == ["reason"]
    assert out["scoring_entry_decision"] == "WAIT"
