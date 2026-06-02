import hashlib
import os
import re
import unicodedata
import uuid
from datetime import datetime
from pathlib import Path

from flask import Blueprint, current_app, flash, jsonify, redirect, render_template, request, send_file, session, url_for
from PIL import ExifTags, Image

from .services import analyze_file, generate_pdf_report


bp = Blueprint("main", __name__)

ALLOWED_EXTENSIONS = {"txt", "png", "jpg", "jpeg"}
MAX_FILE_SIZE = 5 * 1024 * 1024
CLIENT_PATH_FIELD_NAMES = {
    "file_path",
    "uploaded_file_path",
    "static_file_path",
    "upload_path",
    "original_image_path",
}


def secure_korean_filename(filename):
    """Return a normalized, filesystem-safe upload filename."""
    if not filename:
        return ""

    name, ext = os.path.splitext(filename)
    name = unicodedata.normalize("NFC", name)
    safe_chars = re.sub(r"[^\w\s\-.]", "", name, flags=re.UNICODE)
    safe_chars = re.sub(r"\s+", " ", safe_chars).strip() or "uploaded_file"
    safe_ext = re.sub(r"[^a-zA-Z0-9.]", "", ext.lower())
    return safe_chars + safe_ext


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_metadata(image_path):
    try:
        with Image.open(image_path) as image:
            exif = image._getexif()
            metadata = {}
            if exif:
                for tag, value in exif.items():
                    decoded = ExifTags.TAGS.get(tag, tag)
                    metadata[str(decoded)] = str(value)
            metadata["resolution"] = f"{image.width}x{image.height}"
            return metadata
    except Exception:
        return {"resolution": "unknown"}


def get_file_sha256(filepath):
    digest = hashlib.sha256()
    with open(filepath, "rb") as handle:
        for chunk in iter(lambda: handle.read(8192), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _save_upload(file_storage):
    if not file_storage or file_storage.filename == "":
        raise ValueError("No file selected.")
    if not allowed_file(file_storage.filename):
        raise ValueError("Unsupported file type.")

    file_storage.seek(0, os.SEEK_END)
    file_size = file_storage.tell()
    file_storage.seek(0)
    if file_size > MAX_FILE_SIZE:
        raise ValueError("File is larger than 5MB.")

    original_filename = secure_korean_filename(file_storage.filename)
    extension = original_filename.rsplit(".", 1)[1].lower()
    upload_dir = Path(os.getcwd()) / "tmp"
    upload_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{uuid.uuid4().hex}_{datetime.now().strftime('%Y%m%d%H%M%S')}.{extension}"
    file_path = upload_dir / filename
    file_storage.save(file_path)
    return original_filename, extension, str(file_path)


def _record_analysis_session(file_path, original_filename, file_extension, analysis_type, analysis_result):
    session["uploaded_file_path"] = file_path
    session["static_file_path"] = file_path
    session["original_filename"] = original_filename
    session["original_uploaded_filename"] = original_filename
    session["file_extension"] = file_extension
    session["file_stat"] = {"st_size": os.path.getsize(file_path)}
    session["metadata"] = extract_metadata(file_path)
    session["sha256"] = get_file_sha256(file_path)
    session["analysis_type"] = analysis_type
    session["analysis_result"] = analysis_result
    session["last_analysis_file_path"] = file_path
    session["last_analysis_filename"] = original_filename
    session["last_analysis_type"] = analysis_type


def _handle_file_upload_and_analysis(analysis_type):
    try:
        if "file" not in request.files:
            flash("No file was uploaded.")
            return redirect(url_for("main.index"))

        original_filename, file_extension, file_path = _save_upload(request.files["file"])
        analysis_result = analyze_file(file_path, analysis_type, file_extension)
        analysis_result["original_filename"] = original_filename
        analysis_result["file_path"] = file_path
        analysis_result["upload_path"] = file_path
        analysis_result["original_image_path"] = file_path
        _record_analysis_session(file_path, original_filename, file_extension, analysis_type, analysis_result)
        return redirect(url_for("main.results"))
    except Exception as exc:
        current_app.logger.exception("Upload analysis failed")
        flash(f"Analysis failed: {exc}")
        return redirect(url_for("main.index"))


@bp.route("/health")
def health():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "AnsimTalk",
        "version": "0.1.0-oss-candidate",
    }, 200


