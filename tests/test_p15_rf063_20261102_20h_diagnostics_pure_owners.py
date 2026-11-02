from __future__ import annotations

import ast as python_ast
import inspect
import math
from datetime import datetime, timezone
from types import SimpleNamespace

from scripts.diagnostics import audit_target_tree_compat as audit
from scripts.diagnostics import check_monitor_gate_patterns as monitor
from scripts.diagnostics.audit_target_tree_compat_call_targets import _call_targets as call_targets_owner
from scripts.diagnostics.audit_target_tree_compat_has_statement import _has_statement as has_statement_owner
from scripts.diagnostics.audit_target_tree_compat_module_path import _module_path as module_path_owner
from scripts.diagnostics.check_monitor_gate_patterns_build_stale_groups import _build_stale_groups as stale_groups_owner
from scripts.diagnostics.check_monitor_gate_patterns_estimate_reclaim_price import _estimate_reclaim_price as reclaim_owner
from scripts.diagnostics.check_monitor_gate_patterns_followup_from_rows import _followup_from_rows as followup_owner
from scripts.diagnostics.check_monitor_gate_patterns_parse_iso_utc_seconds import _parse_iso_utc_seconds as parse_owner
from scripts.diagnostics.check_monitor_gate_patterns_to_float import _to_float as float_owner

ORIGINAL_SOURCE = {'_parse_iso_utc_seconds': 'def _parse_iso_utc_seconds(value: Any) -> Optional[int]:\n    text = str(value or "").strip()\n    if not text:\n        return None\n    try:\n        return int(datetime.fromisoformat(text).timestamp())\n    except Exception:\n        return None', '_to_float': 'def _to_float(value: Any) -> Optional[float]:\n    try:\n        out = float(value)\n    except Exception:\n        return None\n    if out != out:\n        return None\n    return out', '_estimate_reclaim_price': 'def _estimate_reclaim_price(current_price: Any, vwap_distance: Any, reclaim_tolerance_pct: Any) -> Optional[float]:\n    price = _to_float(current_price)\n    dist = _to_float(vwap_distance)\n    tol = _to_float(reclaim_tolerance_pct)\n    if price is None or dist is None or tol is None:\n        return None\n    denom = 1.0 + dist\n    if abs(denom) < 1e-9:\n        return None\n    est_vwap = price / denom\n    return est_vwap * (1.0 - tol)', '_build_stale_groups': 'def _build_stale_groups(rows: Iterable[Dict[str, Any]], *, stale_age_min: float = 3.0) -> List[Dict[str, Any]]:\n    groups: Dict[tuple[str, str, Any], List[Dict[str, Any]]] = {}\n    for row in rows:\n        if not row.get("minute_source_present"):\n            continue\n        latest_candle_ts = row.get("latest_candle_ts")\n        if latest_candle_ts in (None, ""):\n            continue\n        age = _to_float(row.get("artifact_age_minutes"))\n        if age is None or age < stale_age_min:\n            continue\n        key = (str(row.get("symbol") or ""), str(row.get("evaluation_summary") or ""), latest_candle_ts)\n        groups.setdefault(key, []).append(row)\n    out: List[Dict[str, Any]] = []\n    for (symbol, reason, latest_candle_ts), cases in groups.items():\n        cases = sorted(cases, key=lambda row: str(row.get("ts") or ""))\n        out.append(\n            {\n                "symbol": symbol,\n                "evaluation_summary": reason,\n                "latest_candle_ts": latest_candle_ts,\n                "repeat_count": len(cases),\n                "first_run_id": cases[0].get("run_id"),\n                "last_run_id": cases[-1].get("run_id"),\n                "max_artifact_age_minutes": max((_to_float(row.get("artifact_age_minutes")) or 0.0) for row in cases),\n                "runs": [str(row.get("run_id") or "") for row in cases],\n            }\n        )\n    out.sort(key=lambda row: (-int(row["repeat_count"]), row["symbol"], row["evaluation_summary"]))\n    return out', '_followup_from_rows': 'def _followup_from_rows(case: Dict[str, Any], rows: List[Dict[str, Any]]) -> Dict[str, Any]:\n    latest_candle_ts = int(case.get("latest_candle_ts") or 0)\n    blocked_price = _to_float(case.get("current_price"))\n    breakout_level = _to_float(case.get("breakout_level"))\n    reclaim_price = _to_float(case.get("reclaim_price"))\n    later = [row for row in rows if int(row.get("ts") or 0) > latest_candle_ts]\n    if not later or blocked_price in (None, 0.0):\n        return {"later_bars": 0}\n    max_high = max(_to_float(row.get("high")) or 0.0 for row in later)\n    min_low = min(_to_float(row.get("low")) or 0.0 for row in later)\n    last_close = _to_float(later[-1].get("close"))\n    return {\n        "later_bars": len(later),\n        "max_high_after": max_high,\n        "min_low_after": min_low,\n        "last_close_now": last_close,\n        "move_to_max_pct": ((max_high / blocked_price) - 1.0) * 100.0 if max_high > 0 else None,\n        "move_to_min_pct": ((min_low / blocked_price) - 1.0) * 100.0 if min_low > 0 else None,\n        "move_to_last_pct": ((last_close / blocked_price) - 1.0) * 100.0 if last_close else None,\n        "crossed_breakout_after": bool(breakout_level and max_high >= breakout_level),\n        "crossed_reclaim_after": bool(reclaim_price and max_high >= reclaim_price),\n    }', '_module_path': 'def _module_path(path: str) -> str:\n    if not path.startswith("scripts/") or not path.endswith(".py"):\n        raise ValueError(f"not a Python script path: {path}")\n    return path[:-3].replace("/", ".")', '_call_targets': 'def _call_targets(tree: ast.AST, owner: str, method: str) -> list[str]:\n    """Return literal module names passed to one documented wrapper API."""\n    out: list[str] = []\n    for node in ast.walk(tree):\n        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):\n            continue\n        if not isinstance(node.func.value, ast.Name):\n            continue\n        if node.func.value.id != owner or node.func.attr != method or not node.args:\n            continue\n        if isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str):\n            out.append(node.args[0].value)\n    return out', '_has_statement': 'def _has_statement(statements: list[ast.stmt], source: str) -> bool:\n    expected = ast.dump(ast.parse(source).body[0])\n    return any(ast.dump(statement) == expected for statement in statements)'}

