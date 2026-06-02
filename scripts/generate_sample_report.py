#!/usr/bin/env python3
"""Generate a credential-free AnsimTalk sample report from a synthetic fixture."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


DEFAULT_FIXTURE = REPO_ROOT / "examples" / "fixtures" / "cyberbullying_sample.txt"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "tmp" / "sample_report"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a synthetic AnsimTalk sample report.")
    parser.add_argument("--fixture", default=str(DEFAULT_FIXTURE), help="Synthetic .txt fixture path.")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="Directory for JSON/PDF outputs.")
    parser.add_argument("--json-name", default="sample_report.json", help="Output JSON filename.")
    parser.add_argument("--pdf-name", default="sample_report.pdf", help="Output PDF filename.")
    parser.add_argument(
        "--allow-provider",
        action="store_true",
        help="Allow configured external text-analysis providers. Defaults to offline fallback.",
    )
    return parser.parse_args(argv)


def force_offline_provider_mode() -> None:
    for name in (
        "GOOGLE_GEMINI_API_KEY",
        "SIGHTENGINE_API_USER",
        "SIGHTENGINE_API_SECRET",
        "GOOGLE_CLOUD_VISION_API_KEY",
        "GOOGLE_APPLICATION_CREDENTIALS",
        "GOOGLE_SERVICE_ACCOUNT_JSON",
    ):
        os.environ.pop(name, None)


def build_sample_report(args: argparse.Namespace) -> dict[str, object]:
    if not args.allow_provider:
        force_offline_provider_mode()

    from app import create_app
    from app.services import analyze_file, generate_pdf_report

    fixture_path = Path(args.fixture).resolve()
    output_dir = Path(args.output_dir).resolve()
    json_path = output_dir / args.json_name
    pdf_path = output_dir / args.pdf_name

    if fixture_path.suffix.lower() != ".txt":
        raise ValueError("The sample report command currently expects a .txt fixture.")
    if not fixture_path.exists():
        raise FileNotFoundError(f"Fixture not found: {fixture_path}")

    output_dir.mkdir(parents=True, exist_ok=True)

    app = create_app()
    with app.app_context():
        analysis = analyze_file(str(fixture_path), "cyberbullying", "txt")
        generate_pdf_report(analysis, str(pdf_path), "cyberbullying")

    payload = {
        "schema": "ansimtalk_sample_report.v1",
        "fixture": str(fixture_path.relative_to(REPO_ROOT)),
        "sample_run": {
            "analysis_type": "cyberbullying",
            "provider_mode": "provider_allowed" if args.allow_provider else "offline_fallback",
            "human_review_required": True,
            "privacy_note": "Synthetic fixture only. Do not commit real student data or runtime reports.",
        },
        "analysis": analysis,
        "outputs": {
            "json": str(json_path),
            "pdf": str(pdf_path),
            "pdf_bytes": pdf_path.stat().st_size,
        },
    }

    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return payload


def main(argv: list[str] | None = None) -> int:
    try:
        payload = build_sample_report(parse_args(argv))
    except Exception as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1

    summary = {
        "status": "PASS",
        "schema": payload["schema"],
        "fixture": payload["fixture"],
        "provider_mode": payload["sample_run"]["provider_mode"],
        "json": payload["outputs"]["json"],
        "pdf": payload["outputs"]["pdf"],
        "pdf_bytes": payload["outputs"]["pdf_bytes"],
    }
    print(json.dumps(summary, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
