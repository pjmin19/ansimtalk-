# Contributing

Thank you for helping improve AnsimTalk. Keep changes small, testable, and
safe for a public repository.

## Development Setup

```powershell
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
python -m pip install -r requirements.txt pytest
python -m pytest -q
python scripts/check_oss_readiness.py --repo-root .
```

## Pull Request Checklist

- Explain the user-facing behavior change.
- Add or update tests for the changed behavior.
- Do not commit real credentials, `.env`, uploads, generated reports, or private
  user data.
- Run compile, tests, and OSS readiness checks before requesting review.

## Scope

Good first contributions include documentation cleanup, fallback-mode tests,
PDF report fixtures, CI maintenance, and provider adapter hardening.
