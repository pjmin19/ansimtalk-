import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PROMPT_PATH = REPO_ROOT / "docs" / "CODEX_FOR_OSS_GOAL_PROPULSION_PROMPT_KO.md"


def test_goal_propulsion_prompt_is_under_4000_chars_and_counted():
    text = PROMPT_PATH.read_text(encoding="utf-8")
    body = re.search(
        r"<!-- prompt:goal_propulsion -->(.*?)<!-- /prompt:goal_propulsion -->",
        text,
        re.DOTALL,
    ).group(1).strip()
    declared = int(re.search(r"<!-- chars:goal_propulsion_prompt=(\d+) -->", text).group(1))

    assert len(body) == declared
    assert declared <= 4000


def test_goal_propulsion_prompt_keeps_boundary_terms():
    text = PROMPT_PATH.read_text(encoding="utf-8")
    required_terms = [
        "최종 그림",
        "DTT 방식",
        "TDD 규칙",
        "M8 Claim Boundary Hardening",
        "PASS: Auto-Verified",
        "PASS: Auto-Review-Ready",
        "NOT_PERFORMED",
    ]
    for term in required_terms:
        assert term in text
