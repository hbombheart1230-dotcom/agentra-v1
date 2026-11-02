from __future__ import annotations

from typing import Any, Mapping
import sys
from . import scanner_score_decomposition_num as _a47_num
from . import scanner_score_decomposition_first_num as _a47_first_num
from . import scanner_score_decomposition_nested_mapping as _a47_nested_mapping
from . import scanner_score_decomposition_decompose_scanner_score as _a47_decompose_scanner_score


def _num(value: Any) -> float | None:
    return _a47_num._num(value, facade=sys.modules[__name__])


def _first_num(row: Mapping[str, Any], keys: tuple[str, ...]) -> float | None:
    return _a47_first_num._first_num(row, keys, facade=sys.modules[__name__])


def _nested_mapping(row: Mapping[str, Any], key: str) -> Mapping[str, Any]:
    return _a47_nested_mapping._nested_mapping(row, key, facade=sys.modules[__name__])


def decompose_scanner_score(candidate: Mapping[str, Any] | None) -> dict[str, Any]:
    """Return an additive, read-only score view for scanner candidates.

    This does not change ranking behavior. It only separates the fields that are
    often conflated in reports: raw technical quality, strategy context,
    cost/horizon fit, and execution readiness.
    """
    return _a47_decompose_scanner_score.decompose_scanner_score(candidate, facade=sys.modules[__name__])


__all__ = ["decompose_scanner_score"]
