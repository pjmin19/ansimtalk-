FROM python:3.12-slim

# 환경 변수 설정
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Install system dependencies for ReportLab (한글 폰트 지원)
RUN apt-get update && apt-get install -y \
    fonts-nanum \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD gunicorn --bind 0.0.0.0:$PORT --workers 2 "run:app" 