from __future__ import annotations

from collections import Counter, defaultdict
from typing import Any, Mapping, Sequence
import sys

from .metrics import performance_metrics
from . import horizon_compliance_report_mapping as _a46_mapping
from . import horizon_compliance_report_num as _a46_num
from . import horizon_compliance_report_bucket_key as _a46_bucket_key
from . import horizon_compliance_report_build_horizon_compliance_report as _a46_build_horizon_compliance_report
from . import horizon_compliance_report_render_horizon_compliance_report as _a46_render_horizon_compliance_report


def _mapping(value: Any) -> Mapping[str, Any]:
    return _a46_mapping._mapping(value, facade=sys.modules[__name__])


def _num(value: Any) -> float | None:
    return _a46_num._num(value, facade=sys.modules[__name__])


def _bucket_key(evaluation: Mapping[str, Any]) -> tuple[str, str]:
    return _a46_bucket_key._bucket_key(evaluation, facade=sys.modules[__name__])


def build_horizon_compliance_report(
    evaluations: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    return _a46_build_horizon_compliance_report.build_horizon_compliance_report(evaluations, facade=sys.modules[__name__])


def render_horizon_compliance_report(payload: Mapping[str, Any]) -> str:
    return _a46_render_horizon_compliance_report.render_horizon_compliance_report(payload, facade=sys.modules[__name__])


__all__ = ["build_horizon_compliance_report", "render_horizon_compliance_report"]
