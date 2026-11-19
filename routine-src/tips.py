# 이름 상식 — 그 내용이 처음 나오는 블록에 넣는다 (표 = 이름 | 뜻 | 어디에)
T_SCALE = ('이름 상식 — 색 단계 숫자\n| 이름 | 뜻 |\n| 50 · 100 · 200 … 900 | 숫자가 클수록 진하다. 500이 기준 |\n'
 '| green/500 · green/600 · green/800 | 중간 숫자는 비워 둔다 → 나중에 사이 색을 넣을 자리 |\n| white · black | 흰색·검정은 단계 없이 |')
T_SPACE = ('이름 상식 — 간격·모서리 이름\n| 이름 | 뜻 |\n| space/4 … space/32 | 4의 배수(4px 그리드). 이름 = 값이라 바로 안다 |\n'
 '| space/sm · space/md | 실무에 있는 크기 이름 방식. 처음에는 숫자 이름이 덜 헷갈린다 |\n| radius/999 | 끝이 완전히 둥근 알약 모양(pill) |')
T_LAYER = ('이름 상식 — 변수는 층이 있고, 층을 건너뛰지 않는다\n| 층 | 하는 일 | 예 |\n| Primitive | 실제 값 | green/600 = #3D7A34 |\n'
 '| Semantic | 역할. Primitive를 가리킨다 | action/primary → green/600 |\n| Component | 한 부품 전용. Semantic을 가리킨다 | button/primary/background/hover → action/primary-hover |\n'
 '· 여러 부품이 같이 쓰면 Semantic, 한 부품만 따로 바꿔야 할 때만 Component. ‘하루’는 2층(Primitive → Semantic)\n'
 '· Component → Primitive처럼 건너뛰어 연결하지 않는다 → 층을 지켜야 무엇을 바꾸면 어디가 바뀌는지 예측된다')
T_HIER = ('이름 상식 — 위계(순서)와 진하기는 다른 말\n| 구분 | 이름 | 뜻 | 어디에 |\n'
 '| 위계 | primary · secondary · tertiary | 주인공 · 조연 · 단역 | 버튼 · 글자 |\n'
 '| 진하기 | subtle · default · strong | 옅게 · 보통 · 진하게 | 테두리 · 배경 |\n'
 '· 그래서 테두리는 border/strong. border/primary ✗ → action/primary가 초록이라 “초록 테두리?”로 착각한다\n'
 '· 실무 예: GitHub Primer default · muted · emphasis / Atlassian border · border.bold / Material outline · outline-variant')
T_ON = ('이름 상식 — 짝 이름과 상태 색\n| 이름 | 뜻 |\n| text/on-action | 초록 버튼(action) 위에 올라가는 글자. 배경 이름과 짝으로 짓는다 |\n'
 '| status/error · warning · success · info | 오류(빨강) · 주의(주황) · 완료(초록) · 안내(파랑) — 어느 회사든 거의 같은 이름 |')
T_PAIR = ('이름 상식 — 검사할 색 조합 (글자색 + 그 글자 뒤 배경색)\n| 글자색 | 배경색 |\n| text/primary | bg/surface |\n| text/on-action | action/primary |\n| status/error | bg/surface |')
T_TYPE = ('이름 상식 — 글자 단계 이름\n| 이름 | 뜻 |\n| display > headline > title > body > label | Material 3의 큰 순서: 가장 큰 제목 → 제목 줄 → 제목 → 본문 → 버튼·작은 표시 |\n'
 '| heading · body · caption · button | 이 루틴이 줄여 쓰는 이름 |\n| large · medium · small | 단계 안 크기 |\n'
 '| regular 400 · medium 500 · semibold 600 · bold 700 | 굵기 이름과 숫자 |\n'
 '· 왜: 스타일 이름이 역할이면 크기를 바꿔도 이름을 고칠 필요가 없다')
T_STATE = ('이름 상식 — 상태 이름과 순서\n| 이름 | 뜻 |\n| default | 기본 |\n| hover | 마우스 올림(PC만) |\n| pressed | 누른 순간 |\n'
 '| focused | 키보드로 고름·입력 중 |\n| disabled | 못 누름 — 인터랙션을 넣지 않는다 |\n| selected · loading | 골라진 상태 · 기다리는 중 |\n'
 '· 왜: 이 순서가 실무 명세의 기본 목록이라 빠진 상태를 바로 찾는다')
