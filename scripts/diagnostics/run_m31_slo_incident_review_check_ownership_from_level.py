from __future__ import annotations


def _ownership_from_level(level: str, *, facade: object = None) -> str:
    lv = str(level or "").strip().lower()
    if lv == "incident":
        return "primary_and_secondary_oncall"
    if lv == "watch":
        return "primary_oncall"
    return "none"
