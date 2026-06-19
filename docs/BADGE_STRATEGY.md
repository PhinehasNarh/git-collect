# GitHub Achievement Strategy

> Scope note: GitHub Achievements are a beta feature and GitHub changes the
> rules without notice. Every requirement below was accurate as of early 2026
> but you must verify against your live profile before relying on it. Treat the
> numbers as "last known good," not a contract.

## 1. Badge inventory

Legend for "Private repo?": **Yes** = earnable from a private repository if you
have enabled *Settings → Profile → Include private contributions* style
visibility for achievements; **No** = requires a public repository.

| Badge | What it is | Eligibility | Tiers | Difficulty | Private repo? | Needs others? |
| --- | --- | --- | --- | --- | --- | --- |
| **Pull Shark** | Merged pull requests | Get PRs merged into any branch | 2 / 16 / 128 / 1024 | Easy to hard | Yes | No |
| **YOLO** | Merge without review | Merge a PR that has zero reviews | Single | Trivial | Yes | No |
| **Quickdraw** | Fast close | Close an issue or PR within 5 minutes of opening it | Single | Trivial | Yes | No |
| **Pair Extraordinaire** | Co-authored commits | Merge a PR whose commits carry a valid `Co-authored-by` trailer | 1 / 10 / 24 / 48 | Easy | Yes | Yes (one real co-author) |
| **Galaxy Brain** | Accepted answers | Have your answer marked as the accepted answer in a Discussion | 2 / 8 / 16 / 32 | Medium | No (public repo required) | Effectively yes |
| **Starstruck** | Repo stars | Own a repo that reaches the star threshold | 16 / 128 / 512 / 4096 | Hard | No (public + real stars) | Yes (many) |
| **Public Sponsor** | Sponsorship | Sponsor any account through GitHub Sponsors | Single | Easy (costs money) | N/A | Yes (a sponsoree) |

### Retired / unobtainable (do not plan around these)

| Badge | Status | Why |
| --- | --- | --- |
| **Arctic Code Vault Contributor** | Retired | Awarded only to contributors whose code was in the 2 Feb 2020 Arctic snapshot. The program is not repeating, so it cannot be earned now. |
| **Mars 2020 Helicopter Contributor** | Retired | One-off, tied to repos used in the Ingenuity helicopter. Closed. |

### Highlights (profile flair, not "achievements")

These show on profiles but are not part of the achievement set and are not
"earned" through repo activity: **Pro**, **Developer Program Member**,
**Security Bug Bounty Hunter**, **Discussion moderator**. Mentioned for
completeness; ignore for badge farming.

## 2. Badge acquisition matrix

| Badge | Prerequisites | Fastest legitimate path | Est. time to first tier | Dependencies | Disqualification risk |
| --- | --- | --- | --- | --- | --- |
| **Quickdraw** | A repo with issues enabled | Open an issue, immediately close it (under 5 min) | < 5 min | None | None. Fully legitimate single action. |
| **YOLO** | A repo you can merge into | Open a PR from a branch, merge it with no review requested | < 10 min | A branch with one commit | None, as long as branch protection does not force review. |
| **Pull Shark (tier 1: 2 PRs)** | Repo with branches | Open and merge 2 small PRs | < 30 min | Real, distinct commits | Low. Empty or junk PRs to inflate counts is the gaming pattern to avoid. |
| **Pull Shark (tier 2: 16)** | Same | Spread 16 genuine small PRs over the build-out work below | 1 to 2 weeks | Real changes | Low if PRs carry real diffs. |
| **Pair Extraordinaire** | One additional real GitHub account (a collaborator) | Add `Co-authored-by` to commits in a merged PR | < 1 day once you have a partner | A second consenting human, or a legitimately separate account of your own | Medium. Fabricating a co-author identity or spinning up throwaway accounts solely to credit yourself is the risky pattern. |
| **Galaxy Brain (tier 1: 2)** | A public repo with Discussions enabled | Post Q&A discussions, have answers accepted | 1 to 3 days | Public repo + someone (or your second account) to accept, or you accept answers on your own questions | Medium. Self-answer-then-self-accept loops in a private vacuum read as gaming. Prefer genuine Q&A. |
| **Public Sponsor** | Payment method on file | Sponsor any maintainer for the minimum amount | < 15 min | A funded GitHub Sponsors payment | None. It is a real transaction. |
| **Starstruck (tier 1: 16 stars)** | A genuinely useful public repo | Build something people want, share it honestly | Weeks to months | 16 real, independent humans choosing to star | High if you buy stars or coordinate fake accounts. This is the most ToS-sensitive badge. |

