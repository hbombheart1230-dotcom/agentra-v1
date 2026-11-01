from typing import Any


def predefined_opening_screens(rows: list[dict[str, Any]], *, facade: Any) -> list[dict[str, Any]]:
    def observed(row, key, default):
        value = facade.number(row.get(key)); return default if value is None else value
    def rank_positive_1m(row): return observed(row, "rank1_prev5m_observations", 0) >= 1 and observed(row, "precompleted_return_1m_pct", 0) > 0
    def moderate_relative_volume(row):
        value = facade.number(row.get("opening_relative_volume")); return value is not None and .5 <= value <= 4
    def dislocation(row):
        kospi, extension = facade.number(row.get("kospi_pct")), facade.number(row.get("entry_vs_prior_close_pct")); return bool((kospi is not None and kospi <= -3) or (extension is not None and extension <= -8))
    screens = {"OPEN_0_5_ALL": lambda r: observed(r,"decision_from_open_sec",9999)<300, "OPEN_0_5_ABOVE_VWAP": lambda r: observed(r,"decision_from_open_sec",9999)<300 and r.get("above_vwap") is True, "OPEN_0_5_SCORE_GE_1_25": lambda r: observed(r,"decision_from_open_sec",9999)<300 and observed(r,"scanner_score",-999)>=1.25, "OPEN_0_5_GAP_0_5": lambda r: observed(r,"decision_from_open_sec",9999)<300 and 0<=observed(r,"opening_gap_pct",-999)<5, "OPEN_0_10_NOT_EXTENDED": lambda r: observed(r,"decision_from_open_sec",9999)<600 and observed(r,"entry_vs_prior_close_pct",999)<5, "OPEN_PRIOR_RANK_CONFIRMATION": lambda r: int(observed(r,"rank1_prev5m_observations",0))>=1 and observed(r,"entry_vs_prior_close_pct",999)<5, "CONFIRMED_RANK_POSITIVE_1M": rank_positive_1m, "CONFIRMED_RANK_POSITIVE_1M_MODERATE_VOLUME": lambda r: rank_positive_1m(r) and moderate_relative_volume(r), "CONFIRMED_RANK_POSITIVE_1M_ABOVE_VWAP": lambda r: rank_positive_1m(r) and r.get("above_vwap") is True, "DISLOCATION_MODERATE_VOLUME": lambda r: dislocation(r) and moderate_relative_volume(r)}
    return [{"screen": name, "horizon": horizon, "point_in_time_eligible": True, **facade._group_summary([row for row in rows if predicate(row)], field)} for name, predicate in screens.items() for horizon, field in facade.HORIZONS.items()]
