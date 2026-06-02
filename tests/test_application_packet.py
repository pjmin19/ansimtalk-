from pathlib import Path

from scripts.check_oss_readiness import (
    APPLICATION_REQUIRED_REFERENCES,
    APPLICATION_REQUIRED_TERMS,
    parse_answer_blocks,
    parse_declared_counts,
    run_checks,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
APPLICATION_PACKET = REPO_ROOT / "docs" / "openai-codex-for-oss-application.md"


def test_application_packet_is_ready_for_owner_submission():
    result = run_checks(REPO_ROOT, run_compile=False)
    assert result.status == "PASS: Auto-Verified", result.issues


def test_application_answers_are_under_500_chars_and_declared_counts_match():
    text = APPLICATION_PACKET.read_text(encoding="utf-8")
    blocks = parse_answer_blocks(text)
    declared = parse_declared_counts(text)

    assert set(blocks) == {"repo_qualification", "api_credits_usage", "anything_else"}
    for name, answer in blocks.items():
        assert len(answer) <= 500
        assert declared[name] == len(answer)


def test_application_packet_names_m6_terms_and_evidence_links():
    text = APPLICATION_PACKET.read_text(encoding="utf-8")
    for term in APPLICATION_REQUIRED_TERMS:
        assert term in text
    for reference in APPLICATION_REQUIRED_REFERENCES:
        assert reference in text
