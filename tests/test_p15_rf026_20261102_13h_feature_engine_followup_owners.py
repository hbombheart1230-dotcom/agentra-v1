from libs.runtime import feature_engine as subject


def test_b34_owner_facades_preserve_feature_math(monkeypatch):
    assert subject._pct_change([1.0, 2.0], 1) == 1.0
    assert subject._pct_change([0.0, 2.0], 1) is None
    assert subject._gap_pct([{"close": 2}, {"open": 3}]) == 0.5
    assert subject._rolling_drawdown([2.0, 4.0, 3.0], 2) == -0.25
    assert subject.classify_regime(ma20_gap=0.02, volatility20=0.04) == "high_volatility"
    assert subject._signal_score(ma20_gap=0.1, rsi14=50.0) == 0.5
    assert subject._adx([1.0, 2.0, 3.0], [0.0, 1.0, 2.0], [0.5, 1.5, 2.5], 2) == 100.0
    monkeypatch.setattr(subject, "_to_float", lambda value: 2.0)
    assert subject._vwap_distance([{"vwap": "ignored"}], [4.0], [1.0]) == 1.0


def test_build_feature_row_owner_preserves_key_order_and_facade_helpers(monkeypatch):
    monkeypatch.setattr(subject, "_series", lambda candles, key: [1.0, 2.0] if key == "close" else [1.0, 2.0])
    row = subject.build_feature_row([{"close": 1}, {"close": 2}])
    assert list(row)[:3] == ["close_last", "rsi14", "ma20"]
    assert row["close_last"] == 2.0
