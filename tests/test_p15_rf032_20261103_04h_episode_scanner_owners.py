"""RF-032 A51-1..8: eight ``episode_scanner_review`` helper bodies, original vs thin wrappers + Owners.

Original = A preimage d891f7a4 (SOURCE blob 5bd42ffa == canonical 4751dd92). Each original function is compiled from
``git show`` into a copy of the live module namespace and compared with the final wrapper + Owner (output repr,
exception type/message, input immutability). Fake objects only. The only subprocess is a read-only ``git show`` of the
two pinned commits (needs those objects locally); during the comparisons subprocess/socket/file access is guarded, and
nothing touches the UEF/validation-id writer.
"""
from __future__ import annotations

import ast
import builtins
import copy
import hashlib
import importlib
import inspect
import socket
import subprocess
from pathlib import Path

import pytest

A_PRE = "d891f7a4caa2980aa11b9acb45b408170b9cc793"
CANON = "4751dd928cd12c84c95485b66a8a6f199a6d6188"
EV = "libs/reporting/evaluation/"
# name -> (source stem, pinned blob, owner module stem)
SPEC = {
    "_number": ("episode_scanner_review", "5bd42ffafd07612290dc4138e149d2e627590d60", "episode_scanner_review_number"),
    "_mapping": ("episode_scanner_review", "5bd42ffafd07612290dc4138e149d2e627590d60", "episode_scanner_review_mapping"),
    "_checkpoint_return": ("episode_scanner_review", "5bd42ffafd07612290dc4138e149d2e627590d60", "episode_scanner_review_checkpoint_return"),
    "_epoch": ("episode_scanner_review", "5bd42ffafd07612290dc4138e149d2e627590d60", "episode_scanner_review_epoch"),
    "_setup_key": ("episode_scanner_review", "5bd42ffafd07612290dc4138e149d2e627590d60", "episode_scanner_review_setup_key"),
    "_day": ("episode_scanner_review", "5bd42ffafd07612290dc4138e149d2e627590d60", "episode_scanner_review_day"),
    "_rank_bucket": ("episode_scanner_review", "5bd42ffafd07612290dc4138e149d2e627590d60", "episode_scanner_review_rank_bucket"),
    "_episode_representatives": ("episode_scanner_review", "5bd42ffafd07612290dc4138e149d2e627590d60", "episode_scanner_review_episode_representatives"),
}
MODS = {s: importlib.import_module(f"libs.reporting.evaluation.{s}") for s in {v[0] for v in SPEC.values()}}
OWNERS = {n: importlib.import_module(f"libs.reporting.evaluation.{v[2]}") for n, v in SPEC.items()}
NAN = float("nan")


def _sha(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + bytes([0]) + raw).hexdigest()


@pytest.fixture(scope="module")
def orig_nodes():
    out = {}
    for stem, blob in {(v[0], v[1]) for v in SPEC.values()}:
        raws = {}
        for label, rev in (("A", A_PRE), ("canonical", CANON)):
            try:
                raws[label] = subprocess.run(["git", "show", f"{rev}:{EV}{stem}.py"], check=True, capture_output=True).stdout
            except subprocess.CalledProcessError as exc:
                pytest.fail(f"BLOCKED_PIN {stem} {label}: {exc.stderr!r}")
            assert _sha(raws[label]) == blob, f"BLOCKED_PIN {stem} {label} blob"
        tree = ast.parse(raws["A"].decode("utf-8"))
        for n, v in SPEC.items():
            if v[0] == stem:
                out[n] = [x for x in tree.body if isinstance(x, ast.FunctionDef) and x.name == n][-1]
    assert sorted(out) == sorted(SPEC)
    return out


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
        if any(c in str(mode) for c in "wax+") or str(file).replace("\\", "/").startswith(("/rep", "/fake")):
            raise AssertionError("open attempted")
        return real_open(file, mode, *a, **k)
    monkeypatch.setattr(builtins, "open", guarded_open)


