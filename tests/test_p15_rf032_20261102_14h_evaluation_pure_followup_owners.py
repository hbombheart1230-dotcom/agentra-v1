"""RF-032 A38-1..8: eight evaluation bodies across six modules, original vs thin wrappers + Owners.

Pure/fake only; no UEF/validation-id writer is touched. Originals: A preimage afd8becd (counterfactuals 8429cf73,
daily_scorecard 9c09b971, artifact_inventory 8cf0a236, attribution_score_v0 27fa361d, attribution_score_window
fce6c31e, horizon_alignment c41a0b65); canonical 650ba629 has the same blobs. AST-extracted and compiled in a copy
of the live namespace; dependency overrides apply to both sides. JSON readers use fake path objects (``read_text``)
and a fake ``glob`` root; no real file access, sockets, subprocess or writes.
"""
from __future__ import annotations

import ast
import builtins
import copy
import hashlib
import importlib
import inspect
import json as _json
import socket
import subprocess
from pathlib import Path

import pytest

A_PRE = "afd8becdc6af23e10cfd0abc3bf92efa01727791"
CANON = "650ba629cabc723bdc1e60389eb61888a4ac2b72"
EV = "libs/reporting/evaluation/"
FILES = {
    "cf": (EV + "counterfactuals.py", "8429cf73588fda3cbf200aaa5c207e30a4868ba3", "counterfactuals", ["build_selection_attribution"]),
    "ds": (EV + "daily_scorecard.py", "9c09b97144ce17aeb71e56312265a11075913a1a", "daily_scorecard", ["build_daily_scorecard"]),
    "inv": (EV + "artifact_inventory.py", "8cf0a23641d9cf3c133a98135f5283f4d40c2e64", "artifact_inventory", ["read_json"]),
    "v0": (EV + "attribution_score_v0.py", "27fa361dc1da696a0dae801d1dabb75446856b74", "attribution_score_v0", ["_ledger_day_record", "_read_json"]),
    "win": (EV + "attribution_score_window.py", "fce6c31ec4461454e857573c0c2b0a60f2086ce7", "attribution_score_window", ["_read_json"]),
    "ha": (EV + "horizon_alignment.py", "c41a0b655071a7e14b43305ddd9c26b1114bf685", "horizon_alignment", ["_group_key", "_profit_factor"]),
}
MODS = {k: importlib.import_module(f"libs.reporting.evaluation.{v[2]}") for k, v in FILES.items()}
CASES = [(k, n) for k, v in FILES.items() for n in v[3]]
OWNERS = {(k, n): importlib.import_module(f"libs.reporting.evaluation.{FILES[k][2]}_{n.lstrip('_')}") for k, n in CASES}
NAN, INF = float("nan"), float("inf")


def _sha(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + bytes([0]) + raw).hexdigest()


@pytest.fixture(scope="module")
def orig_nodes():
    nodes = {}
    for key, (path, blob, _stem, names) in FILES.items():
        try:
            a_raw = subprocess.run(["git", "show", f"{A_PRE}:{path}"], check=True, capture_output=True).stdout
            c_raw = subprocess.run(["git", "show", f"{CANON}:{path}"], check=True, capture_output=True).stdout
        except subprocess.CalledProcessError as exc:
            pytest.fail(f"BLOCKED_PIN: {exc.stderr!r}")
        assert _sha(a_raw) == blob, f"BLOCKED_PIN actor blob {path}"
        assert _sha(c_raw) == blob, f"BLOCKED_PIN canonical blob {path}"
        tree = ast.parse(a_raw.decode("utf-8"))
        found = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in names}
        assert sorted(found) == sorted(names)
        nodes[key] = found
    return nodes


@pytest.fixture
def guards(monkeypatch):
    def boom(*a, **k):
        raise AssertionError("real filesystem/effect attempted")
    monkeypatch.setattr(subprocess, "run", boom)
    monkeypatch.setattr(subprocess, "Popen", boom)
    monkeypatch.setattr(socket.socket, "connect", boom)
    for attr in ("read_text", "read_bytes", "write_text", "write_bytes", "mkdir", "touch", "unlink", "rename", "replace",
                 "exists", "is_dir", "is_file", "rglob", "glob", "iterdir"):
        monkeypatch.setattr(Path, attr, boom)
    real_open = builtins.open

    def guarded_open(file, mode="r", *a, **k):
        if any(c in str(mode) for c in "wax+") or str(file).replace("\\", "/").startswith(("/rep", "/fake", "/freeze")):
            raise AssertionError("open attempted")
        return real_open(file, mode, *a, **k)
    monkeypatch.setattr(builtins, "open", guarded_open)


