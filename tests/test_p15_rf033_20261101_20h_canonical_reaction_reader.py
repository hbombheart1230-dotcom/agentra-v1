"""RF-033 A20-1: canonical ``reaction_reader.py`` (integration 8eff2d9e) probed offline in isolation.

The canonical bytes are read with ``git show`` and exec'd into an isolated module that is never
placed in ``sys.modules`` (the real, A-facade ``reaction_reader`` is untouched). The protected Q10
collector is replaced by a stub module; no network, no writers.
"""
from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
import types

import pytest

COMMIT = "8eff2d9e2d5b40ee2049579941597c95890d1ad1"
PKG = "libs.reporting.baseline_samsung_hynix.forward_validation"
PATH = "libs/reporting/baseline_samsung_hynix/forward_validation/reaction_reader.py"
PINS = {
    PATH: "498d4aeb8b26291d83780966be2b11320d305b9c",
    f"{PKG.replace('.', '/')}/contracts.py": "398d7953cb7cbcd5f6e6a77d4e47354b63113b0c",
    "libs/market/q10_observation_integrity.py": "04f5f400131adc0f8655a3d4ada4273e678a916c",
}
DAY = "2026-04-16"


def _git_show(path: str) -> bytes:
    return subprocess.run(["git", "show", f"{COMMIT}:{path}"], check=True, capture_output=True).stdout


def _blob_sha(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + bytes([0]) + raw).hexdigest()


@pytest.fixture(scope="module")
def canon():
    try:
        pins = {p: _git_show(p) for p in PINS}
    except subprocess.CalledProcessError as exc:  # commit object missing locally
        pytest.fail(f"BLOCKED_PIN: cannot read canonical objects: {exc.stderr!r}")
    for p, raw in pins.items():
        assert _blob_sha(raw) == PINS[p], f"BLOCKED_DEPENDENCY: {p}"
    raw = pins[PATH]
    module = types.ModuleType(f"{PKG}._canonical_reaction_probe")
    module.__package__ = PKG
    module.__file__ = f"<{COMMIT[:8]}:{PATH}>"
    exec(compile(raw, module.__file__, "exec"), module.__dict__)
    assert sys.modules.get(f"{PKG}.reaction_reader") is not module
    return module


def _macro(path, current):
    path.write_text(json.dumps({"generated_at": "2026-04-16T09:30:00+09:00",
                                "korea_indices": {"indices": {"KOSPI": {"current": current}}}}),
                    encoding="utf-8")


def test_t1_load_index_timeline(canon, tmp_path):
    d = tmp_path / DAY
    d.mkdir()
    _macro(d / "01_macro_indicators.json", 100)
    _macro(d / "02_macro_indicators.json", 101)
    (d / "03_macro_indicators.json").write_text("{bad", encoding="utf-8")
    rows = canon.load_index_timeline(day=DAY, macro_root=tmp_path, index_name="KOSPI")
    assert len(rows) == 1 and rows[0]["close"] == 101.0
    assert str(rows[0]["source_path"]).startswith(str(tmp_path))
    assert canon.load_index_timeline(day=DAY, macro_root=tmp_path, index_name="NOPE") == []


@pytest.fixture
def stub_collector(monkeypatch):
    state = {"obs": None, "evidence_calls": [], "evidence": True, "obs_calls": []}
    stub = types.ModuleType("libs.market.q10_index_observation_collector")

    def observation_for_slot(day, slot, root=None):
        state["obs_calls"].append((day, slot, root))
        return copy.deepcopy(state["obs"])

    def _has_verification_evidence(indices, *, slot, day, observed_epoch):
        state["evidence_calls"].append((slot, day, observed_epoch))
        return state["evidence"]

    stub.observation_for_slot = observation_for_slot
    stub._has_verification_evidence = _has_verification_evidence
    monkeypatch.setitem(sys.modules, "libs.market.q10_index_observation_collector", stub)
    return state


def test_t2_collector_raw_row_tristate(canon, stub_collector):
    call = lambda: canon._collector_raw_row(day=DAY, index_name="KOSPI", slot="09:30", root=None)  # noqa: E731
    at = "2026-04-16T09:30:00+09:00"

    stub_collector["obs"] = {"availability": "MISSING", "never_attempted": True, "indices": {}}
    assert call() is None

    stub_collector["obs"] = {"availability": "CORRUPT_STATE", "actual_observed_at_kst": at,
                             "indices": {"KOSPI": {"current": 101}}}
    bad = call()
    assert bad["integrity_failure"] is True and bad["collector_status"] == "CORRUPT_STATE"

    stub_collector["obs"] = {"availability": "AVAILABLE", "actual_observed_at_kst": at,
                             "indices": {"KOSPI": {"current": 101, "market_observed_at": at}}}
    good = call()
    assert good["close"] == 101.0 and good["source"] == "q10_index_observation_collector"
    assert len(stub_collector["evidence_calls"]) == 1
    assert len(stub_collector["obs_calls"]) == 3


def test_t3_stock_reaction_close_integrity_failure(canon):
    ep = canon._checkpoint_epoch
    rows = [{"ts": ep(DAY, "09:00"), "open": 100.0, "close": 100.0, "high": 101.0, "low": 99.0, "volume": 10}]
    target = {"symbol": "X"}
    snap = copy.deepcopy((rows, target))

    def override(label):
        if label == "CLOSE":
            return {"integrity_failure": True, "collector_status": "CORRUPT_STATE", "reason": "fixture"}
        return None

    out = canon._stock_reaction(day=DAY, target=target, rows=rows, previous_close=100.0,
                                collector_override=override)
    close = out["points"]["CLOSE"]
    assert close["status"] == "PENDING" and close["integrity_failure"] is True
    assert close["integrity_reason"] == "fixture" and close["collector_status"] == "CORRUPT_STATE"
    assert close["price"] is None
    assert (rows, target) == snap
