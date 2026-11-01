"""selection_evidence_projection projections (moved verbatim from selection_evidence_projection).

Module globals and helpers are resolved on ``facade`` (the selection_evidence_projection module) at call time; this module never imports it.
"""
from __future__ import annotations



def scan_select_value_state_scanner_skill(fallback_reasons, skill_quotes, skill_order_counts, skill_order_rows, quote_meta, order_meta, *, facade):
    return (
{
        "contract_version": facade.SKILL_CONTRACT_VERSION,
        "used": bool(skill_quotes) or bool(skill_order_counts),
        "quote_symbols": len(skill_quotes),
        "account_open_order_symbols": len(skill_order_counts),
        "account_order_rows": int(skill_order_rows),
        "quote_present": bool(quote_meta.get("present")),
        "account_orders_present": bool(order_meta.get("present")),
        "fallback": bool(fallback_reasons),
        "fallback_reasons": fallback_reasons,
        "error_count": len(fallback_reasons),
    }
    )
