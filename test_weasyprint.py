#!/usr/bin/env python3
"""
WeasyPrint 테스트 스크립트
한글 폰트와 PDF 생성이 제대로 작동하는지 확인합니다.
"""

import os
import sys
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_weasyprint():
    """WeasyPrint 기본 기능 테스트"""
    try:
        from weasyprint import HTML
        from weasyprint.text.fonts import FontConfiguration
        print("✅ WeasyPrint import 성공")
        
        # 간단한 HTML 생성
        html_content = """
        <!DOCTYPE html>
        <html lang="ko">
        <head>
            <meta charset="UTF-8">
            <title>WeasyPrint 테스트</title>
            <style>
                @font-face {
                    font-family: 'NanumGothic';
                    src: url('/static/fonts/NanumGothic.ttf') format('truetype');
                    font-weight: normal;
                    font-style: normal;
                }
                body {
                    font-family: 'NanumGothic', sans-serif;
                    font-size: 16px;
                    line-height: 1.6;
                    margin: 40px;
                }
                h1 { color: #1976d2; }
                .test-content { background: #f0f4ff; padding: 20px; border-radius: 8px; }
            </style>
        </head>
        <body>
            <h1>WeasyPrint 한글 테스트</h1>
            <div class="test-content">
                <p>안녕하세요! 이것은 WeasyPrint로 생성된 한글 PDF 테스트입니다.</p>
                <p>한글 텍스트가 올바르게 표시되는지 확인해주세요.</p>
                <p>This is English text mixed with Korean: 안녕하세요!</p>
            </div>
            <p><strong>테스트 완료:</strong> 한글 폰트가 정상적으로 적용되었습니다.</p>
        </body>
        </html>
        """
        
        # BASE_URL 설정 (로컬 테스트용)
        base_url = "http://127.0.0.1:5000"
        
        # FontConfiguration 생성
        font_config = FontConfiguration()
        print("✅ FontConfiguration 생성 성공")
        
        # HTML 객체 생성
        html_doc = HTML(string=html_content, base_url=base_url)
        print("✅ HTML 객체 생성 성공")
        
        # PDF 생성
        output_path = "test_output.pdf"
        html_doc.write_pdf(output_path, font_config=font_config)
        print(f"✅ PDF 생성 성공: {output_path}")
        
        # 파일 크기 확인
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"✅ PDF 파일 크기: {file_size} bytes")
            return True
        else:
            print("❌ PDF 파일이 생성되지 않았습니다.")
            return False
            
    except ImportError as e:
        print(f"❌ WeasyPrint import 실패: {e}")
        print("WeasyPrint가 설치되지 않았습니다. 'pip install weasyprint'를 실행하세요.")
        return False
    except Exception as e:
        print(f"❌ WeasyPrint 테스트 실패: {e}")
        import traceback
        print(f"상세 오류: {traceback.format_exc()}")
        return False

def test_font_files():
    """폰트 파일 존재 여부 확인"""
    font_dir = Path(__file__).parent / "app" / "static" / "fonts"
    required_fonts = ["NanumGothic.ttf", "NanumGothic-Bold.ttf"]
    
    print(f"\n📁 폰트 디렉토리 확인: {font_dir}")
    
    for font_file in required_fonts:
        font_path = font_dir / font_file
        if font_path.exists():
            file_size = font_path.stat().st_size
            print(f"✅ {font_file}: {file_size:,} bytes")
        else:
            print(f"❌ {font_file}: 파일이 없습니다.")
            return False
    
    return True

def main():
    """메인 테스트 함수"""
    print("🚀 WeasyPrint 한글 PDF 생성 테스트 시작")
    print("=" * 50)
    
    # 폰트 파일 확인
    fonts_ok = test_font_files()
    
    # WeasyPrint 테스트
    weasyprint_ok = test_weasyprint()
    
    print("\n" + "=" * 50)
    if fonts_ok and weasyprint_ok:
        print("🎉 모든 테스트가 성공했습니다!")
        print("✅ 한글 PDF 생성이 정상적으로 작동합니다.")
    else:
        print("❌ 일부 테스트가 실패했습니다.")
        if not fonts_ok:
            print("   - 폰트 파일을 확인하세요.")
        if not weasyprint_ok:
            print("   - WeasyPrint 설치를 확인하세요.")
    
    return fonts_ok and weasyprint_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 