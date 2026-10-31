"""quant_shadow_candidate_evaluation projections (moved verbatim from quant_shadow_candidate_evaluation).

Module globals and helpers are resolved on ``facade`` (the quant_shadow_candidate_evaluation module) at call time; this module never imports it.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence


def load_quant_shadow_candidate_payloads_for_range(
    *,
    reports_root: Path,
    start: str,
    end: str,
    drop_q9_row_keys: Optional[Sequence[str]] = None,
    keys: Optional[Sequence[str]] = None,
    facade: Any,
) -> List[Dict[str, Any]]:
    return facade.load_quant_shadow_candidate_payloads(
        reports_root=reports_root,
        days=list(facade._iter_days(start, end)),
        keys=keys,
        drop_q9_row_keys=drop_q9_row_keys,
    )