@bp.route("/")
def index():
    try:
        return render_template("index.html")
    except Exception as exc:
        return f"AnsimTalk is running. Template error: {exc}", 200


@bp.route("/analyze_deepfake", methods=["POST"])
def analyze_deepfake():
    return _handle_file_upload_and_analysis("deepfake")


@bp.route("/analyze_cyberbullying", methods=["POST"])
def analyze_cyberbullying():
    return _handle_file_upload_and_analysis("cyberbullying")


@bp.route("/results")
def results():
    analysis_result = session.get("analysis_result")
    analysis_type = session.get("analysis_type")
    if not analysis_result:
        flash("No analysis result is available.")
        return redirect(url_for("main.index"))
    return render_template("results.html", result=analysis_result, analysis_type=analysis_type)


@bp.route("/evidence")
def evidence():
    return render_template("evidence.html")


@bp.route("/deepfake_help")
def deepfake_help():
    return render_template("deepfake_help.html")


@bp.route("/cyberbullying_help")
def cyberbullying_help():
    return render_template("cyberbullying_help.html")


@bp.route("/download_pdf")
def download_pdf():
    analysis_result = session.get("analysis_result")
    analysis_type = session.get("analysis_type")
    if not analysis_result:
        flash("No analysis result is available.")
        return redirect(url_for("main.index"))

    pdf_path = str(Path(os.getcwd()) / "tmp" / f"evidence_{uuid.uuid4().hex}.pdf")
    generate_pdf_report(analysis_result, pdf_path, analysis_type)
    return send_file(pdf_path, as_attachment=True, download_name=Path(pdf_path).name)


@bp.route("/reset")
def reset():
    for key in ("uploaded_file_path", "static_file_path", "last_analysis_file_path"):
        file_path = session.get(key)
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
            except OSError:
                current_app.logger.warning("Failed to remove temporary file: %s", file_path)
    session.clear()
    return redirect(url_for("main.index"))


@bp.route("/api/health", methods=["GET"])
def api_health():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()}), 200


def _api_analyze(analysis_type):
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file was uploaded."}), 400

        original_filename, file_extension, file_path = _save_upload(request.files["file"])
        analysis_result = analyze_file(file_path, analysis_type, file_extension)
        analysis_result["original_filename"] = original_filename
        analysis_result["file_path"] = file_path
        analysis_result["upload_path"] = file_path
        analysis_result["original_image_path"] = file_path
        _record_analysis_session(file_path, original_filename, file_extension, analysis_type, analysis_result)
        return jsonify(analysis_result), 200
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception as exc:
        current_app.logger.exception("API analysis failed")
        return jsonify({"error": f"Analysis failed: {exc}"}), 500


@bp.route("/api/analyze_deepfake", methods=["POST"])
def api_analyze_deepfake():
    return _api_analyze("deepfake")


@bp.route("/api/analyze_cyberbullying", methods=["POST"])
def api_analyze_cyberbullying():
    return _api_analyze("cyberbullying")


@bp.route("/api/download_pdf", methods=["POST"])
def api_download_pdf():
    payload = request.get_json(silent=True) or {}
    analysis_result = payload.get("analysis_result")
    if not analysis_result:
        return jsonify({"error": "No analysis result was provided."}), 400
    if any(field in analysis_result for field in CLIENT_PATH_FIELD_NAMES):
        return jsonify({"error": "Client-supplied file paths are not allowed."}), 400

    analysis_type = payload.get("analysis_type", analysis_result.get("analysis_type", "unknown"))
    pdf_path = str(Path(os.getcwd()) / "tmp" / f"evidence_{uuid.uuid4().hex}.pdf")
    Path(pdf_path).parent.mkdir(parents=True, exist_ok=True)
    generate_pdf_report(analysis_result, pdf_path, analysis_type)
    return send_file(pdf_path, mimetype="application/pdf", as_attachment=True, download_name=Path(pdf_path).name)
