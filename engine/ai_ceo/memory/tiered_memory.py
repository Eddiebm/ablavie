"""
Three-Tier Persistent Memory System
Hot (active context) → Warm (recent history) → Cold (archived knowledge)
Implements PARA method: Projects, Areas, Resources, Archives
"""

import hashlib
import json
import sqlite3
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

# Optional: use numpy to serialize embeddings when you implement semantic search
# import numpy as np


@dataclass
class MemoryEntry:
    id: str
    tier: str  # "hot", "warm", "cold"
    category: str  # "project", "area", "resource", "archive", "fact", "conversation"
    content: str
    timestamp: datetime
    last_accessed: datetime
    access_count: int
    importance_score: float  # 0-1, calculated from access patterns
    tags: List[str]
    source: str  # Which skill/agent created this
    embedding: Optional[List[float]] = None  # For semantic search

    def to_dict(self):
        return {
            **asdict(self),
            "timestamp": self.timestamp.isoformat(),
            "last_accessed": self.last_accessed.isoformat(),
        }


class TieredMemory:
    """
    Hot tier: Active context (last 24h, high access)
    Warm tier: Recent history (last 7 days, moderate access)
    Cold tier: Archived knowledge (older, rarely accessed but preserved)
    """

    HOT_DAYS = 1
    WARM_DAYS = 7
    DECAY_CHECK_INTERVAL = 3600  # Check every hour

    def __init__(self, db_path: str = "~/life/memory.db"):
        self.db_path = Path(db_path).expanduser()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        """Initialize SQLite with full-text search and vector support"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS memories (
                    id TEXT PRIMARY KEY,
                    tier TEXT NOT NULL,
                    category TEXT NOT NULL,
                    content TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    last_accessed TEXT NOT NULL,
                    access_count INTEGER DEFAULT 0,
                    importance_score REAL DEFAULT 0.5,
                    tags TEXT,
                    source TEXT,
                    embedding BLOB
                )
            """
            )

            conn.execute(
                """
                CREATE VIRTUAL TABLE IF NOT EXISTS memory_fts USING fts5(
                    content,
                    tags
                )
            """
            )

            conn.execute("CREATE INDEX IF NOT EXISTS idx_tier ON memories(tier)")
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_category ON memories(category)"
            )
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_timestamp ON memories(timestamp)"
            )
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_last_accessed ON memories(last_accessed)"
            )

            conn.commit()

    def store(
        self,
        content: str,
        category: str,
        source: str = "",
        tags: Optional[List[str]] = None,
        tier: str = "hot",
    ) -> str:
        """Store new memory entry"""
        entry_id = hashlib.md5(f"{content}{datetime.now()}".encode()).hexdigest()[:12]
        now = datetime.now()

        entry = MemoryEntry(
            id=entry_id,
            tier=tier,
            category=category,
            content=content,
            timestamp=now,
            last_accessed=now,
            access_count=1,
            importance_score=0.5,
            tags=tags or [],
            source=source,
        )

        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute(
                """
                INSERT INTO memories
                (id, tier, category, content, timestamp, last_accessed, access_count, importance_score, tags, source)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    entry.id,
                    entry.tier,
                    entry.category,
                    entry.content,
                    entry.timestamp.isoformat(),
                    entry.last_accessed.isoformat(),
                    entry.access_count,
                    entry.importance_score,
                    json.dumps(entry.tags),
                    entry.source,
                ),
            )
            rowid = cur.lastrowid

            conn.execute(
                "INSERT INTO memory_fts (rowid, content, tags) VALUES (?, ?, ?)",
                (rowid, entry.content, " ".join(entry.tags)),
            )
            conn.commit()

        return entry_id

    def retrieve(
        self,
        query: Optional[str] = None,
        category: Optional[str] = None,
        tier: Optional[str] = None,
        limit: int = 10,
        semantic: bool = False,
    ) -> List[MemoryEntry]:
        """
        Retrieve memories with automatic tier promotion on access

        If accessed from cold → warm, warm → hot (recency bump)
        """
        if semantic:
            raise NotImplementedError(
                "Semantic search requires stored embeddings and an embedder."
            )

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row

            if query:
                cursor = conn.execute(
                    """
                    SELECT m.* FROM memories m
                    JOIN memory_fts ON m.rowid = memory_fts.rowid
                    WHERE memory_fts MATCH ?
                    ORDER BY rank
                    LIMIT ?
                    """,
                    (query, limit),
                )
            else:
                sql = "SELECT * FROM memories WHERE 1=1"
                params: List[Any] = []
                if tier:
                    sql += " AND tier = ?"
                    params.append(tier)
                if category:
                    sql += " AND category = ?"
                    params.append(category)
                sql += " ORDER BY last_accessed DESC LIMIT ?"
                params.append(limit)

                cursor = conn.execute(sql, params)

            rows = cursor.fetchall()

            entries: List[MemoryEntry] = []
            for row in rows:
                entry = MemoryEntry(
                    id=row["id"],
                    tier=row["tier"],
                    category=row["category"],
                    content=row["content"],
                    timestamp=datetime.fromisoformat(row["timestamp"]),
                    last_accessed=datetime.fromisoformat(row["last_accessed"]),
                    access_count=row["access_count"],
                    importance_score=row["importance_score"],
                    tags=json.loads(row["tags"]) if row["tags"] else [],
                    source=row["source"],
                )
                entries.append(entry)

                self._bump_tier(entry.id, entry.tier)

            return entries

    def _bump_tier(self, entry_id: str, current_tier: str):
        """Promote entry to higher tier on access"""
        now = datetime.now()

        with sqlite3.connect(self.db_path) as conn:
            if current_tier == "cold":
                conn.execute(
                    """
                    UPDATE memories
                    SET tier = 'warm', last_accessed = ?, access_count = access_count + 1
                    WHERE id = ?
                    """,
                    (now.isoformat(), entry_id),
                )
            elif current_tier == "warm":
                conn.execute(
                    """
                    UPDATE memories
                    SET tier = 'hot', last_accessed = ?, access_count = access_count + 1
                    WHERE id = ?
                    """,
                    (now.isoformat(), entry_id),
                )
            else:
                conn.execute(
                    """
                    UPDATE memories
                    SET last_accessed = ?, access_count = access_count + 1
                    WHERE id = ?
                    """,
                    (now.isoformat(), entry_id),
                )
            conn.commit()

    def decay_check(self):
        """
        Background task: Move stale entries down tiers
        Hot → Warm: Not accessed in 24h
        Warm → Cold: Not accessed in 7 days
        Cold → Archive: Not accessed in 90 days (optional cleanup)
        """
        now = datetime.now()
        hot_cutoff = (now - timedelta(days=self.HOT_DAYS)).isoformat()
        warm_cutoff = (now - timedelta(days=self.WARM_DAYS)).isoformat()

        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                UPDATE memories
                SET tier = 'warm'
                WHERE tier = 'hot' AND last_accessed < ?
                """,
                (hot_cutoff,),
            )

            conn.execute(
                """
                UPDATE memories
                SET tier = 'cold'
                WHERE tier = 'warm' AND last_accessed < ?
                """,
                (warm_cutoff,),
            )

            conn.commit()

    def get_context_window(self, max_tokens: int = 8000) -> str:
        """
        Build context window for LLM from hot + relevant warm memories
        Prioritizes by importance_score and recency
        """
        hot = self.retrieve(tier="hot", limit=50)

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            warm = conn.execute(
                """
                SELECT * FROM memories
                WHERE tier = 'warm'
                ORDER BY importance_score DESC, last_accessed DESC
                LIMIT 30
                """
            ).fetchall()

        context_parts: List[str] = []

        if hot:
            context_parts.append("## Active Context (Hot Memory)")
            for entry in hot:
                context_parts.append(f"- [{entry.category}] {entry.content}")

        if warm:
            context_parts.append("\n## Recent History (Warm Memory)")
            for row in warm:
                context_parts.append(f"- [{row['category']}] {row['content']}")

        context = "\n".join(context_parts)

        if len(context) > max_tokens * 4:
            context = context[: max_tokens * 4] + "\n...[context truncated]"

        return context

    def get_stats(self) -> Dict[str, Any]:
        """Return memory system statistics"""
        with sqlite3.connect(self.db_path) as conn:
            stats: Dict[str, Any] = {}
            for tier in ["hot", "warm", "cold"]:
                count = conn.execute(
                    "SELECT COUNT(*) FROM memories WHERE tier = ?", (tier,)
                ).fetchone()[0]
                stats[tier] = count

            total = conn.execute("SELECT COUNT(*) FROM memories").fetchone()[0]
            stats["total"] = total

            categories = conn.execute(
                """
                SELECT category, COUNT(*) as count
                FROM memories
                GROUP BY category
                """
            ).fetchall()
            stats["categories"] = {row[0]: row[1] for row in categories}

            return stats


