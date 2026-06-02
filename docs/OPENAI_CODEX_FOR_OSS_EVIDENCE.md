# OpenAI Codex For OSS Evidence

This file maps the public repository evidence to the Codex for Open Source
application criteria visible on the official OpenAI form.

## Repository

- GitHub username: `pjmin19`
- Repository: `https://github.com/pjmin19/ansimtalk-`
- Maintainer role: primary maintainer
- Current public status: `PASS: Auto-Verified` after local and GitHub checks
- M8 claim-boundary PR: `https://github.com/pjmin19/ansimtalk-/pull/24`
- Latest verified M8 main: `a6f909b351d9085787b68bffb4ef3ddea9f36f45`
- GitHub Actions `test`: `success` (`26824757948`)
- GitHub Actions `codeql`: `success` (`26824757970`)
- Official OpenAI form submission: `NOT_PERFORMED`

## Criteria Map

| OpenAI signal | Repository evidence |
| --- | --- |
| Public open-source project | Public GitHub repository with `README.md`, `LICENSE`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, architecture docs, privacy-boundary docs, and human-review docs. |
| Active maintenance | PR #8 merged, issues #2-#6 closed, milestone `v0.1.0-oss-candidate` closed, and release `v0.1.0-oss-candidate` published. |
| PR review and issue triage | Issue templates, PR template, disabled blank issues, maintainer checklist, and closed milestone evidence. |
| Release management | Release notes draft, published release tag, readiness audit, and post-release evidence docs. |
| Security and quality | `SECURITY.md`, security regression tests, secret-like string scanning, CodeQL workflow, Dependabot config, and CI. |
| Reproducible maintainer workflow | `python -m compileall -q .`, `python -m pytest -q`, `python scripts/generate_sample_report.py --output-dir tmp/sample_report`, `python scripts/run_domain_eval.py --output-json tmp/domain_eval/domain_eval_result.json`, `python scripts/generate_maintainer_report.py --output-dir tmp/maintainer_report`, and `python scripts/check_oss_readiness.py --repo-root .`. |
| Codex/API-credit fit | Application answers and maintainer automation docs map credits to issue triage, PR security/privacy review, release-note generation, provider-adapter tests, Korean text/OCR evaluation expansion, fallback-safety checks, and public-safe examples. |
| Submission packet | `docs/CODEX_FOR_OSS_SUBMISSION_PACKET.md` and `docs/openai-codex-for-oss-application.md` hold final owner-review copy with 500-character validation. |
| Ecosystem importance claim | Small but focused OSS candidate for AI-assisted student digital-safety report workflows with educator-facing human-review boundaries. |

## M8-M12 Evidence Sync

- M8 claim-boundary hardening is merged in
  `https://github.com/pjmin19/ansimtalk-/pull/24`.
- The latest verified M8 main commit is
  `a6f909b351d9085787b68bffb4ef3ddea9f36f45`.
- Main GitHub Actions `test` passed in run `26824757948`.
- Main GitHub Actions `codeql` passed in run `26824757970`.
- M9 public evidence sync keeps README, this evidence map, readiness audit, and
  submission packet aligned to those same proof points.
- M10 freezes the three under-500-character owner-review form answers.
- M11 refreshes the 20-file Deep Research bundle under
  `D:\Codex\reports\codex_for_oss_ansimtalk_readiness\LATEST\chatgpt_deep_research_application_review_20260602`.
- M12 keeps official form submission as owner-gated:
  OpenAI Organization ID is `OWNER_INPUT_REQUIRED`, official submission is
  `NOT_PERFORMED`, and acceptance is `NOT_CLAIMED`.

## Automated review risk

An automated reviewer may penalize the repo for low public popularity signals:
stars, downloads, and external contributor base are not the strength of this
application.

The intended pass case is therefore clear ecosystem importance plus responsible
maintenance evidence: the repo addresses an education/youth-safety evidence
workflow, keeps privacy and human-review boundaries visible, and shows how Codex
and API credits would reduce concrete maintainer work.

## Small-Repo Honesty

AnsimTalk does not yet have broad adoption, stars, package downloads, or an
external contributor base. The support case is therefore not popularity. The
case is that the maintainer has made the project public, scoped the safety
claim responsibly, added tests and public maintenance automation, and can use
Codex to reduce review, release, and security-maintenance load while the repo
becomes more reusable.

## Maintainer Evidence Links

- Application copy: `docs/openai-codex-for-oss-application.md`
- Submission packet: `docs/CODEX_FOR_OSS_SUBMISSION_PACKET.md`
- Automated review packet: `docs/CODEX_FOR_OSS_AUTOMATED_REVIEW.md`
- Whole-picture plan: `docs/CODEX_FOR_OSS_GOAL_PROPULSION_PLAN.md`
- Goal propulsion prompt: `docs/CODEX_FOR_OSS_GOAL_PROPULSION_PROMPT_KO.md`
- Readiness audit: `docs/READINESS_AUDIT.md`
- Maintainer checklist: `docs/MAINTAINER_GITHUB_CHECKLIST.md`
- Architecture: `docs/ARCHITECTURE.md`
- Privacy boundaries: `docs/PRIVACY_BOUNDARIES.md`
- Contributor local run: `docs/CONTRIBUTOR_LOCAL_RUN.md`
- Domain evaluation: `docs/EVALUATION.md`
- Educator guide: `docs/EDUCATOR_GUIDE.md`
- Human review workflow: `docs/HUMAN_REVIEW_WORKFLOW.md`
- Human review sample output: `examples/reports/human_review_sample.md`
- Maintainer automation: `docs/MAINTAINER_AUTOMATION.md`
- Domain eval cases: `examples/evaluations/domain_eval_cases.json`
- Maintainer report runner: `scripts/generate_maintainer_report.py`
- Domain eval runner: `scripts/run_domain_eval.py`
- Reference patterns: `docs/GITHUB_REFERENCE_PATTERNS.md`
- Test workflow: `.github/workflows/test.yml`
- CodeQL workflow: `.github/workflows/codeql.yml`
- Dependabot config: `.github/dependabot.yml`
