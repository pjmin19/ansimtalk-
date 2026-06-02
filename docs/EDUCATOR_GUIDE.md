# Educator Guide

This guide explains how educators can read AnsimTalk outputs responsibly. The
project is a developer-facing OSS toolkit for organizing digital-safety review
materials, not a replacement for school policy, guardians, counselors, or local
response procedures.

## Intended Use

- Review synthetic or authorized text/image evidence in a structured format.
- Keep file metadata, hash values, extracted text, and analysis notes together.
- Use offline fallback and sample reports for contributor training.
- Prepare a consistent discussion packet for a human reviewer.

Human review is required before any real-world action.

## Educator Reading Steps

1. Confirm that the material is synthetic, authorized, or otherwise handled
   outside the public repository.
2. Check file metadata and extracted text before reading the AI-assisted
   summary.
3. Read risk labels as review prompts, not final findings.
4. Record what a human reviewer confirmed, could not confirm, and escalated.
5. Follow the school's existing safeguarding, counseling, and reporting rules.

## Boundaries

AnsimTalk is not a legal authority, not a forensic authority, and not an
emergency response authority. It is not a legal determination, not a forensic
conclusion, and not an emergency response tool.

The project does not guarantee safety, does not verify intent, and does not
identify a final victim or offender. It only organizes review material for a
human decision process.

## Data Handling

Do not commit real student data, private chat exports, screenshots, provider
keys, generated reports, or `.env` files. Keep real review material outside the
public repo and follow local authorization rules.

## Sample Output

See `examples/reports/human_review_sample.md` for a public-safe sample of the
phrasing expected in educator-facing review notes.
