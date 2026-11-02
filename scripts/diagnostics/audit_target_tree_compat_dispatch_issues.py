"""Pure AST dispatch audit owner."""
from __future__ import annotations

from typing import Any


def _dispatch_issues(tree: Any, module: str, *, bulk: bool, facade: Any) -> list[str]:
    """Check executable dispatch and ABI aliasing, not merely literal targets."""
    condition = facade.ast.dump(facade.ast.parse("__name__ == '__main__'", mode="eval").body)
    guards = [node for node in tree.body if isinstance(node, facade.ast.If)
              and facade.ast.dump(node.test) == condition]
    if len(guards) != 1:
        return ["exactly one top-level __main__ guard required"]
    guard = guards[0]
    if bulk:
        main = f"_runpy.run_module({module!r}, run_name='__main__')"
        alias = f"_sys.modules[__name__] = _importlib.import_module({module!r})"
    else:
        main = "raise SystemExit(_impl.main())"
        alias = "_sys.modules[__name__] = _impl"
    issues = []
    if not facade._has_statement(guard.body, main):
        issues.append("executable __main__ dispatch missing or invalid")
    if not facade._has_statement(guard.orelse, alias):
        issues.append("module-object ABI alias missing or invalid")
    if not bulk and not facade._has_statement(
        tree.body, f"_impl = _importlib.import_module({module!r})"
    ):
        issues.append("example implementation binding missing or invalid")
    return issues
