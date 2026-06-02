# Maintainer GitHub Checklist

These GitHub maintainer actions were prepared locally and then created on
GitHub on 2026-06-02.

## Issues To Create

- `PERFORMED`: [#2 [security] Remove hardcoded credential history and document rotation](https://github.com/pjmin19/ansimtalk-/issues/2)
- `PERFORMED`: [#3 [ci] Add compile, pytest, and OSS readiness workflow](https://github.com/pjmin19/ansimtalk-/issues/3)
- `PERFORMED`: [#4 [test] Add fallback-mode smoke tests that require no provider credentials](https://github.com/pjmin19/ansimtalk-/issues/4)
- `PERFORMED`: [#5 [docs] Replace contest-style README with public OSS maintainer surface](https://github.com/pjmin19/ansimtalk-/issues/5)
- `PERFORMED`: [#6 [release] Prepare v0.1.0 OSS candidate release notes](https://github.com/pjmin19/ansimtalk-/issues/6)

## Milestone

`v0.1.0-oss-candidate`

Status: `PERFORMED_AND_CLOSED`

URL: https://github.com/pjmin19/ansimtalk-/milestone/1

Acceptance:

- M0-M6 local readiness validator passes.
- Public README and SECURITY.md contain no real credentials.
- Codex review security regressions are covered by tests.
- GitHub secret scanning or equivalent local scanner is run before release.

## Release Draft

Tag: `v0.1.0-oss-candidate`

Title: `AnsimTalk v0.1.0 OSS Candidate`

Status: `PERFORMED`

URL: https://github.com/pjmin19/ansimtalk-/releases/tag/v0.1.0-oss-candidate

Created after PR #8 security review hardening was merged and local/GitHub checks
passed.

## Reference Pattern Hardening

Status: `PERFORMED`

Public GitHub maintainer patterns reviewed and adapted:

- Flask-style release/security maintenance evidence.
- FastAPI-style issue routing with blank issues disabled and contact links.
- PyPA sampleproject-style README as a code-hosting overview surface.
- GitHub-native CodeQL and Dependabot maintenance automation.

Applied files:

- `docs/GITHUB_REFERENCE_PATTERNS.md`
- `docs/OPENAI_CODEX_FOR_OSS_EVIDENCE.md`
- `.github/ISSUE_TEMPLATE/config.yml`
- `.github/dependabot.yml`
- `.github/workflows/codeql.yml`

## OpenAI Form

Status: `NOT_PERFORMED`

The application copy is in `docs/openai-codex-for-oss-application.md`.