def check(orig_nodes, monkeypatch, name, *args, overrides=None, **kwargs):
    mod = MODS[SPEC[name][0]]
    ns = dict(vars(mod))
    tree = ast.Module(body=[copy.deepcopy(orig_nodes[name])], type_ignores=[])
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


import collections

ES = MODS["episode_scanner_review"]


class _Str:
    def __init__(self, text, truthy=True):
        self.text, self.truthy = text, truthy

    def __repr__(self):
        return f"_Str({self.text!r},{self.truthy})"

    def __str__(self):
        return self.text

    def __bool__(self):
        return self.truthy


class _MapSub(dict):
    def __repr__(self):
        return f"_MapSub({dict(self)!r})"


class _Num:
    def __repr__(self):
        return "_Num()"

    def __float__(self):
        return 2.5


class _FloatErr:
    def __init__(self, exc):
        self.exc = exc

    def __repr__(self):
        return f"_FloatErr({self.exc.__name__})"

    def __float__(self):
        raise self.exc("custom float failure")


VALS = [None, "", 0, 0.0, "0", " 1.5 ", "abc", "1e3", "nan", "inf", NAN, True, [], {}, b"2", _Num(), _FloatErr(TypeError), _FloatErr(ValueError), (), "-0", -3]


# ---- A51-1 _number ----
@pytest.mark.parametrize("value", VALS)
def test_number(orig_nodes, monkeypatch, guards, value):
    check(orig_nodes, monkeypatch, "_number", value)


def test_number_exact(orig_nodes, monkeypatch, guards):
    assert check(orig_nodes, monkeypatch, "_number", None) is None and check(orig_nodes, monkeypatch, "_number", "") is None and check(orig_nodes, monkeypatch, "_number", 0) == 0.0
    assert check(orig_nodes, monkeypatch, "_number", _FloatErr(TypeError)) is None and check(orig_nodes, monkeypatch, "_number", _FloatErr(ValueError)) is None
    assert check(orig_nodes, monkeypatch, "_number", _FloatErr(RuntimeError)) == ("err", "RuntimeError", "custom float failure")  # only TypeError/ValueError caught
    out = check(orig_nodes, monkeypatch, "_number", "nan")
    assert out != out


# ---- A51-2 _mapping ----
@pytest.mark.parametrize("value", [None, {}, {"a": 1}, _MapSub(a=1), [], [("a", 1)], "s", 5, {"n": {"deep": [1]}}])
def test_mapping(orig_nodes, monkeypatch, guards, value):
    check(orig_nodes, monkeypatch, "_mapping", value)


def test_mapping_identity_and_seam(orig_nodes, monkeypatch, guards):
    src = {"a": 1}
    assert ES._mapping(src) is src and ES._mapping(None) == {} and ES._mapping(None) is not ES._mapping(None)  # identity, never a copy

    class NeverMapping:
        pass
    assert check(orig_nodes, monkeypatch, "_mapping", {"a": 1}, overrides={"Mapping": NeverMapping}) == {}


# ---- A51-3 _checkpoint_return ----
def _row(cp, **extra):
    return {"shadow_forward_outcome": {"checkpoints": cp, **extra}}


CR = [{}, None, "row", {"shadow_forward_outcome": None}, {"shadow_forward_outcome": "x"}, _row(None), _row("x"), _row({}), _row({"+5m": None}), _row({"+5m": "x"}), _row({"+5m": {}}),
      _row({"+5m": {"status": "pending", "return_pct": 1}}), _row({"+5m": {"status": "observed"}}), _row({"+5m": {"status": "observed", "return_pct": 0}}), _row({"+5m": {"status": "observed", "return_pct": "1.25"}}),
      _row({"+5m": {"status": "observed", "return_pct": "bad"}}), _row({"+5m": {"status": "observed", "return_pct": ""}}), _row({"+15m": {"status": "observed", "return_pct": -2}}),
      _row({"+5m": {"status": "OBSERVED", "return_pct": 1}}), _row({"+5m": _MapSub(status="observed", return_pct=3)}), _row({"+5m": {"status": _Str("observed"), "return_pct": 4}}),
      _row({"+5m": {"status": None, "return_pct": 1}}), _row({"+5m": {"status": 0, "return_pct": 1}})]


