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

## user 설명
### 유저 등록 절차
1. **계정 정보 입력**
2. **이메일 인증**
3. **가입 요청**
4. **가입 완료**

### 로그인 (인증 토큰 발급 절차)
1. **로그인**: 토큰 발급 (인증 토큰, 갱신 토큰)
2. **서버 요청**: 인증 토큰을 가지고 서버에 요청
3. **토큰 갱신**: 만약 인증 토큰이 만료될 시 갱신 토큰을 사용해 인증 토큰 갱신
4. **로그아웃**: 프론트단에서 인증 토큰을 삭제하는 방식으로 로그아웃


## noticeboard CRUD 설명
### 1. 안전한 메서드 (읽기 전용)
- **GET**: 데이터를 조회하는 요청입니다.
  - **전체 목록 조회**: `/board/` - 모든 게시물을 조회합니다.
  - **개별 항목 조회**: `/board/{id}/` - 특정 ID를 가진 게시물을 조회합니다.

### 2. 안전하지 않은 메서드 (쓰기, 수정, 삭제)
- **POST**: 데이터를 생성하는 요청입니다.
  - **새 게시물 생성**: `/board/` - 새로운 게시물을 생성합니다.
- **PUT**: 데이터를 전체 수정하는 요청입니다.
  - **게시물 전체 수정**: `/board/{id}/` - 특정 ID를 가진 게시물의 모든 필드를 수정합니다.
- **PATCH**: 데이터를 부분 수정하는 요청입니다.
  - **게시물 부분 수정**: `/board/{id}/` - 특정 ID를 가진 게시물의 일부 필드를 수정합니다.
- **DELETE**: 데이터를 삭제하는 요청입니다.
  - **게시물 삭제**: `/board/{id}/` - 특정 ID를 가진 게시물을 삭제합니다.

## generativeAI 사용법

1. **서버 실행**
2. **명령어 창(윈도우면 Git Bash에) 실행**
3. **명령어 실행**
    ```sh
    curl -X POST http://127.0.0.1:8000/generativeAI/image_generate/ \
         -F "init_image=@파일위치 \
         -F "text_prompts=Keep existing photos, Recognition of roads and buildings, Plant ginkgo trees on the sidewalk along the road" \
         -o generated_image.png
    ```
4. **결과 확인**