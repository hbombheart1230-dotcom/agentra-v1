"""P15 RF-035 (20261101-08h): eight quant_shadow_forward_outcomes helpers moved to projection Owners; parity with the pre-move bodies (stdlib unittest)."""
from __future__ import annotations

import ast
import hashlib
import inspect
import json
import unittest
from datetime import datetime as _real_datetime
from types import MappingProxyType
from unittest import mock

from libs.reporting import quant_forward_epoch_projection as epoch_owner
from libs.reporting import quant_forward_float_projection as float_owner
from libs.reporting import quant_forward_int_projection as int_owner
from libs.reporting import quant_forward_kst_day_projection as kst_day_owner
from libs.reporting import quant_forward_kst_time_projection as kst_time_owner
from libs.reporting import quant_forward_raw_epoch_projection as raw_epoch_owner
from libs.reporting import quant_forward_row_day_projection as row_day_owner
from libs.reporting import quant_forward_text_projection as text_owner
from libs.reporting import quant_shadow_forward_outcomes as qf

GOLDENS = {
    "a1": "2a0d5d7e3cc9e76233d317b5ef3df76e6be6a9f4f368473ab71a2aeb8dfffebf",
    "a2": "3b7764500313d995d65535bf8c84b4ddc6f63bcd08f82fe83590f61e2bb0b96e",
    "a3": "41b12d9b8f91340b9e6bbc2f349ae2cc912ad55501fbf59caf6ef7b729b2c64b",
    "a4": "525d4ef4a693c122147315140b1941ae52fda5992b620c0c9385fbd1142e7530",
    "a5": "be9ec7fbbf86358927d27da70a965b9481ddc8b09f73c2f72103c83488545021",
    "a6": "2f16b6580ca08470fa0befa39df662b6eb0356a2a5df33c5f9cad887c48a8a3c",
    "a7": "601edda098d80b9c4c4d269a42d55f4eb4d7b2246711a5d9e74f47420d652418",
    "a8": "5fa375d7fc19f2571766ce84d1e5d81e2dc34049974cd3a601e4ecf15bd40592",
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


class _FakeDatetime:
    """Deterministic datetime stand-in used to prove the facade seam is honored at call time."""

    @staticmethod
    def fromisoformat(text):
        return _real_datetime.fromtimestamp(777)

    @staticmethod
    def strptime(text, fmt):
        return _real_datetime(2000, 1, 1, 0, 0, 0)

    @staticmethod
    def fromtimestamp(epoch, tz=None):
        return _real_datetime(2000, 1, 2, 3, 4, 5, tzinfo=tz)


def _a1(fn, mod):
    values = ["1.25", None, "", "bad", 0, 1, True, False, [], "1e3", " 2 ", float("inf"), float("nan"), _Odd(), "-0.5"]
    out = [_call(lambda v=v: fn(v)) for v in values]
    out += [
        _call(lambda: fn(None, 2.0)),
        _call(lambda: fn("bad", 2.0)),
        _call(lambda: fn("", default="d")),
        _call(lambda: fn("x", default=None)),
        _call(lambda: fn()),
    ]
    return out


def _a2(fn, mod):
    values = ["2.9", None, "", "bad", 0, 1.9, -1.9, True, [], "1e3", " 7 ", float("inf"), float("nan"), _Odd()]
    out = [_call(lambda v=v: fn(v)) for v in values]
    out += [
        _call(lambda: fn(None, 7)),
        _call(lambda: fn("bad", 7)),
        _call(lambda: fn("bad", "x")),
        _call(lambda: fn("bad", 2.9)),
        _call(lambda: fn("", default=None)),
        _call(lambda: fn()),
    ]
    return out


def _a3(fn, mod):
    values = ["  ABC  ", None, "", 0, 5, False, True, [], [1], {}, " \n ", _Odd(), 1.5]
    return [_call(lambda v=v: fn(v)) for v in values] + [_call(lambda: fn())]


def _a4(fn, mod):
    values = ["1970-01-01T00:00:01Z", "1", None, "", "bad", 5, 5.9, -3, True, "  ", " 12.7 ", "2026-11-01T00:00:00+09:00", "2026-11-01", "1e3", [], _Odd(), "nan", "inf"]
    out = [_call(lambda v=v: fn(v)) for v in values]
    out.append(_call(lambda: fn()))
    with mock.patch.object(qf, "datetime", _FakeDatetime):
        out.append(_call(lambda: fn("2026-11-01T00:00:00Z")))
        out.append(_call(lambda: fn("1")))
    return out


def _a5(fn, mod):
    values = ["19700101090001", "1970-01-01T00:00:01Z", "bad", "", None, "20261101120000", "2026110112", "20261101120000999", "99999999999999", "00000000000000", 12345678901234, "1", " 20261101120000 ", [], _Odd()]
    out = [_call(lambda v=v: fn(v)) for v in values]
    out.append(_call(lambda: fn()))
    with mock.patch.object(qf, "_parse_epoch", lambda v: 42):
        out.append(_call(lambda: fn("not-raw")))
        out.append(_call(lambda: fn("20261101120000")))
    with mock.patch.object(qf, "_text", lambda v: "20000101000000"):
        out.append(_call(lambda: fn("anything")))
    with mock.patch.object(qf, "datetime", _FakeDatetime):
        out.append(_call(lambda: fn("20261101120000")))
    with mock.patch.object(qf, "KST", None):
        out.append(_call(lambda: fn("20261101120000")))
    return out


def _a6(fn, mod):
    values = [1, 0, "bad", -5, None, "", 86400, 1793430000, "1793430000", 1.9, True, 10**20, [], _Odd()]
    out = [_call(lambda v=v: fn(v)) for v in values]
    out.append(_call(lambda: fn()))
    with mock.patch.object(qf, "_to_int", lambda v, default=0: 3600):
        out.append(_call(lambda: fn("ignored")))
    with mock.patch.object(qf, "datetime", _FakeDatetime):
        out.append(_call(lambda: fn(5)))
    with mock.patch.object(qf, "KST", None):
        out.append(_call(lambda: fn(5)))
    return out


def _a7(fn, mod):
    rows = [{"raw_ts": "20261101120000"}, {"ts": 1}, {}, {"raw_ts": "2026"}, {"raw_ts": "abcdefgh", "ts": 86400}, {"raw_ts": None, "ts": "bad"}, {"raw_ts": " 20260101 "}, MappingProxyType({"ts": 3600}), {"raw_ts": 20261101}]
    out = [_call(lambda r=r: fn(r)) for r in rows] + [_call(lambda: fn(None)), _call(lambda: fn())]
    with mock.patch.object(qf, "_kst_day_from_epoch", lambda v: "PATCHED"):
        out.append(_call(lambda: fn({"ts": 1})))
        out.append(_call(lambda: fn({"raw_ts": "20261101"})))
    with mock.patch.object(qf, "_text", lambda v: "99999999zz"):
        out.append(_call(lambda: fn({"raw_ts": "x"})))
    return out


def _a8(fn, mod):
    rows = [{"ts": 1}, {"ts": 0}, {}, {"raw_ts": "20261101153000"}, {"raw_ts": "bad", "ts": 3600}, {"raw_ts": "20261101153000", "ts": 5}, {"ts": -5}, {"ts": "bad"}, {"raw_ts": "1970-01-01T00:00:01Z"}, MappingProxyType({"ts": 86399}), {"ts": 10**15}]
    out = [_call(lambda r=r: fn(r)) for r in rows] + [_call(lambda: fn(None)), _call(lambda: fn())]
    with mock.patch.object(qf, "_parse_raw_ts_epoch", lambda v: 7200):
        out.append(_call(lambda: fn({"ts": 1})))
    with mock.patch.object(qf, "_parse_raw_ts_epoch", lambda v: 0), mock.patch.object(qf, "_to_int", lambda v, default=0: 10800):
        out.append(_call(lambda: fn({"ts": 1})))
    with mock.patch.object(qf, "datetime", _FakeDatetime):
        out.append(_call(lambda: fn({"ts": 1})))
    return out


CASES = {
    "a1": (_a1, "_to_float", lambda: float_owner._to_float, False, float_owner),
    "a2": (_a2, "_to_int", lambda: int_owner._to_int, False, int_owner),
    "a3": (_a3, "_text", lambda: text_owner._text, False, text_owner),
    "a4": (_a4, "_parse_epoch", lambda: epoch_owner._parse_epoch, True, epoch_owner),
    "a5": (_a5, "_parse_raw_ts_epoch", lambda: raw_epoch_owner._parse_raw_ts_epoch, True, raw_epoch_owner),
    "a6": (_a6, "_kst_day_from_epoch", lambda: kst_day_owner._kst_day_from_epoch, True, kst_day_owner),
    "a7": (_a7, "_row_day", lambda: row_day_owner._row_day, True, row_day_owner),
    "a8": (_a8, "_kst_time_tuple", lambda: kst_time_owner._kst_time_tuple, True, kst_time_owner),
}


def _run(key, which):
    scenario, name, owner_factory, facade, _ = CASES[key]
    if which == "wrapper":
        fn = getattr(qf, name)
    else:
        raw = owner_factory()
        fn = (lambda *a, **k: raw(*a, facade=qf, **k)) if facade else raw
    return json.loads(json.dumps(scenario(fn, qf), default=repr))


class Test(unittest.TestCase):
    def _parity(self, key):
        a = _run(key, "wrapper")
        b = _run(key, "owner")
        self.assertEqual(a, b)
        self.assertEqual(_h(a), GOLDENS[key])
        name, owner_mod = CASES[key][1], CASES[key][4]
        fn = ast.parse(inspect.getsource(getattr(qf, name))).body[0]
        stmts = [n for n in fn.body if not (isinstance(n, ast.Expr) and isinstance(getattr(n, "value", None), ast.Constant))]
        self.assertTrue(len(stmts) == 1 and isinstance(stmts[0], ast.Return))
        self.assertNotIn("import quant_shadow_forward_outcomes", inspect.getsource(owner_mod))
        return a

    def test_a1_to_float(self):
        self._parity("a1")
        self.assertEqual(qf._to_float("1.25"), 1.25)
        self.assertEqual(qf._to_float(None, 2.0), 2.0)
        self.assertEqual(qf._to_float("bad", 2.0), 2.0)

    def test_a2_to_int(self):
        self._parity("a2")
        self.assertEqual(qf._to_int("2.9"), 2)
        self.assertEqual(qf._to_int(None, 7), 7)
        self.assertEqual(qf._to_int("bad", 7), 7)

    def test_a3_text(self):
        out = self._parity("a3")
        self.assertEqual(qf._text("  ABC  "), "ABC")
        self.assertEqual(qf._text(None), "")
        self.assertEqual(out[11][0], "exc")

    def test_a4_parse_epoch(self):
        out = self._parity("a4")
        self.assertEqual(qf._parse_epoch("1970-01-01T00:00:01Z"), 1)
        self.assertEqual(qf._parse_epoch("1"), 1)
        self.assertEqual(qf._parse_epoch("bad"), 0)
        self.assertEqual(out[-2], ["ok", int(_real_datetime.fromtimestamp(777).timestamp())])

    def test_a5_parse_raw_ts_epoch(self):
        out = self._parity("a5")
        self.assertEqual(qf._parse_raw_ts_epoch("19700101090001"), 1)
        self.assertEqual(qf._parse_raw_ts_epoch("1970-01-01T00:00:01Z"), 1)
        self.assertEqual(qf._parse_raw_ts_epoch("bad"), 0)
        self.assertEqual(out[-6 + 1][1], 42)

    def test_a6_kst_day_from_epoch(self):
        self._parity("a6")
        self.assertEqual(qf._kst_day_from_epoch(1), "19700101")
        self.assertEqual(qf._kst_day_from_epoch(0), "")
        self.assertEqual(qf._kst_day_from_epoch("bad"), "")

    def test_a7_row_day(self):
        self._parity("a7")
        self.assertEqual(qf._row_day({"raw_ts": "20261101120000"}), "20261101")
        self.assertEqual(qf._row_day({"ts": 1}), "19700101")

    def test_a8_kst_time_tuple(self):
        self._parity("a8")
        self.assertEqual(qf._kst_time_tuple({"ts": 1}), (9, 0))
        self.assertEqual(qf._kst_time_tuple({"ts": 0}), (0, 0))


if __name__ == "__main__":
    unittest.main()
