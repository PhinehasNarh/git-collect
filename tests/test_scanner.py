"""Tests for the gitcollect scanner."""

from gitcollect.scanner import scan_lines, scan_text, severity_rank


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


def test_detects_github_pat():
    # Token assembled at runtime so no literal credential lives in the repo.
    findings = scan_text("token = ghp_" + "A" * 36)
    assert any(f.rule_id == "github-pat" for f in findings)


def test_detects_slack_webhook():
    findings = scan_text("url = https://hooks.slack.com/services/T000/B000/XXXXXXXXXXXX")
    assert any(f.rule_id == "slack-webhook" for f in findings)


def test_multiline_private_key_block_is_detected_and_not_flagged_malformed():
    pem = "\n".join(
        [
            "-----BEGIN RSA PRIVATE KEY-----",
            "MIIEowIBAAKCAQEA1234567890abcdef",
            "ghijklmnopqrstuvwxyz0987654321",
            "-----END RSA PRIVATE KEY-----",
        ]
    )
    findings = scan_text(pem)
    assert any(f.rule_id == "private-key-block" for f in findings)
    assert not any(f.rule_id == "malformed-key-block" for f in findings)


def test_unterminated_private_key_block_is_flagged():
    findings = scan_text("-----BEGIN RSA PRIVATE KEY-----\nMIIEowIBAA\nmore body")
    assert any(
        f.rule_id == "malformed-key-block" and f.severity == "medium" for f in findings
    )


def test_end_without_begin_does_not_flag_malformed():
    findings = scan_text("-----END RSA PRIVATE KEY-----\nclean code")
    assert all(f.rule_id != "malformed-key-block" for f in findings)


def test_block_past_max_span_is_flagged_and_reset():
    body = "\n".join(["-----BEGIN RSA PRIVATE KEY-----"] + ["x"] * 10)
    findings = scan_lines(body.splitlines(), max_key_span=3)
    assert any(f.rule_id == "malformed-key-block" for f in findings)


def test_scan_lines_matches_scan_text():
    text = 'password = "supersecret"\nclean line'
    assert scan_lines(text.splitlines()) == scan_text(text)