def _original(name, **overrides):
    namespace = {
        "datetime": datetime,
        "ast": python_ast,
        "_to_float": monitor._to_float,
    }
    namespace.update(overrides)
    node = python_ast.parse(ORIGINAL_SOURCE[name]).body[0]
    module = python_ast.Module(body=[node], type_ignores=[])
    exec(compile(module, f"<original:{name}>", "exec"), namespace)
    return namespace[name]


def _parity(name, source_callable, owner_callable, args, kwargs=None):
    kwargs = kwargs or {}
    expected = _original(name)(*args, **kwargs)
    assert source_callable(*args, **kwargs) == expected
    assert owner_callable(*args, facade=monitor if name in {
        "_parse_iso_utc_seconds", "_estimate_reclaim_price",
        "_build_stale_groups", "_followup_from_rows"
    } else audit, **kwargs) == expected


def test_parse_iso_utc_seconds_matches_original_ast_and_facade_clock(monkeypatch):
    cases = ["2026-11-02T12:30:00+09:00", "", "not-a-date"]
    for value in cases:
        _parity("_parse_iso_utc_seconds", monitor._parse_iso_utc_seconds, parse_owner, (value,))
    class Clock:
        @staticmethod
        def fromisoformat(value):
            class Stamp:
                def timestamp(self):
                    return 12.75
            return Stamp()
    monkeypatch.setattr(monitor, "datetime", Clock)
    reference = _original("_parse_iso_utc_seconds", datetime=Clock)
    expected = reference("patched")
    assert monitor._parse_iso_utc_seconds("patched") == expected == 12
    assert parse_owner("patched", facade=monitor) == expected


def test_to_float_matches_original_ast_and_nan_contract():
    class BadFloat:
        def __float__(self):
            raise ValueError("bad float")
    for value in ("2.5", None, float("nan"), BadFloat()):
        _parity("_to_float", monitor._to_float, float_owner, (value,))


def test_estimate_reclaim_price_matches_original_ast_and_helper_monkeypatch(monkeypatch):
    for args in ((100.0, 0.05, 0.01), (None, 0.0, 0.0), (100.0, -1.0, 0.01)):
        _parity("_estimate_reclaim_price", monitor._estimate_reclaim_price, reclaim_owner, args)
    calls=[]
    def patched(value):
        calls.append(value)
        return {"price": 100.0, "distance": 0.1, "tolerance": 0.02}.get(value)
    monkeypatch.setattr(monitor, "_to_float", patched)
    reference = _original("_estimate_reclaim_price", _to_float=patched)
    assert monitor._estimate_reclaim_price("price", "distance", "tolerance") == reference("price", "distance", "tolerance")
    assert reclaim_owner("price", "distance", "tolerance", facade=monitor) == reference("price", "distance", "tolerance")


