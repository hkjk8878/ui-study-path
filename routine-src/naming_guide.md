# Figma 이름 짓기 가이드 v2 — 근거 기준판 (2026-11-23 확정)

> 이 문서가 ‘하루’ 파일(하루v02)과 루틴의 **유일한 이름 기준**이다. 앞선 대화·문서의 이름 규칙과 다르면 이 문서를 따른다.
> 기준 순서: ① **Figma 공식 예제 디자인 시스템 SDS**(Simple Design System, Figma가 직접 공개한 파일과 코드) → ② **Figma 공식 도움말** → ③ **Material 3**(Google, 컴포넌트 토큰과 부품 구조 이름).
> SDS 값은 공개 저장소 `figma/sds`의 `tokens.json`, `styles.json`, `button.css`, Code Connect 파일을 직접 열어 확인했다. ‘속성/역할/변형’ 순서는 Atlassian(`color.background.danger.bold.hovered`) · GitHub Primer(`bgColor-danger-emphasis`)도 같은 방식이다.
>
> **기준 고정 규칙**
> 1. 이름은 **SDS에 있으면 SDS 그대로** 쓴다. SDS에 없을 때만 ② Figma 도움말 → ③ Material 3 순서로 찾는다.
> 2. 다른 예제·글에서 다른 이름을 봐도 **이 문서를 바꾸지 않는다.** (Figma 예제끼리도 이름이 다르다 → 하나를 기준으로 정한 것이 이 문서다)
> 3. 이 문서를 고치는 경우는 두 가지뿐이다: **SDS 실제 파일과 다르게 적은 것을 찾았을 때**, **SDS에 없는 것을 새로 정할 때.** 고칠 때는 근거 파일 이름을 같이 적는다.
> 4. 예외는 대소문자 하나다 (0장 규칙 4).

---

## 0. 큰 규칙 4개

| 규칙 | 내용 | 근거 |
|---|---|---|
| 1. 색은 2층 | `Color Primitives`(실제 값) → `Color`(쓰임) | SDS 컬렉션 구조 |
| 2. 숫자는 1층 | `Size` 컬렉션 하나. 값을 바로 넣고 부품에 바로 연결 | SDS `Size` 컬렉션 |
| 3. Component 층은 Figma에 만들지 않는다 | 부품 전용 값은 개발 코드에서 만든다. 필요해지면 정해진 이름 순서로 만든다 (5장) | Figma 도움말: 컴포넌트 토큰은 큰 엔터프라이즈 시스템용 / SDS는 코드에만 둠 |
| 4. 대소문자는 한 가지로 | ‘하루’는 **영어 소문자 + 하이픈**. 컬렉션 이름만 Title Case | Figma 도움말: Title Case · lower case · camelCase 중 **하나를 정해 지키라**고만 함. SDS는 Figma 안에서 Title Case를 쓰고 코드에서 소문자-하이픈으로 바꾼다. ‘하루’는 코드 이름과 바로 같도록 소문자를 쓴다 |

---

## 1. 변수 컬렉션 — SDS 컬렉션 이름 그대로

| 컬렉션 | 층 | 하는 일 | 부품에 직접 연결? |
|---|---|---|---|
| `Color Primitives` | Primitive | 색 실제 값 | ✗ (Scoping 끄기) |
| `Color` | Semantic | 색 쓰임 (Color Primitives를 가리킴) | ✓ |
| `Size` | (숫자는 1층) | 간격 · 모서리 · 테두리 · 아이콘 크기 | ✓ |
| – | Component | 만들지 않는다 (0장 규칙 3) | – |

- 층 이름(Primitive · Semantic · Component)은 **구조를 설명하는 말**이고, 컬렉션 이름은 SDS처럼 **안에 든 것**(Color · Size)으로 짓는다.
- 참고: Figma Learn 강의(Habitz)는 `Primitives` · `Tokens`라는 다른 이름을 쓴다. 구조는 같고, 이 문서는 기준 고정 규칙 1에 따라 SDS 이름을 쓴다.

---

## 2. Color Primitives — `색상/단계` (100 ~ 1000, 클수록 진함)

**SDS 규칙:** 색상 이름(`gray`, `green` …) + 100 단위 단계. 흰색·검정도 `white/1000`, `black/1000`처럼 단계로 쓴다(낮은 숫자는 투명도).

