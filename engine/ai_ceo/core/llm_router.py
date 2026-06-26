"""
Model-agnostic LLM routing with health-aware fallback.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class ModelCapability:
    """Capabilities and quality hints for a concrete model."""

    name: str
    reliability_score: float
    supports_vision: bool = True
    supports_tools: bool = True


@dataclass(frozen=True)
class ProviderBinding:
    """Resolved provider for a request."""

    provider_key: str
    model: str
    api_key: str
    capabilities: ModelCapability


def _capability_for(provider_key: str, model: str) -> ModelCapability:
    key = provider_key.lower()
    if key == "claude":
        return ModelCapability(
            name=model,
            reliability_score=0.95,
            supports_vision=True,
            supports_tools=True,
        )
    if key == "openai":
        return ModelCapability(
            name=model,
            reliability_score=0.88,
            supports_vision=True,
            supports_tools=True,
        )
    return ModelCapability(
        name=model,
        reliability_score=0.7,
        supports_vision=False,
        supports_tools=False,
    )


class LLMRouter:
    """Select a provider/model from config, honoring priority and health."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.health_status: Dict[str, bool] = {
            k: True for k in config.get("providers", {})
        }

    def _bind(self, provider_key: str) -> ProviderBinding:
        prov = self.config["providers"][provider_key]
        model = prov["model"]
        cap = _capability_for(provider_key, model)
        return ProviderBinding(
            provider_key=provider_key,
            model=model,
            api_key=prov.get("api_key", ""),
            capabilities=cap,
        )

    def select_provider(
        self,
        complexity: str,
        required_capabilities: Optional[List[str]] = None,
    ) -> ProviderBinding:
        required = required_capabilities or []
        need_vision = "vision" in required
        need_tools = "tools" in required

        priority: List[str] = list(self.config.get("priority", []))

        def eligible(key: str) -> bool:
            if not self.health_status.get(key, False):
                return False
            prov = self.config["providers"][key]
            cap = _capability_for(key, prov["model"])
            if need_vision and not cap.supports_vision:
                return False
            if need_tools and not cap.supports_tools:
                return False
            return True

        available = [k for k in priority if eligible(k)]

        if not available:
            raise RuntimeError("No healthy provider matches the request")

        if complexity == "critical":
            best = max(
                available,
                key=lambda k: _capability_for(
                    k, self.config["providers"][k]["model"]
                ).reliability_score,
            )
            return self._bind(best)

        # advisory / standard / supervised: first healthy in priority
        for key in priority:
            if eligible(key):
                return self._bind(key)

        raise RuntimeError("No healthy provider matches the request")
