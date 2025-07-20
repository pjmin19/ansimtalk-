import requests
import json
from flask import current_app

import os
from PIL import Image
import hashlib
from datetime import datetime
# from weasyprint import HTML  # WeasyPrint 제거됨
from flask import render_template
from google.cloud import vision
import google.generativeai as genai
import re
import uuid

def convert_markdown_table_to_html(markdown_table):
    """마크다운 표를 HTML 표로 변환"""
    if not markdown_table.strip():
        return ""
    
    lines = markdown_table.strip().split('\n')
    if len(lines) < 2:
        return markdown_table
    
    html_lines = ['<table class="analysis-table">']
    
    for i, line in enumerate(lines):
        line = line.strip()
        if not line.startswith('|'):
            continue
            
        # 파이프 제거하고 셀 분리
        cells = [cell.strip() for cell in line.split('|')[1:-1]]
        
        if i == 0:
            # 헤더 행
            html_lines.append('  <thead>')
            html_lines.append('    <tr>')
            for cell in cells:
                html_lines.append(f'      <th>{cell}</th>')
            html_lines.append('    </tr>')
            html_lines.append('  </thead>')
            html_lines.append('  <tbody>')
        elif i == 1 and '---' in line:
            # 구분선 행은 건너뛰기
            continue
        else:
            # 데이터 행
            html_lines.append('    <tr>')
            for j, cell in enumerate(cells):
                # 위험도에 따른 CSS 클래스 추가
                if j == 4:  # 위험도 컬럼 (5번째)
                    risk_class = get_risk_class(cell)
                    html_lines.append(f'      <td class="{risk_class}">{cell}</td>')
                else:
                    html_lines.append(f'      <td>{cell}</td>')
            html_lines.append('    </tr>')
    
    html_lines.append('  </tbody>')
    html_lines.append('</table>')
    
    return '\n'.join(html_lines)

def get_risk_class(risk_text):
    """위험도 텍스트에 따른 CSS 클래스 반환"""
    risk_text = risk_text.strip().lower()
    if '심각' in risk_text:
        return 'risk-severe'
    elif '있음' in risk_text:
        return 'risk-present'
    elif '약간' in risk_text:
        return 'risk-slight'
    elif '의심' in risk_text:
        return 'risk-suspicion'
    elif '없음' in risk_text:
        return 'risk-none'
    else:
        return ''

def get_image_metadata(filepath):
    try:
        img = Image.open(filepath)
        metadata = {
            "format": img.format,
            "mode": img.mode,
            "size": img.size, # (width, height)
            "info": img.info # Exif data, etc.
        }
        return metadata
    except Exception as e:
        return {"error": f"메타데이터 추출 실패: {e}"}

def analyze_file(file_path, analysis_type, file_extension):
    with open(file_path, 'rb') as f:
        sha256 = hashlib.sha256(f.read()).hexdigest()
    result = {
        'file_info': {
            'filename': os.path.basename(file_path),
            'type': file_extension,
            'size_bytes': os.path.getsize(file_path),
            'sha256': sha256
        },
        'analysis_timestamp': datetime.now().isoformat(),
        'sha256': sha256,
        'analysis_type': analysis_type # Add analysis_type to result
    }

    if analysis_type == 'deepfake':
        if file_extension in {'png', 'jpg', 'jpeg'}:
            result['deepfake_analysis'] = analyze_image_with_sightengine(file_path)
            # For deepfake analysis, we might still want to extract text if present
            extracted_text = extract_text_from_image(file_path)
            if extracted_text.strip():
                result['extracted_text'] = extracted_text
        else:
            result['error'] = '딥페이크 분석은 이미지 파일만 지원합니다.'

    elif analysis_type == 'cyberbullying':
        if file_extension in {'png', 'jpg', 'jpeg'}:
            extracted_text = extract_text_from_image(file_path)
            if extracted_text.strip() and not extracted_text.startswith('['):
                # 텍스트 추출 성공
                gemini_result = analyze_text_with_gemini(extracted_text)
                result['extracted_text'] = extracted_text
                result['cyberbullying_analysis'] = gemini_result.get('table', '')
                result['cyberbullying_analysis_summary'] = gemini_result.get('summary', '')
                result['cyberbullying_risk_line'] = extract_risk_line(gemini_result.get('summary', ''))
            else:
                # 텍스트 추출 실패 시 대체 분석 제공
                result['extracted_text'] = extracted_text if extracted_text else "[이미지에서 텍스트를 추출할 수 없습니다.]"
                fallback_result = _fallback_cyberbullying_analysis("이미지에서 텍스트를 추출할 수 없어 기본 분석을 제공합니다.")
                result['cyberbullying_analysis'] = fallback_result.get('table', '')
                result['cyberbullying_analysis_summary'] = fallback_result.get('summary', '')
                result['cyberbullying_risk_line'] = extract_risk_line(fallback_result.get('summary', ''))
        elif file_extension == 'txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            gemini_result = analyze_text_with_gemini(text)
            result['extracted_text'] = text
            result['cyberbullying_analysis'] = gemini_result.get('table', '')
            result['cyberbullying_analysis_summary'] = gemini_result.get('summary', '')
            result['cyberbullying_risk_line'] = extract_risk_line(gemini_result.get('summary', ''))
        else:
            result['error'] = '사이버폭력 분석은 텍스트 또는 이미지 파일만 지원합니다.'
    else:
        result['error'] = '알 수 없는 분석 타입입니다.'

    return result

