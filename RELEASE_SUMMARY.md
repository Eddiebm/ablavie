# AI CEO - Release Summary

**Date**: 2026-04-06  
**Version**: 1.0.0  

## What this release is

An open-source Python toolkit and CLI for local-first configuration, multi-provider LLM routing (when you wire API keys), tiered memory, agent registration, and skill health checks. Suitable for development and self-hosted use from source.

## Shipped in this repository

| Component | Notes |
|-----------|--------|
| LLM Router | Priority + health-aware selection for configured providers (see `ai_ceo/core/llm_router.py`) |
| Three-tier memory | SQLite + FTS5; hot / warm / cold; PARA helpers (`ai_ceo/memory/`) |
| Heartbeat / agents | Agent registration in SQLite (`ai_ceo/agents/orchestrator.py`) |
| Skill registry | Health enums and checks (`ai_ceo/skills/registry.py`) |
| Setup wizard | Writes `~/.ai-ceo/config.json` |
| CLI | `ai-ceo` commands; `run` / `dashboard` are placeholders until wired |
| Tests | Pytest (`tests/test_core.py`) |
| Tooling | `scripts/verify.py` syntax check |

## Planned / not in this repo yet

| Area | Notes |
|------|--------|
| Ralph-style agent loops | Roadmap |
| Full circuit breakers | Roadmap (monitor is registration-focused today) |
| Web dashboard + WebSockets | Roadmap |
| Docker / compose | Roadmap |
| GitHub Actions | Roadmap |
| `pip install ai-ceo` from PyPI | Requires publishing the package |
| One-line curl installer | Roadmap |

## Deployment options (from source)

1. **Development install**: `pip install -e ".[dev]"` from a clone (requires compatible Python; see `pyproject.toml`).
2. **PyPI**: `pip install ai-ceo` only **after** the project is published under that name.
3. **Docker / curl one-liner**: Not provided in this repository yet.

## Status

The codebase is usable locally and testable with pytest. Publishing to PyPI, adding CI, and container images are follow-up steps—not implied by this release summary.
