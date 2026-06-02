import base64
import hashlib
import json
import os
import re
from datetime import datetime
from html import escape
from pathlib import Path

import requests
from flask import current_app
from google import genai
from google.cloud import vision
from PIL import Image
from weasyprint import HTML


def convert_markdown_table_to_html(markdown_table):
    """Convert a pipe-delimited Markdown table into a small HTML table."""
    if not markdown_table.strip():
        return "<p>No analysis result.</p>"

    rows = []
    for line in markdown_table.strip().splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.split("|")[1:-1]]
        if cells and not all(set(cell) <= {"-", ":"} for cell in cells):
            rows.append(cells)

    if not rows:
        return "<p>No table rows.</p>"

    html = ['<table class="analysis-table">']
    for index, cells in enumerate(rows):
        tag = "th" if index == 0 else "td"
        html.append("<tr>" + "".join(f"<{tag}>{escape(cell)}</{tag}>" for cell in cells) + "</tr>")
    html.append("</table>")
    return "\n".join(html)


def get_risk_class(risk_text):
    value = str(risk_text or "").strip().lower()
    if value in {"high", "severe"}:
        return "risk-severe"
    if value in {"medium", "present"}:
        return "risk-present"
    if value in {"low", "slight"}:
        return "risk-slight"
    if value in {"none", "-"}:
        return "risk-none"
    return ""


def get_image_metadata(filepath):
    try:
        with Image.open(filepath) as image:
            return {
                "format": image.format,
                "mode": image.mode,
                "size": image.size,
                "info": dict(image.info),
            }
    except Exception as exc:
        return {"error": f"metadata extraction failed: {exc}"}


def analyze_file(file_path, analysis_type, file_extension):
    with open(file_path, "rb") as handle:
        sha256 = hashlib.sha256(handle.read()).hexdigest()

    file_extension = str(file_extension or "").lower()
    result = {
        "file_info": {
            "filename": os.path.basename(file_path),
            "type": file_extension,
            "size_bytes": os.path.getsize(file_path),
            "sha256": sha256,
        },
        "analysis_timestamp": datetime.now().isoformat(),
        "sha256": sha256,
        "analysis_type": analysis_type,
    }

    if analysis_type == "deepfake":
        if file_extension not in {"png", "jpg", "jpeg"}:
            result["error"] = "Deepfake analysis accepts image files only."
            return result

        result["metadata"] = get_image_metadata(file_path)
        result["deepfake_analysis"] = analyze_image_with_sightengine(file_path)
        extracted_text = extract_text_from_image(file_path)
        if extracted_text.strip() and not extracted_text.startswith("["):
            result["extracted_text"] = extracted_text
        return result

    if analysis_type == "cyberbullying":
        if file_extension in {"png", "jpg", "jpeg"}:
            extracted_text = extract_text_from_image(file_path)
        elif file_extension == "txt":
            extracted_text = read_text_file(file_path)
        else:
            result["error"] = "Cyberbullying analysis accepts text or image files only."
            return result

        normalized = _preprocess_kakao_chat_text(extracted_text)
        analysis = analyze_text_with_gemini(normalized)
        result["extracted_text"] = normalized
        result["cyberbullying_analysis"] = analysis.get("table", "")
        result["cyberbullying_analysis_summary"] = analysis.get("summary", "")
        result["cyberbullying_risk_line"] = extract_risk_line(analysis.get("summary", ""))
        return result

    result["error"] = "Unsupported analysis type."
    return result


def read_text_file(file_path):
    for encoding in ("utf-8", "cp949"):
        try:
            return Path(file_path).read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return Path(file_path).read_text(encoding="utf-8", errors="replace")


def analyze_image_with_sightengine(file_path):
    api_user = current_app.config["SIGHTENGINE_API_USER"]
    api_secret = current_app.config["SIGHTENGINE_API_SECRET"]
    if not api_user or not api_secret:
        return {
            "status": "credentials_missing",
            "error": "Sightengine credentials are not configured.",
        }

    params = {
        "models": "deepfake,scam,gore",
        "api_user": api_user,
        "api_secret": api_secret,
    }
    url = "https://api.sightengine.com/1.0/check.json"

    with open(file_path, "rb") as media:
        response = requests.post(url, files={"media": media}, data=params, timeout=30)
    response.raise_for_status()
    return response.json()


def extract_text_from_image(image_path):
    service_account_info = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    credentials_path = current_app.config["GOOGLE_APPLICATION_CREDENTIALS"]

    try:
        if service_account_info:
            from google.oauth2 import service_account

            credentials = service_account.Credentials.from_service_account_info(
                json.loads(service_account_info)
            )
            client = vision.ImageAnnotatorClient(credentials=credentials)
        elif credentials_path and os.path.exists(credentials_path):
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
            client = vision.ImageAnnotatorClient()
        else:
            return "[Google Cloud credentials are not configured.]"

        with open(image_path, "rb") as image_file:
            image = vision.Image(content=image_file.read())
        response = client.text_detection(image=image)
        texts = response.text_annotations
        return texts[0].description.strip() if texts else ""
    except Exception as exc:
        return f"[Google Cloud Vision API error: {exc}]"


