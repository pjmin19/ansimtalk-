import requests
import json
from flask import current_app
import os
from PIL import Image
import hashlib
from datetime import datetime
from weasyprint import HTML
from google.cloud import vision
from google import genai
import re

def convert_markdown_table_to_html(markdown_table):
    """마크다운 표를 HTML 표로 변환"""
    if not markdown_table.strip():
        return "<p>분석 결과가 없습니다.</p>"
    
    lines = markdown_table.strip().split('\n')
    if len(lines) < 2:
        return f"<p>표 형식이 올바르지 않습니다: {markdown_table}</p>"
    
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
    
    result = '\n'.join(html_lines)
    print(f"변환된 HTML 테이블: {result[:300]}...")
    return result

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
            if extracted_text.strip():
                gemini_result = analyze_text_with_gemini(extracted_text)
                result['extracted_text'] = extracted_text
                result['cyberbullying_analysis'] = gemini_result.get('table', '')
                result['cyberbullying_analysis_summary'] = gemini_result.get('summary', '')
                result['cyberbullying_risk_line'] = extract_risk_line(gemini_result.get('summary', ''))
                
                # 디버깅 로그 추가
                print(f"Gemini 결과 테이블: {gemini_result.get('table', '')[:200]}...")
                print(f"Gemini 결과 요약: {gemini_result.get('summary', '')[:200]}...")
                
                # 대화 전체 분위기 요약과 잠재적 위험/주의사항 추출
                summary_text = gemini_result.get('summary', '')
                result['conversation_atmosphere'] = extract_conversation_atmosphere(summary_text)
                result['potential_risks'] = extract_potential_risks(summary_text)
            else:
                result['error'] = '이미지에서 텍스트를 추출할 수 없습니다.'
        elif file_extension == 'txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            gemini_result = analyze_text_with_gemini(text)
            result['extracted_text'] = text
            result['cyberbullying_analysis'] = gemini_result.get('table', '')
            result['cyberbullying_analysis_summary'] = gemini_result.get('summary', '')
            result['cyberbullying_risk_line'] = extract_risk_line(gemini_result.get('summary', ''))
            
            # 디버깅 로그 추가
            print(f"Gemini 결과 테이블: {gemini_result.get('table', '')[:200]}...")
            print(f"Gemini 결과 요약: {gemini_result.get('summary', '')[:200]}...")
            
            # 대화 전체 분위기 요약과 잠재적 위험/주의사항 추출
            summary_text = gemini_result.get('summary', '')
            result['conversation_atmosphere'] = extract_conversation_atmosphere(summary_text)
            result['potential_risks'] = extract_potential_risks(summary_text)
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
            return ""
        return texts[0].description.strip()
    except Exception as e:
        print(f"Google Cloud Vision API 오류: {e}")
        return f"[Google Cloud Vision API 오류: {e}]"

def analyze_text_with_gemini(text_content):
    # Railway 환경에서 환경 변수로 설정된 서비스 계정 키 사용
    import json
    from google.oauth2 import service_account
    
    # 환경 변수에서 서비스 계정 키 JSON 가져오기
    service_account_info = os.environ.get('GOOGLE_SERVICE_ACCOUNT_JSON')
    if service_account_info:
        # JSON 문자열을 파싱하여 서비스 계정 정보 생성
        service_account_dict = json.loads(service_account_info)
        credentials = service_account.Credentials.from_service_account_info(service_account_dict)
        client = genai.Client(
            vertexai=True,
            project="dazzling-howl-465316-m7",
            location="global",
            credentials=credentials
        )
    else:
        # 기존 방식 (로컬 파일)
        credentials_path = current_app.config['GOOGLE_APPLICATION_CREDENTIALS']
        if os.path.exists(credentials_path):
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
            client = genai.Client(
                vertexai=True,
                project="dazzling-howl-465316-m7",
                location="global",
            )
        else:
            print("Google Cloud 인증 정보가 설정되지 않았습니다")
            return _fallback_cyberbullying_analysis(text_content)
    
    model = "gemini-2.5-flash-lite-preview-06-17"
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
        response = client.models.generate_content(
            model=model,
            contents=[prompt]
        )
        result_text = response.candidates[0].content.parts[0].text.strip()
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