@pytest.mark.parametrize("row", CR)
@pytest.mark.parametrize("horizon", ["+5m", "+15m", "missing"])
def test_checkpoint_return(orig_nodes, monkeypatch, guards, row, horizon):
    check(orig_nodes, monkeypatch, "_checkpoint_return", row, horizon)


def test_checkpoint_return_exact_and_seams(orig_nodes, monkeypatch, guards):
    assert check(orig_nodes, monkeypatch, "_checkpoint_return", _row({"+5m": {"status": "observed", "return_pct": 0}}), "+5m") == 0.0
    assert check(orig_nodes, monkeypatch, "_checkpoint_return", _row({"+5m": {"status": "observed"}}), "+5m") is None
    assert check(orig_nodes, monkeypatch, "_checkpoint_return", None, "+5m")[0] == "err"
    seen = []
    out = check(orig_nodes, monkeypatch, "_checkpoint_return", _row({"+5m": {"status": "observed", "return_pct": "7"}}), "+5m", overrides={"_number": lambda v: seen.append(v) or 99.0})
    assert out == 99.0 and seen == ["7", "7"]


def test_checkpoint_return_mapping_seam(orig_nodes, monkeypatch, guards):
    maps = []
    out = check(orig_nodes, monkeypatch, "_checkpoint_return", {"k": 1}, "+5m", overrides={"_mapping": lambda v: maps.append(1) or {"status": "observed", "return_pct": 5, "checkpoints": {}}})
    assert out == 5.0 and len(maps) == 6  # three _mapping calls per side


# ---- A51-4 _epoch ----
EP = [{}, None, {"shadow_forward_base": None}, {"shadow_forward_base": "x"}, {"shadow_forward_base": {}}, {"shadow_forward_base": {"baseline_epoch": 1776297600}}, {"shadow_forward_base": {"baseline_epoch": "1776297600.9"}},
      {"shadow_forward_base": {"baseline_epoch": 0}}, {"shadow_forward_base": {"baseline_epoch": -5}}, {"shadow_forward_base": {"baseline_epoch": "bad"}}, {"shadow_forward_base": {"baseline_epoch": ""}},
      {"shadow_forward_base": {"baseline_epoch": NAN}}, {"shadow_forward_base": {"baseline_epoch": float("inf")}}, {"shadow_forward_base": {"baseline_epoch": 2.9}}, {"shadow_forward_base": _MapSub(baseline_epoch=7)}]


@pytest.mark.parametrize("row", EP)
def test_epoch(orig_nodes, monkeypatch, guards, row):
    check(orig_nodes, monkeypatch, "_epoch", row)


def test_epoch_exact_and_seams(orig_nodes, monkeypatch, guards):
    assert check(orig_nodes, monkeypatch, "_epoch", EP[5]) == 1776297600 and check(orig_nodes, monkeypatch, "_epoch", EP[13]) == 2 and check(orig_nodes, monkeypatch, "_epoch", {}) == 0
    assert check(orig_nodes, monkeypatch, "_epoch", EP[8]) == -5  # negative epochs are returned as int
    assert check(orig_nodes, monkeypatch, "_epoch", EP[11])[0:2] == ("err", "ValueError") and check(orig_nodes, monkeypatch, "_epoch", EP[12])[0:2] == ("err", "OverflowError")
    assert check(orig_nodes, monkeypatch, "_epoch", None)[0] == "err"
    out = check(orig_nodes, monkeypatch, "_epoch", EP[5], overrides={"_number": lambda v: 12.7})
    assert out == 12


