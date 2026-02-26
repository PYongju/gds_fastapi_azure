# 파이썬 3.12 버전 사용
FROM python:3.11-slim

# 서버 내 작업 경로
WORKDIR /app

# 라이브러리 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 코드 복사
COPY . .

# 8000번 포트로 서버 실행
CMD ["gunicorn", "-w", 4, "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000", "main:app"]