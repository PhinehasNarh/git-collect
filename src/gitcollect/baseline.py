"""Baseline/allowlist support: suppress known-accepted findings."""

from __future__ import annotations

import json
from pathlib import Path


def fingerprint(rule_id: str, path: str, line: int) -> str:
    """Stable identifier for a finding, used to match against a baseline."""
    return f"{rule_id}:{path}:{line}"


def load_baseline(path: Path) -> set[str]:
    """Load suppressed-finding fingerprints from a JSON baseline file."""
    if not path.is_file():
        return set()
    data = json.loads(path.read_text(encoding="utf-8"))
    return set(data.get("suppressed", []))


def is_suppressed(rule_id: str, path: str, line: int, baseline: set[str]) -> bool:
    """Return True if the finding is listed in the baseline."""
    return fingerprint(rule_id, path, line) in baseline