def _preprocess_kakao_chat_text(raw_text: str) -> str:
    """Normalize OCR chat text into one speaker/content line per message."""
    if not raw_text:
        return ""

    time_pattern = re.compile(r"^(?:AM|PM|am|pm)?\s?\d{1,2}:\d{2}$")
    date_time_pattern = re.compile(
        r"^\d{4}[./-]\s?\d{1,2}[./-]\s?\d{1,2}"
        r"(?:\s+(?:AM|PM|am|pm)?\s?\d{1,2}:\d{2})?$"
    )
    possible_name_pattern = re.compile(r"^[\w가-힣]{1,16}$")

    processed = []
    pending_speaker = None
    for raw_line in raw_text.splitlines():
        line = re.sub(r"\s+", " ", raw_line.strip())
        if not line or time_pattern.match(line) or date_time_pattern.match(line):
            continue
        if line.lower() in {"photo", "image"}:
            continue

        if ":" in line and not line.endswith(":"):
            speaker, content = [part.strip() for part in line.split(":", 1)]
            processed.append(f"{speaker or '-'}: {content}")
            pending_speaker = None
            continue

        if possible_name_pattern.match(line):
            pending_speaker = line
            continue

        if pending_speaker:
            processed.append(f"{pending_speaker}: {line}")
            pending_speaker = None
        else:
            processed.append(f"-: {line}")

    return "\n".join(processed)


def analyze_text_with_gemini(text_content):
    api_key = os.environ.get("GOOGLE_GEMINI_API_KEY") or current_app.config.get("GOOGLE_GEMINI_API_KEY")
    if not api_key or api_key.lower().startswith("your_"):
        return _fallback_cyberbullying_analysis(text_content)

    prompt = (
        "Analyze the following conversation for cyberbullying risk. "
        "Return a Markdown table with columns: sentence, type, victim, offender, risk, explanation. "
        "Then return summary labels: overall risk, atmosphere, potential risks.\n\n"
        f"{text_content}"
    )

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
        text = (response.text or "").strip()
        table_lines = [line for line in text.splitlines() if line.strip().startswith("|")]
        summary_lines = [line for line in text.splitlines() if not line.strip().startswith("|")]
        return {
            "table": convert_markdown_table_to_html("\n".join(table_lines)),
            "summary": "\n".join(summary_lines).strip(),
        }
    except Exception as exc:
        fallback = _fallback_cyberbullying_analysis(text_content)
        fallback["fallback_used"] = True
        fallback["error"] = f"{type(exc).__name__}: {exc}"
        return fallback


def _fallback_cyberbullying_analysis(text_content):
    normalized = _preprocess_kakao_chat_text(text_content)
    rows = [
        ["sentence", "type", "victim", "offender", "risk", "explanation"],
    ]
    risk_count = 0
    severe_count = 0

    severe_keywords = {
        "kill",
        "die",
        "destroy",
        "threat",
        "\uc8fd\uc5b4",
        "\uc8fd\uc778\ub2e4",
        "\ud611\ubc15",
        "\ub54c\ub9b0\ub2e4",
    }
    insult_keywords = {
        "stupid",
        "idiot",
        "ugly",
        "hate",
        "trash",
        "\ubc14\ubcf4",
        "\uba4d\uccad",
        "\ubabb\uc0dd\uacbc",
        "\uc2eb\uc5b4",
        "\uaebc\uc838",
    }
    exclusion_keywords = {
        "ignore",
        "exclude",
        "leave out",
        "\ub530\ub3cc",
        "\ube7c",
        "\ub07c\uc9c0\ub9c8",
        "\ubb34\uc2dc",
    }

    for line in normalized.splitlines():
        if not line.strip():
            continue
        speaker, content = ("-", line)
        if ":" in line:
            speaker, content = [part.strip() for part in line.split(":", 1)]

        lowered = content.lower()
        risk = "none"
        kind = "-"
        explanation = "No keyword risk detected."

        if any(word in lowered for word in severe_keywords):
            risk = "severe"
            kind = "threat"
            explanation = "Threat or severe harm keyword detected."
            risk_count += 1
            severe_count += 1
        elif any(word in lowered for word in insult_keywords):
            risk = "medium"
            kind = "insult"
            explanation = "Insult or degrading keyword detected."
            risk_count += 1
        elif any(word in lowered for word in exclusion_keywords):
            risk = "low"
            kind = "exclusion"
            explanation = "Exclusion-related keyword detected."
            risk_count += 1

        rows.append([f"{speaker}: {content}", kind, "-", speaker or "-", risk, explanation])

    markdown = "\n".join("| " + " | ".join(row) + " |" for row in rows)
    if severe_count:
        overall = "severe"
    elif risk_count:
        overall = "present"
    else:
        overall = "none"

    summary = (
        f"overall risk: {overall}\n"
        f"atmosphere: fallback keyword analysis found {risk_count} risk signal(s).\n"
        "potential risks: Human review is required before any real-world action."
    )
    return {
        "table": convert_markdown_table_to_html(markdown),
        "summary": summary,
        "fallback_used": True,
    }


