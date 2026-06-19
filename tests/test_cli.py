"""Tests for the gitcollect CLI."""

import json

from gitcollect.cli import main


def _write(tmp_path, content):
    p = tmp_path / "sample.txt"
    p.write_text(content, encoding="utf-8")
    return str(p)


def test_clean_file_returns_zero(tmp_path, capsys):
    path = _write(tmp_path, "def add(a, b):\n    return a + b\n")
    assert main([path]) == 0
    assert "No findings" in capsys.readouterr().out


def test_finding_returns_one(tmp_path):
    path = _write(tmp_path, 'password = "supersecret"\n')
    assert main([path]) == 1


def test_json_output_is_valid(tmp_path, capsys):
    path = _write(tmp_path, 'password = "supersecret"\n')
    rc = main(["--json", path])
    data = json.loads(capsys.readouterr().out)
    assert rc == 1
    assert data["total"] == 1
    assert data["findings"][0]["rule_id"] == "generic-secret-assignment"


def test_severity_threshold_filters(tmp_path, capsys):
    path = _write(tmp_path, 'password = "supersecret"\n')
    rc = main(["--json", "--severity-threshold", "high", path])
    data = json.loads(capsys.readouterr().out)
    assert data["total"] == 0
    assert rc == 0


def test_scans_directory(tmp_path):
    (tmp_path / "a.txt").write_text('password = "supersecret"\n', encoding="utf-8")
    (tmp_path / "b.txt").write_text("clean code\n", encoding="utf-8")
    assert main([str(tmp_path)]) == 1


def test_handles_crlf_line_endings(tmp_path):
    path = _write(tmp_path, 'clean line\r\npassword = "supersecret"\r\n')
    assert main([path]) == 1