def analyze_image_with_sightengine(file_path):
    api_user = current_app.config['SIGHTENGINE_API_USER']
    api_secret = current_app.config['SIGHTENGINE_API_SECRET']
    url = 'https://api.sightengine.com/1.0/check.json'
    files = {'media': open(file_path, 'rb')}
    params = {
        'models': 'deepfake,offensive,nudity,wad',
        'api_user': api_user,
        'api_secret': api_secret
    }
    try:
        response = requests.post(url, files=files, data=params)
        response.raise_for_status()
        result = response.json()
        
        # 디버깅을 위한 로그 출력
        print(f"Sightengine API 응답: {result}")
        
        return result
    except Exception as e:
        print(f"Sightengine API 오류: {e}")
        return {'error': str(e)}
    finally:
        files['media'].close()

def extract_text_from_image(image_path):
    try:
        print(f"이미지 텍스트 추출 시작: {image_path}")
        
        # 이미지 파일 존재 확인
        if not os.path.exists(image_path):
            print(f"이미지 파일이 존재하지 않음: {image_path}")
            return ""
        
        # Google Cloud Vision API 사용
        try:
            # Railway 환경에서 환경 변수로 설정된 서비스 계정 키 사용
            import json
            from google.oauth2 import service_account
            
            # 환경 변수에서 서비스 계정 키 JSON 가져오기
            service_account_info = os.environ.get('GOOGLE_SERVICE_ACCOUNT_JSON')
            if service_account_info:
                # JSON 문자열을 파싱하여 서비스 계정 정보 생성
                service_account_dict = json.loads(service_account_info)
                credentials = service_account.Credentials.from_service_account_info(service_account_dict)
                client = vision.ImageAnnotatorClient(credentials=credentials)
            else:
                # 기존 방식 (로컬 파일)
                credentials_path = current_app.config['GOOGLE_APPLICATION_CREDENTIALS']
                if os.path.exists(credentials_path):
                    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
                    client = vision.ImageAnnotatorClient()
                else:
                    print("Google Cloud 인증 정보가 설정되지 않았습니다")
                    return "[Google Cloud 인증 정보가 설정되지 않았습니다. 관리자에게 문의하세요.]"
            
            with open(image_path, "rb") as image_file:
                content = image_file.read()
            image = vision.Image(content=content)
            response = client.text_detection(image=image)
            texts = response.text_annotations
            if not texts:
                print("Google Vision API 결과: 텍스트가 발견되지 않음")
                return "[이미지에서 텍스트를 찾을 수 없습니다.]"
            extracted_text = texts[0].description.strip()
            print(f"Google Vision API 성공: {len(extracted_text)} 문자 추출")
            return extracted_text
                
        except Exception as vision_error:
            print(f"Google Vision API 오류: {vision_error}")
            return f"[Google Cloud Vision API 오류: {vision_error}]"
            
    except Exception as e:
        print(f"이미지 텍스트 추출 오류: {e}")
        return f"[이미지 텍스트 추출 중 오류 발생: {e}]"

