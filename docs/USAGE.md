# Usage examples

## Scan a single file

```bash
gitcollect config/settings.py
```

## Scan several files

```bash
gitcollect app.py .env deploy/secrets.yaml
```

## Machine-readable output

```bash
gitcollect --json app.py
```

## Per-rule examples

| Rule | Example line that triggers it |
| --- | --- |
| `aws-access-key` | `aws_key = AKIAIOSFODNN7EXAMPLE` |
| `github-pat` | `token = ghp_<36 chars>` |
| `generic-secret-assignment` | `password = "hunter2secret"` |
| `private-key-block` | `-----BEGIN RSA PRIVATE KEY-----` |
| `jwt-token` | `auth = eyJhbGci...<payload>...<sig>` |

## Exit codes

| Code | Meaning |
| --- | --- |
| 0 | No findings |
| 1 | One or more findings detected |
