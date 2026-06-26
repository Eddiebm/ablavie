"""
Agent orchestration: heartbeats, registration, task metadata.
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional


class AutonomyLevel(str, Enum):
    ADVISORY = "advisory"
    SUPERVISED = "supervised"
    AUTONOMOUS = "autonomous"


@dataclass
class AgentTask:
    id: str
    name: str
    skill: str
    prompt: str
    autonomy: AutonomyLevel


class HeartbeatMonitor:
    """Registers agents and persists minimal metadata for monitoring."""

    def __init__(self, db_path: str):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS agents (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    skill TEXT NOT NULL,
                    prompt TEXT NOT NULL,
                    autonomy TEXT NOT NULL,
                    last_heartbeat TEXT
                )
                """
            )
            conn.commit()

    def register_agent(self, task: AgentTask) -> str:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO agents (id, name, skill, prompt, autonomy)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    task.id,
                    task.name,
                    task.skill,
                    task.prompt,
                    task.autonomy.value,
                ),
            )
            conn.commit()
        return task.id
