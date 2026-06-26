"""
Skill registry with lightweight health checks.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict


class SkillStatus(str, Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNAVAILABLE = "unavailable"


@dataclass(frozen=True)
class SkillHealth:
    status: SkillStatus
    detail: str = ""


class SkillRegistry:
    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def check_all_health(self) -> Dict[str, SkillHealth]:
        """Return health for each configured skill surface."""
        out: Dict[str, SkillHealth] = {}
        if "coding_config" in self.config:
            out["coding"] = SkillHealth(status=SkillStatus.HEALTHY)
        if "email_config" in self.config:
            out["email"] = SkillHealth(status=SkillStatus.HEALTHY)
        return out