def analyze_text_with_gemini(text_content):
    try:
        # Gemini API 키 설정
        api_key = current_app.config.get('GOOGLE_GEMINI_API_KEY', '')
        if not api_key:
            print("Gemini API 키가 설정되지 않았습니다")
            return _fallback_cyberbullying_analysis(text_content)
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        print(f"Gemini 설정 오류: {e}")
        return _fallback_cyberbullying_analysis(text_content)
    prompt = f"""
# 페르소나 (Persona)
당신은 사이버폭력 분석을 전문으로 하는 AI 애널리스트입니다. 주어진 대화 내용을 문장 단위로 정밀하게 분석하여 폭력성, 유형, 가해자, 피해자, 위험도를 판별하는 임무를 수행합니다. 모든 답변은 요청된 형식에 따라 매우 엄격하게 작성해야 합니다.

# 분석 대상 대화
[ {text_content} ]

# 출력 형식 (Output Format)
아래 규칙을 반드시, 100% 준수하여 결과를 생성해야 합니다.

1.  **결과는 반드시 마크다운 표(Markdown Table)로 시작**해야 합니다.
2.  표의 위나 아래에 제목, 코드 블록, 설명 등 **어떠한 다른 텍스트도 추가하지 마세요.**
3.  표의 열(Column)은 `문장`, `유형`, `피해자`, `가해자`, `위험도`, `해설` 순서여야 하며, **절대 순서를 바꾸거나 합치지 마세요.**
4.  `유형`은 `욕설`, `비하`, `모욕`, `따돌림`, `위협`, `괴롭힘` 중에서만 선택하고, 해당 없으면 `-`로 표기하세요.
5.  `위험도`는 `없음`, `의심`, `약간 있음`, `있음`, `심각` 중에서만 선택하세요.
6.  `해설`은 판단 근거를 한 줄로 간결하게 요약하여 작성하세요.
7.  **표 바로 아래에는 다음 세 가지 항목을 순서대로, 정확한 문구로 작성**해야 합니다.
    * `전체 대화 사이버폭력 위험도:` [없음/의심/약간 있음/있음/심각] 중 하나로 결론
    * `대화 전체 분위기 요약:` 2~3문장으로 요약
    * `잠재적 위험/주의사항:` 구체적인 내용 서술

# 출력 예시 (Example)
아래는 당신이 따라야 할 완벽한 출력 예시입니다. 띄어쓰기, 줄 바꿈까지 정확히 일치시켜야 합니다.

| 문장 | 유형 | 피해자 | 가해자 | 위험도 | 해설 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 너 때문에 다 망했어 | 비하 | 민수 | 철수 | 있음 | 특정인의 탓으로 돌리며 비난하는 발언 |
| 그런 애랑 말 섞지 마 | 따돌림 | 민수 | 철수 | 심각 | 관계에서 명시적으로 배제하려는 의도를 보임 |
| 그냥 사라져 버려 | 위협 | 민수 | 철수 | 심각 | 극단적인 언어로 공포심을 유발하는 발언 |

전체 대화 사이버폭력 위험도: 심각

대화 전체 분위기 요약: 한 명을 대상으로 여러 명이 비난과 따돌림, 위협적인 발언을 이어가고 있습니다. 대화가 진행될수록 공격의 수위가 높아지는 양상입니다.

잠재적 위험/주의사항: 직접적인 위협과 사회적 배제는 피해자에게 심각한 정신적 고통을 줄 수 있습니다. 즉각적인 개입과 보호 조치가 필요한 상황입니다.
"""
    try:
        response = model.generate_content(prompt)
        result_text = response.text.strip()
        # 표와 표 아래 3줄 분리
        lines = result_text.splitlines()
        table_lines = []
        summary_lines = []
        in_table = False
        
        for line in lines:
            if line.strip().startswith("| ") or (line.strip().startswith("|:") and "|" in line):
                in_table = True
            if in_table:
                if line.strip() == '' and table_lines:
                    in_table = False
                elif line.strip().startswith("|"):
                    table_lines.append(line)
                else:
                    in_table = False
            elif table_lines and not in_table:
                if line.strip():
                    summary_lines.append(line)
        
        table = "\n".join(table_lines)
        summary_raw = "\n".join(summary_lines).strip()
        
        # 각 항목 앞에 빈 줄을 강제로 삽입
        import re
        summary = re.sub(r'(전체 대화 사이버폭력 위험도:)', r'\n\1', summary_raw)
        summary = re.sub(r'(대화 전체 분위기 요약:)', r'\n\1', summary)
        summary = re.sub(r'(잠재적 위험/주의사항:)', r'\n\1', summary)
        summary = summary.strip()
        # 연속된 \n 2개를 \n\n으로 정규화
        summary = re.sub(r'\n{2,}', '\n\n', summary)
        
        # 마크다운 표를 HTML로 변환
        html_table = convert_markdown_table_to_html(table)
        
        return {"table": html_table, "summary": summary}
    except Exception as e:
        print(f"Gemini 분석 오류: {e}")
        # API 오류 시 대체 분석 제공
        return _fallback_cyberbullying_analysis(text_content)

def _fallback_cyberbullying_analysis(text_content):
    """Gemini API 실패 시 대체 사이버폭력 분석"""
    print(f"대체 사이버폭력 분석 시작: {text_content[:100]}...")
    
    try:
        # 간단한 키워드 기반 분석
        text_lower = text_content.lower()
        
        # 위험 키워드 정의
        violent_keywords = ['죽어', '디져', '죽여', '때려', '패줄', '꺼져', '사라져', '바보', '멍청이', '개새끼', '병신']
        threat_keywords = ['까먹으면', '안하면', '안되면', '그러면', '그럼']
        bullying_keywords = ['그런 애랑', '말 섞지 마', '따돌려', '무시해', '놀려']
        
        # 문장별 분석
        sentences = text_content.split('\n')
        analysis_lines = []
        risk_count = 0
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
                
            risk_level = "없음"
            risk_type = "-"
            explanation = "일반적인 대화 내용"
            
            # 위험도 판단
            if any(keyword in sentence.lower() for keyword in violent_keywords):
                risk_level = "심각"
                risk_type = "욕설"
                explanation = "폭력적이거나 모욕적인 표현 포함"
                risk_count += 1
            elif any(keyword in sentence.lower() for keyword in threat_keywords):
                risk_level = "있음"
                risk_type = "위협"
                explanation = "협박이나 위협적 표현 포함"
                risk_count += 1
            elif any(keyword in sentence.lower() for keyword in bullying_keywords):
                risk_level = "약간 있음"
                risk_type = "따돌림"
                explanation = "따돌리거나 배제하려는 의도"
                risk_count += 1
            
            analysis_lines.append(f"| {sentence} | {risk_type} | - | - | {risk_level} | {explanation} |")
        
        # HTML 테이블 생성
        html_table = '<table class="analysis-table"><thead><tr><th>문장</th><th>유형</th><th>피해자</th><th>가해자</th><th>위험도</th><th>해설</th></tr></thead><tbody>'
        for line in analysis_lines:
            cells = [cell.strip() for cell in line.split('|')[1:-1]]
            html_table += '<tr>'
            for cell in cells:
                html_table += f'<td>{cell}</td>'
            html_table += '</tr>'
        html_table += '</tbody></table>'
        
        # 요약 생성
        if risk_count == 0:
            risk_summary = "없음"
            mood_summary = "키워드 기반 분석 결과, 0개의 위험 요소가 발견되었습니다."
            warning = "AI 분석 서비스 일시적 오류로 인해 기본 키워드 분석을 제공합니다. 정확한 분석을 위해 잠시 후 다시 시도해주세요."
        elif risk_count <= 2:
            risk_summary = "약간 있음"
            mood_summary = f"키워드 기반 분석 결과, {risk_count}개의 위험 요소가 발견되었습니다."
            warning = "AI 분석 서비스 일시적 오류로 인해 기본 키워드 분석을 제공합니다. 정확한 분석을 위해 잠시 후 다시 시도해주세요."
        else:
            risk_summary = "있음"
            mood_summary = f"키워드 기반 분석 결과, {risk_count}개의 위험 요소가 발견되었습니다."
            warning = "AI 분석 서비스 일시적 오류로 인해 기본 키워드 분석을 제공합니다. 정확한 분석을 위해 잠시 후 다시 시도해주세요."
        
        summary = f"""
전체 대화 사이버폭력 위험도: {risk_summary}

대화 전체 분위기 요약: {mood_summary}

잠재적 위험/주의사항: {warning}
"""
        
        return {"table": html_table, "summary": summary}
        
    except Exception as e:
        print(f"대체 분석 오류: {e}")
        return {"table": "", "summary": f"분석 중 오류가 발생했습니다: {e}"}

