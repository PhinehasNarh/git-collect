# git-collect

[![CI](https://github.com/PhinehasNarh/git-collect/actions/workflows/ci.yml/badge.svg)](https://github.com/PhinehasNarh/git-collect/actions/workflows/ci.yml)
[![CodeQL](https://github.com/PhinehasNarh/git-collect/actions/workflows/codeql.yml/badge.svg)](https://github.com/PhinehasNarh/git-collect/actions/workflows/codeql.yml)

`gitcollect` is a small, dependency-free Git repository hygiene scanner. It
inspects files for hardcoded credentials, private key material, and other
common secret-leak patterns so they can be caught before they land in history.

It is deliberately tiny so it runs cleanly inside locked-down CI runners.

## Install

```bash
python -m pip install -e ".[dev]"
```

## Usage

```bash
gitcollect path/to/file.py another/file.env
```

The command exits non-zero when any finding is present, which makes it usable
as a pre-merge gate.

## Detection rules

| Rule id | Detects | Severity |
| --- | --- | --- |
| `aws-access-key` | AWS access key ids | high |
| `private-key-block` | PEM private key blocks | high |
| `generic-secret-assignment` | Hardcoded `secret`/`password`/`token` assignments | medium |
| `jwt-token` | JSON Web Tokens | low |

## Development

```bash
pytest --cov=gitcollect
ruff check .
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Security reports go through
[SECURITY.md](SECURITY.md).

## License

MIT.
