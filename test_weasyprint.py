from pathlib import Path


def test_weasyprint_can_generate_pdf(tmp_path):
    from weasyprint import HTML
    from weasyprint.text.fonts import FontConfiguration

    output_path = tmp_path / "test_output.pdf"
    html = """
    <!doctype html>
    <html>
      <head><meta charset="utf-8"><title>AnsimTalk PDF Smoke</title></head>
      <body><h1>AnsimTalk PDF Smoke</h1><p>Sample report text.</p></body>
    </html>
    """

    HTML(string=html, base_url=str(Path(__file__).parent)).write_pdf(
        str(output_path),
        font_config=FontConfiguration(),
    )

    assert output_path.exists()
    assert output_path.stat().st_size > 1000


def test_font_files_exist():
    font_dir = Path(__file__).parent / "app" / "static" / "fonts"

    assert (font_dir / "NanumGothic.ttf").exists()
    assert (font_dir / "NanumGothic-Bold.ttf").exists()