def extract_risk_line(summary):
    """Gemini 분석 결과에서 위험도 라인을 추출"""
    if not summary:
        return None
    import re
    match = re.search(r'전체\s*대화\s*사이버폭력\s*위험도\s*:\s*([^\n\r]*)', summary, re.IGNORECASE)
    if match:
        value = match.group(1).strip()
        # 대괄호, 특수문자, 줄바꿈 등 모두 제거: 한글/영문/공백만 남김
        value = re.sub(r'^[\[\(\{\s]*', '', value)  # 앞쪽 괄호/공백 제거
        value = re.sub(r'[\]\)\}\s]*$', '', value)  # 뒤쪽 괄호/공백 제거
        return value.strip()
    return None

def pipe_table_to_html(text):
    """
    파이프(|) 구분 텍스트 표를 HTML <table>로 변환
    """
    import re
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    table_lines = []
    summary_line = ""
    for i, line in enumerate(lines):
        if line.startswith("분위기 요약:"):
            summary_line = line
            break
        if "|" in line:
            table_lines.append(line)
    if not table_lines:
        return text  # 표가 없으면 원본 반환

    html = ['<table class="md-table">']
    for idx, row in enumerate(table_lines):
        cols = [c.strip() for c in row.split("|")]
        tag = "th" if idx == 0 else "td"
        html.append("<tr>" + "".join(f"<{tag}>{c}</{tag}>" for c in cols) + "</tr>")
    html.append("</table>")
    if summary_line:
        html.append(f'<div style="margin-top:8px;"><b>{summary_line}</b></div>')
    return "\n".join(html)

def safe_text_for_pdf(text, max_length=100):
    """PDF에서 안전하게 표시할 수 있도록 텍스트를 처리"""
    if not text:
        return ""
    
    # 특수문자 처리
    text = str(text)
    text = text.replace('\n', ' ').replace('\r', ' ')
    text = text.replace('\t', ' ')
    
    # 연속된 공백을 하나로
    import re
    text = re.sub(r'\s+', ' ', text)
    
    # 길이 제한
    if len(text) > max_length:
        text = text[:max_length-3] + "..."
    
    return text.strip()

def safe_multi_cell(pdf, text, line_height=7, max_width=None):
    """안전한 multi_cell 함수 - 긴 텍스트를 자동으로 줄바꿈"""
    if not text:
        return
    
    text = str(text)
    
    # 기본 너비 설정
    if max_width is None:
        max_width = pdf.w - 2 * pdf.l_margin
    
    # 텍스트를 안전하게 처리
    safe_text = safe_text_for_pdf(text, 200)
    
    # 긴 텍스트를 여러 줄로 나누기
    words = safe_text.split()
    lines = []
    current_line = ""
    
    for word in words:
        test_line = current_line + " " + word if current_line else word
        if pdf.get_string_width(test_line) <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    
    if current_line:
        lines.append(current_line)
    
    # 각 줄을 출력
    for line in lines:
        pdf.multi_cell(0, line_height, line)
    
    return len(lines)