def test_build_stale_groups_matches_original_ast_and_order():
    rows = [
        {"minute_source_present": True, "latest_candle_ts": 10, "artifact_age_minutes": 4, "symbol": "A", "evaluation_summary": "r", "ts": "2", "run_id": "later"},
        {"minute_source_present": True, "latest_candle_ts": 10, "artifact_age_minutes": 5, "symbol": "A", "evaluation_summary": "r", "ts": "1", "run_id": "first"},
        {"minute_source_present": False, "latest_candle_ts": 11, "artifact_age_minutes": 9, "symbol": "B", "evaluation_summary": "x", "ts": "3", "run_id": "skip"},
    ]
    _parity("_build_stale_groups", monitor._build_stale_groups, stale_groups_owner, (rows,), {"stale_age_min": 3.0})
    assert monitor._build_stale_groups([]) == []
    seen = []
    def patched(value):
        seen.append(value)
        return float(value) if value is not None else None
    original = _original("_build_stale_groups", _to_float=patched)
    assert monitor._build_stale_groups(rows, stale_age_min=3.0) == original(rows, stale_age_min=3.0)
    assert stale_groups_owner(rows, stale_age_min=3.0, facade=monitor) == original(rows, stale_age_min=3.0)
    assert seen


def test_followup_from_rows_matches_original_ast_and_threshold_flags():
    case = {"latest_candle_ts": 100, "current_price": 10, "breakout_level": 12, "reclaim_price": 11}
    rows = [{"ts": 101, "high": 12, "low": 9, "close": 11}]
    _parity("_followup_from_rows", monitor._followup_from_rows, followup_owner, (case, rows))
    assert monitor._followup_from_rows(case, []) == {"later_bars": 0}
    patched = lambda value: float(value) if value is not None else None
    original = _original("_followup_from_rows", _to_float=patched)
    assert monitor._followup_from_rows(case, rows) == original(case, rows)
    assert followup_owner(case, rows, facade=monitor) == original(case, rows)


def test_module_path_matches_original_ast_and_value_error():
    _parity("_module_path", audit._module_path, module_path_owner, ("scripts/diagnostics/example.py",))
    for path in ("docs/example.py", "scripts/example.txt"):
        expected = _original("_module_path")
        with __import__("pytest").raises(ValueError) as source_exc:
            audit._module_path(path)
        with __import__("pytest").raises(ValueError) as owner_exc:
            module_path_owner(path, facade=audit)
        with __import__("pytest").raises(ValueError) as original_exc:
            expected(path)
        assert str(source_exc.value) == str(owner_exc.value) == str(original_exc.value)


def test_call_targets_matches_original_ast_literals_and_order(monkeypatch):
    tree = python_ast.parse("obj.method('pkg.a'); obj.method(target); other.method('pkg.b'); obj.method('pkg.a')")
    _parity("_call_targets", audit._call_targets, call_targets_owner, (tree, "obj", "method"))
    facade_ast = SimpleNamespace(**{name: getattr(python_ast, name) for name in ("walk", "Call", "Attribute", "Name", "Constant")})
    monkeypatch.setattr(audit, "ast", facade_ast)
    original = _original("_call_targets", ast=facade_ast)
    assert audit._call_targets(tree, "obj", "method") == original(tree, "obj", "method")
    assert call_targets_owner(tree, "obj", "method", facade=audit) == original(tree, "obj", "method")


def test_has_statement_matches_original_ast_identity_predicate(monkeypatch):
    statements = python_ast.parse("x = 1\ny = 2").body
    _parity("_has_statement", audit._has_statement, has_statement_owner, (statements, "x = 1"))
    assert audit._has_statement(statements, "x=2") is False
    facade_ast = SimpleNamespace(**{name: getattr(python_ast, name) for name in ("dump", "parse")})
    monkeypatch.setattr(audit, "ast", facade_ast)
    original = _original("_has_statement", ast=facade_ast)
    assert audit._has_statement(statements, "x = 1") == original(statements, "x = 1") is True
    assert has_statement_owner(statements, "x = 1", facade=audit) == original(statements, "x = 1")
    for source in ("x =", "if:"):
        with __import__("pytest").raises(SyntaxError) as original_exc:
            _original("_has_statement")(statements, source)
        with __import__("pytest").raises(SyntaxError) as source_exc:
            audit._has_statement(statements, source)
        with __import__("pytest").raises(SyntaxError) as owner_exc:
            has_statement_owner(statements, source, facade=audit)
        assert str(original_exc.value) == str(source_exc.value) == str(owner_exc.value)
