from typing import Any, Mapping


def _market_snapshot(row: Mapping[str, Any], *, prospective: bool, facade) -> dict[str, Any]:
    number = facade._number
    observation = row.get("opening_observability") if prospective and isinstance(row.get("opening_observability"), Mapping) else {}
    point_in_time = row.get("market_snapshot") if prospective and isinstance(row.get("market_snapshot"), Mapping) else {}
    if not point_in_time and isinstance(observation.get("market_snapshot"), Mapping):
        point_in_time = observation.get("market_snapshot")
    asset = observation.get("asset_observation") if isinstance(observation.get("asset_observation"), Mapping) else {}
    market_return = number(point_in_time.get("kospi_pct")) if prospective else number(row.get("kospi_pct"))
    if market_return is None and prospective:
        market_return = number(observation.get("market_return_pct"))
    exposure = str(asset.get("exposure_direction") or "LONG_RISK_OR_OTHER")
    aligned = None
    if market_return not in (None, 0.0):
        inverse = "INVERSE" in exposure.upper()
        aligned = bool((market_return > 0.0 and not inverse) or (market_return < 0.0 and inverse))
    return {
        "market_return_pct": market_return,
        "kospi_pct": number(point_in_time.get("kospi_pct")) if prospective else number(row.get("kospi_pct")),
        "kosdaq_pct": number(point_in_time.get("kosdaq_pct")) if prospective else number(row.get("kosdaq_pct")),
        "kospi200_pct": number(point_in_time.get("kospi200_pct")) if prospective else number(row.get("kospi200_pct")),
        "krx_night_futures_pct": number(point_in_time.get("krx_night_futures_pct")) if prospective else number(row.get("krx_night_futures_pct")),
        "snapshot_epoch": int(point_in_time.get("snapshot_epoch") or 0) or None,
        "snapshot_time_kst": str(point_in_time.get("snapshot_time_kst") or ""),
        "snapshot_age_sec": int(point_in_time.get("snapshot_age_sec") or 0) if point_in_time.get("snapshot_age_sec") is not None else None,
        "snapshot_source_path": str(point_in_time.get("source_path") or ""),
        "snapshot_selection_policy": str(point_in_time.get("selection_policy") or ""),
        "snapshot_evidence_status": str(point_in_time.get("evidence_status") or ""),
        "nasdaq_pct": number(row.get("nasdaq_pct")),
        "vix_level": number(row.get("vix_level")),
        "market_rising": number(row.get("market_rising")),
        "market_falling": number(row.get("market_falling")),
        "engine_regime": str(row.get("engine_regime") or "MISSING"),
        "asset_class": str(asset.get("asset_class") or "MISSING"),
        "exposure_direction": exposure,
        "exposure_alignment": aligned,
    }
