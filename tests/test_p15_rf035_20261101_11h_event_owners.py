"""P15 RF-035 (20261101-11h): eight live_execution_event_evidence helpers moved to projection Owners; parity with the pre-move bodies (stdlib unittest)."""
from __future__ import annotations

import ast
import hashlib
import inspect
import json
import unittest
from unittest import mock

from libs.reporting import live_event_canonical_filter_projection as filter_owner
from libs.reporting import live_event_expand_run_ids_projection as expand_owner
from libs.reporting import live_event_identity_merge_projection as merge_owner
from libs.reporting import live_event_latest_payload_projection as latest_owner
from libs.reporting import live_event_name_projection as name_owner
from libs.reporting import live_event_row_name_projection as row_name_owner
from libs.reporting import live_event_strategist_source_ids_projection as source_ids_owner
from libs.reporting import live_event_symbol_projection as symbol_owner
from libs.reporting import live_execution_event_evidence as ev

GOLDENS = {
    "a1": "e47e1c89055f1c260541616402722a7420cbf78d09b6cff4ccd8cac240bad9ae",
    "a2": "efc0df5baf08b09017e54425a8a068289425ce05b73fd3ba44334c9ebfc7cdbd",
    "a3": "1840843a88be86189da29d9123cf98c10f63e93f5b280dd5f919a5b9db19f3fe",
    "a4": "1d4daa3fb107f6147cda0748ffb7b3a484a958de8a95da12122bf99aa08df8d8",
    "a5": "3defb5bb52f9c639311373eb381b0da9900527a5b1ea670118caf5bf98453780",
    "a6": "86a3ee90207ec074a20afa2db29a4b98e3860eba5b1eb604a981ac677571fb3d",
    "a7": "29b0e127072abf148fe34abc7591b40de1ae1e83020befbe0fa287fb263271b3",
    "a8": "abccc1a4bbbdc40ee82068125375209fcb5557a08f2a736a169673b70d7d77a7",
}


def _call(fn):
    try:
        return ["ok", fn()]
    except BaseException as exc:  # noqa: BLE001 - parity of exception type/message is the point
        return ["exc", type(exc).__name__, str(exc)]


def _h(obj):
    return hashlib.sha256(json.dumps(obj, ensure_ascii=False, default=repr).encode()).hexdigest()


class _Odd:
    def __bool__(self):
        raise RuntimeError("odd-bool")

    def __str__(self):
        return " Odd "


def _fake_symbol(value, allow_test_symbols=False):
    return f"SYM:{value}:{allow_test_symbols}"


def _a1(fn, mod):
    rows = [{"event_name": " scanner.hit "}, {"stage": "scanner", "event": "hit"}, {}, {"stage": "s"}, {"event": "e"}, {"event_name": "", "stage": " a ", "event": " b "}, {"event_name": None, "stage": None, "event": 5}, {"event_name": 0, "event": "x"}, None, [], _Odd()]
    return [_call(lambda r=r: fn(r)) for r in rows] + [_call(lambda: fn())]


def _a2(fn, mod):
    rows = [{"symbol": "005930"}, {"payload": {"selected_symbol": "000660"}}, {"payload": {"symbol": "A", "selected_symbol": "B"}}, {"payload": {"position_symbol": "P"}}, {}, {"payload": [1], "symbol": "Z"}, {"symbol": " 005930 "}, {"symbol": "abc"}, {"symbol": None, "payload": {"symbol": None, "selected_symbol": None, "position_symbol": "q"}}, None, []]
    out = [_call(lambda r=r: fn(r)) for r in rows] + [_call(lambda: fn())]
    with mock.patch.object(ev, "normalize_symbol", _fake_symbol):
        out += [_call(lambda r=r: fn(r)) for r in rows[:5]]
    return out


def _a3(fn, mod):
    rows = [{"name": "fallback"}, {"event_name": "x"}, {}, {"event": "e", "name": "n"}, {"event_name": "", "name": "", "event": " ev "}, {"event_name": 0, "name": None, "event": 7}, None, [], _Odd()]
    return [_call(lambda r=r: fn(r)) for r in rows] + [_call(lambda: fn())]


