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


def _iter_files(path: Path):
    """Yield files under ``path`` recursively, or ``path`` itself."""
    if path.is_dir():
        for child in sorted(path.rglob("*")):
            if child.is_file():
                yield child
    else:
        yield path


def main(argv: list[str] | None = None) -> int:
    """Entry point. Returns a non-zero exit code when findings are present."""
    parser = argparse.ArgumentParser(
        prog="gitcollect",
        description="Scan files for credential and hygiene issues.",
    )
    parser.add_argument("paths", nargs="+", help="Files to scan.")
    parser.add_argument("--json", action="store_true", help="Emit findings as JSON.")
    parser.add_argument("--sarif", action="store_true", help="Emit findings as SARIF.")
    parser.add_argument(
        "--severity-threshold",
        choices=["low", "medium", "high"],
        default="low",
        help="Only report findings at or above this severity.",
    )
    parser.add_argument("--version", action="version", version=f"gitcollect {__version__}")
    args = parser.parse_args(argv)

    results: dict[str, list[Finding]] = {}
    for raw in args.paths:
        for target in _iter_files(Path(raw)):
            results[str(target)] = _scan_path(target)

    threshold = severity_rank(args.severity_threshold)
    results = {
        p: [f for f in fs if severity_rank(f.severity) >= threshold]
        for p, fs in results.items()
    }

    total = sum(len(v) for v in results.values())

    if args.sarif:
        levels = {"high": "error", "medium": "warning", "low": "note"}
        sarif = {
            "version": "2.1.0",
            "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
            "runs": [
                {
                    "tool": {"driver": {"name": "gitcollect"}},
                    "results": [
                        {
                            "ruleId": f.rule_id,
                            "level": levels[f.severity],
                            "message": {"text": f.label},
                            "locations": [
                                {
                                    "physicalLocation": {
                                        "artifactLocation": {"uri": p},
                                        "region": {"startLine": f.line},
                                    }
                                }
                            ],
                        }
                        for p, fs in results.items()
                        for f in fs
                    ],
                }
            ],
        }
        print(json.dumps(sarif, indent=2))
        return 1 if total else 0

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
