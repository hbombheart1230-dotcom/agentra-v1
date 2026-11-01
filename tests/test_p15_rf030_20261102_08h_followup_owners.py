"""RF-030 A32-1..8: six ``operator_period_summary`` + two ``operator_summary_refresh`` helpers, original vs wrappers + Owners.

Originals: A preimage 85efc323 (period_summary blob 84003eb4, summary_refresh blob 91b2549c); canonical 871c311f has the
same blobs. AST-extracted and compiled in a copy of the live namespace; dependency overrides apply to both sides.
Pure/fake only: no file reads, writes, sockets or subprocess.
"""
from __future__ import annotations

import ast
import builtins
import copy
import datetime as _dt
import hashlib
import importlib
import inspect
import socket
import subprocess
from pathlib import Path

import pytest

A_PRE = "85efc32349af1d7a3626f8ff54a218fe46105213"
CANON = "871c311f98e4fc512291520886d2bf7b7056a26e"
SRC = {
    "libs/reporting/operator_period_summary.py": "84003eb42fc5e5b1c3ac39b7026ce53988ea7ea4",
    "libs/reporting/operator_summary_refresh.py": "91b2549c307fd1c35102bc4bd31e665254606507",
}
PER = ["_as_dict", "_trade_action", "_row_report_day", "_same_day_new_trade_rows", "_is_recovered_partial_marker", "_performance_source_rows"]
REF = ["_parse_day", "_summary_ref"]
ops = importlib.import_module("libs.reporting.operator_period_summary")
osr = importlib.import_module("libs.reporting.operator_summary_refresh")
MODS = {**{n: ops for n in PER}, **{n: osr for n in REF}}
STEM = {**{n: "operator_period_summary" for n in PER}, **{n: "operator_summary_refresh" for n in REF}}
FILE = {**{n: "libs/reporting/operator_period_summary.py" for n in PER}, **{n: "libs/reporting/operator_summary_refresh.py" for n in REF}}
NAMES = PER + REF
OWNERS = {n: importlib.import_module(f"libs.reporting.{STEM[n]}_{n.lstrip('_')}") for n in NAMES}


def _sha(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + bytes([0]) + raw).hexdigest()


@pytest.fixture(scope="module")
def orig_nodes():
    nodes = {}
    for path, blob in SRC.items():
        try:
            a_raw = subprocess.run(["git", "show", f"{A_PRE}:{path}"], check=True, capture_output=True).stdout
            c_raw = subprocess.run(["git", "show", f"{CANON}:{path}"], check=True, capture_output=True).stdout
        except subprocess.CalledProcessError as exc:
            pytest.fail(f"BLOCKED_PIN: {exc.stderr!r}")
        assert _sha(a_raw) == blob, f"BLOCKED_PIN actor blob {path}"
        assert _sha(c_raw) == blob, f"BLOCKED_PIN canonical blob {path}"
        tree = ast.parse(a_raw.decode("utf-8"))
        wanted = [n for n in NAMES if FILE[n] == path]
        found = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in wanted}
        assert sorted(found) == sorted(wanted)
        nodes.update(found)
    return nodes


@pytest.fixture
def guards(monkeypatch):
    def boom(*a, **k):
        raise AssertionError("effect attempted")
    monkeypatch.setattr(subprocess, "run", boom)
    monkeypatch.setattr(subprocess, "Popen", boom)
    monkeypatch.setattr(socket.socket, "connect", boom)
    for attr in ("read_text", "read_bytes", "write_text", "write_bytes", "mkdir", "touch", "unlink", "rename", "replace", "exists", "is_file", "is_dir"):
        monkeypatch.setattr(Path, attr, boom)
    real_open = builtins.open

    def guarded_open(file, mode="r", *a, **k):
        if any(c in str(mode) for c in "wax+"):
            raise AssertionError("write open attempted")
        return real_open(file, mode, *a, **k)
    monkeypatch.setattr(builtins, "open", guarded_open)


def check(orig_nodes, monkeypatch, name, *args, overrides=None, **kwargs):
    mod = MODS[name]
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
    assert got["orig"] == got["new"], got
    return values["new"] if got["new"][0] == "ok" else got["new"]


def run_identity(name, *args, **kwargs):
    """Call the final wrapper once on the live objects (no deepcopy) to assert identity semantics."""
    return getattr(MODS[name], name)(*args, **kwargs)


# A32-1 _as_dict
@pytest.mark.parametrize("value", [None, {}, {"a": 1}, [], [("a", 1)], "str", 5, {"z": 1, "a": 2}])
def test_as_dict(orig_nodes, monkeypatch, guards, value):
    check(orig_nodes, monkeypatch, "_as_dict", value)


