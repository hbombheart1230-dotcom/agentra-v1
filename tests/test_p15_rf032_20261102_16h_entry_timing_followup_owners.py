"""RF-032 A40-1..8: eight more ``entry_timing_attribution`` bodies, original vs thin wrappers + Owners.

Pure/fake only; no UEF/validation-id writer is touched. Original: A preimage f58b41a8 (blob 7f05994c, i.e. after the
A39 wrappers). The canonical blob a7559c35 predates A39 but its selected function bodies are identical, which is
asserted by comparing function source text. ASTs are compiled in a copy of the live namespace; dependency overrides
apply to both sides. ``_read_json`` is tested with fake path objects and ``attach_forward_outcomes`` is a fake, so
there is no real file access, sockets, subprocess or writes.
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

A_PRE = "f58b41a85dd92e3954b6accf910e01f0c224a399"
CANON = "aa8334435fe321e9ef62532abf5f40e54b8b64fc"
PATH = "libs/reporting/evaluation/entry_timing_attribution.py"
A_BLOB = "7f05994c5f8d9a9b4c06ff6e5fd748f640f2222b"
CANON_BLOB = "a7559c358b7ff8e6048586ba1d42a97480ad3c79"
NAMES = ["_mapping", "_num", "_read_json", "_entry_forward", "_checkpoint", "_label", "_fmt", "render_entry_timing_attribution_report"]
mod = importlib.import_module("libs.reporting.evaluation.entry_timing_attribution")
OWNERS = {n: importlib.import_module(f"libs.reporting.evaluation.entry_timing_attribution_{n.lstrip('_')}") for n in NAMES}
NAN, INF = float("nan"), float("inf")


def _sha(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + bytes([0]) + raw).hexdigest()


def _nodes(raw):
    tree = ast.parse(raw.decode("utf-8"))
    found = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in NAMES}
    assert sorted(found) == sorted(NAMES)
    return found


@pytest.fixture(scope="module")
def orig_nodes():
    try:
        a_raw = subprocess.run(["git", "show", f"{A_PRE}:{PATH}"], check=True, capture_output=True).stdout
        c_raw = subprocess.run(["git", "show", f"{CANON}:{PATH}"], check=True, capture_output=True).stdout
    except subprocess.CalledProcessError as exc:
        pytest.fail(f"BLOCKED_PIN: {exc.stderr!r}")
    assert _sha(a_raw) == A_BLOB, "BLOCKED_PIN actor blob"
    assert _sha(c_raw) == CANON_BLOB, "BLOCKED_PIN canonical blob"
    a, c = _nodes(a_raw), _nodes(c_raw)
    for n in NAMES:  # selected function bodies identical across A and canonical
        assert ast.get_source_segment(a_raw.decode(), a[n]) == ast.get_source_segment(c_raw.decode(), c[n]), f"HOLD: {n} differs"
    return a


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


# ---- A40-1 _mapping ----
@pytest.mark.parametrize("value", [None, {}, {"a": 1}, [], [("a", 1)], "s", 5, {"n": {"deep": [1]}}])
def test_mapping(orig_nodes, monkeypatch, guards, value):
    check(orig_nodes, monkeypatch, "_mapping", value)


def test_mapping_identity_and_seam(orig_nodes, monkeypatch, guards):
    src = {"a": 1}
    assert mod._mapping(src) is src  # identity, no copy
    e1, e2 = mod._mapping(None), mod._mapping(None)
    assert e1 == {} and e1 is not e2

    class NeverMapping:
        pass
    assert check(orig_nodes, monkeypatch, "_mapping", {"a": 1}, overrides={"Mapping": NeverMapping}) == {}


# ---- A40-2 _num ----
class _BadFloat:
    def __repr__(self):
        return "_BadFloat()"

    def __float__(self):
        raise RuntimeError("custom float failure")


class _TypeFloat:
    def __repr__(self):
        return "_TypeFloat()"

    def __float__(self):
        raise TypeError("custom type failure")


class _Num:
    def __repr__(self):
        return "_Num()"

    def __float__(self):
        return 2.5


@pytest.mark.parametrize("value", [None, "", 0, 1, -2.5, True, False, "3.5", " 4 ", "abc", NAN, INF, "nan", "-inf", [1], {}, b"1", (1,), _Num(), _TypeFloat()])
def test_num(orig_nodes, monkeypatch, guards, value):
    check(orig_nodes, monkeypatch, "_num", value)


def test_num_does_not_broaden_exceptions(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "_num", _BadFloat())
    assert out == ("err", "RuntimeError", "custom float failure")  # only TypeError / ValueError are caught
    assert check(orig_nodes, monkeypatch, "_num", _Num()) == 2.5


# ---- A40-3 _read_json (fake path objects) ----
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


READ = [('{"a": 1, "b": [1, 2]}', None), ("[1, 2]", None), ("5", None), ('"s"', None), ("null", None), ("not json", None), ("", None), ('{"한글": "값"}', None),
        (None, OSError("fake io")), (None, UnicodeDecodeError("utf-8", b"\xff", 0, 1, "bad")), (None, PermissionError("fake perm"))]


@pytest.mark.parametrize("text,error", READ)
def test_read_json(orig_nodes, monkeypatch, guards, text, error):
    out = check(orig_nodes, monkeypatch, "_read_json", FakeReadPath(text, error))
    assert isinstance(out, dict)
    p = FakeReadPath(text, error)
    mod._read_json(p)
    assert p.calls == ["utf-8"]


def test_read_json_values_and_json_seam(orig_nodes, monkeypatch, guards):
    assert check(orig_nodes, monkeypatch, "_read_json", FakeReadPath('{"x": 1}')) == {"x": 1}
    assert check(orig_nodes, monkeypatch, "_read_json", FakeReadPath("[1]")) == {}

    class FakeJson:
        @staticmethod
        def loads(text):
            return {"fake": text}
    assert check(orig_nodes, monkeypatch, "_read_json", FakeReadPath("anything"), overrides={"json": FakeJson}) == {"fake": "anything"}


# ---- A40-4 _entry_forward ----
def _attach_factory(outcome, rows=True):
    calls = []

    def attach(items, *, minute_rows_by_symbol):
        calls.append((copy.deepcopy(items), minute_rows_by_symbol))
        if not rows:
            return []
        out = copy.deepcopy(items)
        out[0]["shadow_forward_outcome"] = copy.deepcopy(outcome)
        return out
    attach.calls = calls
    return attach


EF_KW = dict(trade_id="T1", symbol="005930", entry_epoch=1776297600, entry_price=100.0, minute_rows_by_symbol={"005930": [{"ts": 1}]})
OUTCOMES = [{}, {"available": True, "reason": None, "observed_checkpoint_count": 2, "checkpoints": {"+5m": {"status": "observed", "return_pct": 1.0}, "+60m": {"status": "pending"}}},
            {"available": False, "reason": "minute_rows_unavailable", "checkpoints": "bad"}, {"checkpoints": {"+15m": {}, "+30m": None, "+999m": {"x": 1}}}]


@pytest.mark.parametrize("override", [dict(symbol=""), dict(entry_epoch=0), dict(entry_epoch=-1), dict(entry_price=None), dict(entry_price=0.0), dict(entry_price=-5.0), {}])
def test_entry_forward_baselines(orig_nodes, monkeypatch, guards, override):
    attach = _attach_factory(OUTCOMES[1])
    check(orig_nodes, monkeypatch, "_entry_forward", **{**EF_KW, **override}, overrides={"attach_forward_outcomes": attach})


@pytest.mark.parametrize("outcome", OUTCOMES)
@pytest.mark.parametrize("rows", [True, False])
def test_entry_forward_outcomes(orig_nodes, monkeypatch, guards, outcome, rows):
    attach = _attach_factory(outcome, rows)
    out = check(orig_nodes, monkeypatch, "_entry_forward", **EF_KW, overrides={"attach_forward_outcomes": attach})
    assert list(out["checkpoints"]) == ["+5m", "+15m", "+30m", "+60m"] and len(attach.calls) == 2  # once per side


def test_entry_forward_call_args_and_seams(orig_nodes, monkeypatch, guards):
    attach = _attach_factory(OUTCOMES[1])
    out = check(orig_nodes, monkeypatch, "_entry_forward", **EF_KW, overrides={"attach_forward_outcomes": attach})
    items, rows = attach.calls[0]
    assert items == [{"symbol": "005930", "trade_id": "T1", "generated_at": "2026-04-16T00:00:00+00:00",
                      "shadow_forward_base": {"available": True, "baseline_epoch": 1776297600, "baseline_price": 100.0, "source": "actual_entry"}}]
    assert out["available"] is True and out["observed_checkpoint_count"] == 2 and out["checkpoints"]["+15m"] == {"status": "pending"}
    assert check(orig_nodes, monkeypatch, "_entry_forward", **{**EF_KW, "symbol": ""}) == {"available": False, "reason": "entry_baseline_unavailable", "checkpoints": {}}
    out = check(orig_nodes, monkeypatch, "_entry_forward", **EF_KW,
                overrides={"attach_forward_outcomes": _attach_factory({"available": True, "checkpoints": {"+5m": {"status": "x"}}}), "HORIZONS": ("+5m", "+7m"),
                           "_iso": lambda e: "FAKE_ISO"})
    assert list(out["checkpoints"]) == ["+5m", "+7m"]


# ---- A40-5 _checkpoint ----
@pytest.mark.parametrize("forward,horizon", [({}, "+5m"), ({"checkpoints": None}, "+5m"), ({"checkpoints": "bad"}, "+5m"), ({"checkpoints": {}}, "+5m"),
                                              ({"checkpoints": {"+5m": {"return_pct": 1}}}, "+5m"), ({"checkpoints": {"+5m": "bad"}}, "+5m"), ({"checkpoints": {"+5m": {"a": 1}}}, "+15m")])
def test_checkpoint(orig_nodes, monkeypatch, guards, forward, horizon):
    check(orig_nodes, monkeypatch, "_checkpoint", forward, horizon)


def test_checkpoint_identity_and_helper_order(orig_nodes, monkeypatch, guards):
    inner = {"return_pct": 1}
    forward = {"checkpoints": {"+5m": inner}}
    assert mod._checkpoint(forward, "+5m") is inner
    seen = []
    out = check(orig_nodes, monkeypatch, "_checkpoint", {"checkpoints": {"+5m": 1}}, "+5m",
                overrides={"_mapping": lambda v: seen.append(v) or ({"+5m": 7} if len(seen) % 2 == 1 else {"z": v})})
    assert out == {"z": 7} and len(seen) == 4  # outer _mapping first (checkpoints), then inner; once per side


# ---- A40-6 _label ----
def _cp(ret=None, mfe=None, mae=None):
    return {k: v for k, v in (("return_pct", ret), ("mfe_pct", mfe), ("mae_pct", mae)) if v is not None}


def _fw(c5=None, c15=None, c30=None):
    return {"checkpoints": {"+5m": c5 or {}, "+15m": c15 or {}, "+30m": c30 or {}}}


LABEL_CASES = [
    dict(scanner_to_entry_delay_sec=None, pre_entry_move_pct=None, forward=_fw()),
    dict(scanner_to_entry_delay_sec=200, pre_entry_move_pct=None, forward=_fw(_cp(1.0, 0.6, -0.1))),
    dict(scanner_to_entry_delay_sec=180, pre_entry_move_pct=0.35, forward=_fw(_cp(-0.1, 0.1, -0.2), _cp(-0.2))),
    dict(scanner_to_entry_delay_sec=179, pre_entry_move_pct=0.3499, forward=_fw(_cp(-0.1, 0.1, -0.56))),
    dict(scanner_to_entry_delay_sec=10, pre_entry_move_pct=0.19, forward=_fw(_cp(-0.1, 0.1, -0.55))),
    dict(scanner_to_entry_delay_sec=10, pre_entry_move_pct=0.2, forward=_fw(_cp(-0.1, 0.1, -0.55))),
    dict(scanner_to_entry_delay_sec=10, pre_entry_move_pct=0.0, forward=_fw(_cp(0.0, 0.49, -0.3))),
    dict(scanner_to_entry_delay_sec=10, pre_entry_move_pct=0.0, forward=_fw(_cp(0.0, 0.5, -0.3))),
    dict(scanner_to_entry_delay_sec=10, pre_entry_move_pct=0.0, forward=_fw(_cp(0.0, 0.1, -0.1), _cp(0.2))),
    dict(scanner_to_entry_delay_sec=10, pre_entry_move_pct=0.0, forward=_fw(_cp(0.0, 0.1, -0.1))),
]


@pytest.mark.parametrize("kw", LABEL_CASES)
@pytest.mark.parametrize("horizon", ["", "5m", "SWING", "overnight", " Position ", "1-2day", "1_2day", "intraday", " INTRADAY "])
def test_label(orig_nodes, monkeypatch, guards, kw, horizon):
    check(orig_nodes, monkeypatch, "_label", **kw, strategy_horizon=horizon)


INTRA = [
    dict(pre_entry_move_pct=None, forward=_fw(c15=_cp(None), c30=_cp(1.0))),
    dict(pre_entry_move_pct=0.35, forward=_fw(c15=_cp(-0.1, 0.1, -0.2), c30=_cp(-0.1))),
    dict(pre_entry_move_pct=0.1, forward=_fw(c15=_cp(-0.1, 0.1, -0.75), c30=_cp(-0.1))),
    dict(pre_entry_move_pct=0.2, forward=_fw(c15=_cp(-0.1, 0.1, -0.75), c30=_cp(-0.1))),
    dict(pre_entry_move_pct=None, forward=_fw(c15=_cp(0.1, 0.1, -0.1), c30=_cp(-0.1))),
    dict(pre_entry_move_pct=None, forward=_fw(c15=_cp(-0.1, 0.7, -0.1), c30=_cp(-0.1))),
    dict(pre_entry_move_pct=None, forward=_fw(c15=_cp(-0.1, 0.69, -0.1), c30=_cp(0.0))),
]


@pytest.mark.parametrize("kw", INTRA)
def test_label_intraday_branch(orig_nodes, monkeypatch, guards, kw):
    out = check(orig_nodes, monkeypatch, "_label", scanner_to_entry_delay_sec=None, strategy_horizon="intraday", **kw)
    assert out[0] in {"ENTRY_TOO_LATE", "ENTRY_TOO_EARLY", "ENTRY_APPROPRIATE", "INSUFFICIENT_EVIDENCE"}


def test_label_values_and_helper_seams(orig_nodes, monkeypatch, guards):
    assert check(orig_nodes, monkeypatch, "_label", **LABEL_CASES[2], strategy_horizon="") == ("ENTRY_TOO_LATE", ["scanner_to_entry_delay>=180s", "pre_entry_move>=0.35pct_then_forward_weak"])
    assert check(orig_nodes, monkeypatch, "_label", **LABEL_CASES[1], strategy_horizon="") == ("ENTRY_APPROPRIATE", ["scanner_to_entry_delay>=180s", "favorable_forward_response"])
    assert check(orig_nodes, monkeypatch, "_label", **LABEL_CASES[0], strategy_horizon="swing") == ("INSUFFICIENT_EVIDENCE", ["strategy_horizon_exceeds_entry_timing_observation_window"])
    seen = []
    out = check(orig_nodes, monkeypatch, "_label", **LABEL_CASES[0], strategy_horizon="",
                overrides={"_checkpoint": lambda f, h: seen.append(h) or {}, "_num": lambda v: 1.0})
    assert out[0] == "ENTRY_APPROPRIATE" and seen == ["+5m", "+15m", "+30m"] * 2


# ---- A40-7 _fmt ----
class _StrOnly:
    def __float__(self):
        raise ValueError("no float")

    def __str__(self):
        return "STR_ONLY"

    def __repr__(self):
        return "_StrOnly()"


@pytest.mark.parametrize("value", [None, "", 0, -0.0, 1, 1.23456, -2.5, "3.14159", " 7 ", "abc", NAN, INF, "-inf", True, [1], {}, _StrOnly(), _BadFloat()])
@pytest.mark.parametrize("suffix", ["", "%", " pts"])
def test_fmt(orig_nodes, monkeypatch, guards, value, suffix):
    check(orig_nodes, monkeypatch, "_fmt", value, suffix)


def test_fmt_values_and_default_suffix(orig_nodes, monkeypatch, guards):
    assert check(orig_nodes, monkeypatch, "_fmt", None) == "-" and check(orig_nodes, monkeypatch, "_fmt", "") == "-"
    assert check(orig_nodes, monkeypatch, "_fmt", 1.23456, "%") == "1.2346%"
    assert check(orig_nodes, monkeypatch, "_fmt", "abc") == "abc"
    assert check(orig_nodes, monkeypatch, "_fmt", _StrOnly(), "%") == "STR_ONLY"
    assert check(orig_nodes, monkeypatch, "_fmt", _BadFloat()) == ("err", "RuntimeError", "custom float failure")  # not broadened


# ---- A40-8 render_entry_timing_attribution_report ----
RPAY = {"day": "2026-04-16", "behavior_effect": "observation_only", "trade_count": 3,
        "label_summary": [{"label": "ENTRY_APPROPRIATE", "trade_count": 2, "performance": {"win_rate": 0.5, "average_return_pct": 0.25}, "avg_scanner_to_entry_delay_sec": 40,
                           "avg_5m_mfe_pct": 0.6, "avg_5m_mae_pct": -0.2}, "bad", {"label": "X", "performance": "bad"}],
        "rows": [{"trade_id": "T1", "symbol": "005930", "label": "ENTRY_TOO_LATE", "scanner_to_entry_delay_sec": 200, "pre_entry_move_pct": 0.4,
                  "entry_forward_quality": {"+5m_return_pct": -0.1, "+5m_mfe_pct": 0.1, "+5m_mae_pct": -0.3}, "entry_return_pct": -0.5, "label_reasons": ["r1", "한글"]},
                 None, {"trade_id": "T2", "entry_forward_quality": "bad"}],
        "limitations": ["lim one", "lim 둘"]}
RPAYS = [{}, {"day": "d"}, {"label_summary": None, "rows": None, "limitations": None}, {"rows": ["bad", 5]}, RPAY, {**RPAY, "limitations": []}]


@pytest.mark.parametrize("payload", RPAYS)
def test_render_entry_timing_attribution_report(orig_nodes, monkeypatch, guards, payload):
    out = check(orig_nodes, monkeypatch, "render_entry_timing_attribution_report", payload)
    assert out.endswith("\n") and "\r" not in out


def test_render_exact_bits_and_seams(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "render_entry_timing_attribution_report", RPAY)
    assert out.startswith("# Q13 Entry Timing Attribution - 2026-04-16\n\n- Behavior effect: `observation_only`\n- Trades: 3\n")
    assert "| ENTRY_APPROPRIATE | 2 | 50.0000% | 0.2500% | 40.0000 | 0.6000% | -0.2000% |" in out
    assert "| T1 | 005930 | ENTRY_TOO_LATE | 200.0000 | 0.4000% | -0.1000% | 0.1000% | -0.3000% | -0.5000% | r1, 한글 |" in out
    assert out.endswith("- lim one\n- lim 둘\n")
    assert "| T2 | None | None | - | - | - | - | - | - | - |" in out
    out = check(orig_nodes, monkeypatch, "render_entry_timing_attribution_report", {"label_summary": [{"label": "L"}], "rows": [{"trade_id": "T"}]},
                overrides={"_fmt": lambda v, suffix="": f"<{v}{suffix}>", "_mapping": lambda v: dict(v) if isinstance(v, dict) else {}})
    assert "<0.0%>" in out and "<None>" in out


# ---- structure ----
@pytest.mark.parametrize("name", NAMES)
def test_wrapper_thin_and_owner_holds_body(name):
    wrapper = ast.parse(inspect.getsource(getattr(mod, name))).body[0]
    stmts = [n for n in wrapper.body if not (isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant))]
    assert len(stmts) == 1 and isinstance(stmts[0], ast.Return)
    assert not [n for n in ast.walk(wrapper) if isinstance(n, (ast.If, ast.For, ast.Try, ast.ListComp, ast.GeneratorExp))]
    call = stmts[0].value
    assert isinstance(call, ast.Call) and "facade" in [k.arg for k in call.keywords], "wrapper must forward to the Owner with facade="
    owner_fn = getattr(OWNERS[name], name)
    node = ast.parse(inspect.getsource(owner_fn)).body[0]
    assert len(node.body) >= 1 and owner_fn.__module__ == OWNERS[name].__name__
    src = inspect.getsource(OWNERS[name]).replace("entry_timing_attribution_", "")
    assert "entry_timing_attribution import" not in src and "import entry_timing_attribution" not in src