하루v02 파일의 실제 색 (11/23 사용자 화면 기준, 밝기를 계산해 단계를 정함):

| 지금 이름 | 값 | 새 이름 |
|---|---|---|
| color/green/50 | D2E077 | `green/300` |
| color/green/100 | A4C263 | `green/400` |
| color/green/200 | 6DC458 | `green/500` |
| color/brown/50 | F3E5C2 | `brown/200` |
| color/brown/100 | E8CFA6 | `brown/300` |
| color/brown/300 | C49A6C | `brown/400` |
| color/brown/400 | AA7959 | `brown/500` |
| color/brown/600 | 8C7369 | `brown/600` |
| color/brown/700 | 7B6762 | `brown/700` |
| color/brown/800 | 645552 | `brown/800` |
| color/netral/0 | FFFFFF | `white/1000` |
| color/netral/200 | C1C8B9 | `gray/300` |
| color/netral/500 | 6B7470 | `gray/500` |
| color/red/300 | CF4843 | `red/500` |

- 컬렉션 이름이 Color Primitives라서 `color/` 그룹은 쓰지 않는다 (SDS도 `green/300`처럼 바로 쓴다). `netral`(오타) → `gray`.
- 단계는 **밝기 순서**로 다시 맞췄다 (예: D9BE92가 E9C989보다 어두워서 400).
- 중간 숫자는 비워 둔다 → 나중에 사이 색을 넣을 자리.

---

## 3. Color — `속성/역할/변형`

**SDS 규칙 (실제 이름 예: `background/brand/default`, `text/brand/on-brand`, `border/danger/default`)**

| 자리 | 고르는 값 |
|---|---|
| 속성 (어디에 칠하나) | `background` · `text` · `icon` · `border` |
| 역할 (무슨 뜻인가) | `default`(기본 화면) · `brand`(주인공 색) · `neutral`(어두운 반전 영역) · `positive` · `warning` · `danger` · `disabled` · `utilities` |
| 변형 (그 안에서 무엇이 다른가) | `default` · `secondary` · `tertiary` · `hover` · `on-brand`(그 색 위의 글자) · `on-neutral` · `on-danger` |

### ‘하루’에 만들 Color 변수

> 이 표의 이름이 기준이다. 오른쪽 색 단계는 하루_연습 파일 색으로 정한 예다 — **하루v02에서는 이미 연결된 값을 그대로 두고 이름만 바꾼다.** 새로 만드는 변수만 밝기가 비슷한 단계를 고르고 대비 플러그인으로 다시 잰다.


| 이름 | → Color Primitives (예) | 쓰는 곳 | 대비 (하루_연습 색으로 계산) |
|---|---|---|---|
| **background** | | | |
| `background/default/default` | brown/100 | 입력칸, 확인창, 체크박스 안 | – |
| `background/default/secondary` | brown/200 | 카드 · 배너 · 탭 묶음, **neutral 버튼** | – |
| `background/default/secondary-hover` | brown/100 | neutral 버튼 마우스 올림 | – |
| `background/default/tertiary` | brown/400 | 화면 전체 바탕 | – |
| `background/brand/default` | green/700 | **primary 버튼**, 체크됨, 고른 탭 | – |
| `background/brand/hover` | green/500 | primary 버튼 마우스 올림 | – |
| `background/brand/pressed` | green/900 | primary 버튼 누름 (SDS에 없는 상태라 같은 규칙으로 추가) | – |
| `background/neutral/default` | brown/900 | tab-bar 바탕 | – |
| `background/danger/default` | red/600 | 삭제 버튼 | – |
| `background/disabled/default` | gray/200 | 못 누르는 버튼 | – |
| **text** | | | |
| `text/default/default` | brown/900 | 일반 글자 | 크림 위 11.6 ✅ |
| `text/default/secondary` | gray/600 | 보조 글자 (09:00, 개수) | 크림 위 약 8.5 ✅ |
| `text/brand/default` | green/900 | 초록 강조 글자 (23:00), subtle 버튼 글자 | 크림 위 약 8.9 ✅ |
| `text/brand/on-brand` | white/1000 | 초록 버튼 위 글자 | 5.2 ✅ |
| `text/neutral/on-neutral` | brown/200 | tab-bar 위 글자 | – |
| `text/danger/default` | red/600 | 오류 문구 | 크림 위 약 4.8 ✅ |
| `text/danger/on-danger` | white/1000 | 삭제 버튼 글자 | – |
| `text/disabled/default` | gray/400 | 못 누르는 글자 (대비 기준 예외) | – |
| **icon** | | | |
| `icon/default/default` | brown/900 | ▲▼ · ← 아이콘 | – |
| `icon/brand/on-brand` | white/1000 | 체크 표시 ✓ | – |
| `icon/neutral/on-neutral` | brown/200 | tab-bar 아이콘 | – |
| `icon/disabled/default` | gray/400 | 못 누르는 아이콘 | – |
| **border** | | | |
| `border/default/default` | brown/900 | 카드 · 버튼 · 입력칸 테두리 | – |
| `border/brand/default` | green/700 | 빈 체크박스 테두리, 초록 칩 테두리 | – |
| `border/danger/default` | red/600 | 오류 난 입력칸 | – |
| `border/disabled/default` | gray/400 | 못 누르는 버튼 테두리 | – |

