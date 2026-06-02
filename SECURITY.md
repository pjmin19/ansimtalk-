# Security Policy

## Supported State

This project is in public OSS candidate preparation. Security reports are
accepted for the current default branch and the next release candidate.

## Reporting

Do not open a public issue with a live credential, exploit payload, private
student data, or deployment secret. Open a private maintainer channel first,
then create a public issue only after sensitive details are removed.

## Credential Rules

- No real API keys, service-account JSON, Flask secrets, OAuth tokens, or `.env`
  files may be committed.
- Runtime credentials must come from environment variables.
- Deployed or multi-worker runs must set `SECRET_KEY` and enable
  `ANSIMTALK_REQUIRE_STABLE_SECRET=1`.
- `.env.example` may contain placeholders only.
- Uploaded user files and generated reports must stay out of git.
- Public API callers must not provide local file path fields for PDF generation.

## Revoke And Rotate Checklist

If a real credential appears in public history:

1. Revoke or delete the exposed credential in the provider console.
2. Create a new credential with the smallest required scope.
3. Update the deployment environment variable outside git.
4. Run `python scripts/check_oss_readiness.py --repo-root .`.
5. Run GitHub secret scanning or an equivalent local scanner before release.
6. Document the incident as a sanitized maintainer note without exposing the
   original value.

## Security Regression Checks

The test suite includes regression coverage for the current public OSS review
risks:

- `/api/download_pdf` rejects client-supplied `file_path`, `upload_path`,
  `uploaded_file_path`, `static_file_path`, and `original_image_path` values.
- `create_app()` fails fast when `ANSIMTALK_REQUIRE_STABLE_SECRET=1` is set and
  `SECRET_KEY` is missing.

## Secret Scanning Procedure

Use the local readiness validator first:

```powershell
python scripts/check_oss_readiness.py --repo-root .
```

Before a public release, also run GitHub secret scanning or `gitleaks` locally
if available:

```powershell
gitleaks detect --source . --no-git --redact
```
