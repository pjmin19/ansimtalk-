# GitHub Reference Patterns

This document records the public GitHub maintenance patterns used to harden
AnsimTalk for a Codex for Open Source application. It is clean-room evidence:
the repository copies no upstream implementation code or project text.

## Public References Checked

- `pallets/flask`: release notes and security-linked maintenance history show
  the value of explicit changelog, release, issue, and security references.
- `fastapi/fastapi`: issue template routing uses disabled blank issues and
  contact links so maintainers receive better triage inputs.
- `pypa/sampleproject`: README and project metadata are treated as code-hosting
  surfaces for users who need overview, usage, and packaging context.
- GitHub Actions, Dependabot, and CodeQL: automated checks make maintenance
  responsibility visible without claiming product maturity.

## Patterns Applied To AnsimTalk

- Keep README focused on what the project does, how to run it, limitations,
  tests, security, and maintainer evidence.
- Keep release and audit notes outside the README so the first page stays
  readable.
- Disable blank issues and route sensitive reports to the security policy.
- Add weekly dependency checks for Python dependencies and GitHub Actions.
- Add CodeQL analysis for a public security-quality signal.
- Keep the OpenAI application packet under 500 characters per official field
  and validate the counts locally.

## Boundary

These patterns improve public maintainer evidence. They do not mean OpenAI has
accepted the application, that the project has broad adoption, or that the app
is customer-ready.
