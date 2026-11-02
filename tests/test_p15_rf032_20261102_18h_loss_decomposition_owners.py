"""RF-032 A42-1..8: eight ``loss_decomposition`` bodies, original vs thin wrappers + Owners.

Original = A preimage 237434c0 (SOURCE blob 87544f1a == canonical c1c435f9). Each original function is compiled from
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

A_PRE = "237434c017aa2a7907c6c1f2bb55738582676375"
CANON = "c1c435f91f301e822b7c3f27bb24b9ebc2fd7ae8"
EV = "libs/reporting/evaluation/"
# name -> (source stem, pinned blob, owner module stem)
SPEC = {
    "_to_float": ("loss_decomposition", "87544f1ad77e164389fce354c02680d70b98f7f7", "loss_decomposition_to_float"),
    "_parse_ts": ("loss_decomposition", "87544f1ad77e164389fce354c02680d70b98f7f7", "loss_decomposition_parse_ts"),
    "_iter_days": ("loss_decomposition", "87544f1ad77e164389fce354c02680d70b98f7f7", "loss_decomposition_iter_days"),
    "_checkpoint_return": ("loss_decomposition", "87544f1ad77e164389fce354c02680d70b98f7f7", "loss_decomposition_checkpoint_return"),
    "_rank_bucket": ("loss_decomposition", "87544f1ad77e164389fce354c02680d70b98f7f7", "loss_decomposition_rank_bucket"),
    "_candidate_rows": ("loss_decomposition", "87544f1ad77e164389fce354c02680d70b98f7f7", "loss_decomposition_candidate_rows"),
    "_group_forward": ("loss_decomposition", "87544f1ad77e164389fce354c02680d70b98f7f7", "loss_decomposition_group_forward"),
    "_realized_trade_summary": ("loss_decomposition", "87544f1ad77e164389fce354c02680d70b98f7f7", "loss_decomposition_realized_trade_summary"),
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


class _Str:
    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return f"_Str({self.text!r})"

    def __str__(self):
        return self.text


class _FloatRaises:
    def __init__(self, exc):
        self.exc = exc

    def __repr__(self):
        return f"_FloatRaises({self.exc.__name__})"

    def __float__(self):
        raise self.exc("custom float failure")


class _Num:
    def __repr__(self):
        return "_Num()"

    def __float__(self):
        return 2.5

    def __int__(self):
        return 7


def _same(a, b):
    return repr(a) == repr(b)


# ---- A42-1 _to_float ----
@pytest.mark.parametrize("value", [None, "", 0, 0.0, "0", " 1.5 ", "abc", "1e3", "nan", "inf", "-inf", NAN, True, [], {}, b"2", "１２", _Num(), _FloatRaises(TypeError),
                                   _FloatRaises(ValueError), (), "-0"])
def test_to_float_values(orig_nodes, monkeypatch, guards, value):
    check(orig_nodes, monkeypatch, "_to_float", value)


def test_to_float_exact_and_not_broadened(orig_nodes, monkeypatch, guards):
    assert check(orig_nodes, monkeypatch, "_to_float", None) is None and check(orig_nodes, monkeypatch, "_to_float", "") is None
    assert check(orig_nodes, monkeypatch, "_to_float", 0) == 0.0 and check(orig_nodes, monkeypatch, "_to_float", "x") is None
    assert check(orig_nodes, monkeypatch, "_to_float", _FloatRaises(TypeError)) is None
    assert check(orig_nodes, monkeypatch, "_to_float", _FloatRaises(ValueError)) is None
    assert check(orig_nodes, monkeypatch, "_to_float", _FloatRaises(RuntimeError)) == ("err", "RuntimeError", "custom float failure")  # not caught
    out = check(orig_nodes, monkeypatch, "_to_float", "nan")
    assert out != out  # NaN preserved


# ---- A42-2 _parse_ts ----
@pytest.mark.parametrize("value", ["2026-04-10T09:00:00Z", "2026-04-10T09:00:00+09:00", "2026-04-10T09:00:00", "2026-04-10", "", None, 0, "garbage", "2026-13-01",
                                   "2026-04-10T09:00:00.123456Z", _Str("2026-04-10T01:02:03Z"), _Str("bad"), 123, ["x"], "ZZ", "2026-04-10 09:00:00z"])
def test_parse_ts_values(orig_nodes, monkeypatch, guards, value):
    check(orig_nodes, monkeypatch, "_parse_ts", value)


def test_parse_ts_exact_and_seam(orig_nodes, monkeypatch, guards):
    import datetime as dt
    out = check(orig_nodes, monkeypatch, "_parse_ts", "2026-04-10T09:00:00Z")
    assert out == dt.datetime(2026, 4, 10, 9, 0, tzinfo=dt.timezone.utc) and out.tzinfo is not None
    assert check(orig_nodes, monkeypatch, "_parse_ts", "2026-04-10T09:00:00").tzinfo is None
    assert check(orig_nodes, monkeypatch, "_parse_ts", "") is None and check(orig_nodes, monkeypatch, "_parse_ts", None) is None

    class Boom:
        @staticmethod
        def fromisoformat(text):
            raise TypeError("type failure")  # only ValueError is caught
    assert check(orig_nodes, monkeypatch, "_parse_ts", "2026-04-10", overrides={"datetime": Boom}) == ("err", "TypeError", "type failure")

    class Seen:
        calls = []

        @staticmethod
        def fromisoformat(text):
            Seen.calls.append(text)
            return text
    assert check(orig_nodes, monkeypatch, "_parse_ts", "AZ", overrides={"datetime": Seen}) == "A+00:00" and Seen.calls == ["A+00:00", "A+00:00"]


# ---- A42-3 _iter_days (generator) ----
def _gen_both(orig_nodes, monkeypatch, start, end, overrides=None):
    mod = MODS["loss_decomposition"]
    ns = dict(vars(mod))
    exec(compile(ast.fix_missing_locations(ast.Module(body=[copy.deepcopy(orig_nodes["_iter_days"])], type_ignores=[])), "<orig>", "exec"), ns)
    for k, v in (overrides or {}).items():
        ns[k] = v
        monkeypatch.setattr(mod, k, v)
    res = {}
    for label, fn in (("orig", ns["_iter_days"]), ("new", mod._iter_days)):
        gen = fn(start, end)  # creation must not raise (lazy)
        assert inspect.isgenerator(gen)
        try:
            res[label] = ("ok", list(gen))
        except Exception as exc:
            res[label] = ("err", type(exc).__name__, str(exc))
    assert res["orig"] == res["new"], res
    return res["new"]


@pytest.mark.parametrize("start,end", [("2026-04-10", "2026-04-10"), ("2026-04-10", "2026-04-13"), ("2026-04-13", "2026-04-10"), ("2024-02-28", "2024-03-01"),
                                       ("2025-02-28", "2025-03-01"), ("2026-12-30", "2027-01-02"), ("2026-04-10T09:00", "2026-04-11T23:59"), ("bad", "2026-04-10"),
                                       ("2026-04-10", "bad"), ("2026-13-01", "2026-04-10"), ("", ""), ("2026-04-10", "2026-04-10 trailing")])
def test_iter_days(orig_nodes, monkeypatch, guards, start, end):
    _gen_both(orig_nodes, monkeypatch, start, end)


def test_iter_days_exact_laziness_and_seams(orig_nodes, monkeypatch, guards):
    assert _gen_both(orig_nodes, monkeypatch, "2024-02-28", "2024-03-01") == ("ok", ["2024-02-28", "2024-02-29", "2024-03-01"])
    assert _gen_both(orig_nodes, monkeypatch, "2026-04-13", "2026-04-10") == ("ok", [])
    mod = MODS["loss_decomposition"]
    gen = mod._iter_days("bad", "worse")  # exception timing: only on first next()
    with pytest.raises(ValueError):
        next(gen)
    gen = mod._iter_days("2026-04-10", "2026-04-12")
    assert next(gen) == "2026-04-10" and next(gen) == "2026-04-11"
    import datetime as dt
    out = _gen_both(orig_nodes, monkeypatch, "2026-04-10", "2026-04-11", overrides={"timedelta": lambda days: dt.timedelta(days=2 * days)})
    assert out == ("ok", ["2026-04-10"])



def test_iter_days_date_seam(orig_nodes, monkeypatch, guards):
    import datetime as dt

    class FakeDate:
        @staticmethod
        def fromisoformat(text):
            return dt.date(2000, 1, 1) if text.startswith("s") else dt.date(2000, 1, 2)
    assert _gen_both(orig_nodes, monkeypatch, "start", "end", overrides={"date": FakeDate}) == ("ok", ["2000-01-01", "2000-01-02"])


# ---- A42-4 _checkpoint_return ----
def _row(cp, **extra):
    return {"shadow_forward_outcome": {"checkpoints": cp, **extra}}


ROWS_CP = [{}, None, "row", {"shadow_forward_outcome": None}, {"shadow_forward_outcome": "x"}, _row(None), _row("x"), _row({}), _row({"+5m": None}), _row({"+5m": "x"}),
           _row({"+5m": {}}), _row({"+5m": {"status": "pending", "return_pct": 1}}), _row({"+5m": {"status": "observed"}}), _row({"+5m": {"status": "observed", "return_pct": 0}}),
           _row({"+5m": {"status": "observed", "return_pct": "1.25"}}), _row({"+5m": {"status": "observed", "return_pct": "bad"}}), _row({"+5m": {"status": "observed", "return_pct": ""}}),
           _row({"+15m": {"status": "observed", "return_pct": -2}}), _row({"+5m": {"status": "OBSERVED", "return_pct": 1}})]


@pytest.mark.parametrize("row", ROWS_CP)
@pytest.mark.parametrize("label", ["+5m", "+15m", "missing"])
def test_checkpoint_return(orig_nodes, monkeypatch, guards, row, label):
    check(orig_nodes, monkeypatch, "_checkpoint_return", row, label)


def test_checkpoint_return_none_vs_zero_and_seams(orig_nodes, monkeypatch, guards):
    assert check(orig_nodes, monkeypatch, "_checkpoint_return", _row({"+5m": {"status": "observed", "return_pct": 0}}), "+5m") == 0.0
    assert check(orig_nodes, monkeypatch, "_checkpoint_return", _row({"+5m": {"status": "observed"}}), "+5m") is None
    seen = []
    out = check(orig_nodes, monkeypatch, "_checkpoint_return", _row({"+5m": {"status": "observed", "return_pct": "7"}}), "+5m",
                overrides={"_to_float": lambda v: seen.append(v) or 99.0})
    assert out == 99.0 and seen == ["7", "7"]

    class NeverMapping:
        pass
    assert check(orig_nodes, monkeypatch, "_checkpoint_return", _row({"+5m": {"status": "observed", "return_pct": 1}}), "+5m", overrides={"Mapping": NeverMapping}) is None
    assert check(orig_nodes, monkeypatch, "_checkpoint_return", None, "+5m")[0] == "err"  # row.get on None


# ---- A42-5 _rank_bucket ----
@pytest.mark.parametrize("value", [1, 2, 3, 4, 5, 6, 10, 11, 100, 0, -1, -100, 1.9, 3.5, "1", "2.7", " 4 ", "5.0", "10", "abc", "", None, [], {}, NAN, float("inf"), float("-inf"),
                                   True, "nan", "1e1", 0.9, _Num()])
def test_rank_bucket(orig_nodes, monkeypatch, guards, value):
    check(orig_nodes, monkeypatch, "_rank_bucket", value)


def test_rank_bucket_exact(orig_nodes, monkeypatch, guards):
    exp = {1: "rank1", 2: "rank2-3", 3: "rank2-3", 4: "rank4-5", 5: "rank4-5", 6: "rank6-10", 10: "rank6-10", 11: "rank11+", 0: "rank2-3", -3: "rank2-3"}
    for rank, name in exp.items():
        assert check(orig_nodes, monkeypatch, "_rank_bucket", rank) == name
    assert check(orig_nodes, monkeypatch, "_rank_bucket", "x") == "unknown" and check(orig_nodes, monkeypatch, "_rank_bucket", None) == "unknown"
    assert check(orig_nodes, monkeypatch, "_rank_bucket", NAN) == "unknown"  # int(nan) raises ValueError -> caught
    assert check(orig_nodes, monkeypatch, "_rank_bucket", float("inf")) == ("err", "OverflowError", "cannot convert float infinity to integer")  # not caught


# ---- A42-6 _candidate_rows ----
def _fakes():
    log = []

    def attach(rows):
        log.append(("attach", copy.deepcopy(rows)))
        return [{**r, "attached": True} for r in rows]

    def dedupe(rows):
        log.append(("dedupe", copy.deepcopy(rows)))
        return list(reversed(rows))
    return attach, dedupe, log


PAYLOADS_CR = [[], [{}], [{"candidates": None}], [{"candidates": []}], [{"generated_at": "g", "candidates": [{"a": 1}, "bad", None, {"b": 2, "_payload_generated_at": "keep"}]}],
               [{"generated_at": "g1", "candidates": [{"a": 1}]}, {"generated_at": "g2", "candidates": [{"a": 1}, {"a": 1}]}], [{"candidates": [{"a": 1}]}]]


@pytest.mark.parametrize("payloads", PAYLOADS_CR)
def test_candidate_rows_fake_seams(orig_nodes, monkeypatch, guards, payloads):
    attach, dedupe, log = _fakes()
    check(orig_nodes, monkeypatch, "_candidate_rows", payloads, overrides={"attach_forward_outcomes": attach, "dedupe_q8_candidates": dedupe})
    half = len(log) // 2
    assert half * 2 == len(log) and log[:half] == log[half:]  # identical call sequence per side


def test_candidate_rows_order_copy_and_errors(orig_nodes, monkeypatch, guards):
    attach, dedupe, log = _fakes()
    src = {"a": 1}
    payload = [{"generated_at": "g", "candidates": [src]}]
    out = check(orig_nodes, monkeypatch, "_candidate_rows", payload, overrides={"attach_forward_outcomes": attach, "dedupe_q8_candidates": dedupe})
    assert [c[0] for c in log] == ["attach", "dedupe", "attach", "dedupe"] and out == [{"a": 1, "_payload_generated_at": "g", "attached": True}] and "_payload_generated_at" not in src
    assert check(orig_nodes, monkeypatch, "_candidate_rows", None, overrides={"attach_forward_outcomes": attach, "dedupe_q8_candidates": dedupe})[0] == "err"
    assert check(orig_nodes, monkeypatch, "_candidate_rows", ["x"], overrides={"attach_forward_outcomes": attach, "dedupe_q8_candidates": dedupe})[0] == "err"

    def boom(rows):
        raise RuntimeError("attach failure")
    assert check(orig_nodes, monkeypatch, "_candidate_rows", payload, overrides={"attach_forward_outcomes": boom, "dedupe_q8_candidates": dedupe}) == ("err", "RuntimeError", "attach failure")

    class NeverMapping:
        pass
    assert check(orig_nodes, monkeypatch, "_candidate_rows", payload, overrides={"Mapping": NeverMapping, "attach_forward_outcomes": attach, "dedupe_q8_candidates": dedupe}) == []


def test_candidate_rows_real_helpers(orig_nodes, monkeypatch, guards):
    # real in-memory helpers (no minute data -> pure projection); same behaviour on both sides
    payload = [{"generated_at": "2026-04-10T00:00:00+00:00", "candidates": [{"symbol": "005930", "quant_tactic_id": "t1"}, {"symbol": "000660", "quant_tactic_id": "t2"}]}]
    check(orig_nodes, monkeypatch, "_candidate_rows", payload)


# ---- A42-7 _group_forward ----
def _gc(sym, **cps):
    return {"symbol": sym, "shadow_forward_outcome": {"checkpoints": {h: {"status": "observed", "return_pct": v} for h, v in cps.items()}}}


GF_ROWS = [[], [_gc("A")], [_gc("A", **{"+5m": 1.0}), _gc("A", **{"+5m": 2.0, "+15m": -1.0}), _gc("B", **{"+60m": 0.5}), _gc("C"), {"symbol": None}],
           [_gc("B", **{"+5m": 1.0}), _gc("A", **{"+5m": 1.0})], [_gc("A", **{"+5m": 0.33333, "+15m": 0.66666, "+30m": 1.0, "+60m": 2.0}), _gc("A", **{"+30m": 0.1})], [{"x": 1}, {"symbol": ""}, {"symbol": 0}]]


@pytest.mark.parametrize("rows", GF_ROWS)
def test_group_forward(orig_nodes, monkeypatch, guards, rows):
    check(orig_nodes, monkeypatch, "_group_forward", rows, lambda r: r.get("symbol"))


def test_group_forward_exact_order_and_seams(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "_group_forward", GF_ROWS[2], lambda r: r.get("symbol"))
    assert [r["name"] for r in out] == ["A", "B", "C", "unknown"]  # None -> "unknown" bucket, sorted last by observed_count/name
    a = out[0]
    assert list(a)[:3] == ["name", "candidate_count", "observed_5m"] and a["avg_return_5m_pct"] == 1.5 and a["coverage"] == 1.0 and a["observed_count"] == 2
    ties = check(orig_nodes, monkeypatch, "_group_forward", [_gc("B", **{"+5m": 1}), _gc("A", **{"+5m": 1})], lambda r: r["symbol"])
    assert [r["name"] for r in ties] == ["A", "B"]  # same observed_count -> name ascending
    out = check(orig_nodes, monkeypatch, "_group_forward", [{"k": 1}, {"k": 2}, {"k": 3}], lambda r: "g", overrides={"_checkpoint_return": lambda row, h: float(row["k"]) if h == "+5m" and row["k"] != 2 else None})
    assert out[0]["observed_5m"] == 2 and out[0]["avg_return_5m_pct"] == 2.0 and out[0]["coverage"] == 0.6667
    assert check(orig_nodes, monkeypatch, "_group_forward", [{"k": 1}], lambda r: (_ for _ in ()).throw(KeyError("kf")))[0] == "err"
    assert check(orig_nodes, monkeypatch, "_group_forward", None, lambda r: "x")[0] == "err"

    made = []
    import collections

    def spy_defaultdict(factory):
        made.append(1)
        return collections.defaultdict(factory)
    check(orig_nodes, monkeypatch, "_group_forward", [{"k": 1}], lambda r: "g", overrides={"defaultdict": spy_defaultdict})
    assert made == [1, 1]


# ---- A42-8 _realized_trade_summary ----
def _m(ret=None, rank=None, selected="AAA", top1=None, outcome=True):
    m = {"selection": {"selected_rank": rank, "selected_symbol": selected, "scanner_top1": top1}}
    if outcome:
        m["outcome"] = {"net_return_pct": ret}
    return m


RTS_CASES = [[], [{}], [_m()], [_m(outcome=False)], [_m(0.0, 1)], [_m(1.5, 1), _m(-2.0, 2, top1={"symbol": "BBB"}), _m(0.3, 12, top1={"symbol": "AAA"}), _m("bad", 3), _m("2", "x")],
             [_m(1.0, 5, top1="notmapping"), _m(1.0, 5, top1={"symbol": ""}), _m(1.0, 6, selected=None, top1={"symbol": "Z"})], [{"outcome": None, "selection": None}],
             [{"outcome": {"net_return_pct": 1.0}}], [_m(1.0, 1)] * 3]


@pytest.mark.parametrize("models", RTS_CASES)
def test_realized_trade_summary(orig_nodes, monkeypatch, guards, models):
    check(orig_nodes, monkeypatch, "_realized_trade_summary", models)


def test_realized_trade_summary_exact_and_seams(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "_realized_trade_summary", RTS_CASES[5])
    assert list(out) == ["performance", "by_executed_rank", "scanner_top1_execution_mismatch_count", "comparable_trade_count"]
    assert out["comparable_trade_count"] == 4 and out["scanner_top1_execution_mismatch_count"] == 1
    assert [r["rank_bucket"] for r in out["by_executed_rank"]] == ["rank1", "rank11+", "rank2-3", "unknown"]  # sorted by bucket name
    assert check(orig_nodes, monkeypatch, "_realized_trade_summary", [])["comparable_trade_count"] == 0
    calls = []
    out = check(orig_nodes, monkeypatch, "_realized_trade_summary", [_m(1.0, 1), _m(2.0, 9)],
                overrides={"_to_float": lambda v: float(v) * 10 if v is not None else None, "_rank_bucket": lambda v: f"B{v}",
                           "performance_metrics": lambda values: calls.append(list(values)) or {"n": len(values)}})
    assert out == {"performance": {"n": 2}, "by_executed_rank": [{"rank_bucket": "B1", "n": 1}, {"rank_bucket": "B9", "n": 1}],
                   "scanner_top1_execution_mismatch_count": 0, "comparable_trade_count": 2}
    assert calls[0] == [10.0, 20.0] and len(calls) == 6  # 3 calls per side

    class NeverMapping:
        pass
    out = check(orig_nodes, monkeypatch, "_realized_trade_summary", [_m(1.0, 1, selected="X", top1={"symbol": "Y"})], overrides={"Mapping": NeverMapping})
    assert out["scanner_top1_execution_mismatch_count"] == 0
    assert check(orig_nodes, monkeypatch, "_realized_trade_summary", None)[0] == "err"
    assert check(orig_nodes, monkeypatch, "_realized_trade_summary", [None])[0] == "err"


# ---- structure ----
@pytest.mark.parametrize("name", list(SPEC))
def test_wrapper_thin_and_owner_holds_body(name):
    mod = MODS[SPEC[name][0]]
    wrapper = ast.parse(inspect.getsource(getattr(mod, name))).body[0]
    stmts = [n for n in wrapper.body if not (isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant))]
    assert len(stmts) == 1
    if name == "_iter_days":  # generator wrapper delegates lazily with a single ``yield from``
        assert isinstance(stmts[0], ast.Expr) and isinstance(stmts[0].value, ast.YieldFrom)
        stmts = [ast.Return(value=stmts[0].value.value)]
    assert isinstance(stmts[0], ast.Return)
    assert not [n for n in ast.walk(wrapper) if isinstance(n, (ast.If, ast.For, ast.Try, ast.ListComp, ast.GeneratorExp))]
    call = stmts[0].value
    assert isinstance(call, ast.Call) and "facade" in [k.arg for k in call.keywords], "wrapper must forward to the Owner with facade="
    owner_fn = getattr(OWNERS[name], name)
    node = ast.parse(inspect.getsource(owner_fn)).body[0]
    assert len(node.body) >= 1 and owner_fn.__module__ == OWNERS[name].__name__
    src = inspect.getsource(OWNERS[name])
    stem = SPEC[name][0]
    assert f"import {stem}" not in src and f"{stem} import" not in src.replace("from . import", "") and f"from .{stem} " not in src
