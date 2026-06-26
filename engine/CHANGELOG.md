# Changelog

## [1.0.0] - 2026-04-06

### Added

- `ai_ceo` package: CLI (`click` + `rich`) with `setup`, `status`, `run`, `dashboard`, `doctor`, and `skill` commands
- `LLMRouter` for priority-ordered providers (Claude / OpenAI in config) with health-aware selection
- Three-tier SQLite memory (hot / warm / cold) with FTS5 search, PARA-oriented categories, and `PARAOrganizer`
- `HeartbeatMonitor` and `AgentTask` registration (SQLite-backed agents table)
- `SkillRegistry` with per-skill health reporting (`SkillStatus`)
- Interactive setup wizard writing `~/.ai-ceo/config.json` (`scripts/setup_wizard.py`)
- Syntax preflight script (`scripts/verify.py`)
- Pytest suite for router, memory, monitor, and registry (`tests/`)
- Project documentation: `PROJECT_SUMMARY.md`, `PREFLIGHT_CHECKLIST.md`, `RELEASE_SUMMARY.md`

### Roadmap (not in this release)

- Additional model providers (e.g. Gemini), Ralph-style coding loops, full circuit-breaker semantics
- Web dashboard with live updates, Docker images, GitHub Actions CI
- End-to-end LLM execution in `ai-ceo run` and a real dashboard server (currently placeholders)
- Prompt-injection hardening and sandboxed skill execution for external integrations

### Security

- Setup wizard collects API keys into `~/.ai-ceo/config.json` (set restrictive file permissions where supported)
