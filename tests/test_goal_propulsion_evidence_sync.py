from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]

M8_MAIN_COMMIT = "a6f909b351d9085787b68bffb4ef3ddea9f36f45"
M8_TEST_RUN = "26824757948"
M8_CODEQL_RUN = "26824757970"
M8_PR_URL = "https://github.com/pjmin19/ansimtalk-/pull/24"


def read(relative_path: str) -> str:
    return (REPO_ROOT / relative_path).read_text(encoding="utf-8")


def test_m9_public_evidence_sync_names_current_m8_main_and_ci():
    checked_files = {
        "README.md": read("README.md"),
        "docs/OPENAI_CODEX_FOR_OSS_EVIDENCE.md": read(
            "docs/OPENAI_CODEX_FOR_OSS_EVIDENCE.md"
        ),
        "docs/READINESS_AUDIT.md": read("docs/READINESS_AUDIT.md"),
        "docs/CODEX_FOR_OSS_SUBMISSION_PACKET.md": read(
            "docs/CODEX_FOR_OSS_SUBMISSION_PACKET.md"
        ),
    }

    for path, text in checked_files.items():
        assert M8_PR_URL in text, path
        assert M8_MAIN_COMMIT in text, path
        assert M8_TEST_RUN in text, path
        assert M8_CODEQL_RUN in text, path


def test_m10_submission_packet_is_frozen_after_m8_main_checks():
    packet = read("docs/CODEX_FOR_OSS_SUBMISSION_PACKET.md")
    application = read("docs/openai-codex-for-oss-application.md")

    required_terms = [
        "M10 submission status: `READY_FOR_OWNER_SUBMISSION`",
        "M8 claim-boundary PR: `https://github.com/pjmin19/ansimtalk-/pull/24`",
        "Latest verified M8 main: `a6f909b351d9085787b68bffb4ef3ddea9f36f45`",
        "GitHub Actions `test`: `success` (`26824757948`)",
        "GitHub Actions `codeql`: `success` (`26824757970`)",
        "Official OpenAI form submission: `NOT_PERFORMED`",
        "OpenAI acceptance: `NOT_CLAIMED`",
    ]
    for term in required_terms:
        assert term in packet

    assert "M10 submission status: `READY_FOR_OWNER_SUBMISSION`" in application
    assert "M6 submission status" not in application


def test_m11_external_review_bundle_prompt_matches_current_main():
    prompt_path = Path(
        r"D:\Codex\reports\codex_for_oss_ansimtalk_readiness\LATEST"
        r"\chatgpt_deep_research_application_review_20260602"
        r"\PROMPT_CHATGPT_DEEP_RESEARCH_KO.md"
    )
    upload_dir = Path(
        r"D:\Codex\reports\codex_for_oss_ansimtalk_readiness\LATEST"
        r"\chatgpt_deep_research_application_review_20260602"
        r"\upload_files"
    )
    if not prompt_path.exists() or not upload_dir.exists():
        pytest.skip("local D:\\Codex external review bundle is not present")

    prompt = prompt_path.read_text(encoding="utf-8")
    assert len([p for p in upload_dir.iterdir() if p.is_file()]) == 20
    assert f"Latest M8 main commit: `{M8_MAIN_COMMIT}`" in prompt
    assert f"Relevant PR: {M8_PR_URL}" in prompt
    assert "PR #23" not in prompt
    assert "6424b1a8d8a605706af4d499c8a014ff4da2bc90" not in prompt


def test_m12_owner_submission_gate_keeps_live_action_boundaries():
    packet = read("docs/CODEX_FOR_OSS_SUBMISSION_PACKET.md")

    for term in [
        "OpenAI Organization ID: `OWNER_INPUT_REQUIRED`",
        "Official OpenAI form submission: `NOT_PERFORMED`",
        "OpenAI acceptance: `NOT_CLAIMED`",
        "not a submission receipt and not an acceptance notice",
        "not Human-Verified and not customer-ready",
    ]:
        assert term in packet