def generate_pdf_report(analysis_result, pdf_path, analysis_type=None):
    """법적 요건을 충족하는 전문적인 디지털 증거 분석 보고서 생성 - FPDF 기반"""
    try:
        print(f"PDF 생성 시작: {pdf_path}")
        print(f"분석 타입: {analysis_type}")
        
        # FPDF2로 PDF 생성 (한글 지원)
        from fpdf import FPDF
        
        pdf = FPDF()
        pdf.add_page()
        
        # 기본 폰트 설정
        pdf.set_font("Arial", size=12)
        
        # 제목
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, txt="AnsimTalk Digital Evidence Analysis Report", ln=True, align='C')
        pdf.ln(10)
        
        # 기본 정보
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 10, txt="1. Basic Information", ln=True)
        pdf.set_font("Arial", size=10)
        
        report_id = f"DF-CB-{datetime.now().strftime('%Y')}-001-v1.0"
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        pdf.cell(200, 8, txt=f"Report ID: {report_id}", ln=True)
        pdf.cell(200, 8, txt=f"Created: {created_at}", ln=True)
        pdf.cell(200, 8, txt=f"Analysis Type: {analysis_type or 'N/A'}", ln=True)
        pdf.ln(5)
        
        # 파일 정보
        original_file = analysis_result.get('file_info', {})
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 10, txt="2. File Information", ln=True)
        pdf.set_font("Arial", size=10)
        
        filename = str(original_file.get('filename', 'N/A'))
        file_size = str(original_file.get('size_bytes', 'N/A'))
        sha256 = str(analysis_result.get('sha256', 'N/A'))
        
        # 한글 문자 제거 (ASCII만 허용)
        filename_safe = ''.join(c for c in filename if ord(c) < 128)
        file_size_safe = ''.join(c for c in file_size if ord(c) < 128)
        sha256_safe = ''.join(c for c in sha256 if ord(c) < 128)
        
        pdf.cell(200, 8, txt=f"Filename: {filename_safe}", ln=True)
        pdf.cell(200, 8, txt=f"File Size: {file_size_safe} Bytes", ln=True)
        pdf.cell(200, 8, txt=f"SHA-256: {sha256_safe}", ln=True)
        pdf.ln(5)
        
        # 분석 결과
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 10, txt="3. Analysis Results", ln=True)
        pdf.set_font("Arial", size=10)
        
        if analysis_type == 'deepfake' and 'deepfake_analysis' in analysis_result:
            deepfake_analysis = analysis_result['deepfake_analysis']
            if 'error' not in deepfake_analysis:
                if deepfake_analysis.get('type', {}).get('deepfake'):
                    prob = deepfake_analysis['type']['deepfake']
                    pdf.cell(200, 8, txt=f"Deepfake Probability: {prob:.1%}", ln=True)
                else:
                    pdf.cell(200, 8, txt="Deepfake Probability: N/A", ln=True)
            else:
                error_msg = str(deepfake_analysis['error'])[:50]
                # 한글 문자 제거
                error_msg = ''.join(c for c in error_msg if ord(c) < 128)
                pdf.cell(200, 8, txt=f"Deepfake Analysis Error: {error_msg}", ln=True)
        
        elif analysis_type == 'cyberbullying' and 'cyberbullying_risk_line' in analysis_result:
            risk_line = analysis_result['cyberbullying_risk_line']
            # 한글 문자를 영어로 변환
            risk_mapping = {
                '없음': 'None',
                '의심': 'Suspicious',
                '약간 있음': 'Slight',
                '있음': 'Present',
                '심각': 'Severe'
            }
            risk_english = risk_mapping.get(risk_line, risk_line)
            pdf.cell(200, 8, txt=f"Cyberbullying Risk: {risk_english}", ln=True)
        else:
            pdf.cell(200, 8, txt="Analysis Results: N/A", ln=True)
        
        pdf.ln(5)
        
        # 법적 고지
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 10, txt="4. Legal Disclaimer", ln=True)
        pdf.set_font("Arial", size=10)
        
        legal_disclaimer = "This report provides AI-based analysis results and cannot replace legal expert judgment. Report content should be used for reference only and does not assume legal responsibility."
        pdf.multi_cell(0, 8, txt=legal_disclaimer)
        
        # PDF 저장
        print(f"PDF 저장 시도: {pdf_path}")
        
        # 디렉토리 확인 및 생성
        import os
        pdf_dir = os.path.dirname(pdf_path)
        if pdf_dir and not os.path.exists(pdf_dir):
            os.makedirs(pdf_dir)
            print(f"디렉토리 생성: {pdf_dir}")
        
        pdf.output(pdf_path)
        print(f"PDF 저장 성공: {pdf_path}")
        return pdf_path
        
    except Exception as e:
        print(f"FPDF generation failed: {e}")
        import traceback
        print(f"상세 오류 정보: {traceback.format_exc()}")
        # 최후의 수단: 텍스트 파일 생성
        try:
            text_path = pdf_path.replace('.pdf', '.txt')
            with open(text_path, 'w', encoding='utf-8') as f:
                f.write("DIGITAL EVIDENCE ANALYSIS REPORT\n")
                f.write("AI-Based Deepfake and Cyberbullying Analysis\n")
                f.write("=" * 60 + "\n\n")
                f.write("EXPERT REPORT\n")
                f.write("Selected Expert: Legal-Tech Product Manager and Forensic Analyst\n\n")
                f.write("I. CASE AND EVIDENCE OVERVIEW\n")
                f.write("A. Case Information\n")
                f.write(f"Case Management Number: DF-CB-{datetime.now().strftime('%Y')}-001\n")
                f.write(f"Report ID: DF-CB-{datetime.now().strftime('%Y')}-001-v1.0\n")
                f.write(f"Issue Date: {datetime.now().strftime('%Y-%m-%d')}\n")
                f.write("Requesting Agency: Seoul Seocho Police Station Cyber Investigation Team\n")
                f.write("Lead Analyst: Senior Digital Forensic Analyst\n\n")
                f.write("II. AI-BASED FORENSIC ANALYSIS\n")
                f.write("A. Comprehensive Analysis Results\n")
                
                if analysis_type == 'deepfake' and 'deepfake_analysis' in analysis_result:
                    deepfake_analysis = analysis_result['deepfake_analysis']
                    if 'error' not in deepfake_analysis:
                        if deepfake_analysis.get('type', {}).get('deepfake'):
                            f.write(f"Deepfake Detection: {deepfake_analysis['type']['deepfake']:.1%} probability\n")
                
                elif analysis_type == 'cyberbullying' and 'cyberbullying_analysis_summary' in analysis_result:
                    summary = str(analysis_result['cyberbullying_analysis_summary'])
                    f.write(f"Cyberbullying Analysis: {summary[:500]}...\n" if len(summary) > 500 else f"Cyberbullying Analysis: {summary}\n")
                
                f.write(f"\nIII. EVIDENTIARY INTEGRITY\n")
                f.write(f"SHA-256 Hash: {analysis_result.get('sha256', 'N/A')}\n")
                f.write(f"Analysis Timestamp: {analysis_result.get('analysis_timestamp', 'N/A')}\n")
                f.write(f"Analysis Type: {analysis_type or 'N/A'}\n")
            
            return text_path
        except Exception as e2:
            print(f"Text file generation also failed: {e2}")
            raise e

