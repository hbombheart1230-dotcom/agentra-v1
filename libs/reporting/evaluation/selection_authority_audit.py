from __future__ import annotations

from collections import Counter
from typing import Any, Mapping, Sequence
import sys
from . import selection_authority_audit_mapping as _a48_mapping
from . import selection_authority_audit_symbol as _a48_symbol
from . import selection_authority_audit_changed as _a48_changed
from . import selection_authority_audit_build_selection_authority_audit as _a48_build_selection_authority_audit
from . import selection_authority_audit_render_selection_authority_audit as _a48_render_selection_authority_audit


def _mapping(value: Any) -> Mapping[str, Any]:
    return _a48_mapping._mapping(value, facade=sys.modules[__name__])


def _symbol(value: Any) -> str:
    return _a48_symbol._symbol(value, facade=sys.modules[__name__])


def _changed(a: str, b: str) -> bool | None:
    return _a48_changed._changed(a, b, facade=sys.modules[__name__])


def build_selection_authority_audit(
    models: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    return _a48_build_selection_authority_audit.build_selection_authority_audit(models, facade=sys.modules[__name__])


def render_selection_authority_audit(payload: Mapping[str, Any]) -> str:
    return _a48_render_selection_authority_audit.render_selection_authority_audit(payload, facade=sys.modules[__name__])


__all__ = ["build_selection_authority_audit", "render_selection_authority_audit"]
