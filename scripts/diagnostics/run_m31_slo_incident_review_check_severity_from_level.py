from __future__ import annotations


def _severity_from_level(level: str, *, facade: object = None) -> str:
    lv = str(level or "").strip().lower()
    if lv == "incident":
        return "SEV-1"
    if lv == "watch":
        return "SEV-2"
    return "SEV-3"
