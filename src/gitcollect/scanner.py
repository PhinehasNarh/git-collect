"""Core scanning logic.

The scanner looks for common credential and hygiene problems in text. It is
intentionally dependency-free so it can run anywhere, including inside a
restricted CI runner.
"""

from __future__ import annotations

import re
from collections.abc import Iterable
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


# PEM private key block delimiters. We track these as state so that an
# unterminated block does not make the scanner carry state forever (see #38).
_PEM_BEGIN_RE = re.compile(r"-----BEGIN (?:[A-Z0-9 ]+ )?PRIVATE KEY-----")
_PEM_END_RE = re.compile(r"-----END (?:[A-Z0-9 ]+ )?PRIVATE KEY-----")

# A private key block that spans more than this many lines without an END is
# treated as malformed, reported, and abandoned.
_MAX_KEY_SPAN = 200


def scan_lines(lines: Iterable[str], *, max_key_span: int = _MAX_KEY_SPAN) -> list[Finding]:
    """Scan an iterable of lines and return any findings.

    This is the streaming core. Only the current line plus a little PEM block
    state is held at once, so it stays within bounded memory on large inputs.
    :func:`scan_text` is a thin wrapper over it.

    In addition to the per-line rules, this tracks
    ``-----BEGIN ... PRIVATE KEY-----`` blocks. A block that is never closed,
    or that runs past ``max_key_span`` lines, yields a medium-severity
    ``malformed-key-block`` finding, since a truncated private key paste is
    still worth investigating.
    """
    findings: list[Finding] = []
    in_key = False
    key_start = 0

    for line_no, line in enumerate(lines, start=1):
        if not in_key and _PEM_BEGIN_RE.search(line):
            in_key = True
            key_start = line_no
        elif in_key:
            if _PEM_END_RE.search(line):
                in_key = False
            elif line_no - key_start >= max_key_span:
                findings.append(
                    Finding(
                        rule_id="malformed-key-block",
                        label="Unterminated private key block",
                        severity="medium",
                        line=key_start,
                        snippet="private key block exceeded max span without END",
                    )
                )
                in_key = False

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

    if in_key:
        findings.append(
            Finding(
                rule_id="malformed-key-block",
                label="Unterminated private key block",
                severity="medium",
                line=key_start,
                snippet="private key block opened but never closed",
            )
        )

    return findings


def scan_text(text: str) -> list[Finding]:
    """Scan ``text`` and return any findings.

    Thin wrapper over :func:`scan_lines` for the common in-memory case.

    Args:
        text: Raw text to inspect.

    Returns:
        A list of :class:`Finding` objects, ordered by line number.
    """
    return scan_lines(text.splitlines())


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
