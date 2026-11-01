"""P15 RF-035 (20261101-10h): eight q8_lane_decision_table / q8_trusted_reaggregation / quant_shadow_forward_outcomes bodies moved to projection Owners; parity with the pre-move bodies (stdlib unittest)."""
from __future__ import annotations

import ast
import hashlib
import inspect
import json
import types
import unittest
from types import MappingProxyType
from unittest import mock

from libs.reporting import q8_lane_decision_table as lane
from libs.reporting import q8_lane_pct_projection as lane_pct_owner
from libs.reporting import q8_lane_render_projection as lane_render_owner
from libs.reporting import q8_trusted_day_projection as day_owner
from libs.reporting import q8_trusted_num_projection as num_owner
from libs.reporting import q8_trusted_pct_projection as pct_owner
from libs.reporting import q8_trusted_reaggregation as tr
from libs.reporting import q8_trusted_render_projection as render_owner
from libs.reporting import q8_trusted_watchlist_projection as watch_owner
from libs.reporting import quant_forward_normalize_projection as normalize_owner
from libs.reporting import quant_shadow_forward_outcomes as qf

GOLDENS = {
    "a1": "1718636b20d5458366bdf25ae8211c1487111eea1fde191982fe4f731a57c49f",
    "a2": "683e1c2e6595364a7dd0761226ae76e7105c2fa7e9645b17faa0fafc047cdf42",
    "a3": "6647ba219ab9adccea9968ca9d829a2398ff310264da2b8655b2e78165bbb41c",
    "a4": "9d1c5f3add9976ce951bf98af7d51c19bdefd41e243894b957ebd488a31aae8c",
    "a5": "35231a3216865cdd53ffa45b2432518d2e3bafb2b163a6f5c2001e3fcc01e6a6",
    "a6": "2f7e6cfb9c50e9c6910f888ef7c443b4704a333090dddc6b38ba8419fe36f6df",
    "a7": "5f5736b60d808a10d1591bf9867e9da4894f88099f6ce4a5915c80803b486b0f",
    "a8": "ec2640ad53e79d020ffa7096a59ca6f7af964944bb92047f86b154583aa5ccd0",
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

    def __int__(self):
        raise ValueError("odd-int")


def _a1(fn, mod):
    values = [None, "", 0.125, "1.5", "bad", 0, 1, True, [], -2.5, float("inf"), float("nan"), _Odd(), " 3 "]
    out = [_call(lambda v=v: fn(v)) for v in values] + [_call(lambda: fn())]
    with mock.patch.object(lane, "_float", lambda v, default=0.0: 7.0):
        out.append(_call(lambda: fn("x")))
        out.append(_call(lambda: fn(None)))
    return out


def _lane_payload():
    return {
        "day": "2026-11-01", "payload_count": 2, "candidate_count": 30, "deduped_candidate_count": 20, "duplicate_candidate_count": 10, "dedupe_key": ["a", "b"],
        "evaluated_count": 25, "forward_outcome_available_count": 18, "forward_outcome_coverage": 0.6, "evaluation_trust_gate": {"status": "blocked", "promotion_allowed": False, "block_reasons": ["low_coverage"]},
        "would_enter_count": 3, "reason_summary": "A 2",
        "rows": [
            {"lane": "trend", "verdict": "GOOD_BLOCK", "decision": "keep blocked", "candidate_count": 5, "observed_count": 4, "avg_return_5m_pct": -0.5, "avg_return_15m_pct": "bad", "avg_mfe_5m_pct": 0.2, "avg_mae_5m_pct": None, "rationale": "r"},
            "junk",
            {"lane": None},
        ],
    }


def _a2(fn, mod):
    p = _lane_payload()
    out = [
        _call(lambda: fn(p)),
        _call(lambda: fn({"day": "d"})),
        _call(lambda: fn({})),
        _call(lambda: fn(dict(p, evaluation_trust_gate=[1], rows=None, dedupe_key=None))),
        _call(lambda: fn(dict(p, evaluation_trust_gate={"promotion_allowed": 1, "reasons": ["x", "y"]}))),
        _call(lambda: fn(dict(p, forward_outcome_coverage="bad"))),
        _call(lambda: fn(MappingProxyType(p))),
        _call(lambda: fn(None)),
        _call(lambda: fn()),
    ]
    with mock.patch.object(lane, "_rows", lambda v: [{"lane": "PATCHED"}]):
        out.append(_call(lambda: fn(p)))
    with mock.patch.object(lane, "_fmt_pct", lambda v: "PCT"), mock.patch.object(lane, "_text", lambda v: "T" if v else ""):
        out.append(_call(lambda: fn(p)))
    with mock.patch.object(lane, "Mapping", tuple):
        out.append(_call(lambda: fn(p)))
    return out


def _a3(fn, mod):
    gen = fn("bad", "bad")
    out = [
        ["lazy", [isinstance(gen, types.GeneratorType)]],
        _call(lambda: list(fn("2026-11-01", "2026-11-02"))),
        _call(lambda: list(fn("2026-11-02", "2026-11-01"))),
        _call(lambda: list(fn("2026-02-27T10:00:00", "2026-03-02"))),
        _call(lambda: list(fn("bad", "2026-11-01"))),
        _call(lambda: list(fn("2026-11-01", "x"))),
        _call(lambda: list(fn(20261101, "2026-11-02"))),
        _call(lambda: list(fn("2026-11-01"))),
    ]
    it = fn("2026-11-01", "2026-11-04")
    out.append(["partial", [next(it), next(it)]])
    with mock.patch.object(tr, "timedelta", lambda days: __import__("datetime").timedelta(days=2 * days)):
        out.append(_call(lambda: list(fn("2026-11-01", "2026-11-05"))))
    return out


def _a4(fn, mod):
    values = [0.125, "invalid", None, "", 0, 1, 1.5, "0.5", True, [], float("inf"), float("nan"), -0.01, _Odd(), "1e-3"]
    return [_call(lambda v=v: fn(v)) for v in values] + [_call(lambda: fn())]


def _a5(fn, mod):
    values = [1234, "invalid", None, "", 0, 1.9, "12", "1,234", True, [], 10**12, -5, float("inf"), float("nan"), _Odd(), " 7 "]
    return [_call(lambda v=v: fn(v)) for v in values] + [_call(lambda: fn())]


def _a6(fn, mod):
    src = {"x": 1}
    res = fn({"promotion_watchlist": [src, None, "junk", MappingProxyType({"m": 1})]})
    out = [
        ["copy", [res == [{"x": 1}, {"m": 1}], res[0] is not src]],
        _call(lambda: fn({})),
        _call(lambda: fn({"promotion_watchlist": None})),
        _call(lambda: fn({"promotion_watchlist": [1, 2]})),
        _call(lambda: fn({"promotion_watchlist": iter([{"a": 1}])})),
        _call(lambda: fn({"promotion_watchlist": {"a": 1}})),
        _call(lambda: fn(None)),
        _call(lambda: fn()),
    ]
    with mock.patch.object(tr, "Mapping", tuple):
        out.append(_call(lambda: fn({"promotion_watchlist": [{"x": 1}, (1, 2)]})))
    return out


def _tr_payload():
    watch = {"name": "w", "observed_count": 55, "candidate_count": 70, "observed_day_count": 3, "avg_return_5m_pct": 0.5, "avg_return_15m_pct": "0.7", "avg_mae_5m_pct": None, "review_state": "promotion_watch"}
    return {
        "range": {"start": "2026-11-01", "end": "2026-11-02"},
        "aggregate": {"candidate_count": 1234, "deduped_candidate_count": 900, "duplicate_candidate_count": 334, "duplicate_rate": 0.27, "forward_outcome_available_count": 800, "trusted_forward_coverage": 0.88,
                      "promotion_allowed_day_count": 1, "cumulative_trust_gate_status": "promotion_review_ready", "cumulative_promotion_allowed": True, "cumulative_trust_reasons": ["a", "b"], "promotion_watchlist": [watch, "junk"]},
        "daily": [{"day": "2026-11-01", "candidate_count": 600, "deduped_candidate_count": 450, "duplicate_rate": 0.25, "trusted_forward_count": 400, "trusted_forward_coverage": 0.9, "trust_gate_status": "ok", "promotion_allowed": 1, "trust_reasons": ["r"], "promotion_watchlist": [watch, None]},
                  {"day": None}],
    }


def _a7(fn, mod):
    p = _tr_payload()
    out = [
        _call(lambda: fn({"range": {}, "aggregate": {}, "daily": []})),
        _call(lambda: fn(p)),
        _call(lambda: fn({})),
        _call(lambda: fn({"range": [1], "aggregate": [2], "daily": None})),
        _call(lambda: fn(dict(p, daily=[{"day": "d", "duplicate_rate": "bad"}]))),
        _call(lambda: fn(MappingProxyType(p))),
        _call(lambda: fn(None)),
        _call(lambda: fn()),
    ]
    with mock.patch.object(tr, "_fmt_num", lambda v: "N"), mock.patch.object(tr, "_fmt_pct", lambda v: "P"):
        out.append(_call(lambda: fn(p)))
    with mock.patch.object(tr, "TRUSTED_FORWARD_MIN_COUNT", 5), mock.patch.object(tr, "TRUSTED_FORWARD_MIN_COVERAGE", 0.5), mock.patch.object(tr, "DUPLICATE_RATE_MAX", 0.1):
        out.append(_call(lambda: fn({"range": {}, "aggregate": {}, "daily": []})))
    with mock.patch.object(tr, "PROMOTION_CANDIDATE_MIN_OBSERVED", 7), mock.patch.object(tr, "PROMOTION_CANDIDATE_MIN_DAYS", 9):
        out.append(_call(lambda: fn({"range": {}, "aggregate": {}, "daily": []})))
    with mock.patch.object(tr, "Mapping", tuple):
        out.append(_call(lambda: fn(p)))
    return out


def _a8(fn, mod):
    rows = [{"ts": 2, "close": 3, "high": 4, "low": 2}, {"ts": 1, "price": 2}, {"ts": 0, "close": 4}, {"ts": 5, "close": -1}, {"ts": "3", "close": "5", "raw_ts": "20261101120000"}, "junk", None,
            {"ts": 4, "close": 1, "high": 0, "low": 0, "datetime": "dt"}, {"ts": 6, "close": "bad"}, {"ts": 7, "close": 2, "time": "t7"}]
    out = [
        _call(lambda: fn(rows)),
        _call(lambda: fn({"rows": rows})),
        _call(lambda: fn({"rows": "notlist"})),
        _call(lambda: fn({})),
        _call(lambda: fn(None)),
        _call(lambda: fn([])),
        _call(lambda: fn(MappingProxyType({"rows": rows[:2]}))),
        _call(lambda: fn(iter(rows))),
        _call(lambda: fn("abc")),
        _call(lambda: fn()),
    ]
    res = fn(rows)
    out.append(["copy", [res[0] is not rows[1], rows[0] == {"ts": 2, "close": 3, "high": 4, "low": 2}]])
    with mock.patch.object(qf, "_to_int", lambda v, default=0: 5):
        out.append(_call(lambda: fn([{"ts": 1, "close": 2}])))
    with mock.patch.object(qf, "_to_float", lambda v, default=None: 9.0):
        out.append(_call(lambda: fn([{"ts": 1, "close": 2}])))
    with mock.patch.object(qf, "_text", lambda v: "TXT"):
        out.append(_call(lambda: fn([{"ts": 1, "close": 2, "raw_ts": "x"}])))
    with mock.patch.object(qf, "Mapping", tuple):
        out.append(_call(lambda: fn({"rows": rows[:2]})))
    return out


CASES = {
    "a1": (_a1, lane, "_fmt_pct", lambda: lane_pct_owner._fmt_pct, True, lane_pct_owner),
    "a2": (_a2, lane, "render_q8_lane_decision_table_markdown", lambda: lane_render_owner.render_q8_lane_decision_table_markdown, True, lane_render_owner),
    "a3": (_a3, tr, "_iter_days", lambda: day_owner._iter_days, True, day_owner),
    "a4": (_a4, tr, "_fmt_pct", lambda: pct_owner._fmt_pct, False, pct_owner),
    "a5": (_a5, tr, "_fmt_num", lambda: num_owner._fmt_num, False, num_owner),
    "a6": (_a6, tr, "_watchlist_rows", lambda: watch_owner._watchlist_rows, True, watch_owner),
    "a7": (_a7, tr, "render_q8_trusted_reaggregation_markdown", lambda: render_owner.render_q8_trusted_reaggregation_markdown, True, render_owner),
    "a8": (_a8, qf, "_normalize_rows", lambda: normalize_owner._normalize_rows, True, normalize_owner),
}


def _run(key, which):
    scenario, mod, name, owner_factory, facade, _ = CASES[key]
    if which == "wrapper":
        fn = getattr(mod, name)
    else:
        raw = owner_factory()
        fn = (lambda *a, **k: raw(*a, facade=mod, **k)) if facade else raw
    return json.loads(json.dumps(scenario(fn, mod), default=repr))


class Test(unittest.TestCase):
    def _parity(self, key):
        a = _run(key, "wrapper")
        b = _run(key, "owner")
        self.assertEqual(a, b)
        self.assertEqual(_h(a), GOLDENS[key])
        _, mod, name, _, _, owner_mod = CASES[key]
        fn = ast.parse(inspect.getsource(getattr(mod, name))).body[0]
        stmts = [n for n in fn.body if not (isinstance(n, ast.Expr) and isinstance(getattr(n, "value", None), ast.Constant))]
        self.assertEqual(len(stmts), 1)
        if key == "a3":
            self.assertTrue(isinstance(stmts[0], ast.Expr) and isinstance(stmts[0].value, ast.YieldFrom))
        else:
            self.assertIsInstance(stmts[0], ast.Return)
        self.assertNotIn("import " + mod.__name__.split(".")[-1], inspect.getsource(owner_mod))
        return a

    def test_a1_lane_fmt_pct(self):
        out = self._parity("a1")
        self.assertEqual(lane._fmt_pct(None), "-")
        self.assertEqual(lane._fmt_pct(0.125), "0.1250%")
        self.assertEqual(out[-1], ["ok", "-"])

    def test_a2_render_q8_lane_decision_table_markdown(self):
        out = self._parity("a2")
        text = out[0][1]
        self.assertTrue(text.startswith("# Q8 Lane Decision Table - 2026-11-01"))
        self.assertIn("promotion_allowed: `False`", text)
        self.assertTrue(out[1][1].endswith("\n"))

    def test_a3_iter_days(self):
        out = self._parity("a3")
        self.assertEqual(out[0], ["lazy", [True]])
        self.assertEqual(list(tr._iter_days("2026-11-01", "2026-11-02")), ["2026-11-01", "2026-11-02"])
        with self.assertRaises(ValueError):
            list(tr._iter_days("bad", "2026-11-01"))

    def test_a4_trusted_fmt_pct(self):
        self._parity("a4")
        self.assertEqual(tr._fmt_pct(0.125), "12.50%")
        self.assertEqual(tr._fmt_pct("invalid"), "-")

    def test_a5_fmt_num(self):
        self._parity("a5")
        self.assertEqual(tr._fmt_num(1234), "1,234")
        self.assertEqual(tr._fmt_num("invalid"), "0")

    def test_a6_watchlist_rows(self):
        out = self._parity("a6")
        self.assertEqual(tr._watchlist_rows({"promotion_watchlist": [{"x": 1}, None]}), [{"x": 1}])
        self.assertEqual(tr._watchlist_rows({}), [])
        self.assertEqual(out[0], ["copy", [True, True]])

    def test_a7_render_q8_trusted_reaggregation_markdown(self):
        out = self._parity("a7")
        empty = out[0][1]
        self.assertIn("# Q8 Trusted Reaggregation", empty)
        self.assertIn("no_watchlist", empty)
        self.assertIn("| cumulative |", out[1][1])
        self.assertNotIn("no_watchlist", out[1][1])

    def test_a8_normalize_rows(self):
        out = self._parity("a8")
        got = qf._normalize_rows([{"ts": 2, "close": 3, "high": 4, "low": 2}, {"ts": 1, "price": 2}, {"ts": 0, "close": 4}])
        self.assertEqual([r["ts"] for r in got], [1, 2])
        self.assertEqual((got[0]["high"], got[0]["low"]), (2.0, 2.0))
        self.assertEqual(out[-5], ["copy", [True, True]])


if __name__ == "__main__":
    unittest.main()
