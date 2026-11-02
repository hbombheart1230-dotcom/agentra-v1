"""RF-032 A36-1..8: eight evaluation helpers across three modules, original vs thin wrappers + Owners.

Pure scope; no UEF/validation-id writer is touched. Originals: A preimage 0538ad0a (attribution_score_range ec958ff4,
attribution_score_window 7efd41ad, artifact_inventory 17e74b6c); canonical 0ca613bc has the same blobs. AST-extracted
and compiled in a copy of the live namespace; dependency overrides apply to both sides. Path.exists / rglob / is_dir /
stat are replaced by fakes where used; no real file access, sockets, subprocess or writes.
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

A_PRE = "0538ad0a112a274344907599b49ebbac742cbe36"
CANON = "0ca613bc04f9881a76ff799a6fb3273a9a615c57"
EV = "libs/reporting/evaluation/"
FILES = {
    "rng": (EV + "attribution_score_range.py", "ec958ff471a81ac74c9be3b97409a37fb5bf8257", "attribution_score_range",
            ["_parse_date", "_trade_dir_count", "_has_source_artifact", "build_attribution_score_range"]),
    "win": (EV + "attribution_score_window.py", "7efd41ad291ddda4209d552f960d9489ec81886a", "attribution_score_window",
            ["_ledger_days", "build_attribution_score_window", "render_attribution_score_window"]),
    "inv": (EV + "artifact_inventory.py", "17e74b6cd47973062555ffcc4b1297527daa3e56", "artifact_inventory", ["_record"]),
}
MODS = {k: importlib.import_module(f"libs.reporting.evaluation.{v[2]}") for k, v in FILES.items()}
CASES = [(k, n) for k, v in FILES.items() for n in v[3]]
OWNERS = {(k, n): importlib.import_module(f"libs.reporting.evaluation.{FILES[k][2]}_{n.lstrip('_')}") for k, n in CASES}


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
        # writes are always forbidden; reads of any fixture path (/rep, /freeze, /fake) are forbidden too
        if any(c in str(mode) for c in "wax+") or str(file).replace("\\", "/").startswith(("/rep", "/freeze", "/fake")):
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


# ---- A36-1 _parse_date ----
class _FakeDate:
    calls = []

    @classmethod
    def fromisoformat(cls, text):
        cls.calls.append(text)
        if text == "boom":
            raise RuntimeError("fake")
        return ("parsed", text)


@pytest.mark.parametrize("value", ["2026-04-16", "2024-02-29", "2026-02-30", "bad", "", " 2026-04-16 ", "20260416", 20260416, None, "2026-04-16T09:00", b"2026-04-16"])
def test_parse_date(orig_nodes, monkeypatch, guards, value):
    check(orig_nodes, monkeypatch, "rng", "_parse_date", value)


def test_parse_date_values_and_fake_date(orig_nodes, monkeypatch, guards):
    assert check(orig_nodes, monkeypatch, "rng", "_parse_date", "2026-04-16") == _dt.date(2026, 4, 16)
    err = check(orig_nodes, monkeypatch, "rng", "_parse_date", "nope")
    assert err[0] == "err" and err[1] == "ValueError"
    _FakeDate.calls.clear()
    assert check(orig_nodes, monkeypatch, "rng", "_parse_date", 5, overrides={"date": _FakeDate}) == ("parsed", "5")  # str() applied
    assert check(orig_nodes, monkeypatch, "rng", "_parse_date", "boom", overrides={"date": _FakeDate})[1] == "RuntimeError"
    assert _FakeDate.calls == ["5", "5", "boom", "boom"]


# ---- A36-2 _trade_dir_count (fake Path.exists / rglob / is_dir) ----
def _patch_tree(monkeypatch, existing, entries):
    """existing: set of str paths that exist; entries: list of (name, is_dir)."""
    monkeypatch.setattr(Path, "exists", lambda self: str(self) in existing)
    monkeypatch.setattr(Path, "rglob", lambda self, pattern: iter([Path(self) / n for n, _ in entries]))
    dirs = {str(Path("/rep/trades/D") / n) for n, d in entries if d}
    monkeypatch.setattr(Path, "is_dir", lambda self: str(self) in dirs)


@pytest.mark.parametrize("exists,entries", [
    (False, []), (True, []), (True, [("TRD_1", True)]), (True, [("TRD_1", True), ("TRD_2", False), ("TRD_3", True)]),
    (True, [("TRD_1", False)]), (True, [("TRD_1", True), ("TRD_1", True)]), (False, [("TRD_1", True)]),
])
def test_trade_dir_count(orig_nodes, monkeypatch, guards, exists, entries):
    _patch_tree(monkeypatch, {str(Path("/rep/trades/D"))} if exists else set(), entries)
    out = check(orig_nodes, monkeypatch, "rng", "_trade_dir_count", Path("/rep"), "D")
    assert out == (sum(1 for _, d in entries if d) if exists else 0)


# ---- A36-3 _has_source_artifact ----
LOCS = ["/rep/trades/D", "/rep/operator_summary/daily/D", "/rep/evaluation/daily/D"]


@pytest.mark.parametrize("present", [set(), {LOCS[0]}, {LOCS[1]}, {LOCS[2]}, {LOCS[0], LOCS[2]}, set(LOCS)])
def test_has_source_artifact(orig_nodes, monkeypatch, guards, present):
    seen = []
    monkeypatch.setattr(Path, "exists", lambda self: seen.append(str(self)) or str(self) in present)
    out = check(orig_nodes, monkeypatch, "rng", "_has_source_artifact", Path("/rep"), "D")
    assert out is bool(present)
    half = len(seen) // 2
    assert seen[:half] == seen[half:]  # identical probe order on both sides
    if LOCS[0] in present:
        assert seen[:half] == [LOCS[0]]  # first hit short-circuits


# ---- A36-4 build_attribution_score_range ----
def _score(status="OK", score=80, reasons=None):
    return {"status": status, "score": score, "reasons": reasons or []}


PAYLOADS = {
    "2026-04-14": {"scores": {"selection_integrity_score": _score("OK", 90, ["a", "b"]), "scanner_alignment_score": _score("OK", 70, ["a"]),
                              "entry_timing_score": _score("INSUFFICIENT_EVIDENCE", None, ["x"])},
                   "weakest_observed_axis": {"name": "scanner_alignment_score", "score": 70}},
    "2026-04-15": {"scores": {"selection_integrity_score": _score("OK", 50, ["b"]), "exit_horizon_score": _score("OK", 40, ["z", "z"])},
                   "weakest_observed_axis": {"name": "exit_horizon_score"}},
    "2026-04-16": {},
}


def _range_overrides(source_days, payloads=None, counts=None):
    payloads = PAYLOADS if payloads is None else payloads
    counts = {"2026-04-14": 3, "2026-04-15": 0, "2026-04-16": 2} if counts is None else counts
    return {"_has_source_artifact": lambda root, day: day in source_days,
            "_day_payload": lambda root, day: copy.deepcopy(payloads.get(day, {})),
            "_day_trade_count": lambda root, day: counts.get(day, 0)}


@pytest.mark.parametrize("start,end,include_empty,source_days", [
    ("2026-04-16", "2026-04-16", False, set()), ("2026-04-16", "2026-04-16", True, set()), ("2026-04-14", "2026-04-16", False, {"2026-04-14", "2026-04-15", "2026-04-16"}),
    ("2026-04-14", "2026-04-16", True, {"2026-04-14"}), ("2026-04-14", "2026-04-17", True, set()), ("2026-04-14", "2026-04-16", False, {"2026-04-16"}),
    ("2026-04-16", "2026-04-14", False, set()), ("bad", "2026-04-14", True, set()),
])
def test_build_attribution_score_range(orig_nodes, monkeypatch, guards, start, end, include_empty, source_days):
    check(orig_nodes, monkeypatch, "rng", "build_attribution_score_range", reports_root=Path("/rep"), start=start, end=end,
          include_empty_days=include_empty, overrides=_range_overrides(source_days))


def test_build_range_values_and_seams(orig_nodes, monkeypatch, guards):
    days = {"2026-04-14", "2026-04-15", "2026-04-16"}
    out = check(orig_nodes, monkeypatch, "rng", "build_attribution_score_range", reports_root=Path("/rep"), start="2026-04-14", end="2026-04-16",
                overrides=_range_overrides(days))
    assert out["day_count"] == 3 and out["available_day_count"] == 2 and out["scored_day_count"] == 2
    assert out["total_trade_count"] == 5 and out["trade_day_count"] == 2 and out["scored_trade_count"] == 3
    assert out["weakest_axis_distribution"] == {"scanner_alignment_score": 1, "exit_horizon_score": 1}
    assert out["weakest_axis_by_average_score"] == {"name": "exit_horizon_score", "average_score": 40.0}
    assert out["axis_summary"]["selection_integrity_score"]["average_score"] == 70.0
    assert out["axis_summary"]["entry_timing_score"]["insufficient_day_count"] == 1
    assert [r["day"] for r in out["daily_rows"]] == ["2026-04-14", "2026-04-15", "2026-04-16"]
    assert out["daily_rows"][2]["scored"] is False
    ov = _range_overrides(days)
    ov["SCORE_KEYS"] = ("selection_integrity_score",)
    out = check(orig_nodes, monkeypatch, "rng", "build_attribution_score_range", reports_root=Path("/rep"), start="2026-04-14", end="2026-04-15", overrides=ov)
    assert list(out["axis_summary"]) == ["selection_integrity_score"]  # SCORE_KEYS read from the facade at call time


def test_build_range_reason_ties_and_default_path(orig_nodes, monkeypatch, guards):
    p = {"2026-04-14": {"scores": {"selection_integrity_score": _score("OK", 10, ["r2", "r1"])}},
         "2026-04-15": {"scores": {"selection_integrity_score": _score("OK", 30, ["r1", "r2"])}}}
    out = check(orig_nodes, monkeypatch, "rng", "build_attribution_score_range", start="2026-04-14", end="2026-04-15",
                overrides=_range_overrides({"2026-04-14", "2026-04-15"}, payloads=p))
    assert out["axis_summary"]["selection_integrity_score"]["top_reasons"] == [{"reason": "r2", "count": 2}, {"reason": "r1", "count": 2}]


# ---- A36-5 _ledger_days ----
LEDGERS = [{}, {"days": None}, {"days": []}, {"days": [{"day": "a"}, "bad", None, {"day": "b", "n": {"deep": 1}}, 5]}, {"days": "notalist"}, {"days": {"k": 1}},
           {"days": [{"day": "z"}, {"day": "a"}]}]


@pytest.mark.parametrize("ledger", LEDGERS)
def test_ledger_days(orig_nodes, monkeypatch, guards, ledger):
    seen = []
    out = check(orig_nodes, monkeypatch, "win", "_ledger_days", Path("/freeze"),
                overrides={"_read_json": lambda p: seen.append(str(p)) or copy.deepcopy(ledger)})
    assert seen[0] == str(Path("/freeze") / "daily_ledger.json") and len(seen) == 2
    assert isinstance(out, list) and all(isinstance(r, dict) for r in out)


def test_ledger_days_copy_semantics(guards):
    nested = {"deep": 1}
    src = {"days": [{"day": "a", "n": nested}]}
    import libs.reporting.evaluation.attribution_score_window as w
    orig = w._read_json
    w._read_json = lambda p: src
    try:
        out = w._ledger_days(Path("/f"))
    finally:
        w._read_json = orig
    assert out[0] is not src["days"][0] and out[0]["n"] is nested  # shallow copy of each row, nested shared


# ---- A36-6 build_attribution_score_window ----
LEDGER = [{"day": "2026-04-14", "counts_as_valid_day": True}, {"day": "2026-04-15", "counts_as_valid_day": False}, {"day": "2026-04-16", "counts_as_valid_day": True},
          {"day": "2026-04-17", "counts_as_valid_day": True}, {"counts_as_valid_day": 1}]
WPAY = {"2026-04-14": PAYLOADS["2026-04-14"], "2026-04-15": PAYLOADS["2026-04-15"], "2026-04-17": {"scores": {"selection_integrity_score": _score("OK", 60, ["q"])}}}


def _win_overrides(ledger, payloads=None, scorecard_counts=None):
    payloads = WPAY if payloads is None else payloads
    sc = {"2026-04-14": 4, "2026-04-15": 9, "2026-04-17": 2} if scorecard_counts is None else scorecard_counts

    def _read_json(path):
        day = Path(path).parent.name
        return {"artifact_integrity": {"trade_count": sc[day]}} if day in sc else {}
    return {"_ledger_days": lambda root: copy.deepcopy(ledger), "_day_payload": lambda root, day: copy.deepcopy(payloads.get(day, {})), "_read_json": _read_json}


@pytest.mark.parametrize("ledger", [[], LEDGER[:1], LEDGER[1:2], LEDGER[2:3], LEDGER, LEDGER[3:]])
@pytest.mark.parametrize("window_id", ["default", "w1"])
def test_build_attribution_score_window(orig_nodes, monkeypatch, guards, ledger, window_id):
    kw = {} if window_id == "default" else {"window_id": window_id}
    check(orig_nodes, monkeypatch, "win", "build_attribution_score_window", reports_root=Path("/rep"), overrides=_win_overrides(ledger), **kw)


def test_build_window_non_numeric_trade_count_error_parity(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "win", "build_attribution_score_window", reports_root=Path("/rep"),
                overrides=_win_overrides([LEDGER[3]], scorecard_counts={"2026-04-17": "bad"}))
    assert out[0] == "err" and out[1] == "ValueError"


def test_build_window_values_and_seams(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "win", "build_attribution_score_window", reports_root=Path("/rep"), window_id="W", overrides=_win_overrides(LEDGER))
    assert out["window_id"] == "W" and out["day_count"] == 5 and out["valid_day_count"] == 4 and out["available_day_count"] == 3
    assert out["weakest_axis_distribution"] == {"scanner_alignment_score": 1}
    assert [r["valid"] for r in out["daily_rows"]] == [True, False, True, True, True]
    assert out["daily_rows"][2]["available"] is False and out["daily_rows"][2]["trade_count"] == 0
    zero = check(orig_nodes, monkeypatch, "win", "build_attribution_score_window", reports_root=Path("/rep"), overrides=_win_overrides([]))
    assert zero["valid_day_count"] == 0 and zero["weakest_axis_by_average_score"] == {"name": "", "average_score": None}
    ov = _win_overrides(LEDGER)
    ov["SCORE_KEYS"] = ("entry_timing_score",)
    out = check(orig_nodes, monkeypatch, "win", "build_attribution_score_window", reports_root=Path("/rep"), overrides=ov)
    assert list(out["axis_summary"]) == ["entry_timing_score"]


# ---- A36-7 render_attribution_score_window ----
WRENDER = {"window_id": "W1", "behavior_effect": "observation_only", "day_count": 5, "valid_day_count": 4, "available_day_count": 3, "total_trade_count_valid_days": 12,
           "weakest_axis_by_average_score": {"name": "exit_horizon_score", "average_score": 40.0},
           "axis_summary": {"exit_horizon_score": {"average_score": 40.0, "min_score": 40, "max_score": 40, "scored_day_count": 1, "insufficient_day_count": 0,
                                                   "top_reasons": [{"reason": "한글", "count": 2}, {"reason": "z", "count": 1}]}, "bad": 5, "empty": {}},
           "weakest_axis_distribution": {"b": 1, "a": 1, "c": 3},
           "daily_rows": [{"day": "d1", "valid": True, "trade_count": 3, "weakest_axis": "x", "selection_integrity_score": 90, "scanner_alignment_score": 80,
                           "entry_timing_score": 35, "exit_horizon_score": 70, "evidence_quality_score": 100}, "bad", {"day": "d2"}],
           "interpretation_rule": "관찰 전용"}


@pytest.mark.parametrize("payload", [{}, {"window_id": "x"}, {"axis_summary": 5, "daily_rows": None}, {"weakest_axis_distribution": {}}, WRENDER, {**WRENDER, "weakest_axis_distribution": None}])
def test_render_attribution_score_window(orig_nodes, monkeypatch, guards, payload):
    check(orig_nodes, monkeypatch, "win", "render_attribution_score_window", payload)


def test_render_window_exact_bits_and_seam(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "win", "render_attribution_score_window", WRENDER)
    assert out.startswith("# Q13 Attribution Score Window - W1\n\n- Behavior effect: `observation_only`\n- Days: 5 total / 4 valid\n")
    assert out.index("- `c`: 3") < out.index("- `a`: 1") < out.index("- `b`: 1")
    assert "| exit_horizon_score | 40.0 | 40 | 40 | 1 | 0 | 한글 (2), z (1) |" in out and out.endswith("- 관찰 전용\n")
    assert "- No valid scored days." in check(orig_nodes, monkeypatch, "win", "render_attribution_score_window", {})
    out = check(orig_nodes, monkeypatch, "win", "render_attribution_score_window", {"weakest_axis_distribution": {}},
                overrides={"_mapping": lambda v: dict(v, tag=1) if isinstance(v, dict) else {"name": "FAKE", "average_score": 9}})
    assert "`FAKE` (9)" in out and "- `tag`: 1" in out


# ---- A36-8 artifact_inventory._record (fake path object) ----
class FakePath:
    def __init__(self, name, exists=True, size=10, mtime=1.5):
        self.name, self._exists, self._size, self._mtime = name, exists, size, mtime
        self.suffix = "." + name.rsplit(".", 1)[-1] if "." in name else ""
        self.stat_calls = 0

    def exists(self):
        return self._exists

    def stat(self):
        self.stat_calls += 1
        return type("S", (), {"st_size": self._size, "st_mtime": self._mtime})()

    def __str__(self):
        return f"/fake/{self.name}"

    def __repr__(self):
        return f"FakePath({self.name!r})"


@pytest.mark.parametrize("name,exists", [("a.json", True), ("A.JSON", True), ("a.json", False), ("a.txt", True), ("noext", True), ("a.txt", False)])
@pytest.mark.parametrize("required", [True, False])
@pytest.mark.parametrize("payload", [{}, {"schema_version": "v1", "evidence_status": "COMPLETE", "forward_windows_complete": 1}, {"schema_version": None, "forward_windows_complete": ""}])
def test_record(orig_nodes, monkeypatch, guards, name, exists, required, payload):
    reads = []
    out = check(orig_nodes, monkeypatch, "inv", "_record", FakePath(name, exists), required=required,
                overrides={"read_json": lambda p: reads.append(str(p)) or copy.deepcopy(payload)})
    assert list(out) == ["path", "required", "exists", "size_bytes", "modified_epoch", "schema_version", "evidence_status", "forward_windows_complete", "missing_reason"]
    assert out["missing_reason"] == ("" if exists else "artifact_not_found")
    assert len(reads) == (2 if exists and name.lower().endswith(".json") else 0)  # once per side


def test_record_error_parity_and_values(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "inv", "_record", FakePath("x.json", True, size=7, mtime=2.5), required=True,
                overrides={"read_json": lambda p: {"schema_version": "s", "evidence_status": "E", "forward_windows_complete": True}})
    assert out == {"path": "/fake/x.json", "required": True, "exists": True, "size_bytes": 7, "modified_epoch": 2.5, "schema_version": "s",
                   "evidence_status": "E", "forward_windows_complete": True, "missing_reason": ""}
    err = check(orig_nodes, monkeypatch, "inv", "_record", FakePath("x.json", True), required=True,
                overrides={"read_json": lambda p: (_ for _ in ()).throw(ValueError("fake read failure"))})
    assert err == ("err", "ValueError", "fake read failure")
    assert check(orig_nodes, monkeypatch, "inv", "_record", FakePath("x.json", False), required=False)["size_bytes"] == 0


# ---- structure ----
@pytest.mark.parametrize("key,name", CASES)
def test_wrapper_thin_and_owner_holds_body(key, name):
    wrapper = ast.parse(inspect.getsource(getattr(MODS[key], name))).body[0]
    assert len(wrapper.body) == 1 and isinstance(wrapper.body[0], ast.Return)
    assert not [n for n in ast.walk(wrapper) if isinstance(n, (ast.If, ast.For, ast.Try, ast.ListComp, ast.GeneratorExp))]
    call = wrapper.body[0].value
    assert isinstance(call, ast.Call) and "facade" in [k.arg for k in call.keywords], "wrapper must forward to the Owner with facade="
    owner_fn = getattr(OWNERS[(key, name)], name)
    node = ast.parse(inspect.getsource(owner_fn)).body[0]
    assert len(node.body) >= 1 and owner_fn.__module__ == OWNERS[(key, name)].__name__
    stem = FILES[key][2]
    src = inspect.getsource(OWNERS[(key, name)]).replace(f"{stem}_", "")
    assert f"{stem} import" not in src and f"import {stem}" not in src
