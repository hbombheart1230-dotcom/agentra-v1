"""RF-032 A35-1..8: eight evaluation helpers across three modules, original vs thin wrappers + Owners.

Pure in-memory scope; no UEF/validation-id writer is touched. Originals: A preimage 17aea578 (artifact_inventory
e2ec5c44, attribution_score_range ea17c616, attribution_score_v0 bbf8438d); canonical 134bab40 has the same blobs.
AST-extracted and compiled in a copy of the live namespace; dependency overrides apply to both sides.
No real file reads (`_read_json` / `_trade_dir_count` are faked), sockets, subprocess or writes.
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

A_PRE = "17aea578a9b3bc5aec63d41e2029fdbf48296de6"
CANON = "134bab407041ed9e872c32a345fd7949d6effb68"
EV = "libs/reporting/evaluation/"
FILES = {
    "inv": (EV + "artifact_inventory.py", "e2ec5c448448c4d74e890fbea556e8c448423803", "artifact_inventory",
            ["_synthetic_identity", "_regular_session_window", "_parse_window_kst"]),
    "rng": (EV + "attribution_score_range.py", "ea17c616ea0034b3711480aeb82a5021b2c2d52c", "attribution_score_range",
            ["_date_range", "_day_trade_count", "render_attribution_score_range"]),
    "v0": (EV + "attribution_score_v0.py", "bbf8438d1ca85eb35c6c528bfc9fb7b0648b0a91", "attribution_score_v0",
           ["_evidence_quality", "render_attribution_score_v0"]),
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
        raise AssertionError("effect attempted")
    monkeypatch.setattr(subprocess, "run", boom)
    monkeypatch.setattr(subprocess, "Popen", boom)
    monkeypatch.setattr(socket.socket, "connect", boom)
    for attr in ("read_text", "read_bytes", "write_text", "write_bytes", "mkdir", "touch", "unlink", "rename", "replace"):
        monkeypatch.setattr(Path, attr, boom)
    real_open = builtins.open

    def guarded_open(file, mode="r", *a, **k):
        if any(c in str(mode) for c in "wax+"):
            raise AssertionError("write open attempted")
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


# ---- A35-1 _synthetic_identity ----
SYN = [
    {}, {"run_id": "run-TEST-1"}, {"decision_id": "my_fixture"}, {"q9_decision_id": "Synthetic"}, {"candidate_pool_id": "pool-test"},
    {"run_id": "ok", "symbol": "005930"}, {"symbol": "AAPL"}, {"symbol": ""}, {"symbol": None, "ticker": "005930"},
    {"layer": {"selected_symbol": "005930", "x": [{"candidate_symbol": "000660"}]}},
    {"layer": {"selected_symbol": "BAD"}}, {"a": [{"b": {"top1_symbol": "12345"}}]},
    {"layer_packet_ids": {"symbol": "NOTKRX"}}, {"x_packet_ids": {"ticker": "NOTKRX"}}, {"outer": {"y_packet_ids": [{"symbol": "NOTKRX"}]}},
    {"nested": {"deeper": [{"symbol": " 005930 "}]}}, {"symbol": 5930}, {"symbol": "００５９３０"}, {"list": [[{"symbol": "ZZZ"}]]},
    {"run_id": "한글-운영", "symbol": "005930"}, {"symbol": "005930\n"},
]


@pytest.mark.parametrize("row", SYN)
def test_synthetic_identity(orig_nodes, monkeypatch, guards, row):
    check(orig_nodes, monkeypatch, "inv", "_synthetic_identity", row)


def test_synthetic_identity_values_and_regex_seam(orig_nodes, monkeypatch, guards):
    assert check(orig_nodes, monkeypatch, "inv", "_synthetic_identity", {"run_id": "TEST"}) is True
    assert check(orig_nodes, monkeypatch, "inv", "_synthetic_identity", {"layer_packet_ids": {"symbol": "NOTKRX"}}) is False
    assert check(orig_nodes, monkeypatch, "inv", "_synthetic_identity", {"symbol": "ABC"}) is True
    import re
    assert check(orig_nodes, monkeypatch, "inv", "_synthetic_identity", {"symbol": "ABC"}, overrides={"_KRX_SYMBOL_RE": re.compile(r"^[A-Z]{3}$")}) is False


# ---- A35-2 _regular_session_window / A35-3 _parse_window_kst ----
STAMPS = [None, "", "  ", "bad", "2026-04-16T00:00:00Z", "2026-04-16T00:00:00+00:00", "2026-04-16T09:00:00+09:00", "2026-04-16T08:59:59+09:00",
          "2026-04-16T15:30:59+09:00", "2026-04-16T15:31:00+09:00", "2026-04-16T06:30:00Z", "2026-04-16T06:31:00Z", "2026-04-16 09:15:00",
          "2026-04-16T09:15:00", "2026-04-16T23:59:59-05:00", 5, [], "2026-13-01T00:00:00Z"]


@pytest.mark.parametrize("stamp", STAMPS)
def test_parse_window_kst(orig_nodes, monkeypatch, guards, stamp):
    check(orig_nodes, monkeypatch, "inv", "_parse_window_kst", stamp)


@pytest.mark.parametrize("stamp", STAMPS)
def test_regular_session_window_real_parser(orig_nodes, monkeypatch, guards, stamp):
    check(orig_nodes, monkeypatch, "inv", "_regular_session_window", {"generated_at": stamp})


def test_parse_window_kst_conversions(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "inv", "_parse_window_kst", "2026-04-16T00:00:00Z")
    assert (out.hour, out.minute, str(out.tzinfo)) == (9, 0, "Asia/Seoul")
    naive = check(orig_nodes, monkeypatch, "inv", "_parse_window_kst", "2026-04-16T09:15:00")  # naive == UTC -> 18:15 KST
    assert naive.hour == 18
    assert check(orig_nodes, monkeypatch, "inv", "_parse_window_kst", "nonsense") is None


@pytest.mark.parametrize("h,m,expected", [(8, 59, False), (9, 0, True), (12, 0, True), (15, 30, True), (15, 31, False), (23, 0, False)])
def test_regular_session_window_fake_parser_boundaries(orig_nodes, monkeypatch, guards, h, m, expected):
    out = check(orig_nodes, monkeypatch, "inv", "_regular_session_window", {"generated_at": "x"},
                overrides={"_parse_window_kst": lambda v: _dt.datetime(2026, 4, 16, h, m)})
    assert out is expected
    assert check(orig_nodes, monkeypatch, "inv", "_regular_session_window", {}, overrides={"_parse_window_kst": lambda v: None}) is True


# ---- A35-4 _date_range ----
@pytest.mark.parametrize("start,end", [
    ("2026-04-16", "2026-04-16"), ("2026-04-16", "2026-04-19"), ("2026-04-19", "2026-04-16"), ("2024-02-27", "2024-03-01"), ("2026-02-27", "2026-03-01"),
    ("2026-12-30", "2027-01-02"), ("bad", "2026-04-16"), ("2026-04-16", "bad"), ("", ""), (None, "2026-04-16"), ("2026-04-16T10:00", "2026-04-17"), ("20260416", "20260417"),
])
def test_date_range(orig_nodes, monkeypatch, guards, start, end):
    check(orig_nodes, monkeypatch, "rng", "_date_range", start, end)


def test_date_range_values_errors_and_seams(orig_nodes, monkeypatch, guards):
    assert check(orig_nodes, monkeypatch, "rng", "_date_range", "2024-02-28", "2024-03-01") == ["2024-02-28", "2024-02-29", "2024-03-01"]
    err = check(orig_nodes, monkeypatch, "rng", "_date_range", "2026-04-17", "2026-04-16")
    assert err == ("err", "ValueError", "start must be before or equal to end")
    out = check(orig_nodes, monkeypatch, "rng", "_date_range", "a", "b",
                overrides={"_parse_date": lambda v: _dt.date(2026, 1, 1) if v == "a" else _dt.date(2026, 1, 3)})
    assert out == ["2026-01-01", "2026-01-02", "2026-01-03"]


def test_date_range_timedelta_seam(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "rng", "_date_range", "2026-01-01", "2026-01-05", overrides={"timedelta": lambda days: _dt.timedelta(days=2)})
    assert out == ["2026-01-01", "2026-01-03", "2026-01-05"]


# ---- A35-5 _day_trade_count ----
def _fakes(scorecard, dir_count=7):
    seen = {"read": [], "dir": []}

    def _read_json(path):
        seen["read"].append(str(path))
        return copy.deepcopy(scorecard)

    def _trade_dir_count(root, day):
        seen["dir"].append((str(root), day))
        return dir_count
    return seen, {"_read_json": _read_json, "_trade_dir_count": _trade_dir_count}


@pytest.mark.parametrize("scorecard", [
    {}, {"artifact_integrity": {}}, {"artifact_integrity": {"trade_count": None}}, {"artifact_integrity": {"trade_count": 3}},
    {"artifact_integrity": {"trade_count": "4"}}, {"artifact_integrity": {"trade_count": "4.9"}}, {"artifact_integrity": {"trade_count": 2.9}},
    {"artifact_integrity": {"trade_count": "bad"}}, {"artifact_integrity": {"trade_count": []}}, {"artifact_integrity": {"trade_count": 0}},
    {"artifact_integrity": {"trade_count": True}},
])
def test_day_trade_count(orig_nodes, monkeypatch, guards, scorecard):
    seen, ov = _fakes(scorecard)
    out = check(orig_nodes, monkeypatch, "rng", "_day_trade_count", Path("/rep"), "2026-04-16", overrides=ov)
    assert isinstance(out, int)
    assert seen["read"][0].endswith("evaluation/daily/2026-04-16/daily_scorecard.json") and len(seen["read"]) == 2


def test_day_trade_count_fallback_values(orig_nodes, monkeypatch, guards):
    seen, ov = _fakes({"artifact_integrity": {"trade_count": None}}, dir_count=11)
    assert check(orig_nodes, monkeypatch, "rng", "_day_trade_count", Path("/rep"), "d", overrides=ov) == 11
    assert seen["dir"] == [("/rep", "d"), ("/rep", "d")]
    seen, ov = _fakes({"artifact_integrity": {"trade_count": "6"}}, dir_count=11)
    assert check(orig_nodes, monkeypatch, "rng", "_day_trade_count", Path("/rep"), "d", overrides=ov) == 6 and seen["dir"] == []


# ---- A35-6 render_attribution_score_range ----
RPAY = {
    "start": "2026-04-01", "end": "2026-04-16", "behavior_effect": "evaluation_only", "day_count": 16, "available_day_count": 10, "scored_day_count": 8,
    "trade_day_count": 6, "total_trade_count": 40, "scored_trade_count": 30,
    "weakest_axis_by_average_score": {"name": "entry_timing_score", "average_score": 61.5},
    "axis_summary": {"entry_timing_score": {"average_score": 61.5, "min_score": 20, "max_score": 100, "scored_day_count": 8, "missing_day_count": 1,
                                            "insufficient_day_count": 1, "top_reasons": [{"reason": "T1:ENTRY_TOO_EARLY", "count": 3}, {"reason": "한글", "count": 1}]},
                     "exit_horizon_score": {"average_score": None}, "bad": "notamapping"},
    "weakest_axis_distribution": {"b_axis": 2, "a_axis": 2, "c_axis": 5},
    "daily_rows": [{"day": "2026-04-15", "available": True, "scored": True, "trade_count": 3, "weakest_axis": "entry_timing_score",
                    "selection_integrity_score": 90, "scanner_alignment_score": 80, "entry_timing_score": 35, "exit_horizon_score": 70, "evidence_quality_score": 100},
                   "bad", {"day": "2026-04-16"}],
    "interpretation_rule": "관찰 전용",
}
RPAYS = [{}, {"start": "a"}, {"weakest_axis_distribution": {}}, {"axis_summary": 5, "daily_rows": None}, RPAY, {**RPAY, "weakest_axis_distribution": None}]


@pytest.mark.parametrize("payload", RPAYS)
def test_render_attribution_score_range(orig_nodes, monkeypatch, guards, payload):
    check(orig_nodes, monkeypatch, "rng", "render_attribution_score_range", payload)


def test_render_range_exact_markdown_bits(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "rng", "render_attribution_score_range", RPAY)
    assert out.startswith("# Q13 Attribution Score Range - 2026-04-01 to 2026-04-16\n\n- Behavior effect: `evaluation_only`\n")
    assert out.index("- `c_axis`: 5") < out.index("- `a_axis`: 2") < out.index("- `b_axis`: 2")  # count desc, then name
    assert "| entry_timing_score | 61.5 | 20 | 100 | 8 | 1 | 1 | T1:ENTRY_TOO_EARLY (3), 한글 (1) |" in out
    assert out.endswith("- 관찰 전용\n")
    assert "No scored days." in check(orig_nodes, monkeypatch, "rng", "render_attribution_score_range", {})


def test_render_range_mapping_seam(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "rng", "render_attribution_score_range", {"axis_summary": {"k": {}}, "weakest_axis_distribution": {}},
                overrides={"_mapping": lambda v: dict(v, tag=1) if isinstance(v, dict) else {"name": "FAKE", "average_score": 1}})
    assert "- Weakest by average score: `FAKE` (1)" in out and "| k | None |" in out and "- `tag`: 1" in out


# ---- A35-7 _evidence_quality ----
def _eq(counts=None, summary=None, sel_rows=True, hor_rows=True, ent_rows=True, ledger=None):
    return dict(
        daily_scorecard={"artifact_integrity": {"status_counts": counts}} if counts is not None else {},
        selection_authority={"summary": summary or {}, "rows": [{"trade_id": "T"}] if sel_rows else []},
        horizon_report={"rows": [{"trade_id": "T"}] if hor_rows else []},
        entry_timing_report={"rows": [{"trade_id": "T"}] if ent_rows else []},
        ledger_day=ledger or {})


EQ = [
    _eq(), _eq({}), _eq({"PASS": 0}), _eq({"PASS": 4}), _eq({"PASS": 2, "WATCH": 2}), _eq({"PASS": 1, "FAIL": 1}), _eq({"PASS": 1, "BLOCKER": 3}),
    _eq({"PASS": 4}, sel_rows=False), _eq({"PASS": 4}, hor_rows=False, ent_rows=False), _eq({"PASS": 4}, sel_rows=False, hor_rows=False, ent_rows=False),
    _eq({"PASS": 4}, ledger={"evidence_status": "PARTIAL"}), _eq({"PASS": 4}, ledger={"evidence_status": "complete"}), _eq({"PASS": 4}, ledger={"evidence_status": ""}),
    _eq({"PASS": 4}, ledger={"other": 1}), _eq({"PASS": 3}, summary={"excluded:a": 3}), _eq({"PASS": 3}, summary={"excluded:a": 1, "excluded:b": 2, "kept": 9}),
    _eq({"PASS": 3}, summary={"excluded:a": 1}, ledger={"evidence_status": "COMPLETE"}), _eq({"PASS": "x"}), _eq({"WATCH": 1}),
]


@pytest.mark.parametrize("kwargs", EQ)
def test_evidence_quality(orig_nodes, monkeypatch, guards, kwargs):
    check(orig_nodes, monkeypatch, "v0", "_evidence_quality", **kwargs)


def test_evidence_quality_values_and_seams(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "v0", "_evidence_quality", **_eq({"PASS": 3}, summary={"excluded:a": 3}, ledger={"evidence_status": "COMPLETE"}))
    assert out["score"] == 100 and out["reasons"] == ["all_trade_rows_explicitly_excluded_from_behavior_metrics"]
    assert out["evidence"]["explicitly_excluded_trade_count"] == 3 and out["evidence"]["ledger_evidence_status"] == "COMPLETE"
    out = check(orig_nodes, monkeypatch, "v0", "_evidence_quality",
                **_eq({"PASS": 4, "FAIL": 1}, sel_rows=False, hor_rows=False, ent_rows=False, ledger={"evidence_status": "PARTIAL"}))
    assert out["reasons"] == ["fail_integrity_rows_present", "selection_authority_rows_missing", "horizon_rows_missing",
                              "entry_timing_rows_missing", "ledger_evidence_status:PARTIAL"] and out["score"] == 35  # 80 - 3*10 - 15
    out = check(orig_nodes, monkeypatch, "v0", "_evidence_quality", **_eq({"PASS": 4}),
                overrides={"_clamp_score": lambda v: 7, "OK": "FAKE_OK", "_score": lambda s, v, r, e=None: {"s": s, "v": v, "r": r}})
    assert out == {"s": "FAKE_OK", "v": 7, "r": ["evidence_surfaces_available"]}


# ---- A35-8 render_attribution_score_v0 ----
VPAY = {"day": "2026-04-16", "behavior_effect": "evaluation_only", "weakest_observed_axis": {"name": "entry_timing_score", "score": 35},
        "scores": {"selection_integrity_score": {"status": "OK", "score": 90, "reasons": ["a", "b"]},
                   "entry_timing_score": {"status": "INSUFFICIENT_EVIDENCE", "score": None, "reasons": []},
                   "exit_horizon_score": {"status": "OK", "score": 72.6, "reasons": ["한글"]}, "bad": 5},
        "interpretation_rule": "관찰 전용", "limitations": ["lim one", "lim 둘"]}
VPAYS = [{}, {"day": "d"}, {"scores": None}, {"scores": {"k": {"status": "OK", "score": "bad"}}}, VPAY, {**VPAY, "limitations": None}]


@pytest.mark.parametrize("payload", VPAYS[:3] + VPAYS[4:])
def test_render_attribution_score_v0(orig_nodes, monkeypatch, guards, payload):
    check(orig_nodes, monkeypatch, "v0", "render_attribution_score_v0", payload)


def test_render_v0_invalid_score_error_parity_and_exact_bits(orig_nodes, monkeypatch, guards):
    err = check(orig_nodes, monkeypatch, "v0", "render_attribution_score_v0", VPAYS[3])
    assert err[0] == "err" and err[1] == "ValueError"
    out = check(orig_nodes, monkeypatch, "v0", "render_attribution_score_v0", VPAY)
    assert out.startswith("# Q13 Attribution Score v0 - 2026-04-16\n") and "| entry_timing_score | INSUFFICIENT_EVIDENCE | - | - |" in out
    assert "| exit_horizon_score | OK | 72 | 한글 |" in out and out.endswith("- lim one\n- lim 둘\n")
    assert check(orig_nodes, monkeypatch, "v0", "render_attribution_score_v0", {}).endswith("## Limitations\n\n")


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
