# Contributing to git-collect

Thanks for contributing. This project favors small, well-tested changes.

## Workflow

1. Open or claim an issue describing the change.
2. Create a topic branch off `main`: `git switch -c feat/short-name`.
3. Make your change with a test.
4. Run the checks:
   ```bash
   pytest
   ruff check .
   ```
5. Open a pull request using the template. Link the issue with `Closes #NN`.
6. A maintainer reviews and merges.

## Commit style

- Use clear, imperative subject lines: `Add JWT detection rule`.
- Sign off your commits: `git commit -s`.
- When pairing, credit your partner with a trailer:
  ```
  Co-authored-by: Partner Name <partner@users.noreply.github.com>
  ```

## Branch protection

`main` expects passing CI before merge. Keep PRs focused so review stays fast.

## Adding a detection rule

Detection rules live in [`src/gitcollect/scanner.py`](src/gitcollect/scanner.py).
Add the pattern to `_RULES` and a matching test in
[`tests/test_scanner.py`](tests/test_scanner.py). Every rule needs at least one
positive and the suite must still pass on clean input.

## Code of conduct

Participation is governed by [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
