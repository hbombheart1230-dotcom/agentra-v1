"""q8_evaluation_contract projections (moved verbatim from q8_evaluation_contract).

Module globals and helpers are resolved on ``facade`` (the q8_evaluation_contract module) at call time; this module never imports it.
"""
from __future__ import annotations

from typing import Any, Mapping


def candidate_day(row: Mapping[str, Any], *, facade: Any) -> str:
    base = facade.forward_base(row)
    raw_ts = facade.text_value(base.get("baseline_raw_ts"))
    if len(raw_ts) >= 8 and raw_ts[:8].isdigit():
        return raw_ts[:8]
    generated = facade.text_value(row.get("_payload_generated_at") or row.get("generated_at"))
    return generated[:10].replace("-", "") if len(generated) >= 10 else ""