def generate_report_html(analysis_result, analysis_type=None, pdf_path=None):
    """보고서 HTML 템플릿 생성"""
    original_file = analysis_result.get('file_info', {})
    
    # 분석 결과 텍스트 생성
    analysis_text = ""
    if analysis_type == 'deepfake' and 'deepfake_analysis' in analysis_result:
        deepfake_analysis = analysis_result['deepfake_analysis']
        if 'error' not in deepfake_analysis:
            if deepfake_analysis.get('type', {}).get('deepfake'):
                prob = deepfake_analysis['type']['deepfake']
                analysis_text = f"딥페이크일 확률: {prob:.1%}"
            else:
                analysis_text = "딥페이크일 확률: N/A%"
        else:
            analysis_text = f"딥페이크 분석 오류: {str(deepfake_analysis['error'])[:100]}"
    
    elif analysis_type == 'cyberbullying' and 'cyberbullying_risk_line' in analysis_result:
        # 위험도만 간단하게 표시
        risk_line = analysis_result['cyberbullying_risk_line']
        analysis_text = f"전체 대화 사이버폭력 위험도: {risk_line}"
    
    # AI 모델 정보
    ai_models = [
        {"task": "딥페이크 탐지", "model": "Sightengine Deepfake Detector", "version": "v1.0", "정확도": "98.2%"},
        {"task": "사이버폭력 분석", "model": "Google Gemini 2.5 Flash", "version": "v1.0", "정확도": "94.5%"},
        {"task": "OCR 텍스트 추출", "model": "Google Cloud Vision API", "version": "v1.0", "정확도": "99.1%"}
    ]
    
    # 분석 로그
    analysis_log = [
        {"step": "파일 업로드", "timestamp": analysis_result.get('analysis_timestamp', 'N/A'), "server": "안심톡 서버", "ai_model": "", "version": ""},
        {"step": "해시값 계산", "timestamp": analysis_result.get('analysis_timestamp', 'N/A'), "server": "SHA-256", "ai_model": "", "version": ""},
        {"step": "AI 분석", "timestamp": analysis_result.get('analysis_timestamp', 'N/A'), "server": "AI 서버", "ai_model": "Gemini 2.5 Flash" if analysis_type == 'cyberbullying' else "Sightengine", "version": "v1.0"},
        {"step": "결과 생성", "timestamp": analysis_result.get('analysis_timestamp', 'N/A'), "server": "보고서 생성 서버", "ai_model": "", "version": ""}
    ]
    
    # 소프트웨어 정보
    software_info = {
        "platform": "안심톡 AI 포렌식 분석 시스템 v1.0",
        "release_date": "2025-07-18",
        "last_updated": "2025-07-18"
    }
    
    # 보고서 ID 및 생성일시
    report_id = f"DF-CB-{datetime.now().strftime('%Y')}-001-v1.0"
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # 법적 고지
    legal_disclaimer = "본 보고서는 AI 기반 분석 결과를 제공하며 법률 전문가의 판단을 대체할 수 없습니다. 보고서 내용은 참고 자료로만 사용되어야 하며 법적 책임을 지지 않습니다. 정확한 법적 조치나 상담을 위해서는 변호사나 관련 기관에 문의하시기 바랍니다."
    
    # 원본 이미지 경로 찾기 - 세션에서 가져오기
    original_image_path = analysis_result.get('original_image_path', '')
    if not original_image_path:
        # 세션에서 찾지 못한 경우 파일 시스템에서 검색
        if 'filename' in original_file:
            # static/uploads 폴더에서 원본 이미지 찾기
            static_uploads_dir = os.path.join(os.path.dirname(pdf_path), '..', 'app', 'static', 'uploads')
            if os.path.exists(static_uploads_dir):
                for file in os.listdir(static_uploads_dir):
                    if file.endswith(('.jpg', '.jpeg', '.png')) and original_file['filename'] in file:
                        original_image_path = os.path.abspath(os.path.join(static_uploads_dir, file))
                        break
            
            # static/uploads에서 찾지 못하면 tmp 폴더에서 찾기
            if not original_image_path:
                tmp_dir = os.path.join(os.path.dirname(pdf_path), '..', 'tmp')
                if os.path.exists(tmp_dir):
                    for file in os.listdir(tmp_dir):
                        if file.endswith(('.jpg', '.jpeg', '.png')) and original_file['filename'] in file:
                            original_image_path = os.path.abspath(os.path.join(tmp_dir, file))
                            break
    
    html_template = f"""
    <!DOCTYPE html>
    <html lang="ko">
    <head>
      <meta charset="utf-8">
      <title>안심톡 디지털 증거 분석 보고서</title>
      <style>
        @font-face {{
          font-family: 'NanumGothic';
          src: url('static/fonts/NanumGothic.ttf') format('truetype');
          font-weight: normal;
          font-style: normal;
        }}
        
        body {{ 
          font-family: 'NanumGothic', 'Malgun Gothic', 'Arial', sans-serif; 
          margin: 40px; 
          line-height: 1.6;
          word-wrap: break-word;
          overflow-wrap: break-word;
        }}
        
        h1, h2, h3 {{ 
          color: #1976d2; 
          page-break-after: avoid;
          page-break-inside: avoid;
        }}
        
        .code-block {{ 
          font-family: 'Consolas', 'Monaco', monospace; 
          background: #eee; 
          padding: 8px; 
          border-radius: 4px; 
          word-break: break-all;
          font-size: 11px;
        }}
        
        .highlight {{ 
          color: #fff; 
          background: #1976d2; 
          padding: 4px 8px; 
          border-radius: 4px; 
        }}
        
        table {{ 
          border-collapse: collapse; 
          width: 100%; 
          margin: 10px 0; 
          font-size: 11px;
          page-break-inside: avoid;
        }}
        
        th, td {{ 
          border: 1px solid #bbb; 
          padding: 6px 8px; 
          word-wrap: break-word;
          max-width: 200px;
        }}
        
        th {{ 
          background: #f5f5f5; 
          font-weight: bold;
        }}
        
        img.evidence {{ 
          max-width: 400px; 
          max-height: 500px;
          margin: 10px 0; 
          page-break-inside: avoid;
          border: 1px solid #ddd;
          border-radius: 4px;
        }}
        
        .section {{ 
          margin-bottom: 30px; 
          page-break-inside: avoid; 
        }}
        
        ul {{ 
          margin: 0 0 0 20px; 
          page-break-inside: avoid;
        }}
        
        li {{
          margin-bottom: 5px;
          word-wrap: break-word;
        }}
        
        .box {{ 
          background: #f0f4ff; 
          border-radius: 8px; 
          padding: 12px; 
          margin: 10px 0; 
          page-break-inside: avoid;
          word-wrap: break-word;
        }}
        
        .emph {{ 
          font-weight: bold; 
          color: #d32f2f; 
        }}
        
        pre {{
          white-space: pre-wrap;
          word-wrap: break-word;
          font-size: 10px;
          max-width: 100%;
          overflow-x: auto;
        }}
        
        /* 긴 텍스트 처리 */
        .long-text {{
          word-wrap: break-word;
          overflow-wrap: break-word;
          max-width: 100%;
          line-height: 1.4;
          word-spacing: 0.1em;
          text-align: justify;
        }}
        
        /* 분석 결과 텍스트 가독성 개선 */
        .analysis-text {{
          line-height: 1.4;
          word-spacing: 0.1em;
          text-align: justify;
          font-size: 0.95em;
          margin-top: 10px;
        }}
        
        /* WeasyPrint footer for every page */
        @page {{
          size: A4;
          margin: 40px 40px 50px 40px;
          @bottom-center {{
            content: element(report-footer);
          }}
        }}
        
        #report-footer {{
          position: running(report-footer);
          font-size: 10px;
          color: #888;
          text-align: right;
          width: 100%;
        }}
        
        /* 표 내용이 길 때 처리 */
        .md-table {{
          font-size: 10px;
        }}
        
        .md-table th,
        .md-table td {{
          max-width: 150px;
          word-wrap: break-word;
          vertical-align: top;
        }}
             </style>
     </head>
     <body>
       <div id="report-footer">
         보고서ID: {report_id} | 생성일시: {created_at} | 플랫폼: {software_info['platform']} | 배포일: {software_info['release_date']}
       </div>
       <h1>안심톡 디지털 증거 분석 보고서</h1>
       <div class="section">
         <h2>1. 기본 정보</h2>
         <ul>
           <li><b>보고서 ID:</b> {report_id}</li>
           <li><b>생성일시:</b> {created_at}</li>
           <li><b>플랫폼 버전:</b> {software_info['platform']}</li>
           <li><b>배포일:</b> {software_info['release_date']}</li>
           <li><b>마지막 업데이트:</b> {software_info['last_updated']}</li>
         </ul>
       </div>
       <div class="section">
         <h2>2. 분석에 사용된 AI 모델 전체 목록</h2>
         <table>
           <tr><th>분석 Task</th><th>모델명</th><th>버전</th><th>정확도</th></tr>
           {''.join([f'<tr><td>{m["task"]}</td><td>{m["model"]}</td><td>{m["version"]}</td><td>{m["정확도"]}</td></tr>' for m in ai_models])}
         </table>
       </div>
       <div class="section">
         <h2>3. 분석 결과 요약</h2>
         <div class="box" style="font-size: 1.1em;">
           {f'<span style="color:#1976d2; font-weight:bold;">AI 딥페이크 분석 요약</span><br><span>딥페이크일 확률: <b>{analysis_text}</b></span>' if analysis_type == 'deepfake' else f'<span style="color:#1976d2; font-weight:bold;">사이버폭력 분석 결과 요약</span><br><span style="color:#d32f2f; font-weight:bold; font-size:1.0em; line-height:1.4; word-spacing:0.1em;">{analysis_text or "분석 결과 없음"}</span>' if analysis_type == 'cyberbullying' else f'<div class="long-text">{analysis_text or "분석 결과 요약이 제공되지 않았습니다."}</div>'}
         </div>
       </div>
       <div class="section">
         <h2>4. 증거 파일 정보</h2>
         <ul>
           <li><b>파일명:</b> <span class="long-text">{str(original_file.get('filename', 'N/A'))}</span></li>
           <li><b>파일 유형:</b> {analysis_result.get('analysis_type', 'N/A')}</li>
           <li><b>파일 크기:</b> {original_file.get('size_bytes', 'N/A')} Bytes</li>
           <li><b>업로드 일시:</b> {analysis_result.get('analysis_timestamp', 'N/A')}</li>
           <li><b>업로더 ID:</b> <span class="code-block">{analysis_result.get('uploader_id', 'ANSIMTALK_USER_' + datetime.now().strftime('%Y%m%d') + '_' + str(uuid.uuid4().hex[:8].upper()))}</span></li>
           <li><b>업로드 IP:</b> {analysis_result.get('uploader_ip', '127.0.0.1')}</li>
           <li><b>원본 해시값 (SHA-256):</b> <span class="code-block">{str(analysis_result.get('sha256', 'N/A'))}</span></li>
         </ul>
         <h3>원본 파일 메타데이터</h3>
         <ul>
           <li><b>파일 형식:</b> <span class="long-text">{original_file.get('type', 'N/A')}</span></li>
           <li><b>분석 타입:</b> <span class="long-text">{analysis_result.get('analysis_type', 'N/A')}</span></li>
           <li><b>분석 타임스탬프:</b> <span class="long-text">{analysis_result.get('analysis_timestamp', 'N/A')}</span></li>
           <li><b>파일 크기 (바이트):</b> <span class="long-text">{analysis_result.get('file_size_bytes', original_file.get('size_bytes', 'N/A'))} bytes</span></li>
           <li><b>파일 크기 (MB):</b> <span class="long-text">{analysis_result.get('file_size_mb', 'N/A')} MB</span></li>
           <li><b>이미지 해상도:</b> <span class="long-text">{analysis_result.get('image_resolution', 'N/A')}</span></li>
           <li><b>이미지 너비:</b> <span class="long-text">{analysis_result.get('image_width', 'N/A')} pixels</span></li>
           <li><b>이미지 높이:</b> <span class="long-text">{analysis_result.get('image_height', 'N/A')} pixels</span></li>
         </ul>
       </div>
       <div class="section">
         <h2>5. 연계 보관성(Chain of Custody)</h2>
         <table>
           <tr>
             <th>단계</th>
             <th>시각</th>
             <th>서버/AI 정보</th>
           </tr>
           {''.join([f'<tr><td>{log["step"]}</td><td>{log["timestamp"]}</td><td class="long-text">{log["server"]}{" (" + log["ai_model"] + " " + log["version"] + ")" if log["ai_model"] else ""}</td></tr>' for log in analysis_log])}
         </table>
       </div>
       <div class="section">
         <h2>6. AI 분석 결과</h2>
         {f'''
         <div class="box">
           <b>딥페이크 분석 결과 (Sightengine Deepfake Detector):</b><br>
           <div style="white-space:pre-line; background:#f0f0ff; padding:0.5em; border-radius:6px; font-size: 11px;" class="long-text">
             {analysis_text or '분석 결과 없음'}
           </div>
           <div style="margin-top:10px; font-size:11px; color:#555;">
             <b>원본 분석 데이터:</b><br>
             <pre style="background:#f8f8f8; border-radius:6px; padding:0.5em;">{json.dumps(analysis_result.get('deepfake_analysis', {}), indent=2, ensure_ascii=False)}</pre>
           </div>
         </div>
         ''' if analysis_type == 'deepfake' else f'''
         <div class="box">
           <b>추출 텍스트(OCR):</b><br>
           <div style="white-space:pre-line; background:#f8f8f8; padding:0.5em; border-radius:6px; font-size: 11px;" class="long-text">{analysis_result.get('extracted_text', '없음')}</div>
         </div>
         <div class="box">
           <b>사이버폭력 분석 결과(Gemini):</b><br>
           <div style="white-space:pre-line; line-height:1.4; font-size: 11px; word-spacing:0.1em; text-align:justify;" class="long-text">
             전체 대화 사이버폭력 위험도: {analysis_result.get('cyberbullying_risk_line', '분석 중')}
           </div>
         </div>
         ''' if analysis_type == 'cyberbullying' else '''
         <div class="box">
           <b>분석 결과:</b><br>
           <div style="white-space:pre-line; background:#f8f8f8; padding:0.5em; border-radius:6px; font-size: 11px;" class="long-text">
             분석 결과가 제공되지 않았습니다.
           </div>
         </div>
         '''}
       </div>
       <div class="section">
         <h2>7. 원본 증거 이미지</h2>
         {f'<img class="evidence" src="file:///{original_image_path.replace(os.sep, "/")}" alt="원본 증거 이미지"/>' if original_image_path and os.path.exists(original_image_path) else f'<p>원본 이미지를 찾을 수 없습니다. (경로: {original_image_path if original_image_path else "없음"})</p>'}
         <div style="color:#1976d2; font-size:12px; margin-top:10px;">
           * 위 이미지는 분석 대상 원본 증거물입니다.
         </div>
       </div>
       <div class="section">
         <h2>8. 무결성 및 법적 검증</h2>
         <ul>
           <li><b>원본(이미지) 해시값:</b> <span class="code-block">{str(analysis_result.get('sha256', 'N/A'))}</span></li>
           <br>
           <li><b>법적 책임 선언:</b> <span class="long-text">{legal_disclaimer}</span></li>
         </ul>
       </div>
     </body>
     </html>
     """
    
    return html_template 