def _a4(fn, mod):
    r1 = {"ts": "1", "run_id": "r", "event_name": "e", "symbol": "005930"}
    r2 = dict(r1)
    r3 = {"timestamp": "1", "run_id": "r", "name": "e", "payload": {"symbol": "005930"}}
    r4 = {"ts": "2", "run_id": "r", "event": "e2"}
    out = []
    res = fn([r1, "junk", None], [r2, r4], [r3])
    out.append(["identity", [len(res), res[0] is r1, res[1] is r4]])
    out += [
        _call(lambda: fn([r1, r2])),
        _call(lambda: fn()),
        _call(lambda: fn([])),
        _call(lambda: fn(None)),
        _call(lambda: fn(None, [r1])),
        _call(lambda: fn(iter([r1, r2, r4]))),
        _call(lambda: fn([r4], [r1])),
        _call(lambda: fn([1, "x", []])),
        _call(lambda: fn(5)),
    ]
    with mock.patch.object(ev, "event_row_name", lambda row: "SAME"), mock.patch.object(ev, "event_row_symbol", lambda row: "S"):
        out.append(_call(lambda: fn([r1, r4], [r3])))
    with mock.patch.object(ev, "event_row_name", lambda row: row.get("ts")), mock.patch.object(ev, "event_row_symbol", lambda row: ""):
        out.append(_call(lambda: fn([r1, r4])))
    return out


def _ev_rows():
    return [
        {"ts": "2026-11-01T00:00:02Z", "agent": "strategist", "run_id": "r1", "event_name": "strategist.decision_frame", "payload": {"a": 1}, "level": "warn", "symbol": 5},
        {"ts": "2026-11-01T00:00:01Z", "stage": "Strategist", "run_id": "r1", "event": "decision_frame", "trade_id": "T", "payload": [1]},
        {"ts": "2026-11-01T00:00:03Z", "agent": "commander", "run_id": "r1", "event_name": "strategist.decision_frame"},
        {"ts": "2026-11-01T00:00:04Z", "agent": "strategist", "run_id": "r2", "event_name": "strategist.decision_frame"},
        {"ts": "bad", "agent": "strategist", "run_id": "r1", "event_name": "other"},
        {"agent": "strategist", "run_id": " r1 ", "event_name": "strategist.decision_frame", "payload": {"b": 2}},
    ]


def _a5(fn, mod):
    rows = _ev_rows()
    res = fn(rows, run_ids=["r1"], agent="strategist", event_names=["strategist.decision_frame"])
    out = [
        _call(lambda: fn(rows, run_ids=["r1"], agent="strategist", event_names=["strategist.decision_frame"])),
        _call(lambda: fn(rows, run_ids=[], agent="strategist", event_names=[])),
        _call(lambda: fn(rows, run_ids=["r2"], agent=" STRATEGIST ", event_names=None)),
        _call(lambda: fn(rows, run_ids=None, agent="commander", event_names=["strategist.decision_frame"])),
        _call(lambda: fn([], run_ids=["r1"], agent="a", event_names=[])),
        _call(lambda: fn(rows, run_ids=["", None], agent=None, event_names=["x"])),
        _call(lambda: fn([None], run_ids=[], agent="a", event_names=[])),
        _call(lambda: fn(None, run_ids=[], agent="a", event_names=[])),
        _call(lambda: fn(rows)),
        _call(lambda: fn()),
        ["copy", [res[0]["payload"] is not rows[1].get("payload"), isinstance(res[0]["payload"], dict)]],
    ]
    with mock.patch.object(ev, "to_epoch", lambda v: -1 if v == "bad" else 0), mock.patch.object(ev, "row_event_name", lambda row: "strategist.decision_frame"):
        out.append(_call(lambda: fn(rows, run_ids=["r1"], agent="strategist", event_names=["strategist.decision_frame"])))
    with mock.patch.object(ev, "to_epoch", lambda v: {"2026-11-01T00:00:02Z": 1}.get(v)):
        out.append(_call(lambda: fn(rows, run_ids=["r1"], agent="strategist", event_names=["strategist.decision_frame"])))
    return out


def _cached_rows(frame_ts=190, fast_ts=200, reuse=180):
    return [
        {"run_id": "r0", "agent": "strategist", "event_name": "strategist.decision_frame", "ts": frame_ts},
        {"run_id": "r1", "agent": "commander", "event_name": "commander_router.fast_path", "ts": fast_ts, "payload": {"path": "integrated_chain_cached_frame", "reuse_sec": reuse}},
    ]


