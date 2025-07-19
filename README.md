# 🛡️ 안심톡(AnsimTalk) - AI 기반 디지털 증거 분석 및 보호 플랫폼

---

## 1. 프로젝트 개요 및 목적

**안심톡(AnsimTalk)**은 사이버폭력, 딥페이크 등 디지털 범죄 피해자가 직접 증거(이미지, 텍스트)를 업로드하여 AI로 분석하고, 법적 효력을 갖춘 PDF 증거보고서를 생성·저장할 수 있는 웹 기반 플랫폼입니다. 피해자는 분석 결과를 바탕으로 상담/신고 기관에 신속히 연결할 수 있으며, 모든 데이터는 프라이버시를 최우선으로 안전하게 관리됩니다.

---

## 2. 전체 폴더/파일 구조

```
ansimtalk/
├── app/
│   ├── __init__.py              # Flask 앱 초기화
│   ├── routes.py                # 웹 라우팅, 파일 처리, 세션 관리
│   ├── services.py              # AI 분석, PDF 생성 등 핵심 비즈니스 로직
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css        # 메인 스타일시트 (버튼/레이아웃/UI)
│   │   ├── fonts/               # NanumGothic 등 한글 폰트
│   │   └── uploads/             # 업로드된 임시 이미지 (자동 삭제)
│   └── templates/
│       ├── index.html           # 메인(분석 선택/업로드/시작/상담안내)
│       ├── results.html         # 분석 결과/다운로드/상담안내/새로시작
│       ├── deepfake_help.html   # 딥페이크 상담/신고 안내
│       ├── cyberbullying_help.html # 사이버폭력 상담/신고 안내
│       └── evidence_report.html # PDF 증거보고서 템플릿
├── tmp/                         # 업로드 파일, PDF 임시 저장
├── .env                         # API 키 등 환경 변수 (Git 무시)
├── config.py                    # 환경 변수 로드 및 앱 설정
├── requirements.txt             # Python 의존성 목록
├── run.py                       # Flask 실행 파일
├── .gitignore                   # Git 제외 파일 목록
├── README.md                    # 전체 구현 가이드(이 파일)
├── 작품설계_최종보고서.md        # 설계 철학/기능 명세/개발 계획
└── 작품원리_설명서.md            # 작동 원리/비전공자용 설명
```

---

## 3. 환경 변수 및 보안 설정

### .env 예시
```env
SECRET_KEY='my-super-secret-key'
GOOGLE_GEMINI_API_KEY='AIzaSy...'
GOOGLE_APPLICATION_CREDENTIALS='/home/user/your-google-credentials.json'
SIGHTENGINE_API_USER='your-sightengine-api-user'
SIGHTENGINE_API_SECRET='your-sightengine-api-secret'
```
- **.env는 반드시 .gitignore에 등록!**

### config.py
```python
import os
from dotenv import load_dotenv
load_dotenv()
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    GOOGLE_GEMINI_API_KEY = os.environ.get('GOOGLE_GEMINI_API_KEY')
    SIGHTENGINE_API_USER = os.environ.get('SIGHTENGINE_API_USER')
    SIGHTENGINE_API_SECRET = os.environ.get('SIGHTENGINE_API_SECRET')
    GOOGLE_APPLICATION_CREDENTIALS = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    UPLOAD_FOLDER = 'tmp'
    STATIC_UPLOAD_FOLDER = 'app/static/uploads'
    PDF_OUTPUT_FOLDER = 'tmp'
    ALLOWED_EXTENSIONS = {'txt', 'png', 'jpg', 'jpeg'}
    MAX_FILE_SIZE = 5 * 1024 * 1024
```

---

## 4. 주요 파일별 역할/핵심 함수/클래스/설정 예시

### app/routes.py (핵심 라우팅)
- `/` : 메인 페이지(index.html)
- `/analyze_deepfake` : 딥페이크 분석(POST)
- `/analyze_cyberbullying` : 사이버폭력 분석(POST)
- `/results` : 분석 결과 페이지
- `/download_pdf` : PDF 다운로드
- `/deepfake_help`, `/cyberbullying_help` : 상담/신고 안내
- `/reset` : 임시파일/세션 삭제 후 메인으로

#### 예시: 파일 업로드 및 분석
```python
@main.route('/analyze_deepfake', methods=['POST'])
def analyze_deepfake_route():
    # 파일 저장, 해시, 분석, 세션 저장, 리다이렉트
    ...
```

### app/services.py (AI 분석/보고서 생성)
- `analyze_deepfake(image_path)` : Sightengine API로 딥페이크/유해성 분석
- `extract_text_from_image(image_path)` : Google Vision OCR
- `analyze_cyberbullying(file_path)` : Gemini로 사이버폭력 분석
- `generate_pdf_report(analysis_result)` : WeasyPrint로 PDF 생성

#### 예시: 사이버폭력 분석
```python
def analyze_cyberbullying(file_path):
    # 이미지면 OCR, 텍스트면 그대로 → Gemini로 분석
    ...
```

### app/templates/
- **index.html**: 분석 유형 선택, 파일 업로드, 분석 시작, 상담/신고 안내 버튼
- **results.html**: 분석 결과, PDF 다운로드, 상담/신고 안내, 새로 시작 버튼
- **deepfake_help.html, cyberbullying_help.html**: 기관별 안내 표, 공식 링크, 주의사항 등
- **evidence_report.html**: PDF 보고서용 템플릿(법적 고지, 해시, AI 정보 등 포함)

---

## 5. UI/UX 흐름 및 주요 화면 예시

- **메인(index.html)**: 분석 유형 선택 → 파일 업로드 → 분석 시작
- **결과(results.html)**: 분석 결과(요약/상세), PDF 다운로드, 상담/신고 안내, 새로 시작
- **상담/신고 안내**: 기관별 표, 공식 링크, 주의사항, 상황별 추천 등
- **PDF 보고서**: 파일 정보, 해시, 분석 결과, AI 정보, 법적 고지 등

---

## 6. 실행 및 테스트 방법

1. **가상환경 생성/활성화**
2. **필수 라이브러리 설치**
   ```bash
   pip install -r requirements.txt
   ```
3. **.env 파일 생성 및 API 키 입력**
4. **애플리케이션 실행**
   ```bash
   python run.py
   ```
5. **웹브라우저에서 접속**
   - http://127.0.0.1:5000
6. **테스트**
   - 다양한 이미지/텍스트 업로드, PDF 다운로드, 상담/신고 안내 페이지 이동 등

---

## 7. 보안/프라이버시/에러 대응

- **임시파일/세션 자동 삭제**: 새로 시작 시 서버에서 즉시 삭제
- **API 키/민감정보**: .env로 분리, .gitignore 등록
- **HTTPS 권장**: 실제 서비스 배포 시 필수
- **에러/예외 처리**: 파일 미선택, 지원하지 않는 확장자, API 오류 등은 flash 메시지로 안내

---

## 8. 확장/유지보수/실전 팁

- **AI 모델 교체/추가**: services.py에서 API 호출부만 교체/확장
- **기관 안내/링크 추가**: help 템플릿만 수정하면 됨
- **PDF 보고서 커스터마이즈**: evidence_report.html 및 generate_report_html 함수 수정
- **모바일/반응형 UI**: style.css에서 미디어쿼리 활용
- **배포**: gunicorn, nginx, Docker 등 활용 가능

---

## 9. 참고/문의

- **API 키 발급**: [Google Cloud Console](https://console.cloud.google.com/), [Sightengine](https://sightengine.com/)
- **문의/이슈**: GitHub Issues 활용
