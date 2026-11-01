from typing import Any, Dict


def _symbol_caps(*, inject_fail: bool, facade: Any) -> Dict[str, float]:
    if inject_fail:
        return {"005930": 10_000.0, "000660": 10_000.0}
    return {"005930": 10_000.0, "000660": 500.0}
