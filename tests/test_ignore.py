"""Tests for ignore-pattern matching."""

from gitcollect.ignore import is_ignored, load_patterns


def test_load_skips_comments_and_blanks(tmp_path):
    f = tmp_path / ".gitcollectignore"
    f.write_text("# comment\n\n*.lock\nvendor/*\n", encoding="utf-8")
    assert load_patterns(f) == ["*.lock", "vendor/*"]


def test_load_missing_file_returns_empty(tmp_path):
    assert load_patterns(tmp_path / "nope") == []


def test_is_ignored_matches_glob():
    assert is_ignored("poetry.lock", ["*.lock"])
    assert not is_ignored("main.py", ["*.lock"])
