"""RF-033 A21-1: canonical original reaction_reader (66e0cf26 / 498d4aeb) vs the A facade + 3 Owners.

The original is read offline via ``git show`` and exec'd into an isolated module (never put in
``sys.modules``). The protected Q10 collector is replaced by an in-memory stub. No network/writers.
"""
from __future__ import annotations

import copy
import hashlib
import importlib
import json
import subprocess
import sys
import types

import pytest

COMMIT = "66e0cf267090e9bde6b66fa8c70d977ed80a05f0"
PKG = "libs.reporting.baseline_samsung_hynix.forward_validation"
D = "libs/reporting/baseline_samsung_hynix/forward_validation"
ORIG_PATH = f"{D}/reaction_reader.py"
ORIG_SHA = "498d4aeb8b26291d83780966be2b11320d305b9c"
CANON_PINS = {
    f"{D}/contracts.py": "398d7953cb7cbcd5f6e6a77d4e47354b63113b0c",
    "libs/market/q10_observation_integrity.py": "04f5f400131adc0f8655a3d4ada4273e678a916c",
}
A_PINS = {  # working-tree files of the A branch
    f"{D}/reaction_reader.py": "5e363c64d584ab425af82a004f52511564b31a2b",
    f"{D}/index_timeline.py": "12bfb2e3af358b7ed822c649989b3b4258b3efa3",
    f"{D}/collector_observations.py": "b2792b51a34e4c107e809a3424d7f2a55b9ec2b1",
    f"{D}/stock_reaction.py": "e3da65e5f69b675104ef8ac5f248606f6e7ce7fd",
}
DAY = "2026-04-16"
AT = "2026-04-16T09:30:00+09:00"


def _sha(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + bytes([0]) + raw).hexdigest()


def _git_show(path: str) -> bytes:
    return subprocess.run(["git", "show", f"{COMMIT}:{path}"], check=True, capture_output=True).stdout


@pytest.fixture(scope="module")
def pair():
    try:
        orig_raw = _git_show(ORIG_PATH)
        canon = {p: _git_show(p) for p in CANON_PINS}
    except subprocess.CalledProcessError as exc:
        pytest.fail(f"BLOCKED_PIN: {exc.stderr!r}")
    assert _sha(orig_raw) == ORIG_SHA, "BLOCKED_PIN original"
    for p, raw in canon.items():
        assert _sha(raw) == CANON_PINS[p], f"BLOCKED_PIN {p}"
    for p, sha in A_PINS.items():
        with open(p, "rb") as fh:
            assert _sha(fh.read()) == sha, f"BLOCKED_PIN A {p}"
    original = types.ModuleType(f"{PKG}._original_parity_probe")
    original.__package__ = PKG
    exec(compile(orig_raw, f"<{COMMIT[:8]}:{ORIG_PATH}>", "exec"), original.__dict__)
    facade = importlib.import_module(f"{PKG}.reaction_reader")
    assert original is not facade
    return original, facade


def _macro(path, current):
    path.write_text(json.dumps({"generated_at": AT,
                                "korea_indices": {"indices": {"KOSPI": {"current": current}}}}),
                    encoding="utf-8")


def test_p1_timeline_parity(pair, tmp_path):
    original, facade = pair
    d = tmp_path / DAY
    d.mkdir()
    _macro(d / "01_macro_indicators.json", 100)
    _macro(d / "02_macro_indicators.json", 101)
    (d / "03_macro_indicators.json").write_text("{bad", encoding="utf-8")
    kw = dict(day=DAY, macro_root=tmp_path, index_name="KOSPI")
    a, b = original.load_index_timeline(**kw), facade.load_index_timeline(**kw)
    assert a == b
    assert len(a) == 1 and a[0]["close"] == 101.0
    miss = dict(kw, index_name="NOPE")
    assert original.load_index_timeline(**miss) == facade.load_index_timeline(**miss) == []


FIXTURES = {
    "missing": {"availability": "MISSING", "never_attempted": True, "indices": {}},
    "corrupt": {"availability": "CORRUPT_STATE", "actual_observed_at_kst": AT,
                "indices": {"KOSPI": {"current": 101}}},
    "available": {"availability": "AVAILABLE", "actual_observed_at_kst": AT,
                  "indices": {"KOSPI": {"current": 101, "market_observed_at": AT}}},
}


def _install_stub(monkeypatch, obs):
    st = {"obs_calls": [], "ev_calls": []}
    stub = types.ModuleType("libs.market.q10_index_observation_collector")

    def observation_for_slot(day, slot, root=None):
        st["obs_calls"].append((day, slot, root))
        return copy.deepcopy(obs)

    def _has_verification_evidence(indices, *, slot, day, observed_epoch):
        st["ev_calls"].append((slot, day, observed_epoch))
        return True

    stub.observation_for_slot = observation_for_slot
    stub._has_verification_evidence = _has_verification_evidence
    monkeypatch.setitem(sys.modules, "libs.market.q10_index_observation_collector", stub)
    return st


@pytest.mark.parametrize("name", sorted(FIXTURES))
def test_p2_collector_raw_row_parity(pair, monkeypatch, name):
    original, facade = pair
    kw = dict(day=DAY, index_name="KOSPI", slot="09:30", root=None)
    st_o = _install_stub(monkeypatch, FIXTURES[name])
    out_o = original._collector_raw_row(**kw)
    st_a = _install_stub(monkeypatch, FIXTURES[name])
    out_a = facade._collector_raw_row(**kw)
    assert out_o == out_a
    assert st_o == st_a
    if name == "missing":
        assert out_a is None
    elif name == "corrupt":
        assert out_a["integrity_failure"] is True and out_a["collector_status"] == "CORRUPT_STATE"
    else:
        assert out_a["close"] == 101.0 and out_a["source"] == "q10_index_observation_collector"


def test_p3_stock_reaction_parity(pair):
    original, facade = pair
    ep = original._checkpoint_epoch
    rows = [{"ts": ep(DAY, "09:00"), "open": 100.0, "close": 100.0, "high": 101.0, "low": 99.0, "volume": 10},
            {"ts": ep(DAY, "09:30"), "open": 101.0, "close": 102.0, "high": 103.0, "low": 100.0, "volume": 10}]
    target = {"symbol": "X"}
    snap = copy.deepcopy((rows, target))

    def override(label):
        return ({"integrity_failure": True, "collector_status": "CORRUPT_STATE", "reason": "fixture"}
                if label == "CLOSE" else None)

    kw = dict(day=DAY, target=target, rows=rows, previous_close=100.0, collector_override=override)
    a = original._stock_reaction(**kw)
    assert (rows, target) == snap
    b = facade._stock_reaction(**kw)
    assert (rows, target) == snap
    assert a == b
    assert b["points"]["CLOSE"]["status"] == "PENDING" and b["points"]["CLOSE"]["integrity_failure"] is True
    assert b["points"]["CLOSE"]["integrity_reason"] == "fixture"