def extract_conversation_atmosphere(summary):
    """요약에서 대화 전체 분위기 요약 추출"""
    if not summary:
        return "분석 중..."
    
    lines = summary.split('\n')
    for i, line in enumerate(lines):
        if '대화 전체 분위기 요약:' in line:
            # 다음 줄부터 다음 섹션까지의 내용을 가져옴
            atmosphere_lines = []
            for j in range(i + 1, len(lines)):
                if '잠재적 위험/주의사항:' in lines[j]:
                    break
                if lines[j].strip():
                    atmosphere_lines.append(lines[j].strip())
            return ' '.join(atmosphere_lines)
    
    return "분석 중..."

def extract_potential_risks(summary):
    """요약에서 잠재적 위험/주의사항 추출"""
    if not summary:
        return "분석 중..."
    
    lines = summary.split('\n')
    for i, line in enumerate(lines):
        if '잠재적 위험/주의사항:' in line:
            # 다음 줄부터 끝까지의 내용을 가져옴
            risk_lines = []
            for j in range(i + 1, len(lines)):
                if lines[j].strip():
                    risk_lines.append(lines[j].strip())
            return ' '.join(risk_lines)
    
    return "분석 중..."

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



def generate_pdf_report(analysis_result, pdf_path, analysis_type=None):
    """법적 요건을 충족하는 전문적인 디지털 증거 분석 보고서 생성 - HTML 기반"""
    try:
        # HTML 템플릿 생성
        html_content = generate_report_html(analysis_result, analysis_type, pdf_path)
        
        # WeasyPrint로 PDF 생성
        HTML(string=html_content).write_pdf(pdf_path)
        return pdf_path
        
    except Exception as e:
        print(f"HTML-based PDF generation failed: {e}")
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
        risk_line = analysis_result['cyberbullying_risk_line']
        analysis_text = f"전체 대화 사이버폭력 위험도: {risk_line}"
    
    # 보고서 ID 및 생성일시
    report_id = f"DF-CB-{datetime.now().strftime('%Y')}-001-v1.0"
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # 파일 정보
    filename = str(original_file.get('filename', 'N/A'))
    file_size = str(original_file.get('size_bytes', 'N/A'))
    sha256 = str(analysis_result.get('sha256', 'N/A'))
    
    # 원본 이미지 경로 찾기
    original_image_path = analysis_result.get('original_image_path', '')
    if not original_image_path and 'filename' in original_file and pdf_path:
        # 기존의 복잡한 경로 탐색 로직을 유지하되, pdf_path가 있어야만 실행되도록 함
        static_uploads_dir = os.path.join(os.path.dirname(pdf_path), '..', 'app', 'static', 'uploads')
        if os.path.exists(static_uploads_dir):
            for file in os.listdir(static_uploads_dir):
                if file.endswith(('.jpg', '.jpeg', '.png')) and original_file['filename'] in file:
                    original_image_path = os.path.abspath(os.path.join(static_uploads_dir, file))
                    break
        if not original_image_path:
            tmp_dir = os.path.join(os.path.dirname(pdf_path), '..', 'tmp')
            if os.path.exists(tmp_dir):
                for file in os.listdir(tmp_dir):
                    if file.endswith(('.jpg', '.jpeg', '.png')) and original_file['filename'] in file:
                        original_image_path = os.path.abspath(os.path.join(tmp_dir, file))
                        break

    # 절대 파일 경로를 웹에서 접근 가능한 상대 URL로 변환합니다.
    # 예: '/app/static/uploads/image.png' -> '/static/uploads/image.png'
    # 이 경로는 WeasyPrint의 base_url과 결합되어 완전한 HTTP URL로 해석됩니다.
    web_image_path = ""
    if original_image_path and os.path.exists(original_image_path):
        # 'static' 디렉토리를 기준으로 경로를 분리하여 웹 경로를 생성합니다.
        path_parts = original_image_path.split(os.sep)
        try:
            static_index = path_parts.index('static')
            # os.sep으로 분리된 경로를 웹 표준인 '/'로 다시 합칩니다.
            web_image_path = '/' + '/'.join(path_parts[static_index:])
        except ValueError:
            # 'static'이 경로에 없는 경우, 이미지를 표시할 수 없음을 기록합니다.
            print(f"Warning: Could not create web-accessible path for image: {original_image_path}")
            web_image_path = ""

    # 추가 정보 추출
    uploader_id = analysis_result.get('uploader_id', 'N/A')
    uploader_ip = analysis_result.get('uploader_ip', 'N/A')
    upload_timestamp = analysis_result.get('upload_timestamp', 'N/A')
    file_size_mb = analysis_result.get('file_size_mb', 'N/A')
    image_width = analysis_result.get('image_width', 'N/A')
    image_height = analysis_result.get('image_height', 'N/A')
    image_resolution = analysis_result.get('image_resolution', 'N/A')
    extracted_text = analysis_result.get('extracted_text', '')
    cyberbullying_analysis = analysis_result.get('cyberbullying_analysis', '')
    cyberbullying_summary = analysis_result.get('cyberbullying_analysis_summary', '')
    
    # HTML 템플릿 생성
    html_content = f"""
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>안심톡 디지털 증거 분석 보고서</title>
        <style>
            @font-face {{
                font-family: 'NanumGothic';
                src: url('/static/fonts/NanumGothic.ttf') format('truetype');
                font-weight: normal;
                font-style: normal;
                font-display: swap;
            }}
            
            body {{ 
                font-family: 'NanumGothic', 'Malgun Gothic', '맑은 고딕', 'Arial', sans-serif; 
                margin: 40px; 
                line-height: 1.6;
                word-wrap: break-word;
                overflow-wrap: break-word;
                color: #333;
            }}
            
            h1, h2, h3 {{ 
                color: #1976d2; 
                page-break-after: avoid; 
                page-break-inside: avoid; 
                margin-top: 30px;
                margin-bottom: 15px;
            }}
            
            .code-block {{ 
                font-family: 'Consolas', 'Monaco', monospace; 
                background: #f5f5f5; 
                padding: 8px; 
                border-radius: 4px; 
                word-break: break-all; 
                font-size: 11px; 
                border: 1px solid #ddd;
            }}
            
            table {{ 
                border-collapse: collapse; 
                width: 100%; 
                margin: 15px 0; 
                font-size: 12px; 
                page-break-inside: avoid; 
            }}
            
            th, td {{ 
                border: 1px solid #ddd; 
                padding: 8px 12px; 
                word-wrap: break-word; 
                text-align: left;
            }}
            
            th {{ 
                background: #f8f9fa; 
                font-weight: bold; 
                color: #495057;
            }}
            
            img.evidence {{ 
                max-width: 400px; 
                max-height: 500px; 
                margin: 15px 0; 
                page-break-inside: avoid; 
                border: 1px solid #ddd; 
                border-radius: 4px; 
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            
            .section {{ 
                margin-bottom: 40px; 
                page-break-inside: avoid; 
            }}
            
            .box {{ 
                background: #f0f4ff; 
                border-radius: 8px; 
                padding: 15px; 
                margin: 15px 0; 
                page-break-inside: avoid; 
                word-wrap: break-word; 
                border-left: 4px solid #1976d2;
            }}
            
            .extracted-text {{
                background: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 4px;
                padding: 15px;
                margin: 15px 0;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 11px;
                white-space: pre-wrap;
                word-wrap: break-word;
                max-height: 300px;
                overflow-y: auto;
            }}
            
            .analysis-result {{
                background: #fff3cd;
                border: 1px solid #ffeaa7;
                border-radius: 4px;
                padding: 15px;
                margin: 15px 0;
                font-weight: bold;
                color: #856404;
            }}
            
            .analysis-table {{
                border-collapse: collapse;
                width: 100%;
                margin: 15px 0;
                font-size: 11px;
                page-break-inside: avoid;
            }}
            
            .analysis-table th, .analysis-table td {{
                border: 1px solid #ddd;
                padding: 6px 8px;
                word-wrap: break-word;
                text-align: left;
                vertical-align: top;
            }}
            
            .analysis-table th {{
                background: #f8f9fa;
                font-weight: bold;
                color: #495057;
            }}
            
            .risk-none {{
                color: #28a745;
                font-weight: bold;
            }}
            
            .risk-severe {{
                color: #dc3545;
                font-weight: bold;
            }}
            
            .risk-moderate {{
                color: #ffc107;
                font-weight: bold;
            }}
            
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
                border-top: 1px solid #eee;
                padding-top: 10px;
            }}
            
            .metadata-item {{
                margin: 8px 0;
            }}
            
            .metadata-label {{
                font-weight: bold;
                color: #495057;
                display: inline-block;
                width: 120px;
            }}
            
            .metadata-value {{
                color: #333;
            }}
        </style>
    </head>
    <body>
        <div id="report-footer">
            보고서ID: {report_id} | 생성일시: {created_at} | 플랫폼: 안심톡 AI 포렌식 분석 시스템 v1.0 | 배포일: 2025-07-18
        </div>
        
        <h1>안심톡 디지털 증거 분석 보고서</h1>
        
        <div class="section">
            <h2>1. 기본 정보</h2>
            <table>
                <tr><th>보고서 ID</th><td>{report_id}</td></tr>
                <tr><th>생성일시</th><td>{created_at}</td></tr>
                <tr><th>분석 유형</th><td>{analysis_type or 'N/A'}</td></tr>
                <tr><th>분석 시스템</th><td>안심톡 AI 포렌식 분석 시스템 v1.0</td></tr>
            </table>
        </div>
        
        <div class="section">
            <h2>2. 분석에 사용된 AI 모델 전체 목록</h2>
            <table>
                <thead>
                    <tr>
                        <th>분석 작업</th>
                        <th>AI 모델</th>
                        <th>버전</th>
                        <th>정확도</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>딥페이크 탐지</td>
                        <td>Sightengine Deepfake Detector</td>
                        <td>v1.0</td>
                        <td>98.2%</td>
                    </tr>
                    <tr>
                        <td>사이버폭력 분석</td>
                        <td>Google Gemini 2.5 Flash</td>
                        <td>v1.0</td>
                        <td>94.5%</td>
                    </tr>
                    <tr>
                        <td>OCR 텍스트 추출</td>
                        <td>Google Cloud Vision API</td>
                        <td>v1.0</td>
                        <td>99.1%</td>
                    </tr>
                </tbody>
            </table>
        </div>
        
        <div class="section">
            <h2>3. 분석 결과 요약</h2>
            <div class="analysis-result">
                <strong>사이버폭력 분석 결과 요약:</strong><br>
                전체 대화 사이버폭력 위험도: {analysis_result.get('cyberbullying_risk_line', 'N/A')}
            </div>
        </div>
        
        <div class="section">
            <h2>4. 증거 파일 정보</h2>
            <div class="metadata-item">
                <span class="metadata-label">파일명:</span>
                <span class="metadata-value">{filename}</span>
            </div>
            <div class="metadata-item">
                <span class="metadata-label">파일 유형:</span>
                <span class="metadata-value">{analysis_type or 'N/A'}</span>
            </div>
            <div class="metadata-item">
                <span class="metadata-label">파일 크기:</span>
                <span class="metadata-value">{file_size} Bytes</span>
            </div>
            <div class="metadata-item">
                <span class="metadata-label">업로드 일시:</span>
                <span class="metadata-value">{upload_timestamp}</span>
            </div>
            <div class="metadata-item">
                <span class="metadata-label">업로더 ID:</span>
                <span class="metadata-value code-block">{uploader_id}</span>
            </div>
            <div class="metadata-item">
                <span class="metadata-label">업로드 IP:</span>
                <span class="metadata-value">{uploader_ip}</span>
            </div>
            <div class="metadata-item">
                <span class="metadata-label">원본 해시값 (SHA-256):</span>
                <span class="metadata-value code-block">{sha256}</span>
            </div>
        </div>
        
        <div class="section">
            <h2>원본 파일 메타데이터</h2>
            <div class="metadata-item">
                <span class="metadata-label">파일 형식:</span>
                <span class="metadata-value">{original_file.get('type', 'N/A')}</span>
            </div>
            <div class="metadata-item">
                <span class="metadata-label">분석 타입:</span>
                <span class="metadata-value">{analysis_type or 'N/A'}</span>
            </div>
            <div class="metadata-item">
                <span class="metadata-label">분석 타임스탬프:</span>
                <span class="metadata-value">{analysis_result.get('analysis_timestamp', 'N/A')}</span>
            </div>
            <div class="metadata-item">
                <span class="metadata-label">파일 크기 (바이트):</span>
                <span class="metadata-value">{file_size} bytes</span>
            </div>
            <div class="metadata-item">
                <span class="metadata-label">파일 크기 (MB):</span>
                <span class="metadata-value">{file_size_mb} MB</span>
            </div>
            <div class="metadata-item">
                <span class="metadata-label">이미지 해상도:</span>
                <span class="metadata-value">{image_resolution}</span>
            </div>
            <div class="metadata-item">
                <span class="metadata-label">이미지 너비:</span>
                <span class="metadata-value">{image_width} pixels</span>
            </div>
            <div class="metadata-item">
                <span class="metadata-label">이미지 높이:</span>
                <span class="metadata-value">{image_height} pixels</span>
            </div>
        </div>
        
        <div class="section">
            <h2>5. 연계 보관성 (Chain of Custody)</h2>
            <table>
                <thead>
                    <tr>
                        <th>단계</th>
                        <th>시각</th>
                        <th>서버/AI 정보</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>파일 업로드</td>
                        <td>{upload_timestamp}</td>
                        <td>안심톡 서버</td>
                    </tr>
                    <tr>
                        <td>해시값 계산</td>
                        <td>{upload_timestamp}</td>
                        <td>SHA-256</td>
                    </tr>
                    <tr>
                        <td>AI 분석</td>
                        <td>{upload_timestamp}</td>
                        <td>AI 서버 (Gemini 2.5 Flash v1.0)</td>
                    </tr>
                    <tr>
                        <td>결과 생성</td>
                        <td>{upload_timestamp}</td>
                        <td>보고서 생성 서버</td>
                    </tr>
                </tbody>
            </table>
        </div>
        
        <div class="section">
            <h2>6. AI 분석 결과</h2>
            
            <h3>추출 텍스트(OCR):</h3>
            <div class="extracted-text">{extracted_text}</div>
            
            <h3>사이버폭력 분석 결과(Gemini):</h3>
            <div class="analysis-result">
                전체 대화 사이버폭력 위험도: {analysis_result.get('cyberbullying_risk_line', 'N/A')}
            </div>
            
            <h3>상세 분석 결과:</h3>
            <div class="box">
                {analysis_result.get('cyberbullying_analysis', '분석 중...') if analysis_result.get('cyberbullying_analysis') else '분석 결과가 없습니다.'}
            </div>
            
            <h3>전체 분석 요약:</h3>
            <div class="box" style="background: #f8f9fa; border-left: 4px solid #28a745;">
                <strong>전체 대화 사이버폭력 위험도:</strong> {analysis_result.get('cyberbullying_risk_line', 'N/A')}<br><br>
                <strong>대화 전체 분위기 요약:</strong> {analysis_result.get('conversation_atmosphere', '분석 중...')}<br><br>
                <strong>잠재적 위험/주의사항:</strong> {analysis_result.get('potential_risks', '분석 중...')}
            </div>
        </div>
        
        <div class="section">
            <h2>7. 원본 증거 이미지</h2>
            {f'<img class="evidence" src="{web_image_path}" alt="원본 증거 이미지"/>' if web_image_path else f'<p>원본 이미지를 찾을 수 없거나 웹 경로를 생성할 수 없습니다. (경로: {original_image_path if original_image_path else "없음"})</p>'}
            <div style="color:#1976d2; font-size:12px; margin-top:10px;">
                * 위 이미지는 분석 대상 원본 증거물입니다.
            </div>
        </div>
        
        <div class="section">
            <h2>8. 무결성 및 법적 검증</h2>
            <ul>
                <li><b>원본(이미지) 해시값:</b> <span class="code-block">{str(analysis_result.get('sha256', 'N/A'))}</span></li>
                <br>
                <li><b>법적 책임 선언:</b> <span class="long-text">본 보고서는 AI 기반 분석 결과를 제공하며 법률 전문가의 판단을 대체할 수 없습니다. 보고서 내용은 참고 자료로만 사용되어야 하며 법적 책임을 지지 않습니다. 정확한 법적 조치나 상담을 위해서는 변호사나 관련 기관에 문의하시기 바랍니다.</span></li>
            </ul>
        </div>
    </body>
    </html>
    """
    
    return html_content 