def _a6(fn, mod):
    lifecycle = {"run_ids_all": ["r1"]}
    direct = [{"run_id": "r1", "agent": "strategist", "event_name": "strategist.decision_frame", "ts": 1}]
    out = [
        _call(lambda: fn(event_rows=direct, lifecycle=lifecycle)),
        _call(lambda: fn(event_rows=_cached_rows(), lifecycle=lifecycle)),
        _call(lambda: fn(event_rows=_cached_rows(frame_ts=100), lifecycle=lifecycle)),
        _call(lambda: fn(event_rows=_cached_rows(frame_ts=100, reuse=500), lifecycle=lifecycle)),
        _call(lambda: fn(event_rows=_cached_rows(frame_ts=250), lifecycle=lifecycle)),
        _call(lambda: fn(event_rows=_cached_rows(), lifecycle={})),
        _call(lambda: fn(event_rows=[], lifecycle=lifecycle)),
        _call(lambda: fn(event_rows=_cached_rows(reuse="bad"), lifecycle=lifecycle)),
        _call(lambda: fn(event_rows=_cached_rows(reuse=1), lifecycle={"run_ids_all": ["r1", "r1", " ", None]})),
        _call(lambda: fn(event_rows=[dict(_cached_rows()[1], payload={"path": "other"}), _cached_rows()[0]], lifecycle=lifecycle)),
        _call(lambda: fn(event_rows=[dict(_cached_rows()[0], run_id="")] + _cached_rows()[1:], lifecycle=lifecycle)),
        _call(lambda: fn(event_rows=_cached_rows() + [{"run_id": "r1", "agent": "strategist", "event_name": "strategist.llm_response_saved", "ts": 5}], lifecycle=lifecycle)),
        _call(lambda: fn(event_rows=None, lifecycle=lifecycle)),
        _call(lambda: fn(event_rows=[], lifecycle=None)),
        _call(lambda: fn()),
    ]
    with mock.patch.object(ev, "safe_int", lambda v, d=0: 1000):
        out.append(_call(lambda: fn(event_rows=_cached_rows(frame_ts=100), lifecycle=lifecycle)))
    with mock.patch.object(ev, "to_epoch", lambda v: 0):
        out.append(_call(lambda: fn(event_rows=_cached_rows(), lifecycle=lifecycle)))
    with mock.patch.object(ev, "row_event_name", lambda row: "strategist.decision_frame"):
        out.append(_call(lambda: fn(event_rows=_cached_rows(), lifecycle=lifecycle)))
    return out


def _a7(fn, mod):
    out = [
        _call(lambda: fn(event_rows=_cached_rows(), targeted_run_ids=["r1"])),
        _call(lambda: fn(event_rows=_cached_rows(frame_ts=100), targeted_run_ids=["r1"])),
        _call(lambda: fn(event_rows=_cached_rows(frame_ts=100, reuse=500), targeted_run_ids=["r1"])),
        _call(lambda: fn(event_rows=[], targeted_run_ids=["r1"])),
        _call(lambda: fn(event_rows=_cached_rows(), targeted_run_ids=[])),
        _call(lambda: fn(event_rows=_cached_rows(), targeted_run_ids=None)),
        _call(lambda: fn(event_rows=_cached_rows()[:1], targeted_run_ids=["r1"])),
        _call(lambda: fn(event_rows=_cached_rows()[1:], targeted_run_ids=["r1"])),
        _call(lambda: fn(event_rows=_cached_rows(), targeted_run_ids=iter(["r1", " ", None]))),
        _call(lambda: fn(event_rows=[dict(_cached_rows()[1], payload={"path": "x"}), _cached_rows()[0]], targeted_run_ids=["r1"])),
        _call(lambda: fn(event_rows=_cached_rows(reuse="bad"), targeted_run_ids=["r1"])),
        _call(lambda: fn(event_rows=None, targeted_run_ids=["r1"])),
        _call(lambda: fn()),
    ]
    with mock.patch.object(ev, "safe_int", lambda v, d=0: 1000):
        out.append(_call(lambda: fn(event_rows=_cached_rows(frame_ts=100), targeted_run_ids=["r1"])))
    with mock.patch.object(ev, "to_epoch", lambda v: 0):
        out.append(_call(lambda: fn(event_rows=_cached_rows(), targeted_run_ids=["r1"])))
    with mock.patch.object(ev, "row_event_name", lambda row: "commander_router.fast_path"):
        out.append(_call(lambda: fn(event_rows=_cached_rows(), targeted_run_ids=["r1"])))
    return out


def _a8(fn, mod):
    inner = {"a": 1}
    res = fn([{"payload": inner}])
    out = [
        ["copy", [res == inner, res is not inner]],
        _call(lambda: fn([])),
        _call(lambda: fn([{"payload": {"a": 1}}, "junk"])),
        _call(lambda: fn([{"payload": [1]}])),
        _call(lambda: fn([{"payload": None}])),
        _call(lambda: fn([{}])),
        _call(lambda: fn([{"payload": {}}])),
        _call(lambda: fn(None)),
        _call(lambda: fn([5])),
        _call(lambda: fn()),
        _call(lambda: fn(iter([{"payload": {}}]))),
    ]
    return out


