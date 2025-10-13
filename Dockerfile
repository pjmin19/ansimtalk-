FROM python:3.12-slim

# 환경 변수 설정
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Install system dependencies for WeasyPrint
RUN apt-get update && apt-get install -y \
    libcairo2-dev \
    libpango1.0-dev \
    libgirepository1.0-dev \
    libglib2.0-dev \
    libffi-dev \
    pkg-config \
    fonts-noto-cjk \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Gunicorn으로 프로덕션 서버 실행
CMD gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 300 --access-logfile - --error-logfile - run:app 