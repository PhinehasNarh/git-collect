# Using gitcollect as a pre-commit hook

`gitcollect` ships a [pre-commit](https://pre-commit.com) hook so it can scan
staged files before every commit.

Add this to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/PhinehasNarh/git-collect
    rev: v0.1.0
    hooks:
      - id: gitcollect
```

Then install and run:

```bash
pre-commit install
pre-commit run --all-files
```

The hook exits non-zero when a finding is present, blocking the commit until the
secret is removed or allowlisted.
