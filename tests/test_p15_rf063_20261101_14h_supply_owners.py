import ast
from pathlib import Path
from tempfile import TemporaryDirectory

from scripts.diagnostics import check_audit_trail_completeness as audit
from scripts.diagnostics import run_m27_closeout_check as m27_closeout
from scripts.diagnostics import run_m27_portfolio_budget_boundary_check as budget
from scripts.diagnostics import run_m29_closeout_check as m29_closeout


def test_budget_parser_wrapper_owner_and_ast():
    assert vars(budget._build_parser().parse_args(["--json", "--inject-fail"])) == {"json": True, "inject_fail": True}
    node = ast.parse(Path(budget.__file__).read_text()).body
    assert any(isinstance(x, ast.FunctionDef) and x.name == "_build_parser" and len(x.body) == 2 for x in node)


def test_profiles_golden_and_independence():
    first, second = budget._profiles(), budget._profiles()
    first[0]["weight"] = 1
    assert [x["strategy_id"] for x in second] == ["trend", "mean_reversion", "event_driven"]
    assert [x["weight"] for x in second] == [.5, .3, .2]


def test_intents_normal_negative_and_independence():
    assert len(budget._intents(inject_fail=False)) == 5
    assert len(budget._intents(inject_fail=True)) == 2
    assert budget._intents(inject_fail=False) is not budget._intents(inject_fail=False)


def test_caps_normal_and_negative():
    assert budget._symbol_caps(inject_fail=False)["000660"] == 500.0
    assert budget._symbol_caps(inject_fail=True)["000660"] == 10_000.0


def test_closeout_parser_owners():
    assert vars(m27_closeout._build_parser().parse_args(["--json", "--no-clear"]))["day"] == "2026-02-20"
    assert vars(m29_closeout._build_parser().parse_args(["--json", "--no-clear"]))["day"] == "2026-02-21"


def test_rows_temp_jsonl_and_missing():
    with TemporaryDirectory() as raw:
        path = Path(raw) / "rows.jsonl"; path.write_text("\nnope\n[]\n{\"run_id\": \"r1\"}\n")
        assert audit._iter_rows(path) == [{"run_id": "r1"}]
        assert audit._iter_rows(Path(raw) / "missing") == []


def test_analysis_normal_and_negative(monkeypatch):
    monkeypatch.setattr(audit, "_extract_decision_action", lambda row: row.get("action", ""))
    monkeypatch.setattr(audit, "_extract_allowed", lambda row: row.get("allowed"))
    assert audit.analyze_day_rows([])["link_success_rate"] == 1.0
    rows = [{"run_id":"r", "stage":"decision", "event":"trace", "action":"BUY"}, {"run_id":"r", "stage":"execute_from_packet", "event":"start"}, {"run_id":"r", "stage":"execute_from_packet", "event":"verdict", "allowed":True}, {"run_id":"r", "stage":"execute_from_packet", "event":"execution"}, {"run_id":"r", "stage":"execute_from_packet", "event":"end"}]
    assert audit.analyze_day_rows(rows)["linked_complete_run_total"] == 1
    assert audit.analyze_day_rows(rows[:-1])["missing_terminal_event_total"] == 1
