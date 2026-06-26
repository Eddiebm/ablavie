# AI CEO

Local-first Python toolkit and CLI: configurable LLM **routing** (Claude / OpenAI-style providers in config), **tiered SQLite memory** (hot / warm / cold, PARA-oriented), **agent registration**, and **skill health** checks.

## Quick start (from source)

```bash
pip install -e .
pip install -e ".[dev]"   # optional: pytest, etc. (see pyproject.toml)
ai-ceo --help
ai-ceo setup              # writes ~/.ai-ceo/config.json
```

## Documentation

- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** — Architecture, shipped vs roadmap, business notes
- **[CHANGELOG.md](CHANGELOG.md)** — What 1.0.0 includes vs future work
- **[RELEASE_SUMMARY.md](RELEASE_SUMMARY.md)** — Release-oriented shipped/planned tables
- **[PREFLIGHT_CHECKLIST.md](PREFLIGHT_CHECKLIST.md)** — Pre-release checks

## Honest scope

- **`ai-ceo run`** and **`ai-ceo dashboard`** are placeholders until wired to backends.
- **PyPI** install (`pip install ai-ceo`) applies only **after** you publish the package.
- **Docker, GitHub Actions, WebSocket dashboard, Ralph loops, Gemini** — not in this repo yet; see CHANGELOG “Roadmap”.

## Development

```bash
python scripts/verify.py
pytest tests/ -v
```

## License

[MIT](LICENSE)
