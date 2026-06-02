# OSS Readiness Audit

Audit date: 2026-06-02

Repository: `pjmin19/ansimtalk-`

Local path: `D:\Codex\oss_research\external_repos\pjmin19_ansimtalk-`

## Judgment

Status: `PASS: Remote-CI + Security-Hardening + Release Evidence Auto-Verified`

Decision: applyable candidate for official OpenAI form submission.

This is not an OpenAI-submitted, human-reviewed, or customer-ready state.

Latest reference-pattern hardening adds GitHub issue routing, Dependabot,
CodeQL, and an OpenAI criteria-to-evidence map. It strengthens public
maintainer evidence without changing the application readiness boundary.

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
- PR #8: merged on 2026-06-02
- Merge commit: `339ebaa`
- PR latest checks: success
- Main branch check: success
- Issues #2-#6: closed
- Milestone `v0.1.0-oss-candidate`: closed
- Release `v0.1.0-oss-candidate`: created
- Release URL:
  `https://github.com/pjmin19/ansimtalk-/releases/tag/v0.1.0-oss-candidate`
- Reference-pattern docs: `docs/GITHUB_REFERENCE_PATTERNS.md`
- OpenAI criteria evidence map: `docs/OPENAI_CODEX_FOR_OSS_EVIDENCE.md`
- GitHub automation added: issue routing, Dependabot, and CodeQL.
- Coupled dependency maintenance: the WeasyPrint 68.1 and pydyf <0.13 update
  is bundled because the independent Dependabot PRs failed when tested apart.

Observed fresh-clone results after PR #8 merge:

- Fresh clone commit: `339ebaa682ab9481539df9e0c068fd65054b1baa`
- `python -m compileall -q .`: pass
- `python -m pytest -q`: 8 passed
- `python scripts/check_oss_readiness.py --repo-root .`: `PASS: Auto-Verified`
- secret-like direct scan: no matches

Observed HTTP smoke results from the earlier fresh clone:

- `GET /health`: 200
- `GET /api/health`: 200
- `POST /api/analyze_cyberbullying` with a local text fixture: 200
- `POST /api/download_pdf`: 200, `application/pdf`, 11906 bytes

JSON evidence:

- `D:\Codex\reports\codex_for_oss_ansimtalk_readiness\LATEST\ansimtalk_oss_readiness_post_pr8_merge.v1.json`
- `D:\Codex\reports\codex_for_oss_ansimtalk_readiness\LATEST\ansimtalk_oss_readiness_fresh_clone_post_pr8.v1.json`
- `D:\Codex\reports\codex_for_oss_ansimtalk_readiness\LATEST\ansimtalk_oss_readiness_release_docs_fixed.v1.json`

## M0-M6

- M0 Security Blocker: env-only config, placeholder `.env.example`, secret-like
  scan pass, SECURITY.md rotation checklist present, client-supplied PDF paths
  rejected, deploy-mode stable secret required.
- M1 OSS Surface: README, LICENSE, SECURITY, CONTRIBUTING, CODE_OF_CONDUCT,
  issue templates, issue routing config, reference-pattern docs, release notes
  draft, and roadmap present.
- M2 Reproducible Execution: compile, pytest, readiness, fresh-clone, HTTP
  smoke checks, and security regression checks pass without provider
  credentials.
- M3 Maintainer Evidence: GitHub issues #2-#6 closed, milestone
  `v0.1.0-oss-candidate` closed, release `v0.1.0-oss-candidate` created,
  reference-pattern hardening recorded, and OpenAI form checklist prepared
  locally.
- M4 CI And Quality: GitHub Actions workflow runs successfully on GitHub; CodeQL
  and Dependabot are configured for the next public maintenance cycle. Workflow
  actions use current major tags checked through the GitHub API on 2026-06-02.
- M5 Application Packet: three application answers verified under 500
  characters.
- M6 Final Audit: this Markdown audit and JSON readiness report exist.

## Character Counts

- `repo_qualification`: 341
- `api_credits_usage`: 328
- `anything_else`: 293

## Live Actions

- GitHub branch push: `PERFORMED`
- GitHub PR creation: `PERFORMED` at https://github.com/pjmin19/ansimtalk-/pull/1
- GitHub PR merge: `PERFORMED`
- GitHub security hardening PR creation: `PERFORMED` at https://github.com/pjmin19/ansimtalk-/pull/8
- GitHub security hardening PR merge: `PERFORMED`
- GitHub reference-pattern PR creation/merge: `PERFORMED` at https://github.com/pjmin19/ansimtalk-/pull/9
- GitHub workflow-major PR creation/merge: `PERFORMED` at https://github.com/pjmin19/ansimtalk-/pull/15
- GitHub issue creation: `PERFORMED` for #2-#6
- GitHub milestone creation: `PERFORMED` for `v0.1.0-oss-candidate`
- GitHub milestone closure: `PERFORMED`
- GitHub release creation: `PERFORMED`
- Fresh clone verification: `PERFORMED`
- HTTP smoke verification: `PERFORMED`
- Security hardening branch push/PR/merge: `PERFORMED`
- OpenAI form submit: `NOT_PERFORMED`
- Provider change: `NOT_PERFORMED`
- Training/model-weight change: `NOT_PERFORMED`