def check(orig_nodes, monkeypatch, key, name, *args, overrides=None, **kwargs):
    mod = MODS[key]
    ns = dict(vars(mod))
    tree = ast.Module(body=[copy.deepcopy(orig_nodes[key][name])], type_ignores=[])
    exec(compile(ast.fix_missing_locations(tree), f"<{A_PRE[:8]}:{name}>", "exec"), ns)
    for k, v in (overrides or {}).items():
        ns[k] = v
        monkeypatch.setattr(mod, k, v)
    got, values = {}, {}
    for label, fn in (("orig", ns[name]), ("new", getattr(mod, name))):
        a, k = copy.deepcopy((args, kwargs))
        try:
            values[label] = fn(*a, **k)
            got[label] = ("ok", repr(values[label]))
        except Exception as exc:
            got[label] = ("err", type(exc).__name__, str(exc))
        assert repr((a, k)) == repr((args, kwargs)), f"{label} mutated input"
    assert got["orig"] == got["new"], got
    return values["new"] if got["new"][0] == "ok" else got["new"]


# ---- A38-1 build_selection_attribution ----
SEL = [
    {}, {"selection": None}, {"selection": "bad"}, {"selection": {}},
    {"selection": {"raw_scanner_top1": {"symbol": "005930", "rank": 3}, "selected_symbol": "005930"}},
    {"selection": {"raw_scanner_top1": {"symbol": "005930"}, "selected_symbol": "000660", "scanner_top1": {"symbol": "035420"}}},
    {"selection": {"raw_scanner_top1": {"symbol": "005930", "rank": 0}, "selected_symbol": ""}},
    {"selection": {"raw_scanner_top1": {"symbol": "", "rank": 5}, "selected_symbol": "A"}},
    {"selection": {"raw_scanner_top1": "notadict", "scanner_top1": ["x"], "selected_symbol": "A", "raw_scanner_control_scope": "custom_scope"}},
    {"selection": {"raw_scanner_top1": {"symbol": "한글", "rank": None}, "selected_symbol": "한글"}},
]


@pytest.mark.parametrize("model", SEL)
def test_build_selection_attribution(orig_nodes, monkeypatch, guards, model):
    out = check(orig_nodes, monkeypatch, "cf", "build_selection_attribution", model)
    assert list(out)[:3] == ["schema_version", "runtime_order", "full_strategist_contribution_status"]
    assert out["scanner_baseline"]["evidence_class"] == "UNAVAILABLE" and len(out["limitations"]) == 3


def test_selection_attribution_values_and_seam(orig_nodes, monkeypatch, guards):
    base = check(orig_nodes, monkeypatch, "cf", "build_selection_attribution", SEL[4])
    assert base["scanner_baseline"]["rank"] == 3 and base["strategist_selected"]["changed_scanner_top1"] is False
    assert check(orig_nodes, monkeypatch, "cf", "build_selection_attribution", SEL[6])["scanner_baseline"]["rank"] == 1  # `rank or 1 if symbol else None`
    assert check(orig_nodes, monkeypatch, "cf", "build_selection_attribution", SEL[7])["scanner_baseline"]["rank"] is None
    assert check(orig_nodes, monkeypatch, "cf", "build_selection_attribution", SEL[5])["strategist_selected"]["changed_scanner_top1"] is True

    class FakeEvidence:
        class UNAVAILABLE:
            value = "FAKE_UNAVAILABLE"
    out = check(orig_nodes, monkeypatch, "cf", "build_selection_attribution", SEL[4], overrides={"EvidenceClass": FakeEvidence})
    assert out["commander_final"]["evidence_class"] == "FAKE_UNAVAILABLE"


# ---- A38-2 build_daily_scorecard ----
def _te(status="PASS", eligible=True, net=1.0, hz=None):
    row = {"integrity": {"status": status, "promotion_metric_eligible": eligible}, "realized_outcome": {"net_return_pct": net}}
    if hz is not None:
        row["horizon_alignment"] = hz
    return row


HZ = {"status": "observed", "bucket": "b1", "horizon_violation_candidate": True, "exited_before_min_hold": True, "exited_before_target_hold": False,
      "target_hold_would_improve_exit": True, "early_exit_cost_pct": 0.25}
