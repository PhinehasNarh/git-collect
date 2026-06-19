"""Command line interface for gitcollect."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from gitcollect import __version__
from gitcollect.scanner import scan_text, severity_rank


def _scan_path(path: Path) -> int:
    """Scan a single file and print findings. Returns the count of findings."""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        print(f"error: could not read {path}: {exc}", file=sys.stderr)
        return 0

    findings = sorted(
        scan_text(text), key=lambda f: (severity_rank(f.severity), f.line), reverse=True
    )
    for f in findings:
        print(f"{path}:{f.line}: [{f.severity}] {f.label} ({f.rule_id})")
    return len(findings)


def main(argv: list[str] | None = None) -> int:
    """Entry point. Returns a non-zero exit code when findings are present."""
    parser = argparse.ArgumentParser(
        prog="gitcollect",
        description="Scan files for credential and hygiene issues.",
    )
    parser.add_argument("paths", nargs="+", help="Files to scan.")
    parser.add_argument("--version", action="version", version=f"gitcollect {__version__}")
    args = parser.parse_args(argv)

    total = 0
    for raw in args.paths:
        total += _scan_path(Path(raw))

    if total:
        print(f"\n{total} finding(s) detected.", file=sys.stderr)
        return 1
    print("No findings.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
