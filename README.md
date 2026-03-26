# JobTracker - 개인 취업 이벤트 관리

개인 취업 활동(회사 지원, 면접, 서류 관리 등)을 추적하는 CRUD 웹 애플리케이션.
로컬 단일 사용자 앱으로, 별도 로그인 없이 바로 사용 가능.

## 기술 스택

| 구분 | 기술 |
|------|------|
| Frontend | Vue 3 + Vite |
| Backend | Django 5 + Django REST Framework |
| DB | PostgreSQL 16 (Docker) |
| HTTP 클라이언트 | Axios |

## 프로젝트 구조

```
job-tracker/
├── docker-compose.yml
├── backend/
│   ├── manage.py
│   ├── requirements.txt
│   ├── config/                 # Django 프로젝트 설정
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── companies/              # 회사 + 전형 절차
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── admin.py
│   ├── resumes/                # 서류 관리 (이력서/포트폴리오/자기소개서)
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── admin.py
│   └── media/                  # 업로드된 PDF 저장소
└── frontend/
    ├── package.json
    ├── vite.config.js
    └── src/
        ├── main.js
        ├── App.vue
        ├── style.css
        ├── api/index.js        # Axios 인스턴스
        ├── router/index.js     # 라우터
        ├── views/
        │   ├── DashboardView.vue
        │   ├── CompanyListView.vue
        │   ├── CompanyFormView.vue
        │   ├── CompanyDetailView.vue
        │   └── ResumeListView.vue
        └── components/
            ├── AppNav.vue
            └── StageForm.vue
```

## 데이터 모델

### Company (회사)

| 필드 | 타입 | 설명 |
|------|------|------|
| company_name | CharField | 회사명 |
| position | CharField | 포지션명 |
| source | Choice | 지원 경로 (사람인/원티드/공식홈페이지/추천/기타) |
| job_url | URLField | 채용 공고 링크 |
| memo | TextField | 메모 |
| created_at | DateTime | 생성일 (자동) |
| updated_at | DateTime | 수정일 (자동) |
| status | Property | 전형 결과에서 자동 계산 (진행중/최종통과/불합격) |

### CompanyStage (전형 절차)

| 필드 | 타입 | 설명 |
|------|------|------|
| company | FK → Company | 소속 회사 |
| stage | JSONField | 형태 목록 (서류/코테/커피챗/면접/과제) |
| method | Choice | 방식 (온라인/오프라인) |
| date | DateField | 날짜 |
| result | Choice | 결과 (진행중/통과/최종통과/불합격) |
| memo | TextField | 메모 |
| documents | M2M → ResumeEvent | 제출 서류 (종류당 1개씩 선택) |

### ResumeEvent (서류)

| 필드 | 타입 | 설명 |
|------|------|------|
| doc_type | Choice | 서류 종류 (이력서/포트폴리오/자기소개서) |
| label | CharField | 제목 (미입력 시 파일명으로 자동 설정) |
| modified_date | DateField | 수정 날짜 |
| pdf_file | FileField | PDF 첨부파일 |

## API 엔드포인트

| Method | URL | 설명 |
|--------|-----|------|
| GET/POST | `/api/companies/` | 회사 목록 조회 / 등록 |
| GET/PUT/PATCH/DELETE | `/api/companies/:id/` | 회사 상세 조회 / 수정 / 삭제 |
| GET/POST | `/api/companies/:id/stages/` | 전형 절차 목록 조회 / 등록 |
| GET/PUT/PATCH/DELETE | `/api/companies/:id/stages/:sid/` | 전형 절차 수정 / 삭제 |
| GET/POST | `/api/resumes/` | 서류 목록 조회 / 등록 |
| GET/PUT/PATCH/DELETE | `/api/resumes/:id/` | 서류 수정 / 삭제 |

## 페이지 구성

| 경로 | 페이지 | 설명 |
|------|--------|------|
| `/` | 대시보드 | 전체 통계 + 최근 지원 현황 |
| `/companies` | 회사 목록 | 상태 필터링, 목록 관리 |
| `/companies/new` | 회사 등록 | 새 회사 등록 폼 |
| `/companies/:id` | 회사 상세 | 회사 정보 + 전형 절차 타임라인 |
| `/companies/:id/edit` | 회사 수정 | 회사 정보 수정 폼 |
| `/resumes` | 서류 관리 | 이력서/포트폴리오/자기소개서 관리 + PDF 업로드 |

## 개발 환경 실행

### 사전 요구사항

- Docker / Docker Compose

### 전체 실행 (Docker Compose)

```bash
cd /home/leejw/projects/jobEvent

# 전체 시작 (DB + 백엔드 + 프론트엔드)
docker compose up -d

# 최초 실행 시 마이그레이션
docker compose exec backend python manage.py migrate
```

| 서비스 | URL | 설명 |
|--------|-----|------|
| Frontend | http://localhost:5173 | Vue 앱 (Vite HMR) |
| Backend | http://localhost:8000 | Django API |
| DB | localhost:5432 | PostgreSQL |

- 소스 코드가 volume mount 되어 있어 **파일 수정 시 자동 반영** (Hot Reload)
- Vite 프록시 설정으로 `/api`, `/media` 요청은 자동으로 백엔드로 전달

### 사용 시작

`http://localhost:5173`에 접속하면 바로 사용 가능.

### Django 관리자 페이지

```bash
docker compose exec backend python manage.py createsuperuser
```

이후 `http://localhost:8000/admin/`에서 데이터 직접 관리 가능.

## 주요 개발 명령어

```bash
# 전체 시작 / 중지
docker compose up -d
docker compose down
docker compose down -v     # 중지 + DB 데이터 삭제

# 로그 확인
docker compose logs -f             # 전체
docker compose logs -f backend     # 백엔드만
docker compose logs -f frontend    # 프론트엔드만

# Django 마이그레이션 (모델 변경 후)
docker compose exec backend python manage.py makemigrations
docker compose exec backend python manage.py migrate

# 패키지 추가 (백엔드) - 추가 후 이미지 재빌드 필요
# backend/requirements.txt에 추가 후:
docker compose up -d --build backend

# 패키지 추가 (프론트엔드) - 추가 후 이미지 재빌드 필요
# frontend에서 npm install 후:
docker compose up -d --build frontend
```