# ---- A51-5 _setup_key ----
SK = [{}, None, {"entry_lane_observation": None}, {"entry_lane_observation": "x"}, {"entry_lane_observation": {"subtype_v2": "v2", "subtype": "s", "primary_lane": "p"}, "reason": "r"},
      {"entry_lane_observation": {"subtype": "s", "primary_lane": "p"}, "reason": "r"}, {"entry_lane_observation": {"primary_lane": "p"}, "reason": "r"}, {"entry_lane_observation": {}, "reason": "r"},
      {"reason": "only_reason"}, {"entry_lane_observation": {"subtype_v2": "", "subtype": 0, "primary_lane": None}, "reason": ""}, {"entry_lane_observation": {"subtype_v2": 5}},
      {"entry_lane_observation": {"subtype_v2": _Str("한글")}}, {"entry_lane_observation": {"subtype_v2": _Str("x", truthy=False)}, "reason": "r"}, {"entry_lane_observation": _MapSub(subtype="m")}]


@pytest.mark.parametrize("row", SK)
def test_setup_key(orig_nodes, monkeypatch, guards, row):
    check(orig_nodes, monkeypatch, "_setup_key", row)


def test_setup_key_exact_and_seam(orig_nodes, monkeypatch, guards):
    assert check(orig_nodes, monkeypatch, "_setup_key", SK[4]) == "v2" and check(orig_nodes, monkeypatch, "_setup_key", SK[5]) == "s" and check(orig_nodes, monkeypatch, "_setup_key", SK[6]) == "p"
    assert check(orig_nodes, monkeypatch, "_setup_key", SK[7]) == "r" and check(orig_nodes, monkeypatch, "_setup_key", {}) == "unknown" and check(orig_nodes, monkeypatch, "_setup_key", SK[9]) == "unknown"
    assert check(orig_nodes, monkeypatch, "_setup_key", None)[0] == "err"

    class NeverMapping:
        pass
    assert check(orig_nodes, monkeypatch, "_setup_key", SK[4], overrides={"Mapping": NeverMapping}) == "r"


# ---- A51-6 _day ----
DY = [{}, None, {"day": "2026-04-10"}, {"day": "20260410"}, {"day": "2026-4-10"}, {"day": "abcdefgh"}, {"day": "2026041"}, {"day": "202604100"}, {"day": ""}, {"day": None}, {"day": 20260410},
      {"generated_at": "2026-04-10T00:00:00+00:00"}, {"generated_at": "2026-04-11T00:00:00+00:00", "day": "2026-04-10"}, {"day": "２０２６０４１０"}, {"day": "2026-04-10 "}, {"day": _Str("2026-04-10")}]


@pytest.mark.parametrize("row", DY)
def test_day(orig_nodes, monkeypatch, guards, row):
    check(orig_nodes, monkeypatch, "_day", row)


def test_day_exact_and_seams(orig_nodes, monkeypatch, guards):
    assert check(orig_nodes, monkeypatch, "_day", {"day": "2026-04-10"}) == "20260410" and check(orig_nodes, monkeypatch, "_day", {"day": "2026041"}) == "" and check(orig_nodes, monkeypatch, "_day", {}) == ""
    assert check(orig_nodes, monkeypatch, "_day", None)[0] == "err"
    seen = []
    out = check(orig_nodes, monkeypatch, "_day", {"day": "ignored"}, overrides={"candidate_day": lambda r: seen.append(r) or "2026-05-06"})
    assert out == "20260506" and len(seen) == 2  # call-time candidate_day, once per side
    assert check(orig_nodes, monkeypatch, "_day", {"day": "20260101"}, overrides={"candidate_day": lambda r: ""}) == "20260101"  # falls back to row["day"]


# ---- A51-7 _rank_bucket ----
@pytest.mark.parametrize("rank", [1, 2, 3, 4, 5, 100, 0, -1, -100, True, False, 1.0, 2.5, 3.9, 0.5, NAN, float("inf"), float("-inf"), "1", None, [], 10 ** 12])
def test_rank_bucket(orig_nodes, monkeypatch, guards, rank):
    check(orig_nodes, monkeypatch, "_rank_bucket", rank)