def test_as_dict_identity(guards):
    d = {"k": [1]}
    assert run_identity("_as_dict", d) is d
    e1, e2 = run_identity("_as_dict", None), run_identity("_as_dict", None)
    assert e1 == {} and e1 is not e2


# A32-2 _trade_action
@pytest.mark.parametrize("row", [{}, {"action": "buy"}, {"last_action": "sell", "action": "buy"}, {"last_action": "", "action": " Sell "},
                                 {"last_action": None, "action": None}, {"last_action": 0, "action": "x"}, {"action": 5}, {"last_action": ["a"]}, {"action": "한글"}])
def test_trade_action(orig_nodes, monkeypatch, guards, row):
    check(orig_nodes, monkeypatch, "_trade_action", row)


def test_trade_action_values(orig_nodes, monkeypatch, guards):
    assert check(orig_nodes, monkeypatch, "_trade_action", {"last_action": "sell", "action": "buy"}) == "SELL"
    assert check(orig_nodes, monkeypatch, "_trade_action", {"last_action": "", "action": " buy "}) == "BUY"
    assert check(orig_nodes, monkeypatch, "_trade_action", "notarow")[0] == "err"


# A32-3 _row_report_day
@pytest.mark.parametrize("row", [{}, {"date": "2026-04-16"}, {"day": "2026-04-17"}, {"date": "2026-04-16", "day": "2026-04-17"}, {"date": "", "day": "2026-04-17"},
                                 {"date": " 2026-04-16T09:00:00 "}, {"date": "2026-04-16extra"}, {"date": None, "day": None}, {"date": "한글날짜입니다열두글자"}, {"date": 20260416}, {"day": "abc"}])
def test_row_report_day(orig_nodes, monkeypatch, guards, row):
    check(orig_nodes, monkeypatch, "_row_report_day", row)


def test_row_report_day_truncation(orig_nodes, monkeypatch, guards):
    assert check(orig_nodes, monkeypatch, "_row_report_day", {"date": " 2026-04-16T09:00:00 "}) == "2026-04-16"
    assert check(orig_nodes, monkeypatch, "_row_report_day", {"day": "2026-04"}) == "2026-04"


# A32-4 _same_day_new_trade_rows
ROWS = [{"id": 1, "carry": False}, {"id": 2, "carry": True}, {"id": 3, "carry": False}, {"id": 4}]


@pytest.mark.parametrize("rows", [[], [ROWS[0]], ROWS, [ROWS[1]], [ROWS[1], ROWS[1]]])
def test_same_day_new_trade_rows_fake_marker(orig_nodes, monkeypatch, guards, rows):
    seen = []
    out = check(orig_nodes, monkeypatch, "_same_day_new_trade_rows", rows,
                overrides={"_is_carryover_exit_marker": lambda r: seen.append(r.get("id")) or bool(r.get("carry"))})
    assert [r["id"] for r in out] == [r["id"] for r in rows if not r.get("carry")]
    assert seen == [r.get("id") for r in rows] * 2  # call-time seam, once per side, in order


def test_same_day_new_trade_rows_real_marker_and_identity(orig_nodes, monkeypatch, guards):
    check(orig_nodes, monkeypatch, "_same_day_new_trade_rows", [{"trade_origin": "carryover"}, {"status": "closed"}, {}])
    rows = [{"a": 1}, {"b": 2}]
    kept = ops._same_day_new_trade_rows(rows)
    expected = [r for r in rows if not ops._is_carryover_exit_marker(r)]
    assert len(kept) == len(expected) and all(a is b for a, b in zip(kept, expected))  # same row objects, original order


# A32-5 _is_recovered_partial_marker
@pytest.mark.parametrize("row", [{}, {"status": "partial"}, {"trade_origin": "recovered_partial"}, {"status": "closed"}, {"status": 5}, {"last_status": None}])
def test_is_recovered_partial_marker_real(orig_nodes, monkeypatch, guards, row):
    check(orig_nodes, monkeypatch, "_is_recovered_partial_marker", row)


@pytest.mark.parametrize("ret", [True, False, 0, 1, "yes", None])
def test_is_recovered_partial_marker_fake(orig_nodes, monkeypatch, guards, ret):
    seen = []
    out = check(orig_nodes, monkeypatch, "_is_recovered_partial_marker", {"id": 1},
                overrides={"_has_partial_lifecycle_marker": lambda r: seen.append(dict(r)) or ret})
    assert out == ret and seen == [{"id": 1}, {"id": 1}]


