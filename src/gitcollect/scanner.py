"""Core scanning logic.

The scanner looks for common credential and hygiene problems in text. It is
intentionally dependency-free so it can run anywhere, including inside a
restricted CI runner.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

# Each rule is (id, human label, severity, compiled pattern).
_RULES: list[tuple[str, str, str, re.Pattern[str]]] = [
    (
        "aws-access-key",
        "AWS access key id",
        "high",
        re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    ),
    (
        "github-pat",
        "GitHub personal access token",
        "high",
        re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36}\b|\bgithub_pat_[A-Za-z0-9_]{22,}\b"),
    ),
    (
        "slack-webhook",
        "Slack incoming webhook URL",
        "medium",
        re.compile(r"https://hooks\.slack\.com/services/[A-Za-z0-9/]+"),
    ),
    (
        "generic-secret-assignment",
        "Hardcoded secret assignment",
        "medium",
        re.compile(
            r"(?i)\b(secret|password|passwd|token|api[_-]?key)\b\s*[:=]\s*['\"][^'\"]{6,}['\"]"
        ),
    ),
    (
        "private-key-block",
        "Private key material",
        "high",
        re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA |PGP )?PRIVATE KEY-----"),
    ),
    (
        "jwt-token",
        "JSON Web Token",
        "low",
        re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b"),
    ),
]


@dataclass(frozen=True)
class Finding:
    """A single hygiene issue located in scanned text."""

    rule_id: str
    label: str
    severity: str
    line: int
    snippet: str


def scan_text(text: str) -> list[Finding]:
    """Scan ``text`` line by line and return any findings.

    Args:
        text: Raw text to inspect.

    Returns:
        A list of :class:`Finding` objects, ordered by line number.
    """
    findings: list[Finding] = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        for rule_id, label, severity, pattern in _RULES:
            if pattern.search(line):
                findings.append(
                    Finding(
                        rule_id=rule_id,
                        label=label,
                        severity=severity,
                        line=line_no,
                        snippet=line.strip()[:120],
                    )
                )
    return findings


def severity_rank(severity: str) -> int:
    """Return a sortable rank for a severity string (higher is worse)."""
    return {"low": 1, "medium": 2, "high": 3}.get(severity, 0)


def shannon_entropy(value: str) -> float:
    """Return the Shannon entropy (bits per character) of ``value``."""
    if not value:
        return 0.0
    from collections import Counter
    from math import log2

    length = len(value)
    return -sum((n / length) * log2(n / length) for n in Counter(value).values())


def find_high_entropy_tokens(
    text: str, min_length: int = 20, threshold: float = 4.0
) -> list[str]:
    """Return whitespace-delimited tokens that look like high-entropy secrets."""
    return [
        token
        for token in text.split()
        if len(token) >= min_length and shannon_entropy(token) >= threshold
    ]
