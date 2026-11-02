from libs.runtime import intraday_monitor_signals as signals


def test_numeric_owner_facades_keep_conversion_and_clamp_contracts():
    assert signals._to_float("1.25") == 1.25
    assert signals._to_float("bad", 2.5) == 2.5
    assert signals._to_int("2.9") == 2
    assert signals._to_int(None, 7) == 7
    assert signals._clamp_score(-2) == 0.0
    assert signals._clamp_score(2) == 1.0
    assert signals._clamp_score("bad") == 0.0
