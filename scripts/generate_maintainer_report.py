#!/usr/bin/env python3
"""Generate a local maintainer automation report from public repo artifacts."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = REPO_ROOT / "tmp" / "maintainer_report"

SOURCE_FILES = {
    "bug_report": ".github/ISSUE_TEMPLATE/bug_report.md",
    "feature_request": ".github/ISSUE_TEMPLATE/feature_request.md",
    "maintenance_task": ".github/ISSUE_TEMPLATE/maintenance_task.md",
    "pull_request_template": ".github/PULL_REQUEST_TEMPLATE.md",
    "release_notes_draft": "docs/RELEASE_NOTES_DRAFT.md",
    "maintainer_checklist": "docs/MAINTAINER_GITHUB_CHECKLIST.md",
    "evaluation": "docs/EVALUATION.md",
}

VALIDATION_COMMANDS = [
    "python -m compileall -q .",
    "python -m pytest -q",
    "python scripts/run_domain_eval.py --output-json tmp/domain_eval/domain_eval_result.json",
    "python scripts/generate_maintainer_report.py --output-dir tmp/maintainer_report",
    "python scripts/check_oss_readiness.py --repo-root .",
]


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate AnsimTalk maintainer report.")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="Output directory.")
    parser.add_argument("--json-name", default="maintainer_report.json", help="Output JSON filename.")
    parser.add_argument("--md-name", default="maintainer_report.md", help="Output Markdown filename.")
    return parser.parse_args(argv)


def read_text(relative: str) -> str:
    return (REPO_ROOT / relative).read_text(encoding="utf-8")


def git_head() -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
    except OSError:
        return "unknown"
    return result.stdout.strip() if result.returncode == 0 else "unknown"


def parse_front_matter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    data: dict[str, str] = {}
    for line in parts[1].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"')
    return data


def checklist_items(text: str) -> list[str]:
    return [
        re.sub(r"^- \[[ xX]\]\s*", "", line.strip()).strip()
        for line in text.splitlines()
        if re.match(r"^- \[[ xX]\]\s+", line.strip())
    ]


def heading_titles(text: str) -> list[str]:
    return [
        line.lstrip("#").strip()
        for line in text.splitlines()
        if line.startswith("##") and line.lstrip("#").strip()
    ]


def build_report() -> dict[str, Any]:
    missing = [relative for relative in SOURCE_FILES.values() if not (REPO_ROOT / relative).exists()]
    issue_templates = []
    for key in ("bug_report", "feature_request", "maintenance_task"):
        relative = SOURCE_FILES[key]
        text = read_text(relative)
        front_matter = parse_front_matter(text)
        issue_templates.append(
            {
                "id": key,
                "path": relative,
                "name": front_matter.get("name", key),
                "label": front_matter.get("labels", ""),
                "checklist_count": len(checklist_items(text)),
                "safety_boundary_present": "private student data" in text,
            }
        )

    pr_text = read_text(SOURCE_FILES["pull_request_template"])
    release_text = read_text(SOURCE_FILES["release_notes_draft"])
    pr_items = checklist_items(pr_text)
    release_sections = heading_titles(release_text)

    codex_plan = [
        {
            "workflow": "issue_triage",
            "repo_sources": [item["path"] for item in issue_templates],
            "credit_use": "Summarize incoming issues into labels, risk level, acceptance criteria, and next maintainer action.",
        },
        {
            "workflow": "pr_security_privacy_review",
            "repo_sources": [SOURCE_FILES["pull_request_template"], "SECURITY.md", "docs/PRIVACY_BOUNDARIES.md"],
            "credit_use": "Review PR diffs against credential, provider, upload, and student-data boundaries before merge.",
        },
        {
            "workflow": "release_note_draft",
            "repo_sources": [SOURCE_FILES["release_notes_draft"], "docs/READINESS_AUDIT.md"],
            "credit_use": "Draft release notes from merged PR evidence and validation commands.",
        },
        {
            "workflow": "maintainer_status_report",
            "repo_sources": [SOURCE_FILES["maintainer_checklist"], SOURCE_FILES["evaluation"]],
            "credit_use": "Turn local validator results into a concise maintainer report without sending private runtime data.",
        },
    ]

    issues = []
    if missing:
        issues.extend(f"missing_source:{relative}" for relative in missing)
    if not any("privacy" in item.lower() for item in pr_items):
        issues.append("pr_checklist_missing_privacy")
    if not any("security" in item.lower() for item in pr_items):
        issues.append("pr_checklist_missing_security")
    if len(issue_templates) < 3:
        issues.append("issue_template_count_below_3")

    return {
        "schema": "ansimtalk_maintainer_report.v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": "PASS" if not issues else "FAIL",
        "issue_count": len(issues),
        "issues": issues,
        "repo": {
            "root": str(REPO_ROOT),
            "head": git_head(),
        },
        "source_files": SOURCE_FILES,
        "issue_triage": {
            "template_count": len(issue_templates),
            "templates": issue_templates,
        },
        "pr_security_privacy_checklist": {
            "path": SOURCE_FILES["pull_request_template"],
            "item_count": len(pr_items),
            "items": pr_items,
        },
        "release_note_draft": {
            "path": SOURCE_FILES["release_notes_draft"],
            "sections": release_sections,
        },
        "validation_commands": VALIDATION_COMMANDS,
        "codex_api_credit_plan": codex_plan,
        "live_actions": {
            "github_api_called": False,
            "openai_api_called": False,
            "openai_form_submit": "NOT_PERFORMED",
            "provider_change": "NOT_PERFORMED",
            "training": "NOT_PERFORMED",
        },
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# AnsimTalk Maintainer Report",
        "",
        f"Status: `{report['status']}`",
        "",
        f"Head: `{report['repo']['head']}`",
        "",
        "## Issue Triage",
    ]
    for item in report["issue_triage"]["templates"]:
        lines.append(f"- `{item['path']}` -> label `{item['label']}`")

    lines.extend(["", "## PR Security And Privacy Checklist"])
    for item in report["pr_security_privacy_checklist"]["items"]:
        lines.append(f"- {item}")

    lines.extend(["", "## Release Note Draft Sources"])
    for section in report["release_note_draft"]["sections"]:
        lines.append(f"- {section}")

    lines.extend(["", "## Codex/API Credit Plan"])
    for item in report["codex_api_credit_plan"]:
        lines.append(f"- `{item['workflow']}`: {item['credit_use']}")

    lines.extend(["", "## Validation Commands"])
    for command in report["validation_commands"]:
        lines.append(f"- `{command}`")

    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This report reads public repository files only. It does not call GitHub",
            "or OpenAI APIs, submit the OpenAI form, change providers, or train models.",
            "",
        ]
    )
    return "\n".join(lines)


def write_outputs(args: argparse.Namespace, report: dict[str, Any]) -> dict[str, str]:
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / args.json_name
    md_path = output_dir / args.md_name
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(report), encoding="utf-8")
    return {"json": str(json_path), "markdown": str(md_path)}


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    report = build_report()
    outputs = write_outputs(args, report)
    print(
        json.dumps(
            {
                "status": report["status"],
                "schema": report["schema"],
                "issue_count": report["issue_count"],
                "issue_template_count": report["issue_triage"]["template_count"],
                "pr_checklist_items": report["pr_security_privacy_checklist"]["item_count"],
                "codex_api_credit_workflows": len(report["codex_api_credit_plan"]),
                "json": outputs["json"],
                "markdown": outputs["markdown"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
