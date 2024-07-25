# backend/Dockerfile

# 베이스 이미지 설정 (Python 3.9)
FROM python:3.11.9

# 작업 디렉토리 설정
WORKDIR /app

# 필요 라이브러리 설치
COPY requirements.txt .
RUN pip install -r requirements.txt

# 프로젝트 파일 복사
COPY . .

# 시작 스크립트 복사
COPY start_server.sh .

# 실행 권한 부여
RUN chmod +x start_server.sh

# 시작 스크립트 실행
CMD ["./start_server.sh"]
