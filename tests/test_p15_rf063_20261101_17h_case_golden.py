import importlib.util
from pathlib import Path

import pytest

from scripts.diagnostics import check_trade_report_runtime_regression as runtime


def _golden():
    spec = importlib.util.spec_from_file_location("trade_golden_test", Path(__file__).with_name("test_p15_rf063_20261101_17h_canonical_trade_golden.py"))
    module = importlib.util.module_from_spec(spec); assert spec and spec.loader; spec.loader.exec_module(module)
    return module._golden()


@pytest.mark.parametrize("text,expected", [("2026-04-16:TRD_01", {"day":"2026-04-16","trade_id":"TRD_01","target_run_id":""}), ("2026-04-16:TRD_01:run-x", {"day":"2026-04-16","trade_id":"TRD_01","target_run_id":"run-x"})])
def test_parse_case_canonical_golden(text, expected):
    golden = _golden(); assert golden._parse_case(text) == runtime._parse_case(text) == expected


def test_case_errors_and_deduplication_canonical_golden():
    golden = _golden()
    for value in ("", ":TRD_01"):
        with pytest.raises(ValueError) as left:
            golden._parse_case(value)
        with pytest.raises(ValueError) as right:
            runtime._parse_case(value)
        assert str(left.value) == str(right.value)
    cases = ["2026-04-16:TRD_01:run-a", "2026-04-16:TRD_01:run-b", "2026-04-17:TRD_02"]
    assert golden._normalize_cases(cases) == runtime._normalize_cases(cases)
    assert golden._normalize_cases(cases)[0]["target_run_id"] == "run-a"
    assert golden._normalize_cases([]) == runtime._normalize_cases([])
    assert [item["trade_id"] for item in golden._normalize_cases([])] == [item[1] for item in runtime.DEFAULT_GOLDEN_CASES]