DS_CASES = [
    dict(trade_evaluations=[], attributions=[], q8_review={}, start_gate={}),
    dict(trade_evaluations=[_te(), _te("WATCH", False, -2.0), _te("FAIL", True, None), {}], attributions=[{"deltas": {"strategist_delta_pct": 0.5}}, {"deltas": {}}, {}],
         q8_review={"candidate_count": 4, "evaluation_trust_gate": {"trusted_forward_count": 2, "trusted_forward_coverage": 0.5, "promotion_allowed": False, "status": "WATCH"}}, start_gate={"status": "READY"}),
    dict(trade_evaluations=[_te(net=-1.0, hz=HZ), _te(net=-3.0, hz={**HZ, "bucket": "b2", "early_exit_cost_pct": None})], attributions=[], q8_review={"evaluation_trust_gate": "bad"}, start_gate={"status": "READY"}),
    dict(trade_evaluations=[_te(net=0.0)], attributions=[], q8_review={}, start_gate={"status": "READY"}),
    dict(trade_evaluations=[_te(net=2.0)], attributions=[{"deltas": {"strategist_delta_pct": 1.0}}, {"deltas": {"strategist_delta_pct": -0.5}}], q8_review={}, start_gate={"status": "NOT_READY"}),
    dict(trade_evaluations=[_te(hz={"status": "pending"}), _te(hz={"status": "observed"})], attributions=[], q8_review={}, start_gate={"status": "READY"}),
]


@pytest.mark.parametrize("case", DS_CASES)
@pytest.mark.parametrize("validity", [None, {"valid": True}])
def test_build_daily_scorecard(orig_nodes, monkeypatch, guards, case, validity):
    kw = dict(day="2026-04-16", inventory={"required_coverage": 0.9}, **case)
    if validity is not None:
        kw["day_validity"] = validity
    out = check(orig_nodes, monkeypatch, "ds", "build_daily_scorecard", **kw)
    assert out["schema_version"] == "daily_scorecard.v1" and list(out)[:4] == ["schema_version", "contract_version", "day", "decision_class"]


def test_daily_scorecard_decisions_and_seams(orig_nodes, monkeypatch, guards):
    def decision(case):
        return check(orig_nodes, monkeypatch, "ds", "build_daily_scorecard", day="d", inventory={}, **case)["decision_class"]
    assert decision(DS_CASES[0]) == "INSUFFICIENT_EVIDENCE" and decision(DS_CASES[4]) == "INSUFFICIENT_EVIDENCE"
    assert decision(DS_CASES[2]) == "ADJUST_AND_RETEST" and decision(DS_CASES[3]) == "RETAIN"
    out = check(orig_nodes, monkeypatch, "ds", "build_daily_scorecard", day="d", inventory={}, **DS_CASES[2])
    assert out["horizon_alignment"]["bucket_counts"] == {"b1": 1, "b2": 1} and out["horizon_alignment"]["average_early_exit_cost_pct"] == 0.25
    gate = {"status": "READY"}
    out = check(orig_nodes, monkeypatch, "ds", "build_daily_scorecard", day="d", inventory={}, trade_evaluations=[_te()], attributions=[], q8_review={}, start_gate=gate)
    assert out["evaluation_phase"]["full_chain_start_gate"] == gate  # equal on both sides (identity is per-call deepcopy)
    out = check(orig_nodes, monkeypatch, "ds", "build_daily_scorecard", day="d", inventory={}, trade_evaluations=[_te()], attributions=[], q8_review={}, start_gate=gate,
                overrides={"performance_metrics": lambda r: {"fake": list(r)}, "contract_metadata": lambda: {"fake_contract": True}, "CONTRACT_VERSION": "CV"})
    assert out["contract"] == {"fake_contract": True} and out["contract_version"] == "CV" and out["realized_performance"]["fake"] == [1.0]
    # start_gate object identity is preserved by the wrapper (no copy)
    import libs.reporting.evaluation.daily_scorecard as ds
    live_gate = {"status": "READY"}
    assert ds.build_daily_scorecard(day="d", inventory={}, trade_evaluations=[], attributions=[], q8_review={}, start_gate=live_gate)["evaluation_phase"]["full_chain_start_gate"] is live_gate


# ---- A38-3/5/6 + read_json variants: fake path objects ----
class FakeReadPath:
    def __init__(self, text=None, error=None):
        self.text, self.error, self.calls = text, error, []

    def __repr__(self):
        return f"FakeReadPath({self.text!r}, {self.error!r})"

    def read_text(self, encoding=None):
        self.calls.append(encoding)
        if self.error:
            raise self.error
        return self.text


READ_CASES = [('{"a": 1, "b": [1, 2]}', None), ("[1, 2]", None), ("5", None), ('"s"', None), ("null", None), ("not json", None), ("", None),
              ('{"한글": "값"}', None), (None, OSError("fake io")), (None, UnicodeDecodeError("utf-8", b"\xff", 0, 1, "bad")), (None, PermissionError("fake perm"))]