## 3. Important constraint: your repo is private

`git-collect` is private. That directly affects the plan:

- **Earnable now in the private repo:** Pull Shark, YOLO, Quickdraw, Pair
  Extraordinaire. Build these here.
- **Not earnable in a private repo:**
  - *Galaxy Brain* needs Discussions and accepted answers in a **public**
    repository. Also, Discussions on private repos are limited to certain
    plans. Plan to either flip a companion repo public or use the public fork
    of this project.
  - *Starstruck* needs a **public** repo and real stars.
  - *Public Sponsor* is account-level and unaffected by repo visibility.

Practical recommendation: keep `git-collect` private for Pull Shark / YOLO /
Quickdraw / Pair Extraordinaire, and stand up a small **public** companion repo
(`git-collect-public` or just make this one public once it is presentable) to
host Discussions for Galaxy Brain and to attract honest stars for Starstruck.

Also enable, on your profile: **Settings → Profile → Achievements** display, and
turn on private contribution counting so private activity is credited.

## 4. Collaboration badges: minimum participants and ethics

| Badge | Minimum extra participants | Ethical method |
| --- | --- | --- |
| Pair Extraordinaire | 1 | Pair with a real colleague or friend who consents to being credited via `Co-authored-by`, on commits where they genuinely contributed (even a review suggestion they wrote counts as a real contribution). |
| Galaxy Brain | 1 | Ask real questions in a public Discussion; let real community members answer, or answer real questions others ask. Accepting a genuine answer is the legitimate trigger. |
| Starstruck | 16+ for tier 1 | Build something useful and share it (README, a blog post, a Show HN, a relevant subreddit). Stars must be unsolicited-in-bulk and voluntary. |

On second accounts: GitHub's current Terms allow a person to maintain more than
one account (for example a personal and a work account) as long as each is used
for a legitimate, distinct purpose and you do not use them to abuse rate limits,
inflate metrics, or evade restrictions. Creating sock-puppet accounts whose only
purpose is to star your repo, accept your own answers, or co-author with
yourself is exactly the "fake engagement" that risks flagging and badge
revocation. The clean path for collaboration badges is one real other human.
Do not automate engagement, do not buy stars, do not script account creation.

## 5. Repository architecture (this repo)

```
git-collect/
  README.md                     # project front door + CI badges
  CONTRIBUTING.md               # PR workflow (drives Pull Shark cleanly)
  SECURITY.md                   # enables a credible security posture
  CODE_OF_CONDUCT.md
  CHANGELOG.md                  # supports tagged Releases
  LICENSE                       # MIT (add via GitHub UI or file)
  pyproject.toml                # real, installable package
  src/gitcollect/               # actual working tool
    __init__.py
    scanner.py
    cli.py
  tests/
    test_scanner.py             # real tests, run by CI
  .github/
    PULL_REQUEST_TEMPLATE.md
    ISSUE_TEMPLATE/
      bug_report.yml
      feature_request.yml
      config.yml
    workflows/
      ci.yml                    # lint + test matrix
      codeql.yml                # security scanning
    dependabot.yml              # weekly dependency PRs (real, mergeable PRs)
  docs/
    BADGE_STRATEGY.md           # this file
    30_DAY_PLAN.md
    DASHBOARD.md
```

### Branch strategy

- `main` is protected: require CI to pass before merge.
- Short-lived topic branches: `feat/...`, `fix/...`, `docs/...`, `chore/...`.
- One logical change per branch so each PR is small and review is fast. Small
  PRs are both good engineering and the most defensible way to accumulate Pull
  Shark tiers.

### Issues

Seed a backlog of genuine work items, each becoming a PR:

