"""Tests for baseline suppression."""

import json

from gitcollect.baseline import fingerprint, is_suppressed, load_baseline


def test_fingerprint_is_stable():
    assert fingerprint("aws-access-key", "a.py", 3) == "aws-access-key:a.py:3"


def test_load_baseline_reads_suppressed(tmp_path):
    f = tmp_path / "baseline.json"
    f.write_text(json.dumps({"suppressed": ["r:a.py:1"]}), encoding="utf-8")
    assert load_baseline(f) == {"r:a.py:1"}


def test_is_suppressed_checks_membership():
    bl = {"aws-access-key:a.py:3"}
    assert is_suppressed("aws-access-key", "a.py", 3, bl)
    assert not is_suppressed("aws-access-key", "a.py", 4, bl)
