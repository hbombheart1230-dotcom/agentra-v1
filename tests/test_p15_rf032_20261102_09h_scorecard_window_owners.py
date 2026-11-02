"""RF-032 A33-1..8: agent_effectiveness_scorecard (6) + attribution_score_window (2), original vs wrappers + Owners.

Pure in-memory scorecard scope only; the validation-id/UEF protected writer is NOT touched. Originals: A preimage
05a7195c (scorecard blob 16b50178, window blob 7deb1f06); canonical 4f478179 has the same blobs. AST-extracted and
compiled in a copy of the live namespace; dependency overrides apply to both sides. No IO, sockets or writes.
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
from collections import OrderedDict
from pathlib import Path

import pytest

A_PRE = "05a7195c4a28300900d9f3870761e6e03348f2ea"
CANON = "4f4781792e314cc3e76cd1a8f2628a6e3dd78740"
SC_PATH, SC_BLOB = "libs/reporting/evaluation/agent_effectiveness_scorecard.py", "16b5017824277136e499a48dec2d9ffffa7905c4"
WIN_PATH, WIN_BLOB = "libs/reporting/evaluation/attribution_score_window.py", "7deb1f069b47f2170cf15c747094f902937f4124"
SC = ["_mapping", "_number", "_delta_state", "_decision_state", "build_agent_effectiveness_scorecard", "render_agent_effectiveness_scorecard"]
WIN = ["_mapping", "_score_value"]
sc = importlib.import_module("libs.reporting.evaluation.agent_effectiveness_scorecard")
win = importlib.import_module("libs.reporting.evaluation.attribution_score_window")
CASES = [("sc", n) for n in SC] + [("win", n) for n in WIN]
MOD = {"sc": sc, "win": win}
PATHS = {"sc": (SC_PATH, SC_BLOB, SC), "win": (WIN_PATH, WIN_BLOB, WIN)}
STEM = {"sc": "agent_effectiveness_scorecard", "win": "attribution_score_window"}
OWNERS = {(k, n): importlib.import_module(f"libs.reporting.evaluation.{STEM[k]}_{n.lstrip('_')}") for k, n in CASES}
NAN, INF = float("nan"), float("inf")


def _sha(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + bytes([0]) + raw).hexdigest()


@pytest.fixture(scope="module")
def orig_nodes():
    nodes = {}
    for key, (path, blob, names) in PATHS.items():
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
    mod = MOD[key]
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


# ---- A33-1 scorecard._mapping ----
@pytest.mark.parametrize("value", [None, {}, {"a": 1}, OrderedDict([("z", 1), ("a", 2)]), [], [("a", 1)], "s", 5, {"n": {"deep": [1]}}])
def test_scorecard_mapping(orig_nodes, monkeypatch, guards, value):
    check(orig_nodes, monkeypatch, "sc", "_mapping", value)


def test_scorecard_mapping_copy_and_order(guards):
    src = {"z": 1, "a": {"n": 1}}
    out = sc._mapping(src)
    assert out == src and out is not src and out["a"] is src["a"] and list(out) == ["z", "a"]
    od = sc._mapping(OrderedDict([("k", 1)]))
    assert type(od) is dict and sc._mapping(None) == {}


# ---- A33-2 _number ----
@pytest.mark.parametrize("value", [None, 0, 1, -2, 1.5, "2.5", " 3 ", "abc", "", NAN, INF, "-inf", "nan", [1], {}, True, b"1"])
def test_number(orig_nodes, monkeypatch, guards, value):
    check(orig_nodes, monkeypatch, "sc", "_number", value)


# ---- A33-3 _delta_state ----
def _m(prefix, count, days, delta, rate):
    return {f"{prefix}_comparison_count": count, f"{prefix}_day_count": days,
            f"average_{prefix}_delta_pct": delta, f"{prefix}_positive_delta_rate": rate}


@pytest.mark.parametrize("prefix", ["strategy_ranking_overlay", "post_scanner_refresh", "commander"])
@pytest.mark.parametrize("count,days,delta,rate", [
    (0, 0, None, None), (5, 1, 0.5, 0.9), (100, 50, None, 0.6), (100, 50, 0.9, None), (10**6, 10**6, 0.9, 0.9),
    (10**6, 10**6, 0.30, 0.55), (10**6, 10**6, 0.2999, 0.9), (10**6, 10**6, 0.9, 0.5499),
    (10**6, 10**6, -0.30, 0.45), (10**6, 10**6, -0.30, 0.4501), (10**6, 10**6, -0.9, 0.1), (10**6, 10**6, 0.1, 0.5),
    ("bad", "x", "1.0", "0.9"), (None, None, NAN, INF),
])
def test_delta_state(orig_nodes, monkeypatch, guards, prefix, count, days, delta, rate):
    check(orig_nodes, monkeypatch, "sc", "_delta_state", _m(prefix, count, days, delta, rate), prefix=prefix, missing_control="mc text")


def test_delta_state_labels_and_seams(orig_nodes, monkeypatch, guards):
    big = 10**6
    labels = {}
    for tag, args in (("nm", (0, 0, None, None)), ("va", (big, big, 0.5, 0.9)), ("dg", (big, big, -0.5, 0.1)), ("ne", (big, big, 0.1, 0.5))):
        out = check(orig_nodes, monkeypatch, "sc", "_delta_state", _m("commander", *args), prefix="commander", missing_control="MC")
        labels[tag] = (out["state"], out["missing_control"])
    assert labels == {"nm": ("NOT_MEASURABLE", "MC"), "va": ("VALUE_ADD", None), "dg": ("DEGRADING", None), "ne": ("NEUTRAL", None)}
    out = check(orig_nodes, monkeypatch, "sc", "_delta_state", {}, prefix="x", missing_control="MC",
                overrides={"DIRECTIONAL_MIN_OBSERVATIONS": 0, "DIRECTIONAL_MIN_DAYS": 0, "_number": lambda v: 0.4})
    assert out["state"] == "NEUTRAL" and out["average_delta_pct"] == 0.4  # thresholds and _number read from the facade


# ---- A33-4 _decision_state ----
@pytest.mark.parametrize("component", [{}, {"decision": "INSUFFICIENT_EVIDENCE"}, {"decision": "REJECT"}, {"decision": "DEPRECATE_CANDIDATE"},
                                       {"decision": "ADJUST_AND_RETEST"}, {"decision": "PROMOTION_CANDIDATE"}, {"decision": "promotion_candidate"},
                                       {"decision": None}, {"decision": 5}, {"decision": "KEEP"}, {"decision": ""}])
def test_decision_state(orig_nodes, monkeypatch, guards, component):
    check(orig_nodes, monkeypatch, "sc", "_decision_state", component)


def test_decision_state_exact_labels(orig_nodes, monkeypatch, guards):
    expected = {"INSUFFICIENT_EVIDENCE": "NOT_MEASURABLE", "REJECT": "DEGRADING", "DEPRECATE_CANDIDATE": "DEGRADING",
                "ADJUST_AND_RETEST": "DEGRADING", "PROMOTION_CANDIDATE": "VALUE_ADD", "promotion_candidate": "NEUTRAL", "": "NEUTRAL"}
    for decision, want in expected.items():
        assert check(orig_nodes, monkeypatch, "sc", "_decision_state", {"decision": decision}) == want


# ---- A33-5 build_agent_effectiveness_scorecard ----
def _review(**parts):
    base = {"range": {"start": "2026-04-01", "end": "2026-04-16"},
            "evidence": {"total_trade_model_count": 12, "excluded_trade_model_count": 2,
                         "decision_window_attribution": {"by_horizon": [
                             {"horizon": "+5m", "commander_comparison_count": 1},
                             "bad",
                             {"horizon": "+30m", **_m("commander", 10**6, 10**6, 0.5, 0.9), **_m("post_scanner_refresh", 3, 1, 0.1, 0.1),
                              "strategist_comparison_count": 10**6, "strategist_day_count": 10**6,
                              "average_strategist_delta_pct": -0.5, "strategist_positive_delta_rate": 0.1}]}},
            "component_decisions": {"scanner": {"decision": "PROMOTION_CANDIDATE", "relative_ranking_effect_positive": True,
                                               "absolute_cost_adjusted_edge_positive": False},
                                    "monitor_entry": {"decision": "REJECT", "finding": "f1"},
                                    "monitor_exit": {"decision": "INSUFFICIENT_EVIDENCE", "finding": "한글"},
                                    "full_system": {"decision": "PROMOTION_CANDIDATE", "finding": None}}}
    base.update(parts)
    return base


REVIEWS = [{}, {"evidence": "bad", "component_decisions": 5}, {"range": {"start": 1}}, _review(), {"evidence": {"decision_window_attribution": {"by_horizon": None}}},
           _review(component_decisions={"scanner": {"decision": "INSUFFICIENT_EVIDENCE"}}),
           _review(evidence={"total_trade_model_count": "7", "excluded_trade_model_count": 0})]


@pytest.mark.parametrize("review", REVIEWS)
def test_build_agent_effectiveness_scorecard(orig_nodes, monkeypatch, guards, review):
    check(orig_nodes, monkeypatch, "sc", "build_agent_effectiveness_scorecard", review)


def test_build_scorecard_shape_and_seams(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "sc", "build_agent_effectiveness_scorecard", _review())
    assert list(out)[:4] == ["schema_version", "contract_version", "behavior_effect", "range"]
    assert out["integrity"] == {"state": "PASS_WITH_EXCLUSIONS", "trade_model_count": 12, "excluded_trade_model_count": 2}
    assert out["components"]["scanner"]["relative_ranking_state"] == "VALUE_ADD" and out["components"]["scanner"]["absolute_edge_state"] == "DEGRADING"
    assert out["behavior_change_authorized"] is False
    seen = []
    out = check(orig_nodes, monkeypatch, "sc", "build_agent_effectiveness_scorecard", _review(),
                overrides={"_delta_state": lambda m, *, prefix, missing_control: seen.append(prefix) or {"state": "FAKE", "p": prefix},
                           "_decision_state": lambda c: "DS", "CONTRACT_VERSION": "CV"})
    assert out["contract_version"] == "CV" and out["components"]["commander"] == {"state": "FAKE", "p": "commander"}
    assert out["components"]["monitor_entry"]["state"] == "DS" and seen[:3] == ["strategy_ranking_overlay", "post_scanner_refresh", "commander"]


# ---- A33-6 render_agent_effectiveness_scorecard ----
PAYLOADS = [{}, {"range": {"start": "a", "end": "b"}}, {"components": 5},
            sc.build_agent_effectiveness_scorecard(_review()), sc.build_agent_effectiveness_scorecard({}),
            {"range": {"start": "시작", "end": "끝"}, "components": {"commander": {"state": "NOT_MEASURABLE", "missing_control": "한글 control"},
                                                                 "strategist": {"full_contribution": {"state": "NOT_MEASURABLE", "reason": "r"}}}}]


@pytest.mark.parametrize("payload", PAYLOADS)
def test_render_agent_effectiveness_scorecard(orig_nodes, monkeypatch, guards, payload):
    out = check(orig_nodes, monkeypatch, "sc", "render_agent_effectiveness_scorecard", payload)
    assert out.endswith("\n") and "\r" not in out


def test_render_exact_header_and_shortfalls(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "sc", "render_agent_effectiveness_scorecard", PAYLOADS[5])
    assert out.startswith("# Agent Effectiveness Scorecard (시작 ~ 끝)\n\nEvaluation-only.")
    assert "- Commander: 한글 control" in out and "- Strategist full: r" in out
    assert check(orig_nodes, monkeypatch, "sc", "render_agent_effectiveness_scorecard", {}).count("None") >= 2


# ---- A33-7 window._mapping ----
@pytest.mark.parametrize("value", [None, {}, {"a": 1}, OrderedDict([("z", 1)]), [], "s", 5])
def test_window_mapping(orig_nodes, monkeypatch, guards, value):
    check(orig_nodes, monkeypatch, "win", "_mapping", value)


def test_window_mapping_identity(guards):
    src = {"a": 1}
    assert win._mapping(src) is src  # unlike scorecard._mapping (copy)
    od = OrderedDict([("k", 1)])
    assert win._mapping(od) is od
    e1, e2 = win._mapping(None), win._mapping(None)
    assert e1 == {} and e1 is not e2


# ---- A33-8 _score_value ----
@pytest.mark.parametrize("row", [
    {}, {"scores": None}, {"scores": {}}, {"scores": {"k": None}}, {"scores": {"k": {}}}, {"scores": {"k": {"status": "INSUFFICIENT_EVIDENCE", "score": 5}}},
    {"scores": {"k": {"score": None}}}, {"scores": {"k": {"score": 3}}}, {"scores": {"k": {"score": "2.5"}}}, {"scores": {"k": {"score": 2.5}}},
    {"scores": {"k": {"score": 3.5}}}, {"scores": {"k": {"score": -1.5}}}, {"scores": {"k": {"score": "bad"}}}, {"scores": {"k": {"score": NAN}}},
    {"scores": {"k": {"score": INF}}}, {"scores": {"k": {"score": [1]}}}, {"scores": {"k": {"status": "OK", "score": 4}}}, {"scores": "bad"}, {"scores": {"k": 5}},
])
def test_score_value(orig_nodes, monkeypatch, guards, row):
    check(orig_nodes, monkeypatch, "win", "_score_value", row, "k")


def test_score_value_seam(orig_nodes, monkeypatch, guards):
    assert check(orig_nodes, monkeypatch, "win", "_score_value", {"scores": {"k": {"score": 9}}}, "k",
                 overrides={"_mapping": lambda v: {"score": 1.4, "k": {"score": 1.4}} if isinstance(v, dict) else {}}) == 1


# ---- structure ----
@pytest.mark.parametrize("key,name", CASES)
def test_wrapper_thin_and_owner_holds_body(key, name):
    wrapper = ast.parse(inspect.getsource(getattr(MOD[key], name))).body[0]
    assert len(wrapper.body) == 1 and isinstance(wrapper.body[0], ast.Return)
    assert not [n for n in ast.walk(wrapper) if isinstance(n, (ast.If, ast.For, ast.Try, ast.ListComp, ast.GeneratorExp))]
    call = wrapper.body[0].value
    assert isinstance(call, ast.Call) and "facade" in [k.arg for k in call.keywords], "wrapper must forward to the Owner with facade="
    owner_fn = getattr(OWNERS[(key, name)], name)
    node = ast.parse(inspect.getsource(owner_fn)).body[0]
    assert len(node.body) >= 1 and owner_fn.__module__ == OWNERS[(key, name)].__name__
    src = inspect.getsource(OWNERS[(key, name)]).replace(f"{STEM[key]}_", "")
    assert f"{STEM[key]} import" not in src and f"import {STEM[key]}" not in src