CASES = {
    "a1": (_a1, "row_event_name", lambda: name_owner.row_event_name, False, name_owner),
    "a2": (_a2, "event_row_symbol", lambda: symbol_owner.event_row_symbol, True, symbol_owner),
    "a3": (_a3, "event_row_name", lambda: row_name_owner.event_row_name, False, row_name_owner),
    "a4": (_a4, "merge_rows_by_identity", lambda: merge_owner.merge_rows_by_identity, True, merge_owner),
    "a5": (_a5, "filter_canonical_events", lambda: filter_owner.filter_canonical_events, True, filter_owner),
    "a6": (_a6, "resolve_strategist_source_run_ids", lambda: source_ids_owner.resolve_strategist_source_run_ids, True, source_ids_owner),
    "a7": (_a7, "expand_targeted_run_ids_with_cached_strategist_sources", lambda: expand_owner.expand_targeted_run_ids_with_cached_strategist_sources, True, expand_owner),
    "a8": (_a8, "latest_event_payload", lambda: latest_owner.latest_event_payload, False, latest_owner),
}


def _run(key, which):
    scenario, name, owner_factory, facade, _ = CASES[key]
    if which == "wrapper":
        fn = getattr(ev, name)
    else:
        raw = owner_factory()
        fn = (lambda *a, **k: raw(*a, facade=ev, **k)) if facade else raw
    out = scenario(fn, ev)
    return json.loads(json.dumps(_sets_to_lists(out), default=repr))


def _sets_to_lists(obj):
    if isinstance(obj, (set, frozenset)):
        return ["__set__", sorted(obj, key=repr)]
    if isinstance(obj, (list, tuple)):
        return [_sets_to_lists(x) for x in obj]
    if isinstance(obj, dict):
        return {k: _sets_to_lists(v) for k, v in obj.items()}
    return obj


class Test(unittest.TestCase):
    def _parity(self, key):
        a = _run(key, "wrapper")
        b = _run(key, "owner")
        self.assertEqual(a, b)
        self.assertEqual(_h(a), GOLDENS[key])
        name, owner_mod = CASES[key][1], CASES[key][4]
        fn = ast.parse(inspect.getsource(getattr(ev, name))).body[0]
        stmts = [n for n in fn.body if not (isinstance(n, ast.Expr) and isinstance(getattr(n, "value", None), ast.Constant))]
        self.assertTrue(len(stmts) == 1 and isinstance(stmts[0], ast.Return))
        self.assertNotIn("import live_execution_event_evidence", inspect.getsource(owner_mod))
        return a

    def test_a1_row_event_name(self):
        self._parity("a1")
        self.assertEqual(ev.row_event_name({"event_name": " scanner.hit "}), "scanner.hit")
        self.assertEqual(ev.row_event_name({"stage": "scanner", "event": "hit"}), "scanner.hit")
        self.assertEqual(ev.row_event_name({}), "")

    def test_a2_event_row_symbol(self):
        out = self._parity("a2")
        self.assertEqual(ev.event_row_symbol({"symbol": "005930"}), ev.normalize_symbol("005930", allow_test_symbols=True))
        self.assertEqual(ev.event_row_symbol({"payload": {"selected_symbol": "000660"}}), ev.normalize_symbol("000660", allow_test_symbols=True))
        self.assertEqual(out[-5], ["ok", "SYM:005930:True"])

    def test_a3_event_row_name(self):
        self._parity("a3")
        self.assertEqual(ev.event_row_name({"name": "fallback"}), "fallback")
        self.assertEqual(ev.event_row_name({"event_name": "x"}), "x")
        self.assertEqual(ev.event_row_name({}), "")

    def test_a4_merge_rows_by_identity(self):
        out = self._parity("a4")
        self.assertEqual(out[0], ["identity", [2, True, True]])
        self.assertEqual(out[2], ["ok", []])

    def test_a5_filter_canonical_events(self):
        out = self._parity("a5")
        rows = out[0][1]
        self.assertTrue(all(r["agent"].lower() == "strategist" for r in rows))
        self.assertEqual(out[-3], ["copy", [True, True]])

    def test_a6_resolve_strategist_source_run_ids(self):
        out = self._parity("a6")
        self.assertEqual(out[0], ["ok", [["r1"], {}]])
        self.assertEqual(out[1], ["ok", [["r0"], {"r1": "r0"}]])
        self.assertEqual(out[5], ["ok", [[], {}]])

    def test_a7_expand_targeted_run_ids_with_cached_strategist_sources(self):
        out = self._parity("a7")
        self.assertEqual(out[0], ["ok", ["__set__", ["r0", "r1"]]])
        self.assertEqual(out[1], ["ok", ["__set__", ["r0", "r1"]]])
        self.assertEqual(out[3], ["ok", ["__set__", ["r1"]]])
        self.assertEqual(out[4], ["ok", ["__set__", []]])

    def test_a8_latest_event_payload(self):
        out = self._parity("a8")
        self.assertEqual(ev.latest_event_payload([{"payload": {"a": 1}}]), {"a": 1})
        self.assertEqual(ev.latest_event_payload([]), {})
        self.assertEqual(ev.latest_event_payload([{"payload": [1]}]), {})
        self.assertEqual(out[0], ["copy", [True, True]])


if __name__ == "__main__":
    unittest.main()
