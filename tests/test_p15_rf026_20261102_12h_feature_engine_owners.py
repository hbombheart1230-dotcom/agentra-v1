import math

from libs.runtime import feature_engine as subject


def test_feature_engine_owner_moves_preserve_numeric_contracts(monkeypatch):
    assert subject._to_float(None) is None
    assert subject._to_float("2.5") == 2.5
    assert subject._series([{"x": "1"}, {"x": None}, {"x": 3}], "x") == [1.0, 3.0]
    assert subject._sma([1.0, 2.0, 3.0], 2) == 2.5
    assert subject._sma([], 1) is None
    monkeypatch.setattr(subject, "sqrt", lambda value: 99.0)
    assert subject._std([1.0, 3.0]) == 99.0
    assert subject._median([3.0, 1.0, 2.0]) == 2.0
    assert subject._median([4.0, 2.0]) == 3.0
    assert subject._rsi([1.0, 2.0], 1) == 100.0
    assert subject._atr([3.0, 5.0], [1.0, 2.0], [2.0, 4.0], 1) == 3.0
    assert subject._pct_returns([1.0, 0.0, 2.0], 2) == [-1.0]
