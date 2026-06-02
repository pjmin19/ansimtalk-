import json
import subprocess
import sys
from pathlib import Path


def test_maintainer_report_command_generates_json_and_markdown(tmp_path):
    repo_root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [
            sys.executable,
            str(repo_root / "scripts" / "generate_maintainer_report.py"),
            "--output-dir",
            str(tmp_path),
        ],
        cwd=repo_root,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr

    summary = json.loads(result.stdout)
    assert summary["status"] == "PASS"
    assert summary["issue_template_count"] >= 3
    assert summary["pr_checklist_items"] >= 4
    assert summary["codex_api_credit_workflows"] >= 4

    json_path = Path(summary["json"])
    markdown_path = Path(summary["markdown"])
    assert json_path.exists()
    assert markdown_path.exists()

    payload = json.loads(json_path.read_text(encoding="utf-8"))
    assert payload["schema"] == "ansimtalk_maintainer_report.v1"
    assert payload["status"] == "PASS"
    assert payload["issue_count"] == 0
    assert payload["issue_triage"]["template_count"] >= 3

    pr_items = "\n".join(payload["pr_security_privacy_checklist"]["items"]).lower()
    assert "security" in pr_items
    assert "privacy" in pr_items

    workflows = {item["workflow"] for item in payload["codex_api_credit_plan"]}
    assert {"issue_triage", "pr_security_privacy_review", "release_note_draft"}.issubset(workflows)
    assert payload["live_actions"]["openai_api_called"] is False
