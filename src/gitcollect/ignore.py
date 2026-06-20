"""Path ignore matching for gitcollect (.gitcollectignore support)."""

from __future__ import annotations

import fnmatch
from pathlib import Path


def load_patterns(path: Path) -> list[str]:
    """Read ignore globs from a .gitcollectignore file (one per line)."""
    if not path.is_file():
        return []
    lines = path.read_text(encoding="utf-8").splitlines()
    return [s.strip() for s in lines if s.strip() and not s.strip().startswith("#")]


def is_ignored(target: str, patterns: list[str]) -> bool:
    """Return True if ``target`` matches any ignore glob."""
    return any(fnmatch.fnmatch(target, pat) for pat in patterns)
