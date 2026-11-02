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
