# Handling false positives

Not every match is a real secret. Two ways to suppress noise:

## Inline allowlist comment

Add a trailing `# gitcollect: allow` comment on a line you have reviewed.
(Planned: see the baseline issue for batch suppression.)

## Raise the severity floor

Use `--severity-threshold high` to report only high-severity findings while
you triage the rest.

## Verify before suppressing

Always confirm a finding is genuinely safe before allowlisting it. A real
leaked credential must be rotated, not silenced.