def extract_risk_line(summary):
    match = re.search(r"overall risk\s*:\s*([^\n\r]*)", summary or "", re.IGNORECASE)
    return match.group(1).strip() if match else None


def extract_conversation_atmosphere(summary):
    match = re.search(r"atmosphere\s*:\s*(.*?)(?=\n\s*potential risks\s*:|$)", summary or "", re.I | re.S)
    if match:
        return re.sub(r"\s+", " ", match.group(1)).strip()
    return "Analysis pending."


def extract_potential_risks(summary):
    match = re.search(r"potential risks\s*:\s*(.*)", summary or "", re.I | re.S)
    if match:
        return re.sub(r"\s+", " ", match.group(1)).strip()
    return "Analysis pending."


def pipe_table_to_html(text):
    if "|" not in text:
        return text
    return convert_markdown_table_to_html(text)


def generate_pdf_report(analysis_result, pdf_path, analysis_type=None):
    html_content = generate_report_html(analysis_result, analysis_type, pdf_path)
    HTML(string=html_content).write_pdf(pdf_path)
    return pdf_path


def generate_image_html(original_image_path, analysis_result, original_file):
    image_path = (
        analysis_result.get("file_path")
        or analysis_result.get("uploaded_file_path")
        or analysis_result.get("static_file_path")
        or original_image_path
    )
    if not image_path or not os.path.exists(image_path):
        return ""

    suffix = Path(image_path).suffix.lower().lstrip(".") or "png"
    with open(image_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode("ascii")
    return (
        '<section class="evidence-image">'
        "<h2>Original Evidence Image</h2>"
        f'<img alt="{escape(str(original_file or "uploaded evidence"))}" '
        f'src="data:image/{suffix};base64,{encoded}" />'
        "</section>"
    )


def generate_report_html(analysis_result, analysis_type=None, pdf_path=None):
    analysis_type = analysis_type or analysis_result.get("analysis_type", "unknown")
    file_info = analysis_result.get("file_info", {})
    summary = analysis_result.get("cyberbullying_analysis_summary") or analysis_result.get("summary") or ""
    table = analysis_result.get("cyberbullying_analysis") or ""
    deepfake = analysis_result.get("deepfake_analysis")

    deepfake_html = ""
    if deepfake:
        deepfake_html = "<pre>" + escape(json.dumps(deepfake, ensure_ascii=False, indent=2)) + "</pre>"

    table_html = table if table.startswith("<table") else pipe_table_to_html(str(table))
    image_html = generate_image_html(
        analysis_result.get("original_image_path", ""),
        analysis_result,
        file_info.get("filename", ""),
    )

    return f"""
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>AnsimTalk Evidence Report</title>
  <style>
    body {{ font-family: Arial, sans-serif; line-height: 1.5; color: #1f2937; }}
    h1, h2 {{ color: #111827; }}
    table {{ border-collapse: collapse; width: 100%; margin: 12px 0; }}
    th, td {{ border: 1px solid #d1d5db; padding: 6px; vertical-align: top; }}
    th {{ background: #f3f4f6; }}
    pre {{ white-space: pre-wrap; background: #f9fafb; padding: 12px; }}
    img {{ max-width: 100%; height: auto; }}
  </style>
</head>
<body>
  <h1>AnsimTalk Evidence Report</h1>
  <h2>Case Metadata</h2>
  <p><strong>Analysis type:</strong> {escape(str(analysis_type))}</p>
  <p><strong>Filename:</strong> {escape(str(file_info.get("filename", "N/A")))}</p>
  <p><strong>SHA-256:</strong> {escape(str(analysis_result.get("sha256", "N/A")))}</p>
  <p><strong>Timestamp:</strong> {escape(str(analysis_result.get("analysis_timestamp", "N/A")))}</p>
  {image_html}
  <h2>Analysis</h2>
  {table_html}
  {deepfake_html}
  <h2>Summary</h2>
  <p>{escape(str(summary or "No summary."))}</p>
  <h2>Review Boundary</h2>
  <p>AI-assisted output is a draft signal and requires human review before action.</p>
</body>
</html>
"""