- **글자색 짝 규칙 (SDS):** 색 바탕 위 글자는 `on-역할` → 초록 위 = `text/brand/on-brand`, 빨강 위 = `text/danger/on-danger`.
- **아이콘은 `icon/`으로 따로** 칠한다 (SDS는 text와 icon을 나눈다).
- **그림자 색은 변수로 만들지 않는다.** SDS는 그림자를 Effect 스타일(`Drop Shadow/100`~`600`)로 둔다 → 6장.
- **SDS hover 방향:** SDS는 hover를 한 단계 **진하게** 한다(brand/800 → 900). ‘하루’는 지금 디자인대로 밝게 두되, 바꾸려면 `background/brand/hover`의 연결만 바꾸면 된다.

---

## 4. Size — `종류/단계` (100 = 4px)

**SDS 실제 값 그대로**, 쓰는 것만 만든다.

| 이름 | 값 | 쓰는 곳 | Scoping |
|---|---|---|---|
| `space/100` | 4 | 아이콘 ↔ 숫자 | Gap · Padding |
| `space/200` | 8 | 버튼 안 아이콘 ↔ 글자, 버튼 ↔ 버튼 | Gap · Padding |
| `space/300` | 12 | 버튼 안쪽 여백 (SDS 버튼 medium), 할 일 행 ↔ 행 | Gap · Padding |
| `space/400` | 16 | 카드 · toast 안쪽, 화면 양옆 | Gap · Padding |
| `space/600` | 24 | 카드 ↔ 카드 | Gap · Padding |
| `space/800` | 32 | 큰 덩어리 사이 | Gap · Padding |
| `space/1200` | 48 | 버튼 높이 (누르는 영역) | Width · Height |
| `radius/100` | 4 | 체크박스 | Corner radius |
| `radius/200` | 8 | 버튼 · 입력칸 · 카드 · toast (SDS 버튼도 200) | Corner radius |
| `radius/400` | 16 | 확인창 | Corner radius |
| `radius/full` | 9999 | 알약 배지 | Corner radius |
| `stroke/border` | 2 | 테두리 굵기 (SDS 값은 1, ‘하루’ 디자인은 2) | Stroke |
| `stroke/focus-ring` | 2 | 키보드 포커스 테두리 | Stroke |
| `icon/small` | 24 | 아이콘 | Width · Height |

---

## 5. Component 층 — 지금은 만들지 않는다. 만들 때의 이름

- SDS는 부품 전용 값을 **코드에서만** 만든다: `--button-background-color`, `--button-border-color`, `--button-color`, `--button-padding-x`.
- Material 3 이름 순서: **부품 → 상태 → 부분 → 속성** (실제 예: `md.comp.filled-button.hover.label-text.color`, 코드에서는 `--md-filled-button-container-color`).
- ‘하루’에서 필요해지면 (예: “토글만 파랑으로”) Figma 이름은 `toggle/selected/track/color` 처럼 `부품/상태/부분/속성`으로 짓고, 값은 Color 변수를 가리킨다.

| 자리 | 예 |
|---|---|
| 부품 | `button` · `toggle` · `input-field` |
| 상태 (없으면 생략) | `hover` · `pressed` · `disabled` · `selected` |
| 부분 (Material 3 부품 구조 이름) | `container` · `label-text` · `icon` · `track` · `supporting-text` |
| 속성 | `color` · `shape` · `height` |

