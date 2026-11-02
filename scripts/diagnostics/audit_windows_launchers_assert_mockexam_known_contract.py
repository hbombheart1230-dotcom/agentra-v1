"""Pure frozen MockExam contract projection owner."""
from __future__ import annotations

from typing import Any


def assert_mockexam_known_contract(result: dict, *, facade: Any) -> None:
    """Assert frozen source names only; never assert live cleanup success."""
    contract = result["mockexam_task_contract"]
    if (contract["status"] != "PROVEN"
            or set(contract["registered"]) != facade._FROZEN_REGISTERED
            or set(contract["unregistered"]) != facade._FROZEN_UNREGISTERED):
        result["issues"].append("MockExam frozen task-name contract not proven or changed")
    result["ok"] = not result["issues"]
