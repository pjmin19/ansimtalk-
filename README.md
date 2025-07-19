# 🛡️ 안심톡(AnsimTalk) - AI 기반 디지털 증거 분석 및 보호 플랫폼

---

## 📋 프로젝트 개요

안심톡(AnsimTalk)은 사이버폭력, 딥페이크 등 디지털 범죄 피해자가 직접 증거(이미지, 텍스트)를 업로드하여 AI로 분석하고, 법적 효력을 갖춘 PDF 증거보고서를 생성·저장할 수 있는 웹 기반 플랫폼입니다.

### 🎯 주요 기능
- 딥페이크 분석: Sightengine API를 활용한 이미지 진위 여부 분석
- 사이버폭력 분석: Google Gemini AI를 활용한 텍스트 유해성 분석
- PDF 증거보고서 생성: 법적 효력을 갖춘 상세 분석 보고서
- 상담/신고 안내: 기관별 연락처 및 신고 방법 안내

---

## 📁 프로젝트 구조

```
ansimtalk/
├── app/                      # Flask 앱 모듈
│   ├── __init__.py          # Flask 앱 초기화 및 설정
│   ├── routes.py            # 웹 라우팅 및 요청 처리
│   ├── services.py          # AI 분석 및 PDF 생성 서비스
│   ├── static/              # 정적 파일
│   │   ├── css/
│   │   │   └── style.css    # 메인 스타일시트
│   │   ├── fonts/           # NanumGothic 한글 폰트
│   │   └── uploads/         # 업로드된 임시 파일
│   └── templates/           # HTML 템플릿
│       ├── index.html       # 메인 페이지
│       ├── results.html     # 분석 결과 페이지
│       ├── deepfake_help.html # 딥페이크 상담 안내
│       ├── cyberbullying_help.html # 사이버폭력 상담 안내
│       ├── evidence_report.html # PDF 증거보고서 템플릿
│       └── evidence.html    # 증거 페이지
├── no/                      # 민감한 파일들 (Git 제외)
│   ├── .env                # 환경 변수 파일
│   ├── google-credentials.json # Google API 인증 파일
│   └── 기타_민감_파일들
├── config.py               # 환경 변수 설정
├── requirements.txt        # Python 의존성 목록
├── Procfile               # Railway 배포 설정
├── run.py                 # Flask 앱 실행 파일
├── .gitignore             # Git 제외 파일 목록
├── README.md              # 프로젝트 설명서
├── 완전구현가이드.md       # 상세 구현 가이드
├── 작품설계_최종보고서.md   # 설계 보고서
└── 작품원리_설명서.md       # 작동 원리 설명
```

---

## 🚀 설치 및 실행

### 1. 저장소 클론
```bash
git clone [your-repository-url]
cd ansimtalk
```

### 2. 가상환경 생성 및 활성화
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. 의존성 설치
```bash
pip install -r requirements.txt
```

### 4. 환경 변수 설정
`.env` 파일을 생성하고 다음 내용을 입력:
```env
SECRET_KEY=your-secret-key-here
SIGHTENGINE_API_USER=1052068557
SIGHTENGINE_API_SECRET=JbRcN79c6iunXBHG29WRzyQyFHRoYnQa
GOOGLE_GEMINI_API_KEY=your-gemini-api-key-here
```

### 5. 앱 실행
```bash
python run.py
```

### 6. 브라우저에서 접속
```
http://127.0.0.1:5000
```

---

## 🔧 주요 파일 설명

### `app/__init__.py`
Flask 앱 초기화 및 설정
- 앱 생성 및 설정 로드
- 블루프린트 등록
- 업로드 폴더 설정

### `app/routes.py`
웹 라우팅 및 요청 처리
- `/`: 메인 페이지
- `/analyze_deepfake`: 딥페이크 분석
- `/analyze_cyberbullying`: 사이버폭력 분석
- `/results`: 분석 결과 페이지
- `/download_pdf`: PDF 다운로드
- `/deepfake_help`, `/cyberbullying_help`: 상담 안내
- `/reset`: 세션 초기화

### `app/services.py`
AI 분석 및 PDF 생성 서비스
- `analyze_deepfake()`: Sightengine API 딥페이크 분석
- `analyze_cyberbullying()`: Gemini AI 사이버폭력 분석
- `extract_text_from_image()`: Google Vision OCR
- `generate_pdf_report()`: PDF 증거보고서 생성

### `config.py`
환경 변수 설정
- API 키 및 보안 설정
- 파일 업로드 설정
- 앱 기본 설정

---

## 🌐 배포 (Railway)

### 1. Railway 프로젝트 생성
- Railway.app에서 새 프로젝트 생성
- GitHub 저장소 연결

### 2. 환경 변수 설정
Railway Variables 탭에서 다음 변수 설정:
```json
{
  "SECRET_KEY": "ansimtalk-secret-key-2024",
  "SIGHTENGINE_API_USER": "1052068557",
  "SIGHTENGINE_API_SECRET": "JbRcN79c6iunXBHG29WRzyQyFHRoYnQa",
  "GOOGLE_GEMINI_API_KEY": "your-actual-gemini-api-key"
}
```

### 3. 배포 확인
- Deployments 탭에서 배포 상태 확인
- 성공 시 제공되는 URL로 접속

---

## 🔒 보안 및 프라이버시

- 임시 파일 자동 삭제: 분석 완료 후 서버에서 즉시 삭제
- 세션 관리: 사용자별 독립적인 세션 관리
- API 키 보안: 환경 변수로 민감 정보 분리
- HTTPS 권장: 실제 서비스 배포 시 필수

---

## 🛠️ 기술 스택

- Backend: Python Flask
- AI/ML: Google Gemini AI, Sightengine API, Google Vision OCR
- PDF 생성: WeasyPrint
- 배포: Railway
- 버전 관리: Git/GitHub

---

## 📞 상담/신고 기관

### 딥페이크 관련
- 경찰청 사이버수사과: 182
- 한국정보통신기술협회: 02-580-0123
- 디지털성범죄피해자지원센터: 1366

### 사이버폭력 관련
- 경찰청 사이버수사과: 182
- 청소년사이버상담센터: 1388
- 한국청소년상담복지개발원: 1388

---

## 📝 라이선스

이 프로젝트는 교육 및 연구 목적으로 개발되었습니다.

---

## 🤝 기여

버그 리포트나 기능 제안은 GitHub Issues를 통해 해주세요.

---

안심톡으로 더 안전한 디지털 세상을 만들어가겠습니다. 🛡️