# UI Study Path

**24주 UX/UI 학습·포트폴리오 체크리스트 PWA** — 원본 학습 PDF를 변경하지 않고 개인 공부 진행도를 관리합니다.

현재 GitHub에는 전체 UI, CSS, JavaScript, 24주/168일 계획, 학습 기록 및 체크 기능, 프로젝트 마감, 자기점검, 데이터 백업·복구, 원본 PDF, 독립 Worker 코드가 업로드되어 있습니다.

## 기능

- **오늘**: 날짜별 강의·과제 체크, 실제 공부 시간, 학습 메모
- **24주 계획**: 2026-11-02 ~ 2027-04-18, 자료 링크·주간 제출물
- **프로젝트**: 영어학원 앱, 소비자 UX, 조건부 인터랙션, 각 마감일·제출물 확인
- **자기점검**: 주간 점검·진행률
- **PWA**: iPhone/iPad/Android/PC 반응형, 홈 화면에 추가
- **백업**: 앱 설정에서 공부 기록 JSON 내보내기·가져오기

## Cloudflare 배포 — 기존 트임과 완전히 독립적으로

GitHub 저장소: https://github.com/hkjk8878/ui-study-path

**트임(teuim) 저장소/Worker/KV/Pages와 연결하거나 수정하지 않습니다.**

### 1. 새 KV 만들기

[Cloudflare Dashboard](https://dash.cloudflare.com/) → **Storage & databases → KV → Create namespace** → 이름 **`ui-study-path-data`**.

### 2. 새 Worker 만들기

**Workers & Pages → Create → Worker**에서 **`ui-study-path-sync`** 이름의 새 Worker 생성.

GitHub 저장소의 [worker.js](https://github.com/hkjk8878/ui-study-path/blob/main/worker.js)를 Cloudflare Worker 코드 편집기에 복사하여 배포.

새 Worker 설정 **Bindings → Add binding → KV**:
- Variable name: **`STUDY_KV`**
- Namespace: 방금 만든 **`ui-study-path-data`**

저장 후 새 Worker의 `https://ui-study-path-sync.<account-subdomain>.workers.dev/health` 주소를 열어 `{"ok":true,...}` 표시 확인.

### 3. Worker 주소를 앱에 입력

GitHub [config.js](https://github.com/hkjk8878/ui-study-path/blob/main/config.js)의

`window.UI_STUDY_WORKER = '';`

를

`window.UI_STUDY_WORKER = 'https://ui-study-path-sync.<account-subdomain>.workers.dev';`

로 수정. **반드시 새 UI Study Path Worker 주소**를 넣고, 트임 URL은 넣지 마세요.

### 4. 새 Cloudflare Pages 사이트 연결

Cloudflare **Workers & Pages → Create → Pages → Connect to Git → GitHub**에서 **`hkjk8878/ui-study-path`**만 선택.

- Project name: **`ui-study-path`** (사용 가능하면)
- Production branch: `main`
- Framework preset: **None**
- Build command: **비워둠**
- Build output directory: **`.`** (저장소 루트)

저장/Deploy. 새 `*.pages.dev` 사이트를 열어 확인.

### 5. 동기화 테스트

PC·휴대폰에서 새 Pages 사이트 접속 → 같은 날짜 과제 체크 → 양쪽에서 확인. 앱은 페이지가 열려 있을 때 약 8초마다 동기화를 시도합니다. Workers KV는 지역에 따라 전파가 늦을 수 있습니다. 동시 수정은 충돌할 수 있으니 같은 항목을 여러 기기에서 동시에 편집하지 마세요.

## 사용 전 중요 사항

- **로그인 없음.** 새 Worker 주소를 아는 사람은 체크·메모를 읽거나 수정할 수 있어요. 학생·학원 관련 개인정보는 입력하지 마세요.
- `config.js`의 Worker 주소를 비워두면 **해당 기기에만 저장되는 체험 모드**입니다.
- Github 연결과 Cloudflare 계정 연결은 별개입니다. **현재 Github에는 업로드했지만 Cloudflare 프로젝트를 직접 생성하지 않았습니다.**
- ZIP 다운로드 없이 Github에서 바로 Cloudflare Pages에 연결할 수 있습니다.
- `payload.txt`는 앱 코드·스타일·일일 계획을 묶은 데이터 파일입니다. 삭제하거나 이름을 바꾸면 앱이 열리지 않습니다.
- `assets/reference-plan.pdf`는 이전에 제작한 원본 PDF이며 내용은 수정하지 않았습니다.
- 기존 체크·메모는 앱 업데이트 시 유지되도록 안정적인 작업 ID와 독립 KV를 사용합니다. 중요한 기록은 주기적으로 백업하세요.

## 홈 화면에 설치

- iPhone/iPad: Safari → 공유 → **홈 화면에 추가**
- Android: Chrome → 메뉴 → **앱 설치/홈 화면에 추가**
- PC: Chrome/Edge 주소 표시줄의 앱 설치 메뉴

**배포 상태:** Github 소스 업로드 완료. Cloudflare Pages/Worker/KV 설정 및 실제 기기 간 동기화는 아직 별도 진행 필요.
