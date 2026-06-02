from pathlib import Path

from scripts.check_codex_for_oss_application import run_checks


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_codex_for_oss_automated_review_surface_is_ready():
    result = run_checks(REPO_ROOT)
    assert result.status == "PASS: Auto-Review-Ready", result.issues
    assert result.issue_count == 0
    assert "early_adoption_low_popularity_signal" in result.risks


def test_codex_for_oss_application_does_not_claim_acceptance():
    result = run_checks(REPO_ROOT)
    assert result.evidence["official_form_submission"] == "NOT_PERFORMED"
    assert result.evidence["openai_acceptance"] == "NOT_CLAIMED"
