# GreenCity Backend Program

### 5기 AIVLE School Big Project 29조
지역데이터기반 도시림 네트워크 조성 프로젝트

## 프로젝트 소개
GreenCity는 지역 데이터를 기반으로 도시림 네트워크를 조성하는 프로젝트입니다. 이 백엔드 프로그램은 Django Rest Framework(DRF), JWT(JSON Web Token), SMTP를 사용하여 구현되었습니다.

## 사용 기술
- **DRF (Django Rest Framework)**: Django 기반의 강력한 REST API 프레임워크
- **JWT (JSON Web Token)**: 안전한 사용자 인증을 위한 토큰 기반 인증 방법
- **SMTP**: 이메일 전송 프로토콜

## 실행 방법
1. **환경 설정 파일 준비**
   - `example_config.json` 파일의 이름을 `config.json`으로 변경합니다.
   - `config.json` 파일에 필요한 값을 양식에 맞게 입력합니다.
   - 이 단계를 건너뛰면 프로그램이 에러를 발생시키며 실행되지 않습니다.

2. **프로그램 실행**
   - 다음 명령어를 사용하여 프로그램을 실행합니다.
   ```bash
   python manage.py runserver