T_BTN = ('이름 상식 — 버튼 위계\n| 이름 | 뜻 | 규칙 |\n| primary | 주요 | 화면마다 하나만 |\n| secondary | 보조 | |\n| tertiary | 가장 약함 | 글자만 있는 버튼 |\n'
 '| danger | 위험(빨강) | 지우기처럼 되돌리기 어려운 행동 |')
T_DANGER = ('이름 상식 — 지우기 확인창\n| 버튼 | 이름 | 글자 |\n| 삭제 | type=danger | ‘확인’이 아니라 하는 일 그대로 ‘삭제’ |\n| 취소 | type=secondary | 취소 |')
T_BP = ('이름 상식 — 화면 너비와 그리드\n| 이름 | 뜻 |\n| mobile · tablet · desktop | 390 · 768 · 1280 |\n| breakpoint | 화면 구성이 바뀌는 너비 |\n'
 '| columns · gutter · margin | 열 수 · 열 사이 간격 · 바깥 여백 |')
T_LIST = ('이름 상식 — 목록 한 줄의 구조 (Material 3 · iOS 공통)\n| 자리 | 이름 | 들어가는 것 |\n| 앞 | leading | 체크박스 · 아이콘 |\n'
 '| 가운데 | content (headline · supporting-text) | 제목 · 보조 글 |\n| 뒤 | trailing | 더보기 · reorder(순서 바꾸기) |\n'
 '· 아이콘만 예외로 모양 이름(icon/check · icon/more). 무슨 일을 하는지는 그 아이콘을 쓰는 버튼이 정한다')
T_MOTION = ('이름 상식 — 움직임 값 이름\n| 이름 | 뜻 |\n| duration/fast · normal · slow | 100ms · 200ms · 300ms |\n'
 '| easing/standard | 보통 움직임 |\n| easing/enter | 나타날 때(ease-out: 빨리 시작해 천천히 멈춤) |\n| easing/exit | 사라질 때(ease-in: 천천히 시작해 빨리 나감) |\n'
 '· 왜: 이름으로 쓰면 앱 전체 움직임이 같은 리듬이 된다')
T_ELEV = ('이름 상식 — 그림자 단계 (Material은 elevation = 높이)\n| 이름 | 쓰는 곳 |\n| shadow/small | 카드 |\n| shadow/medium | 떠 있는 메뉴 |\n| shadow/large | 확인창 |')
T_DATA = ('이름 상식 — 화면 상태 이름\n| 이름 | 뜻 |\n| empty | 빈 상태 |\n| loading | 불러오는 중 |\n| error | 오류 |\n| success | 완료 |\n| no-permission | 권한 없음 |\n'
 '· 화면 Frame은 한국어(일정 목록-빈 상태), 부품 Variant는 영어(state=empty)')
T_REVIEW = ('이름 상식 (3주차 복습)\n| 주제 | 이름 |\n| 위계 | primary · secondary · tertiary |\n| 진하기 | subtle · default · strong |\n'
 '| 목록 한 줄 | leading · content · trailing |\n| 상태 순서 | default → hover → pressed → focused → disabled |\n| 변수 층 | Primitive → Semantic (필요한 부품만 Component) |')
T_CARD = ('이름 상식 — 카드 안 이름\n| 이름 | 뜻 |\n| thumbnail | 썸네일 |\n| title | 제목 |\n| meta | 작은 정보(회차·날짜) |\n| badge | 배지 |\n| progress | 이어 보기 진행 |\n| size = small · medium · large | 크기 Variant |')
TIPS = {
 ('11-16','08:30'): [T_SCALE], ('11-16','10:10'): [T_SPACE], ('11-17','08:00'): [T_LAYER],
 ('11-17','08:20'): [T_HIER, T_ON], ('11-17','10:10'): [T_TYPE], ('11-18','10:10'): [T_PAIR],
 ('11-19','10:10'): [T_STATE, T_BTN], ('11-20','08:30'): [T_BP], ('11-22','09:00'): [T_DANGER],
 ('11-23','08:20'): [T_LIST], ('11-24','08:00'): [T_MOTION], ('12-21','08:00'): [T_REVIEW],
 ('12-28','09:00'): [T_ELEV], ('12-30','08:00'): [T_DATA], ('02-15','09:00'): [T_CARD], ('03-11','10:10'): [T_MOTION],
}
