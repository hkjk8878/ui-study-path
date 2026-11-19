## 이름 짓기 가이드 (Figma 실무 기준)

### 왜 이름이 중요한가
- **개발자는 이름을 그대로 본다.** 개발 전달 화면에 레이어·컴포넌트·변수 이름이 그대로 뜨고, 변수 이름은 코드 토큰(`--action-primary`)으로 바뀐다.
- **찾을 때 쓴다.** Assets 검색, Ctrl+F, 레이어 패널 모두 이름으로 찾는다.
- **Figma 공식 안내:** 지금 보이는 모양이 아니라 *무엇인지*로 짓는다. 정답 규칙은 없고, 팀이 먼저 정해 그대로 지킨다. 이 루틴과 ‘하루_연습’ 파일은 아래 규칙을 쓴다.

### 표기법 — 딱 3가지
| 표기 | 모양 | 어디에 쓰나 |
|---|---|---|
| **한국어** | `추가-오류` | 페이지 · 화면 Frame · Flow · Section |
| **영어 소문자** | `button` · `todo/row` · `state=default` · `header` · `more-button` · `text/primary` | 그 밖의 영어 이름 전부 (컴포넌트 · Variant · 레이어 · 변수 · 스타일) |
| **첫 글자 대문자** | `Primitives` · `Semantic` | 변수 컬렉션 이름만 |

> **한 줄 기억** · 큰 단위(페이지·화면·흐름)는 한국어 · 영어는 모두 소문자(컬렉션 이름만 예외) · / = 폴더(컴포넌트·변수·스타일), - = 두 단어 잇기

### 대상별 정리
| 대상 (Figma에서 보이는 곳) | 예 |
|---|---|
| 페이지 (왼쪽 위 Pages) | 표지 · 기초 · 컴포넌트 · 화면 · 프로토타입 · 전달 · 주간 기록 |
| 화면 Frame (맨 위 Frame) | 목록 · 추가-오류 · 일정 변경-완료 |
| 화면 안의 칸 | header · content · footer (탭이 있으면 tab-bar) |
| Main component (◆) | button · input · checkbox · todo/row · icon/check |
| Variant (오른쪽 패널) | type=primary · secondary / state=default · hover · pressed · disabled (값이 true/false면 토글로 보인다) |
| 컴포넌트 속성 | label · show icon · icon |
| 목록 한 줄 안쪽 레이어 | leading · content(headline · supporting-text) · trailing(reorder) |
| 변수 컬렉션 / 변수 | Primitives · Semantic / green/600 · space/16 · text/primary · action/primary-hover |
| 스타일 | heading/large · body/regular · caption · shadow/small |
| Instance (◇) | 이름은 바꾸지 않아도 된다. 바꿔도 원본 연결은 안전하다 |

### 이름 상식 (루틴 곳곳에 다시 나온다)
| 주제 | 핵심 |
|---|---|
| 위계와 진하기 | 중요도 순서는 primary · secondary · tertiary, 진하기는 subtle · default · strong. 그래서 테두리는 border/strong이지 border/primary가 아니다 |
| 변수 층 | Primitive(실제 값) → Semantic(역할) → Component(한 부품 전용). 건너뛰지 않는다. ‘하루’는 2층 |
| on- | text/on-action = 초록 버튼 위 글자. 배경과 짝으로 짓는다 |
| 상태 색 | status/error · warning · success · info |
| 색 단계 | 50~900, 클수록 진함, 500 기준, 중간 숫자는 비워 둔다 |
| 간격 | space/4 … space/32 (4의 배수, 이름 = 값), radius/999 = 알약 모양 |
| 글자 단계 | display > headline > title > body > label (Material 3). 굵기 regular 400 · medium 500 · semibold 600 · bold 700 |
| 상태 순서 | default → hover → pressed → focused → disabled (+ selected · loading) |
| 버튼 위계 | primary는 화면마다 하나, 되돌리기 어려운 행동은 danger |
| 화면 너비 | mobile 390 · tablet 768 · desktop 1280 (바뀌는 지점 = breakpoint) |
| 움직임 | duration/fast · normal · slow, easing/enter(ease-out) · exit(ease-in) |

### 실무 팁
1. **생김새 말고 역할로.** `button/blue` ✗ → `button` + `type=primary` ✓ · `text/gray-900` ✗ → `text/primary` ✓. 색을 바꾸면 생김새 이름은 거짓말이 된다.
2. **같은 뜻은 같은 단어 하나로.** 상태 단어는 위 ‘상태 순서’ 목록에서만 고른다.
3. **폴더는 2단계까지.** `todo/row` ✓ · `app/todo/list/row` ✗.
4. **아이콘만 예외로 모양 이름.** icon/check · icon/more · icon/close.
5. **한 번에 바꾸기.** 여러 레이어 선택 → Ctrl+R(일괄 이름 바꾸기, 번호 붙이기도 된다).
6. **레이어를 컴포넌트로 만들 때(Ctrl+Alt+K) 이름도 바꾼다.** todo-card(레이어) → todo/card(컴포넌트).

### 자주 하는 실수 → 고치기
| 실수 | 고친 이름 |
|---|---|
| Frame 12 · Rectangle 3이 남음 | Ctrl+F로 찾아 역할 이름으로 |
| 한 세트 안에서 대소문자가 섞임 (Default · disabled) | default · disabled |
| 레이어에 대문자·띄어쓰기 (More Button) | more-button |
| 컴포넌트에 하이픈 (reader-button) | button/reader |
| 테두리에 위계 이름 (border/primary) | border/strong |
| 변수에 색 이름 (text/gray) | text/secondary |
