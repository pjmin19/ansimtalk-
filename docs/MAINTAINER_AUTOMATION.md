# Maintainer Automation

AnsimTalk keeps maintainer automation local and inspectable. The goal is to
show how Codex or API credits can reduce routine open-source maintenance work
without sending private runtime data or changing provider settings.

## Command

```powershell
python scripts/generate_maintainer_report.py --output-dir tmp/maintainer_report
```

The command reads public repository files and writes:

- `tmp/maintainer_report/maintainer_report.json`
- `tmp/maintainer_report/maintainer_report.md`

It does not call GitHub, OpenAI, Gemini, Sightengine, or any live provider.

## Inputs

- `.github/ISSUE_TEMPLATE/bug_report.md`
- `.github/ISSUE_TEMPLATE/feature_request.md`
- `.github/ISSUE_TEMPLATE/maintenance_task.md`
- `.github/PULL_REQUEST_TEMPLATE.md`
- `docs/RELEASE_NOTES_DRAFT.md`
- `docs/MAINTAINER_GITHUB_CHECKLIST.md`
- `docs/EVALUATION.md`

## What It Reports

- issue triage templates and labels
- PR security and privacy checklist items
- release-note draft sections
- validation commands for local maintainers
- Codex/API credit workflows tied to concrete repo files

## Codex/API Credit Use

The current support case is maintainer leverage, not popularity. Credits would
be used for:

- summarizing issue reports into labels, risk level, and acceptance criteria
- reviewing pull requests against security and privacy boundaries
- drafting release notes from merged PR and validator evidence
- turning readiness, domain evaluation, and CI results into maintainer reports

The report generator packages the public-safe context for these tasks. It is a
repo-local function, so the API credit plan is backed by a runnable command.

## Boundaries

- Do not put real student data, uploaded evidence, generated runtime reports,
  provider keys, service-account JSON, or `.env` contents into generated
  reports.
- Generated reports under `tmp/` are local artifacts and should not be
  committed.
- Human review is still required before release, public claims, or any
  real-world use decision.
