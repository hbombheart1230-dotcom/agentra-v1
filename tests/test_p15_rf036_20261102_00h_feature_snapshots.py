import ast
import copy
import subprocess
import types
from pathlib import Path
from typing import Any, Mapping

import pytest

from libs.research.rank1_feature_mart import builder


_SHA = "0ba22527e5e07f770e2e21e9841921ceaafd9328"
_PATH = "libs/research/rank1_feature_mart/builder.py"
_BLOB = "cc332d9c5811690d4d5117f52842eeb001fa9d8d"


def _originals(number):
    assert subprocess.check_output(["git", "rev-parse", f"{_SHA}:{_PATH}"], text=True).strip() == _BLOB
    raw = subprocess.check_output(["git", "show", f"{_SHA}:{_PATH}"], text=True)
    nodes = [node for node in ast.parse(raw).body if isinstance(node, ast.FunctionDef) and node.name in {"_market_snapshot", "_strategy_snapshot"}]
    module = types.ModuleType("canonical_rank1_feature_snapshots")
    module.__dict__.update({"Any": Any, "Mapping": Mapping, "_number": number})
    exec(compile(ast.fix_missing_locations(ast.Module(body=nodes, type_ignores=[])), "canonical_rank1_feature_snapshots", "exec"), module.__dict__)
    return module


def _guard_effects(monkeypatch):
    monkeypatch.setattr(subprocess, "run", lambda *_a, **_kw: (_ for _ in ()).throw(AssertionError("subprocess invoked")))
    monkeypatch.setattr(subprocess, "Popen", lambda *_a, **_kw: (_ for _ in ()).throw(AssertionError("Popen invoked")))
    monkeypatch.setattr(Path, "mkdir", lambda *_a, **_kw: (_ for _ in ()).throw(AssertionError("mkdir invoked")))
    monkeypatch.setattr(Path, "write_text", lambda *_a, **_kw: (_ for _ in ()).throw(AssertionError("write invoked")))


def test_market_historical_parity_and_input_immutability(monkeypatch):
    original = _originals(builder._number)
    row = {"kospi_pct": "1.2", "kosdaq_pct": "0.4", "nasdaq_pct": "-0.1", "vix_level": "18", "engine_regime": "RISK_ON"}
    before = copy.deepcopy(row)
    _guard_effects(monkeypatch)
    assert builder._market_snapshot(row, prospective=False) == original._market_snapshot(row, prospective=False)
    assert row == before


def test_market_prospective_nested_inverse_alignment_parity(monkeypatch):
    original = _originals(builder._number)
    row = {"opening_observability": {"market_snapshot": {"kospi_pct": "-1.5", "kosdaq_pct": "0.2", "snapshot_epoch": "10", "snapshot_age_sec": 0}, "asset_observation": {"exposure_direction": "INVERSE", "asset_class": "ETF"}}}
    _guard_effects(monkeypatch)
    actual = builder._market_snapshot(row, prospective=True)
    assert actual == original._market_snapshot(row, prospective=True)
    assert actual["exposure_alignment"] is True and actual["snapshot_epoch"] == 10


@pytest.mark.parametrize("market_return", [0, None])
def test_market_zero_none_and_use_time_number_monkeypatch(monkeypatch, market_return):
    calls = []
    def custom_number(value):
        calls.append(value)
        return None if value is None else float(value)
    original = _originals(custom_number)
    row = {"market_snapshot": {"kospi_pct": market_return}, "opening_observability": {"asset_observation": {"exposure_direction": "INVERSE"}}}
    monkeypatch.setattr(builder, "_number", custom_number)
    _guard_effects(monkeypatch)
    actual = builder._market_snapshot(row, prospective=True)
    assert actual == original._market_snapshot(row, prospective=True)
    assert actual["exposure_alignment"] is None and calls


def test_strategy_empty_default_parity(monkeypatch):
    original = _originals(builder._number)
    row, window = {}, {}
    _guard_effects(monkeypatch)
    assert builder._strategy_snapshot(row, window) == original._strategy_snapshot(row, window)


def test_strategy_canonical_policy_precedence_and_copies(monkeypatch):
    original = _originals(builder._number)
    row = {"strategist_scenario": "ROW", "playbook": "ROW_PLAY", "tactic_id": "ROW_TAC", "strategy_horizon": "ROW_H"}
    window = {"strategist_selection": {"scenario": "STRAT", "playbook": "STRAT_PLAY", "horizon": "STRAT_H"}, "_canonical_strategist": {"market_regime": "CANON", "final_playbook": "FINAL", "playbook": "CANON_PLAY", "tactical_strategy": "CANON_TAC", "tactical_subtype": "SUB", "strategy_horizon": "CANON_H", "strategy_scores": {"x": 1}, "theme_strength": {"fallback": 1}, "policy_selected": {"strategy_policy": {"market_policy": {"theme_policy": {"preferred_themes": ["AI", 7], "theme_strength": {"AI": 3}}}}}}}
    before = copy.deepcopy((row, window))
    _guard_effects(monkeypatch)
    actual = builder._strategy_snapshot(row, window)
    assert actual == original._strategy_snapshot(row, window)
    assert actual["playbook"] == "ROW_PLAY" and actual["market_playbook"] == "FINAL"
    assert actual["preferred_themes"] == ["AI", "7"] and actual["theme_strength"] == {"AI": 3}
    assert (row, window) == before


def test_wrappers_are_thin_and_each_owner_has_the_decision_body():
    tree = ast.parse(Path(builder.__file__).read_text(encoding="utf-8"))
    funcs = {node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)}
    for name in ("_market_snapshot", "_strategy_snapshot"):
        assert not any(isinstance(node, ast.Dict) for node in ast.walk(funcs[name]))
        assert sum(isinstance(node, ast.Return) for node in ast.walk(funcs[name])) == 1
    for filename, name in (("builder_market_snapshot.py", "_market_snapshot"), ("builder_strategy_snapshot.py", "_strategy_snapshot")):
        owner = ast.parse((Path(builder.__file__).parent / filename).read_text(encoding="utf-8"))
        function = next(node for node in owner.body if isinstance(node, ast.FunctionDef) and node.name == name)
        assert any(isinstance(node, ast.Dict) for node in ast.walk(function))
