"""Timing benchmark for the scanner.

Run: python benchmarks/bench_scanner.py
"""

import time

from gitcollect.scanner import scan_text


def run(lines: int = 10000) -> float:
    half = lines // 2
    sample = ('password = "supersecret"\n' * half) + ("clean line\n" * half)
    start = time.perf_counter()
    scan_text(sample)
    return time.perf_counter() - start


if __name__ == "__main__":
    print(f"scanned sample in {run():.3f}s")
