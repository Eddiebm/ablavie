#!/usr/bin/env python3
"""Syntax-check all project Python sources (compile-only). Exit 1 on failure."""

from __future__ import annotations

import py_compile
import sys
from pathlib import Path


def _py_files(root: Path) -> list[Path]:
    out: list[Path] = []
    for pattern in ("*.py",):
        out.extend(root.glob(pattern))
    for sub in ("ai_ceo", "tests", "scripts"):
        d = root / sub
        if d.is_dir():
            out.extend(p for p in d.rglob("*.py") if "__pycache__" not in p.parts)
    return sorted(set(out))


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    errors: list[tuple[Path, BaseException]] = []
    for path in _py_files(root):
        try:
            py_compile.compile(str(path), doraise=True)
        except py_compile.PyCompileError as e:
            errors.append((path, e))
    if errors:
        for path, err in errors:
            print(f"FAIL {path}: {err}", file=sys.stderr)
        return 1
    print(f"OK: {len(_py_files(root))} files compiled")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
