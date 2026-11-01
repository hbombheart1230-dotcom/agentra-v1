"""RF-023 A26-6/7: live_session_watch formatters, original (b2e48863 preimage, blob 5b229dec) vs wrappers + Owners.

Pure string formatting on supplied mappings; ``main``/``_run_once``/clock/IO are never called. Sockets, subprocess and
Path writes are guarded.
"""
from __future__ import annotations

import ast
import copy
import hashlib
import importlib
import inspect
import socket
import subprocess
from pathlib import Path

import pytest

PRE = "b2e48863ae8a44d7ab41090160816d504052f2e0"
PATH = "libs/runtime/entrypoints/live_session_watch.py"
PRE_BLOB = "5b229dec3eadb5c17c6e15fc777ea9f6aaed074f"
NAMES = ["_build_markdown", "_build_console_line"]
lsw = importlib.import_module("libs.runtime.entrypoints.live_session_watch")
OWNERS = {
    "_build_markdown": importlib.import_module("libs.runtime.entrypoints.live_session_watch_build_markdown"),
    "_build_console_line": importlib.import_module("libs.runtime.entrypoints.live_session_watch_build_console_line"),
}


def _sha(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + bytes([0]) + raw).hexdigest()


@pytest.fixture(scope="module")
def orig_nodes():
    try:
        raw = subprocess.run(["git", "show", f"{PRE}:{PATH}"], check=True, capture_output=True).stdout
    except subprocess.CalledProcessError as exc:
        pytest.fail(f"BLOCKED_PIN: {exc.stderr!r}")
    assert _sha(raw) == PRE_BLOB, "BLOCKED_PIN original blob"
    tree = ast.parse(raw.decode("utf-8"))
    nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in NAMES]
    assert sorted(n.name for n in nodes) == sorted(NAMES)
    return nodes


@pytest.fixture
def guards(monkeypatch):
    def boom(*a, **k):
        raise AssertionError("effect attempted")
    monkeypatch.setattr(subprocess, "run", boom)
    monkeypatch.setattr(subprocess, "Popen", boom)
    monkeypatch.setattr(socket.socket, "connect", boom)
    monkeypatch.setattr(Path, "mkdir", boom)
    monkeypatch.setattr(Path, "write_text", boom)


def check(orig_nodes, name, snapshot):
    ns = dict(vars(lsw))
    mod = ast.Module(body=copy.deepcopy(orig_nodes), type_ignores=[])
    exec(compile(ast.fix_missing_locations(mod), f"<{PRE[:8]}:{PATH}>", "exec"), ns)
    got = {}
    for label, fn in (("orig", ns[name]), ("new", getattr(lsw, name))):
        a = copy.deepcopy(snapshot)
        try:
            got[label] = ("ok", fn(a))
        except Exception as exc:
            got[label] = ("err", type(exc).__name__, str(exc))
        assert a == snapshot, f"{label} mutated input"
    assert got["orig"] == got["new"], got
    return got["new"]


FULL = {
    "ts_kst": "2026-04-16 09:30:00 KST", "loop_alive": True, "loop_pid": 4242, "event_lag_sec": 7, "summary_rc": 0,
    "health": {"status": "YELLOW", "reasons": ["window_empty", "한글 이유"],
               "recommended_actions": ["verify market session", "점검 필요"],
               "metrics": {"window_total": 12, "llm_error_rate": 0.1234, "blocked_rate": 0.5,
                           "executed_broker_fail_total": 2}},
    "summary": {"decision": {"action_counts": {"SELL": 2, "BUY": 3, "NOOP": 9, "한글": 1}}},
    "summary_report_json_path": "/tmp/x/summary.json", "summary_report_md_path": "/tmp/x/summary.md",
    "watch_jsonl_path": "/tmp/x/watch.jsonl",
}

SNAPSHOTS = [
    {},
    FULL,
    {"health": "bad", "summary": [], "loop_alive": 0, "loop_pid": None, "summary_rc": None},
    {"health": {"metrics": "bad", "reasons": "not a list", "recommended_actions": None}, "summary": {"decision": 5}},
    {"ts_kst": None, "event_lag_sec": None, "health": {"status": "RED", "reasons": [], "recommended_actions": [],
                                                      "metrics": {"window_total": None, "llm_error_rate": None}}},
    {"health": {"reasons": [1, None, {"a": 1}], "recommended_actions": [("t", 1)]},
     "summary": {"decision": {"action_counts": {"b": 1, "a": 2}}}},
]


@pytest.mark.parametrize("idx", range(len(SNAPSHOTS)))
def test_build_markdown(orig_nodes, guards, idx):
    check(orig_nodes, "_build_markdown", SNAPSHOTS[idx])


@pytest.mark.parametrize("idx", range(len(SNAPSHOTS)))
def test_build_console_line(orig_nodes, guards, idx):
    check(orig_nodes, "_build_console_line", SNAPSHOTS[idx])


def test_markdown_exact_strings(orig_nodes, guards):
    status, text = check(orig_nodes, "_build_markdown", FULL)
    assert status == "ok"
    assert text.startswith("# Live Session Watch (2026-04-16 09:30:00 KST)\n\n- status: **YELLOW**\n")
    assert '- decision action_counts: `{"SELL": 2, "BUY": 3, "NOOP": 9, "한글": 1}`' in text  # key order + unicode
    assert "- llm_error_rate: **12.34%**" in text and "- 한글 이유" in text
    assert text.endswith("- watch_jsonl_path: `/tmp/x/watch.jsonl`") and not text.endswith("\n")
    empty = check(orig_nodes, "_build_markdown", {})[1]
    assert empty.count("- none") == 2 and "status: **UNKNOWN**" in empty


def test_console_line_exact(orig_nodes, guards):
    _, line = check(orig_nodes, "_build_console_line", FULL)
    assert line == ("[2026-04-16 09:30:00 KST] status=YELLOW loop_alive=True lag_sec=7 window=12 buy=3 sell=2 "
                    "noop=9 llm_error_rate=12.34% blocked_rate=50.00%")
    _, empty = check(orig_nodes, "_build_console_line", {})
    assert empty == "[None] status=None loop_alive=False lag_sec=None window=0 buy=0 sell=0 noop=0 llm_error_rate=0.00% blocked_rate=0.00%"


@pytest.mark.parametrize("name", NAMES)
def test_wrapper_thin_and_owner_holds_body(name):
    wrapper = ast.parse(inspect.getsource(getattr(lsw, name))).body[0]
    assert len(wrapper.body) == 1 and isinstance(wrapper.body[0], ast.Return)
    assert not [n for n in ast.walk(wrapper) if isinstance(n, (ast.If, ast.For, ast.Try, ast.ListComp))]
    owner_fn = getattr(OWNERS[name], name)
    assert len(list(ast.walk(ast.parse(inspect.getsource(owner_fn)).body[0]))) > 30
    assert owner_fn.__module__ == OWNERS[name].__name__
    assert "live_session_watch import" not in inspect.getsource(OWNERS[name])
