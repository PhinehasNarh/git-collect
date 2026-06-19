"""Tests for the gitcollect scanner."""

from gitcollect.scanner import scan_text, severity_rank


def test_clean_text_has_no_findings():
    assert scan_text("def add(a, b):\n    return a + b\n") == []


def test_detects_aws_access_key():
    findings = scan_text("aws_key = AKIAIOSFODNN7EXAMPLE")
    assert any(f.rule_id == "aws-access-key" for f in findings)


def test_detects_hardcoded_password():
    findings = scan_text('password = "hunter2secret"')
    assert any(f.rule_id == "generic-secret-assignment" for f in findings)


def test_detects_private_key_block():
    findings = scan_text("-----BEGIN RSA PRIVATE KEY-----")
    assert any(f.rule_id == "private-key-block" for f in findings)


def test_reports_line_numbers():
    text = "line one\npassword = \"supersecret\"\nline three"
    findings = scan_text(text)
    assert findings
    assert findings[0].line == 2


def test_severity_rank_orders_high_above_low():
    assert severity_rank("high") > severity_rank("medium") > severity_rank("low")
