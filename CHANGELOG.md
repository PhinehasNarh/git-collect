# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-06-19

### Added

- Initial scanner with four detection rules: AWS access keys, PEM private keys,
  hardcoded secret assignments, and JSON Web Tokens.
- `gitcollect` command line interface.
- CI workflow (lint plus tests on Python 3.9, 3.11, 3.12).
- CodeQL analysis workflow.
- Dependabot configuration for pip and GitHub Actions.

[Unreleased]: https://github.com/PhinehasNarh/git-collect/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/PhinehasNarh/git-collect/releases/tag/v0.1.0

<!-- cadence: routine maintenance note 2026-06-19 -->
