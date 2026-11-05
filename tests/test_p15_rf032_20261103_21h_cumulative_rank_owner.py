"""RF-032 A57-1: ``cumulative_improvement_review._rank_row``, original vs thin wrappers + Owners.

Original = A preimage a0149439 (SOURCE blob a2f64696 == canonical f804efdd). Each original function is compiled from
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

A_PRE = "a0149439392300f94876e553e11d99fec053d1d5"
CANON = "f804efddedea841a0df36da441118e511080e548"
EV = "libs/reporting/evaluation/"
# name -> (source stem, pinned blob, owner module stem)
SPEC = {
    "_rank_row": ("cumulative_improvement_review", "a2f64696546cb729afd7c5b89d9d1c1e06edeac7", "cumulative_improvement_review_rank_row", "_rank_row"),
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
                out[n] = [x for x in tree.body if isinstance(x, ast.FunctionDef) and x.name == v[3]][-1]
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
    fname = SPEC[name][3]
    for k, v in (overrides or {}).items():
        ns[k] = v
        monkeypatch.setattr(mod, k, v)
    got, values = {}, {}
    for label, fn in (("orig", ns[fname]), ("new", getattr(mod, fname))):
        a, k = copy.deepcopy((args, kwargs))
        try:
            values[label] = fn(*a, **k)
            got[label] = ("ok", repr(values[label]))
        except Exception as exc:
            got[label] = ("err", type(exc).__name__, str(exc))
        assert repr((a, k)) == repr((args, kwargs)), f"{label} mutated input"
    assert got["orig"] == got["new"], got
    return values["new"] if got["new"][0] == "ok" else got["new"]


CI = MODS["cumulative_improvement_review"]


class NeverMapping:
    pass


class _MapSub(dict):
    def __repr__(self):
        return f"_MapSub({dict(self)!r})"


def _row(bucket, horizon, **extra):
    return {"rank_bucket": bucket, "horizon": horizon, **extra}


ROWS = [_row("rank1", "+5m", t="r1_5"), _row("rank1", "+30m", t="r1_30_first"), _row("rank2_3", "+30m", t="r23_30"), _row("rank1", "+30m", t="r1_30_second")]
REVIEWS = {"empty": {}, "none_rows": {"rank_horizon_rows": None}, "empty_rows": {"rank_horizon_rows": []}, "rows": {"rank_horizon_rows": ROWS}, "non_mapping_rows": {"rank_horizon_rows": ["bad", None, 5, [], ROWS[1]]},
           "mapping_subclass": {"rank_horizon_rows": [_MapSub(rank_bucket="rank1", horizon="+30m", t="sub")]}, "rows_not_list": {"rank_horizon_rows": "abc"}, "rows_tuple": {"rank_horizon_rows": tuple(ROWS)},
           "rows_dict": {"rank_horizon_rows": {"rank_bucket": "rank1"}}, "rows_int": {"rank_horizon_rows": 5}, "falsy_rows": {"rank_horizon_rows": 0}, "missing_keys": {"rank_horizon_rows": [{}, {"rank_bucket": "rank1"}, {"horizon": "+30m"}]},
           "non_str_values": {"rank_horizon_rows": [{"rank_bucket": 1, "horizon": 30}]}}


@pytest.mark.parametrize("case", list(REVIEWS))
@pytest.mark.parametrize("bucket,horizon", [("rank1", "+30m"), ("rank2_3", "+30m"), ("rank1", "+5m"), ("rank4_plus", "+30m"), ("", ""), (1, 30), (None, None)])
def test_rank_row(orig_nodes, monkeypatch, guards, case, bucket, horizon):
    check(orig_nodes, monkeypatch, "_rank_row", REVIEWS[case], bucket=bucket, horizon=horizon)


def test_rank_row_first_match_identity_and_defaults(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "_rank_row", REVIEWS["rows"], bucket="rank1", horizon="+30m")
    assert out["t"] == "r1_30_first"  # first match wins, later duplicates are ignored
    assert CI._rank_row(REVIEWS["rows"], bucket="rank1", horizon="+30m") is ROWS[1]  # the matching row itself, not a copy
    miss = CI._rank_row(REVIEWS["rows"], bucket="rank9", horizon="+30m")
    assert miss == {} and miss is not CI._rank_row(REVIEWS["rows"], bucket="rank9", horizon="+30m")  # a fresh empty dict per call
    assert check(orig_nodes, monkeypatch, "_rank_row", REVIEWS["non_mapping_rows"], bucket="rank1", horizon="+30m")["t"] == "r1_30_first"  # non-Mapping rows skipped
    assert check(orig_nodes, monkeypatch, "_rank_row", REVIEWS["mapping_subclass"], bucket="rank1", horizon="+30m")["t"] == "sub"
    assert [p.kind.name for p in inspect.signature(CI._rank_row).parameters.values()] == ["POSITIONAL_OR_KEYWORD", "KEYWORD_ONLY", "KEYWORD_ONLY"]


def test_rank_row_errors(orig_nodes, monkeypatch, guards):
    assert check(orig_nodes, monkeypatch, "_rank_row", None, bucket="rank1", horizon="+30m")[0] == "err"  # None.get
    assert check(orig_nodes, monkeypatch, "_rank_row", REVIEWS["rows_not_list"], bucket="rank1", horizon="+30m") == {}
    assert check(orig_nodes, monkeypatch, "_rank_row", REVIEWS["rows_int"], bucket="rank1", horizon="+30m")[0:2] == ("err", "TypeError")
    assert check(orig_nodes, monkeypatch, "_rank_row", ["not a mapping"], bucket="rank1", horizon="+30m")[0] == "err"


def test_rank_row_generator_short_circuit(orig_nodes, monkeypatch, guards):
    consumed = []

    def lazy_rows():
        for r in ROWS:
            consumed.append(r["t"])
            yield r
    out = CI._rank_row({"rank_horizon_rows": lazy_rows()}, bucket="rank1", horizon="+5m")
    assert out["t"] == "r1_5" and consumed == ["r1_5"]  # stops at the first match
    consumed.clear()
    out = CI._rank_row({"rank_horizon_rows": lazy_rows()}, bucket="rank1", horizon="+30m")
    assert out["t"] == "r1_30_first" and consumed == ["r1_5", "r1_30_first"]


def test_rank_row_mapping_seam(orig_nodes, monkeypatch, guards):
    assert check(orig_nodes, monkeypatch, "_rank_row", REVIEWS["rows"], bucket="rank1", horizon="+30m", overrides={"Mapping": NeverMapping}) == {}  # call-time Mapping


# ---- structure ----
@pytest.mark.parametrize("name", list(SPEC))
def test_wrapper_thin_and_owner_holds_body(name):
    mod = MODS[SPEC[name][0]]
    fname = SPEC[name][3]
    wrapper = ast.parse(inspect.getsource(getattr(mod, fname))).body[0]
    stmts = [n for n in wrapper.body if not (isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant))]
    assert len(stmts) == 1 and isinstance(stmts[0], ast.Return)
    assert not [n for n in ast.walk(wrapper) if isinstance(n, (ast.If, ast.For, ast.Try, ast.ListComp, ast.GeneratorExp))]
    call = stmts[0].value
    assert isinstance(call, ast.Call) and "facade" in [k.arg for k in call.keywords], "wrapper must forward to the Owner with facade="
    owner_fn = getattr(OWNERS[name], fname)
    node = ast.parse(inspect.getsource(owner_fn)).body[0]
    assert len(node.body) >= 1 and owner_fn.__module__ == OWNERS[name].__name__
    owner_tree = ast.parse(inspect.getsource(OWNERS[name]))
    stem = SPEC[name][0]
    imported = []
    for n in ast.walk(owner_tree):
        if isinstance(n, ast.Import):
            imported += [alias.name for alias in n.names]
        elif isinstance(n, ast.ImportFrom):
            imported.append(("." * n.level) + (n.module or ""))
            imported += [alias.name for alias in n.names]
    assert not [i for i in imported if i.split(".")[-1] == stem], f"Owner must not import its SOURCE: {imported}"