---

## 6. 스타일

### 텍스트 스타일 — SDS 이름 순서
| 이름 | 크기 / 줄 높이 | 굵기 | SDS 이름 | 쓰는 곳 |
|---|---|---|---|---|
| `heading` | 24 / 32 | regular | Heading | 화면 큰 제목 |
| `subheading` | 20 / 28 | regular | Subheading | 카드 제목 |
| `body/base` | 16 / 24 | regular | Body Base | 본문, 할 일 제목 |
| `body/strong` | 16 / 24 | bold | Body Strong | 강조 본문 |
| `body/small` | 14 / 20 | regular | Body Small | 보조 글자 (09:00) |
| `single-line/body-base` | 16 / 16 | regular | Single Line/Body Base | 버튼 · 탭 글자 (한 줄만 쓰는 곳) |

- 보조 글자는 13 → **14**: SDS Body Small이 14이고, Galmuri14 픽셀 폰트의 기준 크기와도 같다. 줄 높이 20은 4의 배수.
- 지금 이름 → 새 이름: `heading/large` → `heading`, `heading/medium` → `subheading`, `body/regular` → `body/base`, `caption` → `body/small`, `button` → `single-line/body-base`.

### Effect 스타일 — SDS 이름
| 이름 | 쓰는 곳 |
|---|---|
| `drop-shadow/100` | 버튼 · 카드 그림자 (X 0, Y 2, Blur 0, 색 brown/900) |
| `drop-shadow/200` | 확인창처럼 더 떠 있는 것 (필요할 때) |

---

## 7. 컴포넌트 이름 — SDS 컴포넌트 이름을 따른다

Figma 도움말: **생김새가 아니라 무엇인지로 짓고, 개발 용어와 맞춘다** (`Button` ↔ `<Button>`).

| ‘하루’ 부품 | 컴포넌트 이름 | SDS 이름 | 지금 이름 |
|---|---|---|---|
| 버튼 | `button` | Button | button |
| 삭제 버튼 | `button-danger` (따로 만든다) | Button Danger | button `type=danger` |
| 아이콘만 있는 버튼 (▲▼, ←) | `icon-button` | Icon Button | reorder-button / reader-button |
| 체크박스 | `checkbox` | Checkbox (글자 포함은 Checkbox Field) | checkbox |
| 입력칸 | `input-field` | Input Field | input |
| 확인창 | `dialog` | Dialog | dialog |
| 버튼 묶음 (취소 + 삭제) | `button-group` | Button Group | – |
| 잠깐 뜨는 알림 | `notification` | Notification (“Toast notifications and alerts”) | toast |
| 칩 · 배지 | `tag` | Tag | – |
| 탭 하나 | `tab` | Tab | tabs/tab |
| 할 일 한 줄 | `list-item` | (Material 3 List item) | todo/row |
| 아이콘 | `icon/check` · `icon/arrow-up` · `icon/arrow-left` | Icon | icon/… |

- `/`는 Assets 폴더다 (Figma 도움말: 슬래시마다 한 단계). 2단계까지만 쓴다.

---

## 8. 컴포넌트 속성 — SDS 속성 이름을 따른다

| 속성 | 종류 | 값 | SDS 근거 | 지금 이름 |
|---|---|---|---|---|
| `variant` | Variant | `primary` · `neutral` · `subtle` | Button `Variant` = Primary · Neutral · Subtle | type = primary · secondary · tertiary |
| `state` | Variant | `default` · `hover` · `pressed` · `disabled` | Button `State` (SDS 코드에 hover · disabled 상태가 있음, pressed는 Material 3 상태) | state |
| `size` | Variant | `medium` · `small` | Button `Size` | – |
| `label` | Text | 버튼 글자 | Button `Label` | label |
| `has icon start` | Boolean | true · false | Button `Has Icon Start` | show icon |
| `icon start` | Instance swap | 아이콘 | Button `Icon Start` | icon |
| `value type` | Variant | `unchecked` · `checked` | Checkbox `Value Type` (SDS 값: Checked · Indeterminate 등) | state = unchecked · checked |
| `has description` | Boolean | true · false | Checkbox · Input `Has Description` | – |

