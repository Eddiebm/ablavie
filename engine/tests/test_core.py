"""
Test suite for AI CEO core components
"""

import tempfile
from pathlib import Path

import pytest

from ai_ceo.agents.orchestrator import AgentTask, AutonomyLevel, HeartbeatMonitor
from ai_ceo.core.llm_router import LLMRouter
from ai_ceo.memory.tiered_memory import TieredMemory
from ai_ceo.skills.registry import SkillRegistry, SkillStatus


class TestLLMRouter:
    """Test model-agnostic LLM routing"""

    @pytest.fixture
    def router_config(self):
        return {
            "providers": {
                "claude": {"api_key": "test-key", "model": "claude-sonnet-4"},
                "openai": {"api_key": "test-key", "model": "gpt-4o"},
            },
            "priority": ["claude", "openai"],
        }

    def test_provider_selection_by_complexity(self, router_config):
        router = LLMRouter(router_config)
        router.health_status = {"claude": True, "openai": True}
        provider = router.select_provider("critical", ["vision", "tools"])
        assert provider.capabilities.reliability_score >= 0.9

    def test_graceful_fallback(self, router_config):
        router = LLMRouter(router_config)
        router.health_status = {"claude": False, "openai": True}
        provider = router.select_provider("standard")
        assert provider.capabilities.name.startswith("gpt")


class TestTieredMemory:
    """Test three-tier memory with PARA"""

    @pytest.fixture
    def memory(self):
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "test_memory.db"
            mem = TieredMemory(str(db_path))
            yield mem

    def test_store_and_retrieve(self, memory):
        entry_id = memory.store("Test content", "project", "test")
        assert entry_id is not None
        results = memory.retrieve(query="Test")
        assert len(results) > 0
        assert results[0].content == "Test content"

    def test_tier_promotion_on_access(self, memory):
        entry_id = memory.store("Cold content", "resource", "test", tier="cold")
        # Must touch the row (FTS or unfiltered retrieve) so promotion runs
        memory.retrieve(query="Cold")
        warm_results = memory.retrieve(tier="warm")
        assert any(r.id == entry_id for r in warm_results)


class TestHeartbeatMonitor:
    """Test heartbeat monitoring and circuit breakers"""

    @pytest.fixture
    def monitor(self):
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "agents.db"
            mon = HeartbeatMonitor(str(db_path))
            yield mon

    def test_agent_registration(self, monitor):
        task = AgentTask(
            id="test-1",
            name="Test Agent",
            skill="coding",
            prompt="Test",
            autonomy=AutonomyLevel.SUPERVISED,
        )
        agent_id = monitor.register_agent(task)
        assert agent_id == "test-1"


class TestSkillRegistry:
    """Test skill system with health checks"""

    def test_skill_health_check(self):
        config = {
            "coding_config": {},
            "email_config": {},
        }
        registry = SkillRegistry(config)
        health = registry.check_all_health()
        assert health["coding"].status == SkillStatus.HEALTHY
