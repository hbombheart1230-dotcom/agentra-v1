"""RF-032 A50-1..8: eight ``scanner_alignment_root_cause`` helper bodies, original vs thin wrappers + Owners.

Original = A preimage 74fe2120 (SOURCE blob 561fbdce == canonical 8fe92ce5). Each original function is compiled from
``git show`` into a copy of the live module namespace and compared with the final wrapper + Owner (output repr,
exception type/message, input immutability). Fake objects only: attach/dedupe/performance helpers are faked, no real
file reads/writes, sockets, subprocess or UEF/validation-id writer.
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

A_PRE = "74fe2120932e1dcdc367e2769558be3b1d406c77"
CANON = "8fe92ce5f9dc3c9bb131a59b7b75d87150bdf59d"
EV = "libs/reporting/evaluation/"
# name -> (source stem, pinned blob, owner module stem)
SPEC = {
    "_symbol": ("scanner_alignment_root_cause", "561fbdced4acd99e6c7acb9153e99b0280a977a4", "scanner_alignment_root_cause_symbol"),
    "_selected_rank": ("scanner_alignment_root_cause", "561fbdced4acd99e6c7acb9153e99b0280a977a4", "scanner_alignment_root_cause_selected_rank"),
    "_score_gap": ("scanner_alignment_root_cause", "561fbdced4acd99e6c7acb9153e99b0280a977a4", "scanner_alignment_root_cause_score_gap"),
    "_outcome_return": ("scanner_alignment_root_cause", "561fbdced4acd99e6c7acb9153e99b0280a977a4", "scanner_alignment_root_cause_outcome_return"),
    "_impact_score": ("scanner_alignment_root_cause", "561fbdced4acd99e6c7acb9153e99b0280a977a4", "scanner_alignment_root_cause_impact_score"),
    "_diagnostic_kind": ("scanner_alignment_root_cause", "561fbdced4acd99e6c7acb9153e99b0280a977a4", "scanner_alignment_root_cause_diagnostic_kind"),
    "_largest_cause": ("scanner_alignment_root_cause", "561fbdced4acd99e6c7acb9153e99b0280a977a4", "scanner_alignment_root_cause_largest_cause"),
    "_patch_candidate": ("scanner_alignment_root_cause", "561fbdced4acd99e6c7acb9153e99b0280a977a4", "scanner_alignment_root_cause_patch_candidate"),
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


SAR = MODS["scanner_alignment_root_cause"]


class _Str:
    def __init__(self, text, truthy=True):
        self.text, self.truthy = text, truthy

    def __repr__(self):
        return f"_Str({self.text!r},{self.truthy})"

    def __str__(self):
        return self.text

    def __bool__(self):
        return self.truthy


class _BadStr:
    def __repr__(self):
        return "_BadStr()"

    def __str__(self):
        raise RuntimeError("str failure")


class _MapSub(dict):
    def __repr__(self):
        return f"_MapSub({dict(self)!r})"


# ---- A50-1 _symbol ----
@pytest.mark.parametrize("value", [None, "", " ", " 005930 ", "한글", 0, 5, 1.5, [], {}, {"symbol": " A "}, {"symbol": None}, {"symbol": 0}, {"other": 1}, _MapSub(symbol="B"), _Str(" x "), _Str("y", truthy=False),
                                   [1], {"symbol": _Str(" z ")}, {"symbol": _BadStr()}, _BadStr()])
def test_symbol(orig_nodes, monkeypatch, guards, value):
    check(orig_nodes, monkeypatch, "_symbol", value)


def test_symbol_exact_and_seam(orig_nodes, monkeypatch, guards):
    assert check(orig_nodes, monkeypatch, "_symbol", {"symbol": " A "}) == "A" and check(orig_nodes, monkeypatch, "_symbol", " B ") == "B" and check(orig_nodes, monkeypatch, "_symbol", None) == ""
    assert check(orig_nodes, monkeypatch, "_symbol", {"symbol": 0}) == "" and check(orig_nodes, monkeypatch, "_symbol", 0) == ""
    assert check(orig_nodes, monkeypatch, "_symbol", _BadStr()) == ("err", "RuntimeError", "str failure")

    class NeverMapping:
        pass
    assert check(orig_nodes, monkeypatch, "_symbol", {"symbol": "A"}, overrides={"Mapping": NeverMapping}) == "{'symbol': 'A'}"


# ---- A50-2 _selected_rank ----
def _m(rank=None, cand_rank=None, **extra):
    sel = {}
    if rank is not None:
        sel["selected_rank"] = rank
    if cand_rank is not None:
        sel["selected_candidate"] = {"rank": cand_rank}
    sel.update(extra)
    return {"selection": sel}


SR = [{}, None if False else {"selection": None}, {"selection": "bad"}, _m(), _m(3), _m("4"), _m(0, 5), _m(None, 6), _m("x"), _m(2.9), _m("2.9"), _m(-1), _m(True), _m(rank=0, cand_rank=0),
      _m(selected_candidate="bad", rank=None), {"selection": {"selected_candidate": {"rank": "7"}}}, {"selection": {"selected_rank": "nan"}}, {"selection": {"selected_rank": "inf"}}, _m([]), _m(_Str("8"))]


@pytest.mark.parametrize("model", SR)
def test_selected_rank(orig_nodes, monkeypatch, guards, model):
    check(orig_nodes, monkeypatch, "_selected_rank", model)


def test_selected_rank_exact_and_seams(orig_nodes, monkeypatch, guards):
    assert check(orig_nodes, monkeypatch, "_selected_rank", _m(3)) == 3 and check(orig_nodes, monkeypatch, "_selected_rank", _m(0, 5)) == 5  # falsy rank falls back to candidate rank
    assert check(orig_nodes, monkeypatch, "_selected_rank", _m(2.9)) == 2  # int() truncation
    assert check(orig_nodes, monkeypatch, "_selected_rank", _m()) is None and check(orig_nodes, monkeypatch, "_selected_rank", _m("x")) is None
    assert check(orig_nodes, monkeypatch, "_selected_rank", {"selection": {"selected_rank": "nan"}})[0:2] == ("err", "ValueError")  # int(nan) not caught
    assert check(orig_nodes, monkeypatch, "_selected_rank", {"selection": {"selected_rank": "inf"}})[0:2] == ("err", "OverflowError")
    assert check(orig_nodes, monkeypatch, "_selected_rank", None)[0] == "err"
    seen = []
    out = check(orig_nodes, monkeypatch, "_selected_rank", _m(3), overrides={"_num": lambda v: seen.append(v) or 42.9, "_mapping": lambda v: v if isinstance(v, dict) else {}})
    assert out == 42 and seen == [3, 3]


# ---- A50-3 _score_gap ----
def _g(top=None, sel=None):
    s = {}
    if top is not None:
        s["scanner_top1"] = {"score_total": top}
    if sel is not None:
        s["selected_candidate"] = {"score_total": sel}
    return {"selection": s}


SG = [{}, {"selection": None}, _g(), _g(10), _g(None, 5), _g(10, 4), _g(4, 10), _g(5, 5), _g("7.5", "2.25"), _g(1.0000004, 1.0000001), _g(0, 0), _g("x", 1), _g(1, "x"), _g(NAN, 1), _g(float("inf"), 1),
      {"selection": {"scanner_top1": "bad", "selected_candidate": "bad"}}, _g(1e-7, 0)]


@pytest.mark.parametrize("model", SG)
def test_score_gap(orig_nodes, monkeypatch, guards, model):
    check(orig_nodes, monkeypatch, "_score_gap", model)


def test_score_gap_exact_and_seams(orig_nodes, monkeypatch, guards):
    assert check(orig_nodes, monkeypatch, "_score_gap", _g(10, 4)) == 6.0 and check(orig_nodes, monkeypatch, "_score_gap", _g(4, 10)) == -6.0 and check(orig_nodes, monkeypatch, "_score_gap", _g(0, 0)) == 0.0
    assert check(orig_nodes, monkeypatch, "_score_gap", _g(1.0004, 1.0001)) == 0.0003 and check(orig_nodes, monkeypatch, "_score_gap", _g(1.0000004, 1.0000001)) == 0.0 and check(orig_nodes, monkeypatch, "_score_gap", _g(10)) is None
    assert check(orig_nodes, monkeypatch, "_score_gap", None)[0] == "err"
    out = check(orig_nodes, monkeypatch, "_score_gap", _g(1, 1), overrides={"_num": lambda v: 5.5 if v == 1 else None})
    assert out == 0.0

    class NeverMapping:
        pass
    assert check(orig_nodes, monkeypatch, "_score_gap", _g(10, 4), overrides={"Mapping": NeverMapping}) is None


# ---- A50-4 _outcome_return ----
def _ev(ev_ret=None, model_ret=None, ev_raw=None, model_raw=None):
    ev = {} if ev_raw is None else ev_raw
    md = {} if model_raw is None else model_raw
    if ev_ret is not None:
        ev = {"realized_outcome": {"net_return_pct": ev_ret}}
    if model_ret is not None:
        md = {"outcome": {"net_return_pct": model_ret}}
    return ev, md


OR = [_ev(), _ev(1.5), _ev(None, 2.5), _ev(1.5, 2.5), _ev(0, 2.5), _ev("3", "4"), _ev("x", 4), _ev("x", "y"), _ev("", ""), _ev(NAN, 1), _ev(ev_raw={"realized_outcome": "bad"}, model_raw={"outcome": "bad"}),
      _ev(ev_raw={"realized_outcome": {"net_return_pct": 0}}, model_raw={"outcome": {"net_return_pct": 7}}), ({}, {}), (None, {}), ({}, None)]


@pytest.mark.parametrize("pair", OR)
def test_outcome_return(orig_nodes, monkeypatch, guards, pair):
    check(orig_nodes, monkeypatch, "_outcome_return", pair[0], pair[1])


def test_outcome_return_exact_and_seams(orig_nodes, monkeypatch, guards):
    assert check(orig_nodes, monkeypatch, "_outcome_return", *_ev(0, 2.5)) == 0.0  # evaluation 0.0 wins (not None)
    assert check(orig_nodes, monkeypatch, "_outcome_return", *_ev("x", 4)) == 4.0 and check(orig_nodes, monkeypatch, "_outcome_return", *_ev()) is None
    assert check(orig_nodes, monkeypatch, "_outcome_return", None, {})[0] == "err"
    seen = []
    out = check(orig_nodes, monkeypatch, "_outcome_return", *_ev(1, 2), overrides={"_num": lambda v: seen.append(v) or None})
    assert out is None and seen == [1, 2, 1, 2]


# ---- A50-5 _impact_score ----
@pytest.mark.parametrize("returns", [[], [1.0], [-1.0], [0.0], [-1.5, 2.0, -0.25], [-0.00004, -0.00004], [NAN], [-1, 0, 1], [-1e-9], (-1, -2), {-1.0, 2.0}, ["-1"], [None], None, [-0.12345, -0.00006], [float("-inf")]])
def test_impact_score(orig_nodes, monkeypatch, guards, returns):
    check(orig_nodes, monkeypatch, "_impact_score", returns)


def test_impact_score_exact(orig_nodes, monkeypatch, guards):
    assert check(orig_nodes, monkeypatch, "_impact_score", [-1.5, 2.0, -0.25]) == -1.75 and check(orig_nodes, monkeypatch, "_impact_score", []) == 0 and check(orig_nodes, monkeypatch, "_impact_score", [1.0]) == 0
    assert check(orig_nodes, monkeypatch, "_impact_score", [-0.12345, -0.00006]) == -0.1235
    assert check(orig_nodes, monkeypatch, "_impact_score", ["-1"])[0:2] == ("err", "TypeError") and check(orig_nodes, monkeypatch, "_impact_score", None)[0:2] == ("err", "TypeError")
    gen_consumed = []

    def gen():
        for v in (-1.0, 2.0):
            gen_consumed.append(v)
            yield v
    assert SAR._impact_score(gen()) == -1.0 and gen_consumed == [-1.0, 2.0]


# ---- A50-6 _diagnostic_kind ----
@pytest.mark.parametrize("cause", ["Scanner Ranking Failure", "Aligned / No Alignment Issue", "Missing Evidence", "Rank Drift", "Strategist Override", "Candidate Filtering", "Symbol Mapping", "", "unknown", None, 5, " Missing Evidence"])
def test_diagnostic_kind(orig_nodes, monkeypatch, guards, cause):
    check(orig_nodes, monkeypatch, "_diagnostic_kind", cause)


def test_diagnostic_kind_exact_and_seams(orig_nodes, monkeypatch, guards):
    assert check(orig_nodes, monkeypatch, "_diagnostic_kind", "Scanner Ranking Failure") == "outcome_conditioned" and check(orig_nodes, monkeypatch, "_diagnostic_kind", "Missing Evidence") == "evidence_gap"
    assert check(orig_nodes, monkeypatch, "_diagnostic_kind", "Rank Drift") == "structural"
    assert check(orig_nodes, monkeypatch, "_diagnostic_kind", [])[0:2] == ("err", "TypeError")  # unhashable cause
    assert check(orig_nodes, monkeypatch, "_diagnostic_kind", "Rank Drift", overrides={"OUTCOME_CONDITIONED_CAUSES": {"Rank Drift"}}) == "outcome_conditioned"


def test_diagnostic_kind_evidence_gap_seam(orig_nodes, monkeypatch, guards):
    assert check(orig_nodes, monkeypatch, "_diagnostic_kind", "Rank Drift", overrides={"EVIDENCE_GAP_CAUSES": {"Rank Drift"}}) == "evidence_gap"


# ---- A50-7 _largest_cause ----
def _row(cause, count, impact=0.0):
    return {"root_cause": cause, "trade_count": count, "negative_impact_pct": impact}


CS = [[], [_row("A", 0)], [_row("A", 1)], [_row("A", 1, -2.0), _row("B", 1, -3.0)], [_row("A", 2, -1.0), _row("B", 1, -9.0)], [_row("A", 2, -1.0), _row("B", 2, 1.0)], [_row("A", 2, -1.0), _row("B", 2, -1.0)],
      [_row("A", "x")], [{"root_cause": "A"}], [{"trade_count": "3", "negative_impact_pct": "-4"}], ["bad"], [_row("A", 1, "x")], [_row(None, 1, -1.0)], [_row("한글", 2, -5.5)]]


@pytest.mark.parametrize("summary", CS)
@pytest.mark.parametrize("excluded", ["omit", None, set(), {"A"}, {"A", "B"}, {""}])
def test_largest_cause(orig_nodes, monkeypatch, guards, summary, excluded):
    if excluded == "omit":
        check(orig_nodes, monkeypatch, "_largest_cause", summary)
    else:
        check(orig_nodes, monkeypatch, "_largest_cause", summary, excluded=excluded)


def test_largest_cause_exact_and_errors(orig_nodes, monkeypatch, guards):
    assert check(orig_nodes, monkeypatch, "_largest_cause", CS[4]) == _row("A", 2, -1.0)  # count first, then |impact|
    assert check(orig_nodes, monkeypatch, "_largest_cause", CS[5]) == _row("A", 2, -1.0)  # equal count and equal |impact| -> max keeps the first
    assert check(orig_nodes, monkeypatch, "_largest_cause", CS[6]) == _row("A", 2, -1.0)  # full tie -> first element (max keeps first)
    assert check(orig_nodes, monkeypatch, "_largest_cause", CS[3], excluded={"B"}) == _row("A", 1, -2.0) and check(orig_nodes, monkeypatch, "_largest_cause", []) == {}
    src = _row("A", 1)
    out = SAR._largest_cause([src])
    assert out == src and out is not src  # copy, not the same dict
    assert check(orig_nodes, monkeypatch, "_largest_cause", None)[0:2] == ("err", "TypeError") and check(orig_nodes, monkeypatch, "_largest_cause", CS[7])[0:2] == ("err", "ValueError")
    sig = inspect.signature(SAR._largest_cause)
    assert [p.kind.name for p in sig.parameters.values()] == ["POSITIONAL_OR_KEYWORD", "KEYWORD_ONLY"] and sig.parameters["excluded"].default is None


# ---- A50-8 _patch_candidate ----
@pytest.mark.parametrize("cause", ["Candidate Filtering", "Strategist Override", "Rank Drift", "Scanner Ranking Failure", "Symbol Mapping", "Missing Evidence", "Aligned / No Alignment Issue", "", "other", None, 5, " Rank Drift", "rank drift"])
def test_patch_candidate(orig_nodes, monkeypatch, guards, cause):
    check(orig_nodes, monkeypatch, "_patch_candidate", cause)


def test_patch_candidate_exact(orig_nodes, monkeypatch, guards):
    assert check(orig_nodes, monkeypatch, "_patch_candidate", "Candidate Filtering") == "Tighten runner-up/candidate filtering evidence before selecting below post-strategy top1."
    assert check(orig_nodes, monkeypatch, "_patch_candidate", "Strategist Override") == "Audit strategy-context rank adjustments before allowing post-strategy top1 to replace raw top1."
    assert check(orig_nodes, monkeypatch, "_patch_candidate", "Rank Drift") == "Require explicit rank-drift reason and score-gap evidence when Top1 changes."
    assert check(orig_nodes, monkeypatch, "_patch_candidate", "Scanner Ranking Failure") == "Decompose scanner raw score components for aligned losing Top1 trades."
    assert check(orig_nodes, monkeypatch, "_patch_candidate", "Symbol Mapping") == "Fix symbol propagation before any trading behavior patch."
    assert check(orig_nodes, monkeypatch, "_patch_candidate", "Missing Evidence") == "Fix missing selection evidence before interpreting scanner alignment."
    assert check(orig_nodes, monkeypatch, "_patch_candidate", "anything else") == "No scanner-alignment behavior patch candidate from aligned rows."


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
