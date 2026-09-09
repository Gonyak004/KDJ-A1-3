# KDJ-A1-3

Python 응용:AI 웹 개발: 내 아이디어를 현실로, AI 웹 서비스 빌딩

목차

[1. 서비스 소개](#1-서비스-소개)

[2. 기술 스택](#2-기술-스택)

[3. 실행 배포 방법](#3-실행-배포-방법)

[4. 프로젝트 구조](#4-프로젝트-구조)

[5. API 키 보안 관리 조치](#5-API-키-보안-관리-조치)

[6. 필요 증빙 자료](#6-필요-증빙-자료)


#

### 1. 서비스 소개

### FitFinal 스토리
>운동을 시작하기는 쉽지만, 꾸준히 이어가기는 어렵습니다. 많은 이들이 무작정 시작한 운동과 무리한 식단으로 쉽게 피로감을 느끼고 중간에 포기합니다.
 **FitFinal**은 이러한 문제를 해결하기 위해 출발했습니다. 복잡하고 막막한 건강 관리 과정을 명확한 데이터와 쉬운 가이드라인으로 바꾸어 드립니다. 옆에서 방향을 잡아주는 든든한 페이스메이커처럼, 목표 체중과 체형에 도달할 때까지 매일의 여정을 함께합니다.

###  서비스 핵심 가치
- **퍼스널라이징 (Personalized):** 개인의 체형, 운동 수행 능력, 식습관에 맞춘 유일무이한 맞춤 플랜을 제공합니다.

- **지속 가능성 (Sustainable):** 극단적인 단식이나 과도한 운동 대신, 일상에 자연스럽게 녹아드는 건강한 라이프스타일 형성을 목표로 합니다.

- **전문성과 데이터 (Professional & Data-driven):** 감에 의존하지 않는 데이터 분석과 검증된 트레이닝 이론을 바탕으로 솔루션을 제안합니다.

### 주요 기능
- **AI 맞춤 루틴 생성:** 운동 목표, 운동 수준, 주당 운동 횟수를 분석하여 맞춤형 주간 운동 루틴 및 핵심 포인트 제공

- **맞춤 식단 관리:** 신장, 체중, 성별, 목표 체중 데이터를 기반으로 기초대사량 추정치, 일일 권장 칼로리, 영양소 비율 및 추천 식단 예시 구성

- **운동 가이드 영상 검색:** YouTube Data API v3를 연동하여 타겟 운동의 정확한 자세 가이드 영상 수집 및 제공

- **일일 기록장:** LocalStorage를 활용하여 당일 운동 및 식단 기록을 개별 브라우저에 저장하고 관리하는 기능 제공

#

### 2. 기술 스택

### Frontend
- **HTML5 / CSS3 / JavaScript (ES6+)**: Pure Vanilla JS 기반 UI 반응형 인터페이스 및 동적 DOM 제어

### Backend
- **Python 3.9+ / FastAPI**: 서버리스 비동기 API 서버 구축 및 외부 API 호출 대리(Proxy) 수행
- **Uvicorn**: ASGI 서버 (로컬 개발 환경)

### External APIs
- **Google Generative AI (Gemini API)**: `gemini-3.5-flash` 모델 기반 운동 루틴 및 식단 생성
- **`YouTube Data API v3`**: 운동 자세 및 가이드 관련 영상 정보 탐색

### Infrastructure & Deployment
- **Vercel**: Vercel을 통한 백엔드(FastAPI Serverless Functions) 및 프론트엔드 통합 자동 배포

**저장소 클론 (Clone Repository)**
git clone [https://github.com/Gonyak004/KDJ-A1-3]

#

### 3. 실행 배포 방법

의존성 패키지 확인 (requirements.txt)

    fastapi
    pydantic
    google-generativeai

가상환경 생성

     (Windows / macOS / Linux 공통)
     python -m venv venv

가상환경 활성화

     (Windows)
     venv\Scripts\activate

가상환경 활성화

     (macOS / Linux)
     source venv/bin/activate

의존성 패키지 설치

     pip install -r requirements.txt


**사이트 URL**

     https://kdj-a1-3.vercel.app/

>브라우저에서 해당 URL로 접속하여 서비스를 테스트할 수 있습니다.

로컬 실행 환경변수 설정

*본 프로젝트는 보안을 위해 소스코드 및 로컬 설정 파일에 API 키를 직접 저장하지 않습니다. 터미널(CLI) 환경에서 직접 환경변수를 내보내어 서버를 실행합니다.*

### Vercel 클라우드 배포 방법

본 프로젝트는 Vercel의 Serverless Functions(Python runtime) 환경을 기반으로 프론트엔드와 백엔드가 함께 배포됩니다.

1. GitHub 저장소 연결Vercel 대시보드에서 Add New Project를 선택하고 본 프로젝트의 GitHub 저장소를 Import합니다.

2. Vercel 환경 변수(Environment Variables) 등록별도의 .env 파일 배포 없이 Vercel 대시보드 내 [Settings] -> [Environment Variables] 메뉴에서 아래 Key-Value 값을 등록합니다.

**별도의 .env 파일 배포 없이 Vercel 대시보드 내 [Settings]  -> [Environment Variables] 메뉴에서 아래 Key 값을 등록합니다.**


|Key | Description |
| ---   |--- |
|GEMINI_API_KEY|Google AI Studio에서 발급받은 Gemini API 키|
|YOUTUBE_API_KEY|Google Cloud Console에서 발급받은 YouTube Data API v3 키|

적용 대상(Target Environments)

 **YOUTUBE_API_KEY**의 Production, Preview, Development 항목을 모두 체크합니다.

배포 및 재배포(Redeploy) 가이드

- 최초 배포 시 Vercel이 루트의 index.html과 api/app.py를 감지하여 서버리스 환경 구축을 자동으로 시작합니다.

- 주의사항: 환경 변수를 신규 추가하거나 변경한 경우, 기존 배포본에는 자동으로 적용되지 않습니다. 반드시 [Deployments] 탭에서 최신 배포 항목 우측의 메뉴(...)를 누르고 [Redeploy]를 실행해야 설정한 환경 변수가 서버리스 함수에 주입됩니다.

#

### 4. 프로젝트 구조


      fitfinal/
      ├── api/
      │   └── app.py            
      ├── css/
      │   └── style.css          
      ├── js/
      │   └── main.js            
      ├── index.html      
      ├── requirements.txt 
      └── README.md               

**백엔드 (fitfinal/api/app.py)**

**CSS (fitfinal/css/style.css)**

**자바스크립트 (fitfinal/js/main.js)**

**프론트엔드 (fitfinal/index.html)**

**의존성 패키지 (fitfinal/requirements.txt)**

#

### 5. API 키 보안 관리 조치

>클라이언트(프론트엔드 JavaScript) 코드에 API 키를 직접 하드코딩하거나 로컬 설정 파일(.env)을 소스코드 저장소(Git)에 포함시킬 경우, 브라우저 개발자 도구나 저장소 노출을 통한 키 유출 및 무단 도용 위험이 존재합니다. FitFinal은 다음과 같은 철저한 보안 조치를 통해 이 문제를 해결했습니다.


**1. .env 파일 배포 전면 배제 및 Git 노출 차단**
- 소스코드 저장소 내에 .env 파일을 일체 작성하지 않으며, 환경 변수를 파일 형태로 저장하지 않고 클라우드 호스팅 인프라에 직접 주입하는 방식을 채택했습니다. 이를 통해 로컬 환경변수 파일의 실수 인한 Git 커밋 및 노출 위험을 근본적으로 차단했습니다.

**2. 순수 Vercel 환경 변수(Environment Variables) 인프라 활용**
- API 키는 오직 Vercel 대시보드의 암호화된 저장 공간(Environment Variables)에만 입력·보관됩니다.
- 서버리스 함수가 실행되는 런타임 시점에만 os.environ을 통해 메모리상에 키가 로드되므로 외부에서 키 값에 직접 접근하는 것이 불가능합니다.

**3. 서버리스 백엔드 대리 호출 (Proxy Pattern)**
- 프론트엔드는 API 키를 전혀 소유하지 않으며, 백엔드 API 엔드포인트(/api/recommend, /api/diet, /api/youtube)로 필요한 파라미터만 전달합니다.
- 모든 외부 API(Gemini, YouTube) 통신은 Vercel Serverless 기반의 백엔드(api/app.py)에서만 처리되므로 클라이언트 개발자 도구의 Network 탭에서도 API 키가 노출되지 않습니다.

**4. API 키 사용 권한 및 도메인 제어**
- 자체 Google Cloud Console을 통해 백엔드가 필요한 전용 API 서비스(Gemini API, YouTube Data API v3) 키 활용 범위를 해당 사이트만 제한하여, 키 오용 가능성을 최소화했습니다.

#

### 6. 필요 증빙 자료

**AI 코딩 사용 도구 대화 로그**

<img width="495" height="68" alt="Image" src="https://github.com/user-attachments/assets/4c40c4bb-ad23-4a65-8a1b-26ecc43f7e4f" />

<img width="720" height="625" alt="Image" src="https://github.com/user-attachments/assets/9ac9d31c-dd0d-4fe0-925d-9623b2210f83" />

<img width="744" height="749" alt="Image" src="https://github.com/user-attachments/assets/b94c00c4-d35d-4805-94a6-b18c4407ce42" />

---

### **메인 홈**

<img width="988" height="940" alt="Image" src="https://github.com/user-attachments/assets/be1edfce-1267-420b-8e86-dc75eb9b9f63" />

---

### **운동 가이드 서비스 메뉴 사용**

<img width="967" height="948" alt="Image" src="https://github.com/user-attachments/assets/a503f929-9e2d-47f9-bb99-665a7abd5966" />

---

### **AI 루틴 매니저 서비스 사용**

<img width="997" height="937" alt="Image" src="https://github.com/user-attachments/assets/1d511ba1-54bd-4891-a076-2e0c26ac52f3" />

---

### **AI 식단 서비스 사용**

<img width="984" height="936" alt="Image" src="https://github.com/user-attachments/assets/d4365cb0-9fc3-456d-99e5-46b7427c613f" />
