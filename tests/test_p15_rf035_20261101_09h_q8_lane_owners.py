"""P15 RF-035 (20261101-09h): eight q8_lane_decision_table helpers moved to projection Owners; parity with the pre-move bodies (stdlib unittest)."""
from __future__ import annotations

import ast
import hashlib
import inspect
import json
import unittest
from types import MappingProxyType
from unittest import mock

from libs.reporting import q8_lane_counts_projection as counts_owner
from libs.reporting import q8_lane_decision_table as lane
from libs.reporting import q8_lane_float_projection as float_owner
from libs.reporting import q8_lane_forward_rows_projection as forward_owner
from libs.reporting import q8_lane_int_projection as int_owner
from libs.reporting import q8_lane_reason_summary_projection as reason_owner
from libs.reporting import q8_lane_rows_projection as rows_owner
from libs.reporting import q8_lane_text_projection as text_owner
from libs.reporting import q8_lane_verdict_projection as verdict_owner

GOLDENS = {
    "a1": "28b1c46823f646889dfb6df1d5c1899c6edd2d807b01daa2005c7e8152c5c405",
    "a2": "a113c657cf7ecd6d2c5b6c2566f0c2e8a2286bf32b9e05dd130121b07df7aabf",
    "a3": "2903e6c4729538674598bf2d9875d011154aeac7546a5b2353e72a1331291340",
    "a4": "11a97d76ed01df0ba47fd2366a3745fa7024b8dea89d52314b826629c9a2c42b",
    "a5": "59ddc720242250ae0869f7a03a393c5a6afdb63580b910b028be685f0283eee1",
    "a6": "c57c06bf02553862215863956e9216c1bda3a0f7e349c9d59fdb6291738c5a4d",
    "a7": "1c3b4858c5adbe4dffb15431498fae8cedbae41e2ed6ee97d187e8263e62c3b2",
    "a8": "cab5098b86585ae708aebb9f37409268c2f0532e0bcf9e03113f9f05f757fbfb",
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
        raise ValueError("odd-str")

    def __float__(self):
        raise ValueError("odd-float")


def _a1(fn, mod):
    values = [" A ", None, "", 0, 5, False, True, [], [1], {}, " \n ", 1.5, _Odd()]
    return [_call(lambda v=v: fn(v)) for v in values] + [_call(lambda: fn())]


def _a2(fn, mod):
    values = ["1.5", None, "", "bad", 0, 1, True, [], "1e3", " 2.5 ", float("inf"), float("nan"), _Odd(), "-0.5"]
    out = [_call(lambda v=v: fn(v)) for v in values]
    out += [
        _call(lambda: fn("bad", 3)),
        _call(lambda: fn(None, 2)),
        _call(lambda: fn("", default="x")),
        _call(lambda: fn("bad", default=None)),
        _call(lambda: fn("bad", default=_Odd())),
        _call(lambda: fn()),
    ]
    return out


def _a3(fn, mod):
    values = ["2.9", None, "", "bad", 0, 1.9, -1.9, True, [], "1e3", " 7 ", float("inf"), float("nan"), _Odd()]
    out = [_call(lambda v=v: fn(v)) for v in values]
    out += [
        _call(lambda: fn("bad", 4)),
        _call(lambda: fn(None, 4)),
        _call(lambda: fn("bad", "x")),
        _call(lambda: fn("bad", 2.9)),
        _call(lambda: fn("", default=None)),
        _call(lambda: fn()),
    ]
    return out


def _a4(fn, mod):
    src = {"x": 1}
    res = fn([src, None])
    out = [
        ["copy", [res == [{"x": 1}], res[0] is not src]],
        _call(lambda: fn({"rows": []})),
        _call(lambda: fn(None)),
        _call(lambda: fn([])),
        _call(lambda: fn([MappingProxyType({"m": 1}), "junk", 5, [1]])),
        _call(lambda: fn(iter([{"a": 1}]))),
        _call(lambda: fn((i for i in [{"b": 2}]))),
        _call(lambda: fn("abc")),
        _call(lambda: fn(5)),
        _call(lambda: fn({"a": 1})),
        _call(lambda: fn()),
    ]
    with mock.patch.object(lane, "Mapping", tuple):
        out.append(_call(lambda: fn([{"x": 1}, (1, 2)])))
    return out


def _a5(fn, mod):
    out = [
        _call(lambda: fn({"entry_lane_forward_outcomes": {"by_primary_lane": [{"name": "x"}]}})),
        _call(lambda: fn({})),
        _call(lambda: fn({"entry_lane_forward_outcomes": [1]})),
        _call(lambda: fn({"entry_lane_forward_outcomes": {}})),
        _call(lambda: fn({"entry_lane_forward_outcomes": {"by_primary_lane": None}})),
        _call(lambda: fn({"entry_lane_forward_outcomes": MappingProxyType({"by_primary_lane": [{"name": "m"}, 5]})})),
        _call(lambda: fn(None)),
        _call(lambda: fn()),
    ]
    with mock.patch.object(lane, "_rows", lambda v: [{"patched": True}]):
        out.append(_call(lambda: fn({"entry_lane_forward_outcomes": {"by_primary_lane": []}})))
        out.append(_call(lambda: fn({})))
    with mock.patch.object(lane, "Mapping", tuple):
        out.append(_call(lambda: fn({"entry_lane_forward_outcomes": {"by_primary_lane": [{"name": "x"}]}})))
    return out


def _a6(fn, mod):
    out = [
        _call(lambda: fn([{"name": " A ", "count": "2.9"}, {"name": "B", "count": 3}])),
        _call(lambda: fn([{"name": "", "count": 5}, {"name": None}, {"count": 1}])),
        _call(lambda: fn([])),
        _call(lambda: fn(iter([{"name": "I", "count": 1}]))),
        _call(lambda: fn([{"name": "A", "count": 1}, {"name": "A", "count": 4}])),
        _call(lambda: fn([{"name": "A", "count": "bad"}])),
        _call(lambda: fn([None])),
        _call(lambda: fn(None)),
        _call(lambda: fn()),
    ]
    with mock.patch.object(lane, "_int", lambda v, default=0: 99):
        out.append(_call(lambda: fn([{"name": "A", "count": 1}])))
    with mock.patch.object(lane, "_text", lambda v: "T" if v else ""):
        out.append(_call(lambda: fn([{"name": "zz", "count": 2}, {"name": "", "count": 3}])))
    return out


def _a7(fn, mod):
    ev = {"by_reason": [{"name": "A", "count": 2}, {"name": "B"}, {"name": "", "count": 9}, {"name": "C", "count": 0}, "junk"] + [{"name": f"R{i}", "count": i} for i in range(8)]}
    out = [
        _call(lambda: fn({"by_reason": [{"name": "A", "count": 2}]})),
        _call(lambda: fn({})),
        _call(lambda: fn(ev)),
        _call(lambda: fn(ev, limit=0)),
        _call(lambda: fn(ev, limit=2)),
        _call(lambda: fn(ev, limit=-1)),
        _call(lambda: fn({"by_reason": [{"name": "A", "count": None}]})),
        _call(lambda: fn({"by_reason": None})),
        _call(lambda: fn(None)),
        _call(lambda: fn()),
    ]
    with mock.patch.object(lane, "_rows", lambda v: [{"name": "P", "count": 7}] * 8):
        out.append(_call(lambda: fn({})))
        out.append(_call(lambda: fn({}, limit=1)))
    with mock.patch.object(lane, "_text", lambda v: "T" if v else ""):
        out.append(_call(lambda: fn({"by_reason": [{"name": "A", "count": 2}]})))
    return out


def _a8(fn, mod):
    def run(promotion_allowed=True, **row):
        return _call(lambda: fn(row, promotion_allowed=promotion_allowed))

    out = [
        run(promotion_allowed=False),
        run(observed_count=5, coverage=1),
        run(observed_count=12, coverage=0.1),
        run(observed_count=12, coverage=1, name="vwap_reclaim", avg_return_5m_pct=-1, avg_return_15m_pct=-1),
        run(observed_count=12, coverage=1, avg_return_5m_pct=0.6),
        run(observed_count=12, coverage=1, avg_return_15m_pct=0.8),
        run(observed_count=12, coverage=1, avg_mfe_5m_pct=1.5),
        run(observed_count=12, coverage=1, avg_return_5m_pct=0.6, avg_mae_5m_pct=-1.6),
        run(observed_count=12, coverage=1, avg_return_5m_pct=-0.1, avg_return_15m_pct=-0.1),
        run(observed_count=12, coverage=1, avg_return_5m_pct=0.1, avg_return_15m_pct=0.1),
        run(observed_count=12, coverage=1, name="vwap_reclaim", avg_return_5m_pct=-1, avg_return_15m_pct=1),
        run(observed_count="12", coverage="1", avg_return_5m_pct="0.7"),
        run(observed_count="bad", coverage="bad"),
        run(),
        _call(lambda: fn(None, promotion_allowed=True)),
        _call(lambda: fn({})),
        _call(lambda: fn()),
    ]
    with mock.patch.object(lane, "TRUSTED_FORWARD_MIN_COVERAGE", 0.99):
        out.append(run(observed_count=12, coverage=0.9, avg_return_5m_pct=0.6))
    with mock.patch.object(lane, "TRUSTED_FORWARD_MIN_COVERAGE", 0.0):
        out.append(run(observed_count=12, coverage=0.0, avg_return_5m_pct=0.6))
    with mock.patch.object(lane, "_int", lambda v, default=0: 50):
        out.append(run(observed_count=1, coverage=1, avg_return_5m_pct=0.6))
    with mock.patch.object(lane, "_float", lambda v, default=0.0: 2.0):
        out.append(run(observed_count=12))
    with mock.patch.object(lane, "_text", lambda v: "vwap_reclaim"):
        out.append(run(observed_count=12, coverage=1, avg_return_5m_pct=-1, avg_return_15m_pct=-1))
    return out


CASES = {
    "a1": (_a1, "_text", lambda: text_owner._text, False, text_owner),
    "a2": (_a2, "_float", lambda: float_owner._float, False, float_owner),
    "a3": (_a3, "_int", lambda: int_owner._int, False, int_owner),
    "a4": (_a4, "_rows", lambda: rows_owner._rows, True, rows_owner),
    "a5": (_a5, "_forward_rows", lambda: forward_owner._forward_rows, True, forward_owner),
    "a6": (_a6, "_counts_by_name", lambda: counts_owner._counts_by_name, True, counts_owner),
    "a7": (_a7, "_reason_summary", lambda: reason_owner._reason_summary, True, reason_owner),
    "a8": (_a8, "_verdict", lambda: verdict_owner._verdict, True, verdict_owner),
}


def _run(key, which):
    scenario, name, owner_factory, facade, _ = CASES[key]
    if which == "wrapper":
        fn = getattr(lane, name)
    else:
        raw = owner_factory()
        fn = (lambda *a, **k: raw(*a, facade=lane, **k)) if facade else raw
    return json.loads(json.dumps(scenario(fn, lane), default=repr))


class Test(unittest.TestCase):
    def _parity(self, key):
        a = _run(key, "wrapper")
        b = _run(key, "owner")
        self.assertEqual(a, b)
        self.assertEqual(_h(a), GOLDENS[key])
        name, owner_mod = CASES[key][1], CASES[key][4]
        fn = ast.parse(inspect.getsource(getattr(lane, name))).body[0]
        stmts = [n for n in fn.body if not (isinstance(n, ast.Expr) and isinstance(getattr(n, "value", None), ast.Constant))]
        self.assertTrue(len(stmts) == 1 and isinstance(stmts[0], ast.Return))
        self.assertNotIn("import q8_lane_decision_table", inspect.getsource(owner_mod))
        return a

    def test_a1_text(self):
        out = self._parity("a1")
        self.assertEqual(lane._text(" A "), "A")
        self.assertEqual(lane._text(None), "")
        self.assertEqual(out[-2][0], "exc")

    def test_a2_float(self):
        self._parity("a2")
        self.assertEqual(lane._float("1.5"), 1.5)
        self.assertEqual(lane._float("bad", 3), 3.0)
        self.assertEqual(lane._float(None, 2), 2.0)

    def test_a3_int(self):
        self._parity("a3")
        self.assertEqual(lane._int("2.9"), 2)
        self.assertEqual(lane._int("bad", 4), 4)
        self.assertEqual(lane._int(None, 4), 4)

    def test_a4_rows(self):
        out = self._parity("a4")
        self.assertEqual(lane._rows([{"x": 1}, None]), [{"x": 1}])
        self.assertEqual(lane._rows({"rows": []}), [])
        self.assertEqual(out[0], ["copy", [True, True]])

    def test_a5_forward_rows(self):
        out = self._parity("a5")
        self.assertEqual(lane._forward_rows({"entry_lane_forward_outcomes": {"by_primary_lane": [{"name": "x"}]}}), [{"name": "x"}])
        self.assertEqual(lane._forward_rows({}), [])
        self.assertEqual(out[1], ["ok", []])

    def test_a6_counts_by_name(self):
        out = self._parity("a6")
        self.assertEqual(lane._counts_by_name([{"name": " A ", "count": "2.9"}, {"name": "B", "count": 3}]), {"A": 2, "B": 3})
        self.assertEqual(out[1], ["ok", {}])

    def test_a7_reason_summary(self):
        out = self._parity("a7")
        self.assertEqual(lane._reason_summary({"by_reason": [{"name": "A", "count": 2}]}), "A 2")
        self.assertEqual(lane._reason_summary({}), "-")
        self.assertEqual(out[3], ["ok", "-"])

    def test_a8_verdict(self):
        out = self._parity("a8")
        self.assertEqual(lane._verdict({}, promotion_allowed=False)["verdict"], "TRUST_GATE_BLOCKED")
        self.assertEqual(lane._verdict({"observed_count": 5}, promotion_allowed=True)["verdict"], "DATA_INCOMPLETE")
        self.assertEqual(lane._verdict({"observed_count": 12, "coverage": 1, "name": "vwap_reclaim", "avg_return_5m_pct": -1, "avg_return_15m_pct": -1}, promotion_allowed=True)["verdict"], "GOOD_BLOCK")
        self.assertEqual(lane._verdict({"observed_count": 12, "coverage": 1, "avg_return_5m_pct": 0.6}, promotion_allowed=True)["verdict"], "MISSED_OPPORTUNITY")
        self.assertEqual(out[17][1]["verdict"], "DATA_INCOMPLETE")  # raised coverage floor at SOURCE changes the result


if __name__ == "__main__":
    unittest.main()
