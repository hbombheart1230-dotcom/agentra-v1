"""evaluation_lens_report: ``_metric_avg`` body (moved verbatim from ``evaluation_lens_report``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Mapping


def _metric_avg(metric: Mapping[str, Any], *, facade: Any) -> str:
    data = facade._as_dict(metric)
    if int(data.get("count") or 0) <= 0:
        return "-"
    return str(data.get("average_return_pct"))