class PARAOrganizer:
    """
    PARA Method implementation: Projects, Areas, Resources, Archives
    Organizes memory into actionable structure
    """

    def __init__(self, memory: TieredMemory):
        self.memory = memory

    def create_project(self, name: str, goal: str, deadline: Optional[str] = None):
        """Create new project with automatic tracking"""
        content = f"Project: {name}\nGoal: {goal}"
        if deadline:
            content += f"\nDeadline: {deadline}"

        return self.memory.store(
            content=content,
            category="project",
            source="para_system",
            tags=["active", "project", name.lower().replace(" ", "-")],
            tier="hot",
        )

    def create_area(self, name: str, description: str, responsibility: str):
        """Create ongoing area of responsibility"""
        content = f"Area: {name}\nDescription: {description}\nResponsibility: {responsibility}"

        return self.memory.store(
            content=content,
            category="area",
            source="para_system",
            tags=["ongoing", "area", name.lower().replace(" ", "-")],
            tier="warm",
        )

    def add_resource(self, topic: str, content: str, source_url: Optional[str] = None):
        """Add reference material"""
        full_content = f"Resource: {topic}\n{content}"
        if source_url:
            full_content += f"\nSource: {source_url}"

        return self.memory.store(
            content=full_content,
            category="resource",
            source="para_system",
            tags=["reference", topic.lower().replace(" ", "-")],
            tier="cold",
        )

    def archive_project(self, project_id: str):
        """Move completed project to archives"""
        with sqlite3.connect(self.memory.db_path) as conn:
            conn.execute(
                """
                UPDATE memories
                SET category = 'archive', tier = 'cold'
                WHERE id = ? AND category = 'project'
                """,
                (project_id,),
            )
            conn.commit()

    def get_active_projects(self) -> List[MemoryEntry]:
        """Get all active projects"""
        return self.memory.retrieve(category="project", tier="hot")

    def get_dashboard(self) -> Dict[str, List[MemoryEntry]]:
        """Get PARA dashboard view"""
        return {
            "projects": self.memory.retrieve(category="project", limit=10),
            "areas": self.memory.retrieve(category="area", limit=10),
            "resources": self.memory.retrieve(category="resource", limit=5),
            "archives": self.memory.retrieve(category="archive", limit=5),
        }
