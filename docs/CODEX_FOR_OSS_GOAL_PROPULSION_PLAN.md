# Codex For OSS Goal Propulsion Plan

This plan keeps AnsimTalk from drifting through small cosmetic edits. The goal
is one finished public-review picture, then milestone slices, then DTT/TDD
implementation.

## Finished Picture

AnsimTalk should be reviewable as an early but serious public OSS maintainer
case for OpenAI Codex for Open Source:

- A first-time reviewer can find the application packet, evidence map, roadmap,
  and validation commands from the README in under two minutes.
- The repo admits early adoption instead of hiding low public popularity
  signals.
- The app, docs, examples, and submission copy never imply legal, forensic,
  emergency, disciplinary, or guaranteed-safety authority.
- The maintainer burden is visible: issue triage, PR review, release work,
  security checks, domain evaluation, and provider-adapter maintenance.
- Every submission claim has a repo-local test, validator, or GitHub check.

## DTT Operating Loop

DTT means `Define -> Test -> Transform`:

1. Define the reviewer-facing risk and the exact evidence that should exist.
2. Test the current repo for that risk before claiming progress.
3. Transform only the smallest slice needed to make the test pass.

TDD is the implementation discipline inside each DTT slice: write or extend a
failing check first, patch the repo, run local validators, then confirm GitHub
CI.

## Milestones

| Milestone | Red condition | Green condition | Core artifacts |
| --- | --- | --- | --- |
| M8 Claim Boundary Hardening | App UI or generated report says legal evidence, legal verification, guaranteed safety, or similar authority language. | Public docs and app templates describe review material only, and regression tests reject unsafe claims. | `app/templates/*`, `tests/test_public_claim_boundary.py`, `scripts/check_oss_readiness.py` |
| M9 Public Evidence Sync | README, PRs, release, application packet, and latest main evidence disagree. | README and evidence docs name latest merged PR, CI status, risk boundary, and final prompt path. | `README.md`, `docs/OPENAI_CODEX_FOR_OSS_EVIDENCE.md`, `docs/READINESS_AUDIT.md` |
| M10 Submission Packet Freeze | Official form answers are stale, too long, or unsupported by repo evidence. | All answers are under 500 characters, source-linked, and revalidated after GitHub main checks pass. | `docs/openai-codex-for-oss-application.md`, `tests/test_application_packet.py` |
| M11 Fresh External Review | Internal validators pass but external review sees contradiction or overclaim. | A 20-file Deep Research bundle and prompt are current, public-safe, and matched to main. | `D:\Codex\reports\codex_for_oss_ansimtalk_readiness\LATEST\chatgpt_deep_research_application_review_20260602` |
| M12 Owner Submission Gate | Repo is ready but official owner/account fields are missing. | Owner can submit the form with final answers, repo URL, and OpenAI Organization ID. | `docs/CODEX_FOR_OSS_SUBMISSION_PACKET.md` |

## Current Slice

PR #24 implemented M8. The highest-risk contradiction was that submission docs
said "not legal/forensic/safety authority" while app templates still used legal
evidence wording. That slice is now merged and verified on main at
`a6f909b351d9085787b68bffb4ef3ddea9f36f45` with GitHub Actions `test`
success run `26824757948` and `codeql` success run `26824757970`.

The current continuation slice is M9-M12 evidence sync: freeze the public
evidence packet after M8, keep the submission answers under 500 characters,
refresh the 20-file external review bundle, and leave the owner-only official
form gate as `NOT_PERFORMED`/`NOT_CLAIMED`.

Exit criteria:

- `python -m pytest -q`
- `python scripts/check_oss_readiness.py --repo-root .`
- `python scripts/check_codex_for_oss_application.py --repo-root .`
- GitHub `test` and `codeql` pass on `main`
