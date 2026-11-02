"""Pure AST statement-identity predicate owner for the target-tree audit."""
from __future__ import annotations

from typing import Any


def _has_statement(statements: list[Any], source: str, *, facade: Any) -> bool:
    expected = facade.ast.dump(facade.ast.parse(source).body[0])
    return any(facade.ast.dump(statement) == expected for statement in statements)
