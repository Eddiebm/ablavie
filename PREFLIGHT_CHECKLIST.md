# Pre-Flight Checklist - AI CEO Release

## Code Quality

- [ ] All Python files pass syntax check
- [ ] No `src` imports remaining
- [ ] Code formatted with Black
- [ ] No hardcoded secrets

## Testing

- [ ] All tests pass
- [ ] Test coverage meets team target (e.g. **> 80%** on `ai_ceo/` when enforced—currently a small suite)
- [ ] Type checking passes (`mypy ai_ceo/`)

## Documentation

- [ ] README.md reflects current capabilities (no overstated features)
- [ ] CHANGELOG.md matches what is released vs roadmap
- [ ] Marketing docs (e.g. `RELEASE_SUMMARY.md`) aligned with shipped code

## Release

- [ ] Version bumped in all files
- [ ] Git tag created
- [ ] GitHub Release drafted

## Commands

```bash
python scripts/verify.py
pytest tests/ -v --cov=ai_ceo
python -m build
```

Install tooling as needed, for example:

```bash
pip install -e ".[dev]"
```

Coverage requires `pytest-cov`; `python -m build` requires the `build` package (`pip install build`).
