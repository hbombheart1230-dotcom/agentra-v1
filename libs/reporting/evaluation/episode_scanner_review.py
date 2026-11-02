from __future__ import annotations

from collections import defaultdict
from math import sqrt
from typing import Any, Mapping, Sequence
import sys

from libs.reporting.q8_evaluation_contract import candidate_day

from .metrics import performance_metrics
from .scanner_quality import SCANNER_HORIZONS, pre_strategist_candidate_rows
from . import episode_scanner_review_number as _a51_number
from . import episode_scanner_review_mapping as _a51_mapping
from . import episode_scanner_review_checkpoint_return as _a51_checkpoint_return
from . import episode_scanner_review_epoch as _a51_epoch
from . import episode_scanner_review_setup_key as _a51_setup_key
from . import episode_scanner_review_day as _a51_day
from . import episode_scanner_review_rank_bucket as _a51_rank_bucket
from . import episode_scanner_review_episode_representatives as _a51_episode_representatives
from . import episode_scanner_review_build_episode_scanner_review as _a54_esr_build
from . import episode_scanner_review_build_same_symbol_reentry_review as _a54_esr_reentry


RANK_BUCKETS = ("rank1", "rank2_3", "rank4_plus", "unknown")


def _number(value: Any) -> float | None:
    return _a51_number._number(value, facade=sys.modules[__name__])


def _mapping(value: Any) -> Mapping[str, Any]:
    return _a51_mapping._mapping(value, facade=sys.modules[__name__])


def _checkpoint_return(row: Mapping[str, Any], horizon: str) -> float | None:
    return _a51_checkpoint_return._checkpoint_return(row, horizon, facade=sys.modules[__name__])


def _epoch(row: Mapping[str, Any]) -> int:
    return _a51_epoch._epoch(row, facade=sys.modules[__name__])


def _setup_key(row: Mapping[str, Any]) -> str:
    return _a51_setup_key._setup_key(row, facade=sys.modules[__name__])


def _day(row: Mapping[str, Any]) -> str:
    return _a51_day._day(row, facade=sys.modules[__name__])


def _rank_bucket(rank: int) -> str:
    return _a51_rank_bucket._rank_bucket(rank, facade=sys.modules[__name__])


def _episode_representatives(
    rows: Sequence[Mapping[str, Any]],
    *,
    episode_gap_sec: int,
) -> list[dict[str, Any]]:
    return _a51_episode_representatives._episode_representatives(rows, episode_gap_sec=episode_gap_sec, facade=sys.modules[__name__])


def build_episode_scanner_review(
    payloads: list[dict[str, Any]],
    *,
    mock_drag_pct: float,
    live_drag_pct: float,
    episode_gap_sec: int = 900,
    prepared_rows: Sequence[Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    return _a54_esr_build.build_episode_scanner_review(payloads, mock_drag_pct=mock_drag_pct, live_drag_pct=live_drag_pct, episode_gap_sec=episode_gap_sec, prepared_rows=prepared_rows, facade=sys.modules[__name__])


def build_same_symbol_reentry_review(
    rows: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    return _a54_esr_reentry.build_same_symbol_reentry_review(rows, facade=sys.modules[__name__])


__all__ = [
    "build_episode_scanner_review",
    "build_same_symbol_reentry_review",
]
