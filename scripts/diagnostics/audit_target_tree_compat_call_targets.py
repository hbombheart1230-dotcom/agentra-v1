"""Pure AST call-target inspection owner for the target-tree audit."""
from __future__ import annotations

from typing import Any


def _call_targets(tree: Any, owner: str, method: str, *, facade: Any) -> list[str]:
    """Return literal module names passed to one documented wrapper API."""
    out: list[str] = []
    for node in facade.ast.walk(tree):
        if not isinstance(node, facade.ast.Call) or not isinstance(node.func, facade.ast.Attribute):
            continue
        if not isinstance(node.func.value, facade.ast.Name):
            continue
        if node.func.value.id != owner or node.func.attr != method or not node.args:
            continue
        if isinstance(node.args[0], facade.ast.Constant) and isinstance(node.args[0].value, str):
            out.append(node.args[0].value)
    return out
