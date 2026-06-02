# OSS Readiness Audit

Audit date: 2026-06-02

Repository: `pjmin19/ansimtalk-`

Local path: `D:\Codex\oss_research\external_repos\pjmin19_ansimtalk-`

## Judgment

Status: `PASS: Local Security-Hardening Auto-Verified`

Decision: applyable candidate after the security hardening PR is merged, a small
release is created, and the official OpenAI form is submitted manually.

This is not an OpenAI-submitted, human-reviewed, or customer-ready state.

## Evidence

Commands:

```powershell
python -m compileall -q .
python -m pytest -q
python scripts/check_oss_readiness.py --repo-root . --json-out D:\Codex\reports\codex_for_oss_ansimtalk_readiness\LATEST\ansimtalk_oss_readiness.v1.json
```

Observed local results before the security hardening branch:

- `compileall`: pass
- `pytest`: 5 passed
- `oss_readiness`: `PASS: Auto-Verified`
- `issue_count`: 0
- `scanned_text_files`: 42

Observed local results after the security hardening branch:

- `compileall`: pass
- `pytest`: 8 passed
- `oss_readiness`: `PASS: Auto-Verified`
- `issue_count`: 0
- `scanned_text_files`: 43
- `tests/test_security_review_regressions.py`: client path rejection and stable
  deploy secret checks covered.

Observed GitHub results:

- PR #1: merged on 2026-06-02
- Merge commit: `3d1a13a674f43ba6c8c2bfb25d7b27000bc470bf`
- PR latest checks: success
- Main branch check: success

Observed fresh-clone results:

- Fresh clone commit: `3d1a13a674f43ba6c8c2bfb25d7b27000bc470bf`
- `python -m compileall -q .`: pass
- `python -m pytest -q`: 5 passed
- `python scripts/check_oss_readiness.py --repo-root .`: `PASS: Auto-Verified`
- secret-like direct scan: no matches

Observed HTTP smoke results from fresh clone:

- `GET /health`: 200
- `GET /api/health`: 200
- `POST /api/analyze_cyberbullying` with a local text fixture: 200
- `POST /api/download_pdf`: 200, `application/pdf`, 11906 bytes

JSON evidence:

`D:\Codex\reports\codex_for_oss_ansimtalk_readiness\LATEST\ansimtalk_oss_readiness.v1.json`

## M0-M6

- M0 Security Blocker: env-only config, placeholder `.env.example`, secret-like
  scan pass, SECURITY.md rotation checklist present, client-supplied PDF paths
  rejected, deploy-mode stable secret required.
- M1 OSS Surface: README, LICENSE, SECURITY, CONTRIBUTING, CODE_OF_CONDUCT,
  issue templates, release notes draft, and roadmap present.
- M2 Reproducible Execution: compile, pytest, readiness, fresh-clone, HTTP
  smoke checks, and security regression checks pass without provider
  credentials.
- M3 Maintainer Evidence: GitHub issue, milestone, release, and OpenAI form
  checklist prepared locally. Issues #2-#6 and milestone
  `v0.1.0-oss-candidate` were created on GitHub.
- M4 CI And Quality: GitHub Actions workflow runs successfully on GitHub.
- M5 Application Packet: three application answers verified under 500
  characters.
- M6 Final Audit: this Markdown audit and JSON readiness report exist.

## Character Counts

- `repo_qualification`: 303
- `api_credits_usage`: 275
- `anything_else`: 264

## Live Actions

- GitHub branch push: `PERFORMED`
- GitHub PR creation: `PERFORMED` at https://github.com/pjmin19/ansimtalk-/pull/1
- GitHub PR merge: `PERFORMED`
- GitHub issue creation: `PERFORMED` for #2-#6
- GitHub milestone creation: `PERFORMED` for `v0.1.0-oss-candidate`
- GitHub release creation: `NOT_PERFORMED`
- Fresh clone verification: `PERFORMED`
- HTTP smoke verification: `PERFORMED`
- Security hardening branch push/PR/merge: `NOT_PERFORMED`
- OpenAI form submit: `NOT_PERFORMED`
- Provider change: `NOT_PERFORMED`
- Training/model-weight change: `NOT_PERFORMED`
