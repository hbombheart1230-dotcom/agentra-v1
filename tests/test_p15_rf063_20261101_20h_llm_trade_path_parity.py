import subprocess
import types
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Dict

from libs.reporting import llm_artifacts as b_module


_SHA = "8eff2d9e2d5b40ee2049579941597c95890d1ad1"
_PATH = "libs/reporting/llm_artifacts_trade_path_projection.py"
_BLOB = "cf17542917ac15c34dba2e6bd9f3694cc97a13f7"


def _canonical_owner():
    raw = subprocess.check_output(["git", "show", f"{_SHA}:{_PATH}"], text=True)
    assert subprocess.check_output(["git", "hash-object", "--stdin"], input=raw, text=True).strip() == _BLOB
    module = types.ModuleType("canonical_llm_trade_path_projection")
    module.__dict__.update({"Any": Any, "Dict": Dict, "Path": Path})
    exec(compile(raw, "canonical_llm_trade_path_projection", "exec"), module.__dict__)
    return module


def _canonical_facade():
    return SimpleNamespace(
        canonical_trade_day_root=b_module.canonical_trade_day_root,
        resolve_trade_day_root=b_module.resolve_trade_day_root,
        find_trade_dir=b_module.find_trade_dir,
    )


def _assert_equal(tmp_path, *, owner=None, **kwargs):
    owner = owner or _canonical_owner()
    before = list(tmp_path.rglob("*"))
    expected = owner.trade_artifact_paths(tmp_path, "2026-04-16", "TRD_X", facade=_canonical_facade(), **kwargs)
    actual = b_module.trade_artifact_paths(tmp_path, "2026-04-16", "TRD_X", **kwargs)
    assert actual == expected
    assert list(tmp_path.rglob("*")) == before
    return actual


def test_empty_root_path_dictionary_matches_canonical_owner(tmp_path):
    actual = _assert_equal(tmp_path, prefer_existing_day_root=False)
    assert actual["trade_root"] == tmp_path / "trades" / "2026-04-16" / "TRD_X"


def test_time_bucket_path_dictionary_matches_canonical_owner(tmp_path):
    actual = _assert_equal(tmp_path, prefer_existing_day_root=False, time_bucket="0930")
    assert actual["trade_root"] == tmp_path / "trades" / "2026-04-16" / "0930" / "TRD_X"


def test_prefer_existing_without_directories_is_pure_and_matches(tmp_path, monkeypatch):
    owner = _canonical_owner()
    monkeypatch.setattr(subprocess, "run", lambda *_a, **_kw: (_ for _ in ()).throw(AssertionError("subprocess invoked")))
    _assert_equal(tmp_path, owner=owner, prefer_existing_day_root=True)
