# Privacy Boundaries

AnsimTalk handles digital safety report workflows, so public OSS work must be
careful about student data, uploaded evidence, provider credentials, and model
output claims.

## Public Repository Rule

Do not commit:

- real student names, phone numbers, school identifiers, chat exports, or
  screenshots
- uploaded files, generated PDFs, or runtime `tmp/` contents
- provider keys, OAuth tokens, service-account JSON, `.env`, or deployment
  secrets
- unsanitized examples copied from real incidents

Use placeholders, synthetic fixtures, or sanitized samples only.

## Runtime Data Flow

- Uploads are accepted by the Flask app and written to `tmp/` with generated
  filenames.
- File metadata and SHA-256 hashes are used for evidence tracking.
- Optional external providers may receive uploaded images or extracted text
  only when credentials are configured by the operator.
- Missing credentials should keep the local workflow testable through fallback
  behavior.
- Generated PDF reports are runtime artifacts and are not repository evidence.

## Human Review Boundary

Model and fallback outputs are review aids. They must not be treated as final
disciplinary, legal, forensic, medical, emergency, or safety decisions.

Every real workflow needs a responsible adult or maintainer to review:

- source context and whether the sample is complete
- provider or fallback limitations
- risk labels and explanations
- whether any private data should be redacted before sharing
- whether a separate emergency, school, legal, or platform process is needed

## Provider Boundary

Provider calls are optional and controlled by environment variables. A
contributor should be able to run tests without live provider credentials.

If real credentials were exposed, follow `SECURITY.md`: revoke, rotate, update
the deployment environment outside git, run readiness checks, and document only
sanitized incident details.

## Documentation Boundary

Public docs should say what the tool does and where review is required. They
must not promise guaranteed detection, automatic intervention, legal proof, or
customer-ready deployment.
