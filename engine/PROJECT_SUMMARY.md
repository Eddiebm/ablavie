# AI CEO - Project Summary

## What we built

An open-source Python foundation for a local “AI CEO” workflow: CLI, configurable LLM routing, tiered memory, agent registration, and skill health—without requiring a Node/npm stack for core usage.

## What's shipped vs roadmap

| Shipped today | Roadmap (not implemented here) |
|---------------|-------------------------------|
| `LLMRouter` (Claude/OpenAI-style config, priority, health) | Additional providers (e.g. Gemini), live LLM calls from `ai-ceo run` |
| `TieredMemory` + PARA-oriented storage | Ralph-style coding loops |
| `SkillRegistry` health | Full monitoring dashboard UI, circuit breakers |
| `HeartbeatMonitor` + `AgentTask` persistence | Sandboxed execution for third-party skills |
| CLI (`setup`, `status`, `doctor`, `skill`, …) | Real `dashboard` server, Docker, GitHub Actions |

See [CHANGELOG.md](CHANGELOG.md) for version-scoped detail.

## Key improvements over Felix (directional)

These rows describe **design intent**; only the middle column reflects what exists **today** where noted.

| Felix problem | Our direction / current code |
|---------------|------------------------------|
| Long manual setup | Interactive wizard → `~/.ai-ceo/config.json` (implemented) |
| Single-vendor lock-in | Multi-provider **routing** in code; you supply keys (implemented) |
| Fragile JS/npm stacks for core flows | Python-first CLI and libraries (implemented) |
| Silent skill issues | **Registry** health checks (`SkillStatus`) (implemented); live dashboard TBD |
| Context bloat | Tiered memory + decay + context window helper (implemented); Ralph-style loops TBD |

## Architecture

The codebase is organized in layers under the `ai_ceo` package:

| Layer | Location | Role |
|-------|----------|------|
| **CLI** | `ai_ceo/cli.py` | Click + Rich: `setup`, `status`, `run`, `doctor`, `skill`, `dashboard` |
| **Routing** | `ai_ceo/core/llm_router.py` | Priority-ordered providers, health-aware selection, complexity-aware picks |
| **Memory** | `ai_ceo/memory/tiered_memory.py` | SQLite + FTS5; hot / warm / cold tiers; decay; PARA-oriented categories |
| **Agents** | `ai_ceo/agents/orchestrator.py` | `HeartbeatMonitor`, `AgentTask` registration (SQLite-backed) |
| **Skills** | `ai_ceo/skills/registry.py` | `SkillRegistry` and per-skill health (`SkillStatus`) |
| **Tooling** | `scripts/` | `setup_wizard.py` (writes `~/.ai-ceo/config.json`), `verify.py` (syntax preflight) |
| **Tests** | `tests/` | Pytest for router, memory, monitor, registry |

**Configuration:** runtime settings live in `~/.ai-ceo/config.json` (memory directory, provider, API keys). Tiered memory defaults to `memory.db` under the configured memory directory.

**Compatibility:** root `tiered_memory.py` re-exports the package module for older import paths.

```text
User / automation
       │
       ▼
  ai-ceo CLI ──► config (~/.ai-ceo)
       │
       ├──► LLMRouter (providers + health)
       ├──► TieredMemory (SQLite / FTS)
       ├──► SkillRegistry (health)
       └──► HeartbeatMonitor (agents)
```

## Business model

| Tier | Price | Status |
|------|-------|--------|
| Core | Free (open source) | Available as this repository |
| Cloud | $29/mo (managed) | Not offered until a managed product exists |
| Enterprise | Custom | Not offered until sales/process exists |

## Next steps

1. Push to GitHub
2. Configure PyPI trusted publisher (if publishing)
3. Tag v1.0.0 when ready
4. Monitor issues

**Status:** Core library and CLI are usable from source; commercial tiers and PyPI are optional follow-ups—see [RELEASE_SUMMARY.md](RELEASE_SUMMARY.md).
