# Roadmap

This roadmap uses DTT milestones and TDD-style acceptance checks.

## M0 Security Blocker

Red condition: secret-like values, hardcoded credential fallbacks, or real API
keys appear in public files.

Green condition: config is env-only, `.env.example` has placeholders, secret
rotation is documented, and readiness validation passes.

## M1 OSS Surface

Red condition: the README makes broad claims without reproducible setup,
license, contribution, conduct, or security guidance.

Green condition: the repository has a concise README, MIT license, security
policy, contribution guide, code of conduct, and issue templates.

## M2 Reproducible Execution

Red condition: local tests require live provider credentials.

Green condition: compile, pytest, and fallback-mode smoke tests pass without
network credentials.

## M3 Maintainer Evidence

Red condition: there is no clear public maintainer trail.

Green condition: issue, milestone, and release checklist items are prepared for
GitHub execution.

## M4 CI And Quality

Red condition: checks exist only on one local machine.

Green condition: GitHub Actions can run compile, pytest, and OSS readiness
validation.

## M5 OpenAI Application Packet

Red condition: application text is generic or above field limits.

Green condition: the three application answers are public-safe, specific, and
verified at 500 characters or fewer each.

## M6 Final Audit

Red condition: the maintainer cannot tell what passed, what was not performed,
and what still requires live execution.

Green condition: readiness evidence names status, blockers, commands, and
source paths. The maximum claim is `PASS: Auto-Verified` until a human executes
the public GitHub and OpenAI steps.