def test_rank_bucket_exact(orig_nodes, monkeypatch, guards):
    exp = {1: "rank1", 2: "rank2_3", 3: "rank2_3", 4: "rank4_plus", 5: "rank4_plus", 100: "rank4_plus", 0: "unknown", -3: "unknown"}
    for rank, name in exp.items():
        assert check(orig_nodes, monkeypatch, "_rank_bucket", rank) == name
    assert check(orig_nodes, monkeypatch, "_rank_bucket", 3.9) == "unknown"  # 3 < 3.9 < 4 falls through and check(orig_nodes, monkeypatch, "_rank_bucket", 2.5) == "rank2_3" and check(orig_nodes, monkeypatch, "_rank_bucket", NAN) == "unknown"
    assert check(orig_nodes, monkeypatch, "_rank_bucket", "1")[0:2] == ("err", "TypeError") and check(orig_nodes, monkeypatch, "_rank_bucket", None)[0:2] == ("err", "TypeError")


# ---- A51-8 _episode_representatives ----
def _c(day="2026-04-10", sym="A", epoch=1000, rank=1, **extra):
    row = {"generated_at": f"{day}T00:00:00+00:00", "symbol": sym, "rank": rank, "shadow_forward_base": {"baseline_epoch": epoch}, "entry_lane_observation": {"subtype_v2": "S1"},
           "shadow_forward_outcome": {"checkpoints": {"+5m": {"status": "observed", "return_pct": 1.5}, "+15m": {"status": "pending", "return_pct": 9}}}}
    row.update(extra)
    return row


ROWS = [_c(), _c(epoch=1100, rank=2), _c(epoch=1300), _c(epoch=1000, rank=3), _c(sym="B", epoch=500), _c(day="2026-04-11", epoch=2000), _c(sym=""), {"symbol": "A"}, _c(epoch=0), _c(epoch=0, rank=0), _c(epoch=-5),
        _c(epoch=1050, q9_candidate_sources=["s1", "", "s2"]), _c(epoch=1060, sources=["z"]), _c(epoch=1070, q9_candidate_sources=[], sources=None), _c(rank="x", epoch=1080), _c(rank=None, epoch=1090),
        _c(entry_lane_observation={"primary_lane": "P"}, epoch=1100), _c(score_breakdown={"m": 1}, epoch=3000)]


@pytest.mark.parametrize("rows", [[], ROWS, ROWS[:3], ROWS[3:6], ROWS[6:10], ROWS[10:14], ROWS[14:], [ROWS[0]] * 3])
@pytest.mark.parametrize("gap", [0, 60, 300, 100000])
def test_episode_representatives(orig_nodes, monkeypatch, guards, rows, gap):
    check(orig_nodes, monkeypatch, "_episode_representatives", rows, episode_gap_sec=gap)


