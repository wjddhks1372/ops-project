# 1. 베이스 이미지 설정 (가볍고 안정적인 python 3.11 slim 버전)
FROM python:3.11-slim

# 2. 작업 디렉토리 설정
WORKDIR /app

# 3. 의존성 파일 복사 및 설치
# (소스코드보다 먼저 복사하여 Docker 레이어 캐싱을 활용, 빌드 속도 향상)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. 소스 코드 복사
COPY . .

# 5. 실행 명령 설정
# uvicorn 서버 실행, 0.0.0.0으로 열어야 컨테이너 외부에서 접속 가능
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]