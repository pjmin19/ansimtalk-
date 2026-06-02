# Human Review Workflow

AnsimTalk keeps AI-assisted analysis inside a human review loop. The workflow is
designed so local maintainers and educators can see what was generated, what
was checked, and what still needs a person to decide.

## Workflow

1. Collect only synthetic or authorized material for a public-safe run.
2. Run the local sample report or domain evaluation command.
3. Inspect extracted text, metadata, hashes, and analysis notes.
4. Compare the output against the original context.
5. Mark each item as confirmed, needs more context, or not actionable.
6. Use the school's existing safeguarding or counseling route for any real
   case.

Human review is required before any real-world action.

## Decision Record

For each reviewed item, record:

- reviewer role
- source material checked
- model or fallback output reviewed
- confirmed facts
- uncertainty or missing context
- escalation route or no-action reason

## Boundary Rules

The workflow is not a legal authority, not a forensic authority, and not an
emergency response authority. It is not a legal determination, not a forensic
conclusion, and not an emergency response process.

Never use AnsimTalk output as an automatic sanction, automatic diagnosis,
automatic report to guardians, or automatic emergency instruction. A human
reviewer must decide what the material means and which existing policy applies.

## Public Repo Rule

The public repository may contain synthetic fixtures and public-safe examples
only. Real student data, uploaded evidence, generated runtime reports, provider
keys, and service-account JSON must stay out of git.
