from libs.runtime import decision_observability as d

def test_simple_owner_facades():
    assert d._to_float("1.5")==1.5
    assert d._to_int("2.9")==2
    assert d._clip("abcd",max_len=3)=="..."
    assert d._humanize_reason_code("a_b")=="a b"
    assert d._normalize_decision_outcome(" buy ")=="BUY"
    assert d._extract_error_type("ValueError: x")=="ValueError"
    assert d._dedupe_non_empty([" a ", "a", "", "b"], limit=1)==["a"]
    assert d._extract_failed_names([{"name":"x","status":"FAIL"}],statuses=("fail",))==["x"]


def test_dedupe_owner_edge_cases_and_input_order():
    values = [" a ", "", "a", "b", "b", " c "]
    assert d._dedupe_non_empty(values, limit=None) == ["a", "b", "c"]
    assert d._dedupe_non_empty(values, limit=0) == ["a"]
    assert d._dedupe_non_empty(values, limit=1) == ["a"]
    assert values == [" a ", "", "a", "b", "b", " c "]


def test_extract_failed_names_uses_call_time_dedupe(monkeypatch):
    seen = []
    monkeypatch.setattr(d, "_dedupe_non_empty", lambda values, **kwargs: seen.append(list(values)) or ["patched"])
    rows = [{"name": "one", "status": " FAIL "}, {"name": "two", "status": "ok"}, {"name": "three", "status": "fail"}]
    assert d._extract_failed_names(rows, statuses=("fail",)) == ["patched"]
    assert seen == [["one", "three"]]
