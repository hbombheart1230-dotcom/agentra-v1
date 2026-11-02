"""Fake-only parity coverage for B38 diagnostics owners."""
from __future__ import annotations

import ast
from datetime import datetime, timezone

import pytest

from scripts.diagnostics import audit_target_tree_compat as tree_audit
from scripts.diagnostics import audit_windows_launchers as launchers
from scripts.diagnostics import check_phase_5_2_5_3_runtime_health as health
from scripts.diagnostics import query_intent_state_store as intent_store
from scripts.diagnostics import reconstruct_incident_timeline as timeline
from scripts.diagnostics import run_m29_incident_timeline_check as m29
from scripts.diagnostics.audit_target_tree_compat_dispatch_issues import _dispatch_issues as dispatch_owner
from scripts.diagnostics.audit_windows_launchers_assert_mockexam_known_contract import assert_mockexam_known_contract as contract_owner
from scripts.diagnostics.audit_windows_launchers_resolve_task import _resolve_task as task_owner
from scripts.diagnostics.check_phase_5_2_5_3_runtime_health_build_parser import _build_parser as health_parser_owner
from scripts.diagnostics.query_intent_state_store_build_parser import _build_parser as state_parser_owner
from scripts.diagnostics.query_intent_state_store_summary import _summary as summary_owner
from scripts.diagnostics.reconstruct_incident_timeline_utc_day import _utc_day as day_owner
from scripts.diagnostics.run_m29_incident_timeline_check_build_parser import _build_parser as m29_parser_owner


def test_dispatch_issues_fake_ast_parity_and_facade_helper(monkeypatch):
    tree = ast.parse("if __name__ == '__main__':\n _runpy.run_module('x.y', run_name='__main__')\nelse:\n _sys.modules[__name__] = _importlib.import_module('x.y')")
    assert tree_audit._dispatch_issues(tree, "x.y", bulk=True) == []
    assert dispatch_owner(tree, "x.y", bulk=True, facade=tree_audit) == []
    monkeypatch.setattr(tree_audit, "_has_statement", lambda *_: False)
    assert dispatch_owner(tree, "x.y", bulk=True, facade=tree_audit) == [
        "executable __main__ dispatch missing or invalid", "module-object ABI alias missing or invalid"
    ]


@pytest.mark.parametrize("raw,prefix,expected", [
    ("Task.1", None, ("Task.1", "LITERAL")),
    ("%TASK_PREFIX%-Run", "Pre", ("Pre-Run", "PREFIX_RESOLVED")),
    ("bad task", "Pre", (None, "UNRESOLVED")),
])
def test_resolve_task_parity(raw, prefix, expected):
    assert launchers._resolve_task(raw, prefix) == expected
    assert task_owner(raw, prefix, facade=launchers) == expected


def test_utc_day_clock_and_to_epoch_parity(monkeypatch):
    assert timeline._utc_day(0) == "1970-01-01"
    assert day_owner(3600, facade=timeline) == "1970-01-01"
    monkeypatch.setattr(timeline, "_to_epoch", lambda value: None)
    class Clock:
        @classmethod
        def now(cls, tz):
            return datetime(2030, 1, 2, tzinfo=timezone.utc)
        @classmethod
        def fromtimestamp(cls, value, tz):
            return datetime(2000, 1, 1, tzinfo=timezone.utc)
    monkeypatch.setattr(timeline, "datetime", Clock)
    assert timeline._utc_day("bad") == "2030-01-02"
    assert day_owner("bad", facade=timeline) == "2030-01-02"


def test_summary_in_memory_filter_stuck_and_identity_parity():
    rows = [{"state": "executing", "updated_ts": 5}, {"state": "executed", "updated_ts": 20}]
    kwargs = dict(now_epoch=20, stuck_executing_sec=10, journal_transition_total={"x": 1}, limit=0)
    out = intent_store._summary(rows, **kwargs)
    assert out == summary_owner(rows, facade=intent_store, **kwargs)
    assert out["active_total"] == 1 and out["terminal_total"] == 1 and out["stuck_executing_total"] == 1
    assert rows[0] == {"state": "executing", "updated_ts": 5}


def test_query_state_parser_defaults_and_flags():
    assert vars(intent_store._build_parser().parse_args(["--limit", "1", "--json"])) == vars(
        state_parser_owner(facade=intent_store).parse_args(["--limit", "1", "--json"])
    )


def test_health_parser_defaults_and_flags():
    assert vars(health._build_parser().parse_args(["--run-id", "x", "--only-buy"])) == vars(
        health_parser_owner(facade=health).parse_args(["--run-id", "x", "--only-buy"])
    )


def test_frozen_contract_mutates_only_fake_result_and_preserves_identity(monkeypatch):
    result = {"mockexam_task_contract": {"status": "PROVEN", "registered": list(launchers._FROZEN_REGISTERED),
              "unregistered": list(launchers._FROZEN_UNREGISTERED)}, "issues": []}
    identity = id(result)
    launchers.assert_mockexam_known_contract(result)
    assert id(result) == identity and result["ok"] is True
    bad = {"mockexam_task_contract": {"status": "NO", "registered": [], "unregistered": []}, "issues": ["prior"]}
    contract_owner(bad, facade=launchers)
    assert bad["issues"][-1] == "MockExam frozen task-name contract not proven or changed" and bad["ok"] is False


def test_m29_parser_defaults_and_custom_flags():
    assert vars(m29._build_parser().parse_args(["--day", "2020-01-01", "--json"])) == vars(
        m29_parser_owner(facade=m29).parse_args(["--day", "2020-01-01", "--json"])
    )


