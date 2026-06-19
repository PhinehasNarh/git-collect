"""Command line interface for gitcollect."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from gitcollect import __version__
from gitcollect.scanner import Finding, scan_text, severity_rank


def _scan_path(path: Path) -> list[Finding]:
    """Scan a single file and return findings (sorted, worst first)."""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        print(f"error: could not read {path}: {exc}", file=sys.stderr)
        return []
    return sorted(
        scan_text(text), key=lambda f: (severity_rank(f.severity), f.line), reverse=True
    )


def _print_text(path: Path, findings: list[Finding]) -> None:
    for f in findings:
        print(f"{path}:{f.line}: [{f.severity}] {f.label} ({f.rule_id})")


def main(argv: list[str] | None = None) -> int:
    """Entry point. Returns a non-zero exit code when findings are present."""
    parser = argparse.ArgumentParser(
        prog="gitcollect",
        description="Scan files for credential and hygiene issues.",
    )
    parser.add_argument("paths", nargs="+", help="Files to scan.")
    parser.add_argument("--json", action="store_true", help="Emit findings as JSON.")
    parser.add_argument("--version", action="version", version=f"gitcollect {__version__}")
    args = parser.parse_args(argv)

    results: dict[str, list[Finding]] = {}
    for raw in args.paths:
        path = Path(raw)
        results[str(path)] = _scan_path(path)

    total = sum(len(v) for v in results.values())

    if args.json:
        payload = {
            "total": total,
            "findings": [
                {
                    "path": p,
                    "line": f.line,
                    "rule_id": f.rule_id,
                    "label": f.label,
                    "severity": f.severity,
                    "snippet": f.snippet,
                }
                for p, fs in results.items()
                for f in fs
            ],
        }
        print(json.dumps(payload, indent=2))
        return 1 if total else 0

    for p, fs in results.items():
        _print_text(Path(p), fs)
    if total:
        print(f"\n{total} finding(s) detected.", file=sys.stderr)
        return 1
    print("No findings.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