- **버튼 variant 3개의 뜻 (SDS button.css 그대로):**

| variant | 배경 | 테두리 | 글자 |
|---|---|---|---|
| `primary` | background/brand/default | border/brand/default | text/brand/on-brand |
| `neutral` | background/default/secondary | border/default/default | text/default/default |
| `subtle` | 없음 | 없음 | text/brand/default |
| (모든 variant) `state=disabled` | background/disabled/default | border/disabled/default | text/disabled/default |

- ‘하루’의 베이지 버튼 = `neutral`, 글자만 있는 ‘되돌리기’ = `subtle`. 회색 버튼(secondary)은 흰 글자 대비가 부족하고 SDS에 없는 종류라 **없앤다.**
- Boolean은 `has ○○` 한 가지 방식만 쓴다 (Figma 도움말: Has Icon · Show Icon · Icon Visible 중 하나를 골라 통일).

---

## 9. 레이어 이름

Figma 도움말: 구조상 뜻이 있는 레이어는 `card-thumbnail`, `user-avatar`처럼 이름을 붙이고 `Rectangle 4`, `Frame 22`는 남기지 않는다.

| 어디 | 이름 | 근거 |
|---|---|---|
| 화면 칸 | `header` · `content` · `footer` (탭이면 `tab-bar`) | HTML 구조 이름, SDS Headers · Footers |
| 버튼 안 | `icon-start` · `label` · `icon-end` | SDS Button 속성 이름 |
| 입력칸 안 | `label` · `input` · `description` · `error` | SDS Input Field 속성 이름 |
| 할 일 한 줄 안 | `leading` · `content`(`headline` · `supporting-text`) · `trailing` | Material 3 List item 구조 |
| 확인창 안 | `heading` · `body` · `button-group` | SDS Dialog 속성 `Heading` · `Body`, SDS Button Group 컴포넌트 |
| 알림(notification) 안 | `icon` · `title` · `body` | SDS Notification 속성 `Icon` · `Title` · `Body` |
| 그 밖 | 무엇인지 + 하이픈: `add-bar` · `date-text` · `card-thumbnail` | Figma 도움말 예시 형식 |

- 한국어: 페이지 · 화면 Frame · Flow · Section 이름만 (내가 빨리 찾는 용도, 코드로 가지 않는다).

---

## 10. 지금 파일 → 새 이름 바꾸기 표

| 지금 | 새 이름 |
|---|---|
| action/primary-default · -hover · -pressed | background/brand/default · hover · pressed |
| action/tertiary-default · -hover | background/default/secondary · secondary-hover |
| action/secondary-* (회색) | 삭제 |
| action/disabled (빨강) | background/disabled/default → gray/200 |
| text/primary | text/default/default |
| text/on-primary | text/brand/on-brand |
| text/on-secondary · text/on-teriary | 삭제 (neutral 버튼 글자는 text/default/default) |
| text/accent | text/brand/default → **green/900** (대비 때문) |
| text/disabled | text/disabled/default |
| bg/screen · bg/surface · bg/inverse | background/default/tertiary · background/default/secondary · background/neutral/default |
| border/strong | border/default/default |
| shadow/strong | Effect 스타일 drop-shadow/100 |
| 컬렉션 Primitives(색만 있음) · Segmantic · Size | Color Primitives · Color · Size(그대로) |
| spacing/… · radius/sm… (Primitives) | Size 컬렉션 space/… · radius/… |

Figma에서 변수 이름을 바꾸면 **연결된 레이어는 그대로 따라온다** → 이름만 바꾸면 되고 다시 연결할 필요는 없다(삭제하는 변수만 다시 연결).

---

## 근거 자료
- Figma Simple Design System (Figma 공식): https://github.com/figma/sds — `scripts/tokens/tokens.json`, `scripts/tokens/styles.json`, `src/ui/primitives/Button/button.css`, `src/figma/primitives/*.figma.ts`
- Figma 도움말 · Components collection: Tips for component management: https://help.figma.com/hc/en-us/articles/39747637290263
- Figma 도움말 · Update 1: Tokens, variables, and styles: https://help.figma.com/hc/en-us/articles/18490793776023
- Figma Resource Library · Design tokens: https://www.figma.com/resource-library/design-tokens/
- Material Web · Theming (component tokens): https://material-web.dev/theming/material-theming