READERS = [("inv", "read_json"), ("v0", "_read_json"), ("win", "_read_json")]


@pytest.mark.parametrize("key,name", READERS)
@pytest.mark.parametrize("text,error", READ_CASES)
def test_json_readers(orig_nodes, monkeypatch, guards, key, name, text, error):
    path = FakeReadPath(text, error)
    out = check(orig_nodes, monkeypatch, key, name, path)
    assert isinstance(out, dict)
    # check() deep-copies the argument for each side, so the original object's call log stays empty; verify encoding separately
    p2 = FakeReadPath(text, error)
    getattr(MODS[key], name)(p2)
    assert p2.calls == ["utf-8"]


@pytest.mark.parametrize("key,name", READERS)
def test_json_reader_values_and_json_seam(orig_nodes, monkeypatch, guards, key, name):
    assert check(orig_nodes, monkeypatch, key, name, FakeReadPath('{"x": 1}')) == {"x": 1}
    assert check(orig_nodes, monkeypatch, key, name, FakeReadPath("[1]")) == {}
    assert check(orig_nodes, monkeypatch, key, name, FakeReadPath(None, OSError("e"))) == {}

    class FakeJson:
        @staticmethod
        def loads(text):
            return {"fake": text}
    assert check(orig_nodes, monkeypatch, key, name, FakeReadPath("anything"), overrides={"json": FakeJson}) == {"fake": "anything"}

    class RaisingJson:
        @staticmethod
        def loads(text):
            raise RuntimeError("fake")
    assert check(orig_nodes, monkeypatch, key, name, FakeReadPath("x"), overrides={"json": RaisingJson}) == {}


# ---- A38-4 _ledger_day_record (fake root with glob) ----
class FakeP(str):
    pass


class FakeRoot:
    def __init__(self, files, label="/rep"):
        self.files, self.label = files, label

    def __repr__(self):
        return f"FakeRoot({self.files!r}, {self.label!r})"

    def __truediv__(self, other):
        return FakeRoot(self.files, f"{self.label}/{other}")

    def glob(self, pattern):
        assert pattern == "*/daily_ledger.json"
        return iter([FakeP(f) for f in self.files])


LEDGERS = {
    "/rep/evaluation/freeze_window/a/daily_ledger.json": {"days": [{"day": "2026-04-15", "n": {"deep": 1}}, {"day": "2026-04-16", "from": "a"}, "bad"]},
    "/rep/evaluation/freeze_window/b/daily_ledger.json": {"days": [{"day": "2026-04-16", "from": "b"}, None]},
    "/rep/evaluation/freeze_window/c/daily_ledger.json": {"days": None},
    "/rep/evaluation/freeze_window/d/daily_ledger.json": {},
}


