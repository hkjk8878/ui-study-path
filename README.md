# UI Study Path — 24주 UX/UI 공부 관리 PWA

GitHub: https://github.com/hkjk8878/ui-study-path

**이 앱은 트임(teuim)과 완전히 별개입니다.** 트임의 Worker, GitHub 저장소, KV, 데이터를 수정하거나 사용하지 않습니다.

## 현재 구조 (GitHub에서 자동 배포)
- 새 Cloudflare Worker 애플리케이션 **ui-study-path** 하나로 웹사이트와 API를 함께 배포합니다.
- GitHub 저장소에 `wrangler.jsonc`, `index.html`, `payload.txt`, `worker.js`, `config.js`, `sw.js` 등이 있습니다.
- `payload.txt`: HTML 화면·CSS·JS·24주 168일 학습 데이터를 압축한 파일. 삭제하면 앱이 열리지 않습니다.
- `assets/reference-plan.pdf`: 기존 24주 PDF 원본 (변경하지 않음).
- `worker.js`: 이 앱 **전용** 공부 기록 저장 API. 트임 API·KV와 공유하지 않습니다.
- `wrangler.jsonc`: 정적 사이트 + API를 Worker 하나로 배포하고 **STUDY_KV**를 바인딩하도록 구성했습니다.
- `config.js`: 같은 도메인의 앱/저장 API를 사용하도록 `location.origin` 지정.
- 각 기기는 체크 기록을 우선 브라우저에 보관하고, 인터넷이 되면 저장 API에 전송합니다. 화면이 활성화된 동안 약 8초마다 새 기록을 확인하나 KV 특성상 변경 전파는 지연될 수 있습니다.

## Cloudflare에서 확인할 항목 (별도 Pages나 Worker를 새로 만들지 마세요)

현재 생성한 **Workers & Pages → ui-study-path** 프로젝트를 그대로 이용하세요.

1. **Deployments** 탭에서 최신 GitHub 배포의 상태 확인. 빌드 실패라면 빌드 로그를 확인하세요. GitHub에 새 커밋이 푸시되면 Cloudflare가 다시 배포합니다.
2. **Settings → Builds**에서 **Build command 비움** (정적 소스라 별도 빌드 불필요), **Deploy command `npx wrangler deploy`** 확인.
3. **Settings → Domains & Routes** (또는 **Domains**)에서 **workers.dev** 주소가 비활성화되어 있다면 **Enable**. 계정 전체 workers.dev 서브도메인 설정이 추가로 필요할 수 있습니다. UI는 변경될 수 있습니다.
4. **Settings → Bindings**에서 **STUDY_KV**가 있는지 확인. `wrangler.jsonc`는 Cloudflare Wrangler 4.45.0+의 자동 KV 프로비저닝을 요청합니다. 빌드가 이를 지원하면 자동 생성됩니다. **자동 생성에 실패하면** 새 KV 네임스페이스를 만든 뒤 STUDY_KV로 연결해야 하며, 그때는 설정 파일에 네임스페이스 id를 추가해야 할 수 있습니다.
5. 공개 도메인 `https://ui-study-path.<실제 workers.dev 서브도메인>/`에서 앱 화면 확인. (서브도메인은 반드시 Cloudflare가 실제로 표시한 주소를 쓰세요.)
6. 동일 도메인의 `/health`에서 `{"ok":true,...}` 확인하고 **동일 도메인의 `/api/session`에서 JSON 사용자 응답** 확인. 저장 기능은 KV가 연결되어 있어야 동작합니다.

## 사용 방법
- 날짜별 강의·과제 체크 / 실제 공부시간 기록 / 학습 메모 / 24주 계획 및 자료 링크 / 프로젝트 마감 / 주간 자기점검 / JSON 기록 백업 및 복원.
- iPhone/iPad: Safari로 사이트 접속 → 공유 → **홈 화면에 추가**.
- Android: Chrome → 메뉴 → **앱 설치** 또는 홈 화면에 추가.
- PC: Chrome/Edge 설치 버튼.

## 데이터와 주의 사항
- **로그인이 없습니다.** UI Study Path의 공개 Worker 주소를 아는 사람은 기록을 열람·수정할 수 있습니다. 실제 학생·학원 개인정보 또는 민감한 기록은 적지 마세요.
- KV는 최종 일관성 저장소입니다. 여러 기기에서 동일 항목 동시 수정은 충돌할 수 있고 반영이 지연될 수 있습니다.
- GitHub 배포로 앱을 업데이트하더라도 **기존 KV를 유지**하면 서버 기록이 유지됩니다. 앱 설정 화면에서 주기적으로 JSON 백업을 권장합니다.
- Cloudflare Worker가 연결되지 않은 동안 저장된 기록은 기기별 로컬에만 존재할 수 있으므로, 동기화 표시와 실제 반영을 확인하세요.

**현재 상태**: GitHub 소스 및 Worker 설정 업로드 완료. Cloudflare 실제 빌드 완료·공개 URL 활성화·KV 생성·다른 기기 기록 반영은 아직 실사용 검증 전입니다.

Cloudflare 공식 문서:
- https://developers.cloudflare.com/workers/static-assets/binding/
- https://developers.cloudflare.com/changelog/post/2025-10-24-automatic-resource-provisioning/
- https://developers.cloudflare.com/workers/ci-cd/builds/configuration/