1. Add `slack-webhook` detection rule
2. Add `github-pat` (`ghp_...`) detection rule
3. Add `--json` output format
4. Add `--severity-threshold` flag
5. Recurse directories, not just files
6. Add `.gitcollectignore` support
7. Baseline/allowlist file support
8. Pre-commit hook example
9. Performance: compile rules once (already done) and benchmark
10. Docs: usage examples per rule

Each is a real feature. That is sixteen-plus merges without a single junk PR.

### Pull requests

Every issue above is one PR. Dependabot adds more real, mergeable PRs weekly.
This is how you reach Pull Shark tier 2 (16) honestly.

### Discussions (public companion only)

Categories: Q&A (for Galaxy Brain), Ideas, Show and tell. Galaxy Brain triggers
only from Q&A accepted answers in a public repo.

### Actions workflows

`ci.yml` and `codeql.yml` make the repo technically credible and give real
status checks for branch protection. CodeQL on a **private** repo needs GitHub
Advanced Security (free on public repos; paid otherwise). If you stay private
without GHAS, keep `ci.yml` and drop `codeql.yml`, or make the repo public.

### Milestones

- `v0.1.0` Core scanner (done)
- `v0.2.0` Output formats + directory scanning
- `v0.3.0` Allowlist + pre-commit integration

Milestones group issues and give Releases something to mark.

### Releases

Tag `v0.1.0`, `v0.2.0`, etc. Releases are not their own badge but they make the
repo look maintained and give natural pause points in the 30-day plan.

### Security features

- `SECURITY.md` + private vulnerability reporting enabled
- Dependabot alerts + security updates
- CodeQL (if public or GHAS)
- Secret scanning (GitHub-side, enable in Settings)

## 6. Daily / weekly cadence

**Daily (10 to 20 min):**

- Merge any green Dependabot or topic PR (Pull Shark).
- Triage one issue (label, comment, or close stale: Quickdraw opportunities).
- If pairing that day, ensure commits carry the `Co-authored-by` trailer.

**Weekly:**

- Open 3 to 5 genuine feature PRs from the backlog.
- Cut a release if a milestone closed.
- On the public companion: post or answer one real Q&A discussion.

## 7. Pull request workflow (repeatable)

```bash
git switch -c feat/github-pat-rule
# implement rule + test
pytest && ruff check .
git add -A
git commit -s -m "Add GitHub PAT detection rule"
# pairing? add the trailer:
#   git commit -s -m "Add GitHub PAT detection rule" -m "Co-authored-by: Partner <partner@users.noreply.github.com>"
git push -u origin feat/github-pat-rule
gh pr create --fill
gh pr merge --squash --delete-branch   # YOLO if no review requested
```

## 8. Review workflow

For PRs where you want a real review (and to avoid YOLO when you do not want
it), request your collaborator as reviewer, let them approve, then merge. Real
review comments from your partner are also legitimate contributions you can
co-author follow-up fixes with.

## 9. Collaboration workflow (Pair Extraordinaire)

1. Collaborator forks or is added with write access.
2. You pair on a change (screen share, or they hand you a patch/suggestion).
3. The merged PR's commit includes:
   `Co-authored-by: Their Name <their-noreply-email@users.noreply.github.com>`
4. Use the GitHub no-reply email format so it links to their account:
   `ID+username@users.noreply.github.com`.
5. Merge. Both accounts get credit. Repeat with real shared work to climb tiers.

## 10. Compliance guardrails (read before every action)

Allowed and encouraged:

- Real PRs with real diffs, real issues, real questions and answers.
- One real collaborator for pairing and Q&A.
- Honest sharing to attract real stars.
- Real sponsorship for Public Sponsor.

Disqualifying / prohibited (never do these):

- Buying stars or followers, or coordinating accounts to star.
- Scripting account creation or using bots to simulate engagement.
- Empty/duplicate "filler" PRs purely to inflate Pull Shark.
- Fabricating a co-author who did not contribute.
- Any automation that abuses rate limits or evades GitHub controls.

If a badge cannot be earned honestly within your constraints, the correct answer
is to skip it, not to fake it. Starstruck in particular should be treated as a
byproduct of building something good, not a target to game.