@pytest.mark.parametrize("files,day", [
    ([], "2026-04-16"), (list(LEDGERS), "2026-04-16"), (list(LEDGERS)[::-1], "2026-04-16"), (list(LEDGERS), "2026-04-15"), (list(LEDGERS), "2099-01-01"),
    (list(LEDGERS)[2:], "2026-04-16"), ([list(LEDGERS)[1], list(LEDGERS)[0]], "2026-04-16"),
])
def test_ledger_day_record(orig_nodes, monkeypatch, guards, files, day):
    seen = []
    out = check(orig_nodes, monkeypatch, "v0", "_ledger_day_record", FakeRoot(files), day,
                overrides={"_read_json": lambda p: seen.append(str(p)) or copy.deepcopy(LEDGERS.get(str(p), {}))})
    assert isinstance(out, dict)
    assert seen[: len(seen) // 2] == seen[len(seen) // 2:]  # same read order on both sides


def test_ledger_day_record_first_sorted_match_and_copy(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "v0", "_ledger_day_record", FakeRoot(list(LEDGERS)[::-1]), "2026-04-16",
                overrides={"_read_json": lambda p: copy.deepcopy(LEDGERS.get(str(p), {}))})
    assert out == {"day": "2026-04-16", "from": "a"}  # sorted by str: a before b
    nested = {"deep": 1}
    src = {"days": [{"day": "d", "n": nested}]}
    monkeypatch.setattr(MODS["v0"], "_read_json", lambda p: src)
    live = MODS["v0"]._ledger_day_record(FakeRoot(["/rep/evaluation/freeze_window/z/daily_ledger.json"]), "d")
    assert live is not src["days"][0] and live["n"] is nested


# ---- A38-7 _group_key / A38-8 _profit_factor ----
GK_ROWS = [{}, {"entry_lane_observation": {"time_bucket": "open_0_20m", "primary_lane": "strict", "market_regime_rail": "BULL"}, "quant_tactic_id": "T1", "shadow_role": "R"},
           {"entry_lane_observation": "bad", "quant_tactic_id": "  "}, {"entry_lane_observation": {"time_bucket": " "}, "quant_tactic_id": None, "shadow_role": 0},
           {"entry_lane_observation": {"time_bucket": "한글", "primary_lane": None}, "quant_tactic_id": "T2"}]
DIMS = [(), ("time_bucket",), ("tactic", "time_bucket"), ("selection_role", "market_regime_rail", "primary_lane", "tactic", "time_bucket"), ("tactic", "tactic"), ("nope",), ("time_bucket", "nope")]


@pytest.mark.parametrize("row", GK_ROWS)
@pytest.mark.parametrize("dims", DIMS)
def test_group_key(orig_nodes, monkeypatch, guards, row, dims):
    check(orig_nodes, monkeypatch, "ha", "_group_key", row, dims)


def test_group_key_values_errors_and_seams(orig_nodes, monkeypatch, guards):
    assert check(orig_nodes, monkeypatch, "ha", "_group_key", GK_ROWS[1], ("tactic", "time_bucket", "selection_role")) == ("T1", "open_0_20m", "R")
    assert check(orig_nodes, monkeypatch, "ha", "_group_key", GK_ROWS[0], ("tactic", "primary_lane")) == ("unknown", "unknown")
    err = check(orig_nodes, monkeypatch, "ha", "_group_key", GK_ROWS[0], ("nope",))
    assert err == ("err", "KeyError", "'nope'")
    seen = []
    out = check(orig_nodes, monkeypatch, "ha", "_group_key", GK_ROWS[1], ("tactic", "primary_lane"),
                overrides={"_lane_observation": lambda r: seen.append("lane") or {"primary_lane": "PL"}, "_text": lambda v, fallback="unknown": f"<{v}>"})
    assert out == ("<T1>", "<PL>") and seen == ["lane", "lane"]


PF = [[], [1.0], [-1.0], [1.0, 2.0, 3.0], [-1.0, -2.0], [1.0, -2.0, 3.0, -4.0], [0.0, 0.0], [0, -0.0], [1.5, -1.0], [1.0, -3.0], [1.0, -0.3333], [0.00004, -1.0],
      [NAN], [1.0, NAN], [INF, -1.0], [1.0, -INF], ["a"], [None], [1.0, 2.0, -0.0001], [10**6, -1], [True, False]]


@pytest.mark.parametrize("values", PF)
def test_profit_factor(orig_nodes, monkeypatch, guards, values):
    check(orig_nodes, monkeypatch, "ha", "_profit_factor", values)


def test_profit_factor_values(orig_nodes, monkeypatch, guards):
    assert check(orig_nodes, monkeypatch, "ha", "_profit_factor", [1.0, 2.0]) == 999.0
    assert check(orig_nodes, monkeypatch, "ha", "_profit_factor", [-1.0, 0.0]) == 0.0
    assert check(orig_nodes, monkeypatch, "ha", "_profit_factor", []) == 0.0
    assert check(orig_nodes, monkeypatch, "ha", "_profit_factor", [1.0, -3.0]) == 0.3333


# ---- structure ----
@pytest.mark.parametrize("key,name", CASES)
def test_wrapper_thin_and_owner_holds_body(key, name):
    wrapper = ast.parse(inspect.getsource(getattr(MODS[key], name))).body[0]
    stmts = [n for n in wrapper.body if not (isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant))]
    assert len(stmts) == 1 and isinstance(stmts[0], ast.Return)
    assert not [n for n in ast.walk(wrapper) if isinstance(n, (ast.If, ast.For, ast.Try, ast.ListComp, ast.GeneratorExp))]
    call = stmts[0].value
    assert isinstance(call, ast.Call) and "facade" in [k.arg for k in call.keywords], "wrapper must forward to the Owner with facade="
    owner_fn = getattr(OWNERS[(key, name)], name)
    node = ast.parse(inspect.getsource(owner_fn)).body[0]
    assert len(node.body) >= 1 and owner_fn.__module__ == OWNERS[(key, name)].__name__
    stem = FILES[key][2]
    src = inspect.getsource(OWNERS[(key, name)]).replace(f"{stem}_", "")
    assert f"{stem} import" not in src and f"import {stem}" not in src