def test_episode_representatives_exact_and_seams(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "_episode_representatives", [_c(), _c(epoch=1100, rank=2), _c(epoch=1500)], episode_gap_sec=300)
    assert [e["episode_id"] for e in out] == ["20260410:A:S1:1", "20260410:A:S1:2"] and out[0]["rank"] == 1 and out[0]["rank_bucket"] == "rank1" and out[0]["returns"]["+5m"] == 1.5
    assert list(out[0]) == ["episode_id", "day", "symbol", "setup", "baseline_epoch", "rank", "rank_bucket", "score_breakdown", "sources", "returns"] and list(out[0]["returns"]) == list(ES.SCANNER_HORIZONS)
    z = check(orig_nodes, monkeypatch, "_episode_representatives", [_c(epoch=0, rank=0)], episode_gap_sec=300)[0]
    assert z["baseline_epoch"] is None and z["rank"] is None and z["rank_bucket"] == "unknown"
    assert check(orig_nodes, monkeypatch, "_episode_representatives", [], episode_gap_sec=1) == []
    assert check(orig_nodes, monkeypatch, "_episode_representatives", None, episode_gap_sec=1)[0] == "err" and len(check(orig_nodes, monkeypatch, "_episode_representatives", [_c()], episode_gap_sec="x")) == 1  # gap only compared from the 2nd row on
    assert check(orig_nodes, monkeypatch, "_episode_representatives", [_c(), _c(epoch=1100)], episode_gap_sec=None)[0:2] == ("err", "TypeError")
    assert check(orig_nodes, monkeypatch, "_episode_representatives", [_c(q9_candidate_sources=["s1", "", "s2"])], episode_gap_sec=1)[0]["sources"] == ["s1", "s2"]
    src = copy.deepcopy(ROWS)
    ES._episode_representatives(src, episode_gap_sec=300)
    assert src == ROWS  # inputs untouched
    assert [p.kind.name for p in inspect.signature(ES._episode_representatives).parameters.values()] == ["POSITIONAL_OR_KEYWORD", "KEYWORD_ONLY"]
    out = check(orig_nodes, monkeypatch, "_episode_representatives", [{"k": 1}, {"k": 2}], episode_gap_sec=10,
                overrides={"_day": lambda r: "D", "_setup_key": lambda r: "K", "_epoch": lambda r: r["k"], "_number": lambda v: None, "_rank_bucket": lambda rank: f"B{rank}",
                           "_checkpoint_return": lambda r, h: 0.5, "SCANNER_HORIZONS": ("+5m",), "_mapping": lambda v: {"x": 1}})
    assert out == []  # rows without a symbol are skipped
    out = check(orig_nodes, monkeypatch, "_episode_representatives", [{"k": 1, "symbol": "S"}, {"k": 2, "symbol": "S"}, {"k": 40, "symbol": "S"}], episode_gap_sec=10,
                overrides={"_day": lambda r: "D", "_setup_key": lambda r: "K", "_epoch": lambda r: r["k"], "_number": lambda v: None, "_rank_bucket": lambda rank: f"B{rank}",
                           "_checkpoint_return": lambda r, h: 0.5, "SCANNER_HORIZONS": ("+5m",)})
    assert [(e["episode_id"], e["baseline_epoch"]) for e in out] == [("D:S:K:1", 1), ("D:S:K:2", 40)] and out[0]["returns"] == {"+5m": 0.5} and out[0]["rank_bucket"] == "B0"
    made = []

    def spy(factory):
        made.append(1)
        return collections.defaultdict(factory)
    check(orig_nodes, monkeypatch, "_episode_representatives", ROWS[:3], episode_gap_sec=300, overrides={"defaultdict": spy})
    assert made == [1, 1]


# ---- structure ----
@pytest.mark.parametrize("name", list(SPEC))
def test_wrapper_thin_and_owner_holds_body(name):
    mod = MODS[SPEC[name][0]]
    wrapper = ast.parse(inspect.getsource(getattr(mod, name))).body[0]
    stmts = [n for n in wrapper.body if not (isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant))]
    assert len(stmts) == 1 and isinstance(stmts[0], ast.Return)
    assert not [n for n in ast.walk(wrapper) if isinstance(n, (ast.If, ast.For, ast.Try, ast.ListComp, ast.GeneratorExp))]
    call = stmts[0].value
    assert isinstance(call, ast.Call) and "facade" in [k.arg for k in call.keywords], "wrapper must forward to the Owner with facade="
    owner_fn = getattr(OWNERS[name], name)
    node = ast.parse(inspect.getsource(owner_fn)).body[0]
    assert len(node.body) >= 1 and owner_fn.__module__ == OWNERS[name].__name__
    src = inspect.getsource(OWNERS[name])
    stem = SPEC[name][0]
    assert f"import {stem}" not in src and f"{stem} import" not in src.replace("from . import", "") and f"from .{stem} " not in src