# A32-6 _performance_source_rows
@pytest.mark.parametrize("closed,nonclosed", [(set(), set()), ({1}, set()), (set(), {2}), ({1, 3}, {2}), ({1, 2, 3, 4}, {1, 2, 3, 4})])
def test_performance_source_rows(orig_nodes, monkeypatch, guards, closed, nonclosed):
    rows = [{"id": i} for i in (1, 2, 3, 4)]
    calls = []
    out = check(orig_nodes, monkeypatch, "_performance_source_rows", rows,
                overrides={"_is_closed_trade": lambda r: calls.append(("c", r["id"])) or r["id"] in closed,
                           "_is_realized_nonclosed_exit": lambda r: calls.append(("n", r["id"])) or r["id"] in nonclosed})
    assert [r["id"] for r in out] == [i for i in (1, 2, 3, 4) if i in closed or i in nonclosed]
    assert calls[: len(calls) // 2] == calls[len(calls) // 2:]  # identical short-circuit call order on both sides


def test_performance_source_rows_real_helpers_empty(orig_nodes, monkeypatch, guards):
    assert check(orig_nodes, monkeypatch, "_performance_source_rows", []) == []
    check(orig_nodes, monkeypatch, "_performance_source_rows", [{"status": "closed"}, {"action": "SELL", "status": "partial"}, {}])


# A32-7 _parse_day
@pytest.mark.parametrize("value", [None, "", "  ", "2026-04-16", " 2026-04-16 ", "2026-04-16T09:30:00", "20260416", "2026-13-01", "2026-02-30", "bad", 20260416, [], "2026-04-1", "한글한글한글한글한글한글"])
def test_parse_day(orig_nodes, monkeypatch, guards, value):
    check(orig_nodes, monkeypatch, "_parse_day", value)


def test_parse_day_values_and_fake_date(orig_nodes, monkeypatch, guards):
    assert check(orig_nodes, monkeypatch, "_parse_day", "2026-04-16T09:30:00") == _dt.date(2026, 4, 16)
    assert check(orig_nodes, monkeypatch, "_parse_day", "bad") is None

    class FakeDate:
        seen = []

        @classmethod
        def fromisoformat(cls, text):
            cls.seen.append(text)
            if text == "boom":
                raise RuntimeError("fake")
            return ("parsed", text)
    assert check(orig_nodes, monkeypatch, "_parse_day", " 2026-04-16 ", overrides={"date": FakeDate}) == ("parsed", "2026-04-16")
    assert check(orig_nodes, monkeypatch, "_parse_day", "boom", overrides={"date": FakeDate}) is None
    assert FakeDate.seen == ["2026-04-16", "2026-04-16", "boom", "boom"]


# A32-8 _summary_ref
@pytest.mark.parametrize("payload", [None, {}, "str", [], {"metrics": None}, {"metrics": []}, {"metrics": {}}, {"metrics": {"a": 1, "b": {"n": [1]}}}, {"other": 1}])
@pytest.mark.parametrize("paths", [(Path("/x/a.md"), Path("/x/a.json")), ("raw.md", "raw.json"), (Path("rel/한글.md"), Path("rel/b.json"))])
def test_summary_ref(orig_nodes, monkeypatch, guards, payload, paths):
    check(orig_nodes, monkeypatch, "_summary_ref", paths[0], paths[1], payload)
    check(orig_nodes, monkeypatch, "_summary_ref", md_path=paths[0], json_path=paths[1])


def test_summary_ref_shape_and_shallow_copy(guards, tmp_path):
    nested = {"n": [1]}
    payload = {"metrics": {"a": 1, "nested": nested}}
    out = run_identity("_summary_ref", tmp_path / "s.md", tmp_path / "s.json", payload)
    assert list(out) == ["status", "md_path", "json_path", "metrics"]
    assert out["md_path"] == str(tmp_path / "s.md") and out["metrics"] is not payload["metrics"] and out["metrics"]["nested"] is nested
    assert run_identity("_summary_ref", "a", "b") == {"status": "ok", "md_path": "a", "json_path": "b", "metrics": {}}


# structure
@pytest.mark.parametrize("name", NAMES)
def test_wrapper_thin_and_owner_holds_body(name):
    wrapper = ast.parse(inspect.getsource(getattr(MODS[name], name))).body[0]
    assert len(wrapper.body) == 1 and isinstance(wrapper.body[0], ast.Return)
    assert not [n for n in ast.walk(wrapper) if isinstance(n, (ast.If, ast.For, ast.Try, ast.ListComp, ast.GeneratorExp))]
    call = wrapper.body[0].value
    assert isinstance(call, ast.Call) and "facade" in [k.arg for k in call.keywords], "wrapper must forward to the Owner with facade="
    owner_fn = getattr(OWNERS[name], name)
    node = ast.parse(inspect.getsource(owner_fn)).body[0]
    assert len(node.body) >= 1 and owner_fn.__module__ == OWNERS[name].__name__
    src = inspect.getsource(OWNERS[name]).replace(f"{STEM[name]}_", "")
    assert f"{STEM[name]} import" not in src and f"import {STEM[name]}" not in src
