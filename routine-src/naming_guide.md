# Figma 이름 짓기 가이드 v2 — 근거 기준판 (2026-11-23 개정)

> 이 문서가 ‘하루’ 파일(하루v02)과 루틴의 **유일한 이름 기준**이다. 앞선 대화·문서의 이름 규칙과 다르면 이 문서를 따른다.
> 기준 순서: ① **Figma 공식 예제 디자인 시스템 SDS**(Simple Design System, Figma가 직접 공개한 파일과 코드) → ② **Figma 공식 도움말** → ③ **Material 3**(Google, 컴포넌트 토큰과 부품 구조 이름).
> SDS 값은 공개 저장소 `figma/sds`의 `tokens.json`, `styles.json`, Button Code Connect 파일을 직접 열어 확인했다(11/23 다시 확인). ‘속성/역할/변형’ 순서는 Atlassian(`color.background.danger.bold.hovered`) · GitHub Primer(`bgColor-danger-emphasis`)도 같은 방식이다.

---

## 0. 큰 규칙 4개

| 규칙 | 내용 | 근거 |
|---|---|---|
| 1. 색은 2층 | `Color Primitives`(실제 값) → `Color`(쓰임) | SDS 컬렉션 구조 |
| 2. 숫자는 1층 | `Size` 컬렉션 하나. 값을 바로 넣고 부품에 바로 연결 | SDS `Size` 컬렉션 |
| 3. Component 층은 Figma에 만들지 않는다 | 부품 전용 값은 개발 코드에서 만든다. 필요해지면 정해진 이름 순서로 만든다 (5장) | Figma 도움말: 컴포넌트 토큰은 큰 엔터프라이즈 시스템용 / SDS는 코드에만 둠 |
| 4. 대소문자는 한 가지로 | ‘하루’는 **영어 소문자 + 하이픈**. 컬렉션 이름만 Title Case | Figma 도움말: 하나를 정해 지키라고만 함. SDS는 Figma 안에서 Title Case, 코드에서 소문자-하이픈. ‘하루’는 코드 이름과 바로 같도록 소문자 |

---

## 1. 변수 컬렉션

| 컬렉션 (Title Case) | 하는 일 | 부품에 직접 연결? | SDS 이름 |
|---|---|---|---|
| `Color Primitives` | 색 실제 값 | ✗ (Scoping 끄기) | Color Primitives |
| `Color` | 색 쓰임 (Primitives를 가리킴) | ✓ | Color |
| `Size` | 간격 · 모서리 · 테두리 · 아이콘 크기 | ✓ | Size |

> Figma에는 변수를 다른 컬렉션으로 **옮기는** 기능이 없다(복사만 됨, 복사하면 다시 연결해야 함). 그래서 하루v02는 간격·모서리가 든 `Primitives`를 `Size`로 이름만 바꾸고, `Color Primitives`를 새로 만들어 색만 다시 만든다.

---

## 2. Color Primitives — `색상/단계` (100 ~ 1000, 클수록 진함)

**SDS 규칙:** 색상 이름(`gray`, `green` …) + 100 단위 단계. 흰색·검정도 `white/1000`, `black/1000`처럼 단계로 쓴다(낮은 숫자는 투명도).

| 이름 | 값 |
|---|---|
| `white/1000` | FFFFFF |
| `gray/100` | F1F1F1 |
| `gray/200` | DEDEDE |
| `gray/400` | B8B8B8 |
| `gray/500` | 7D7D7D |
| `gray/600` | 424242 |
| `gray/800` | 282828 |
| `brown/100` | FFF9ED |
| `brown/200` | F7EBD3 |
| `brown/300` | E9C989 |
| `brown/400` | D9BE92 |
| `brown/900` | 3A2A22 |
| `green/500` | 5EB44A |
| `green/700` | 3F7A31 |
| `green/900` | 27471F |
| `red/600` | D00000 |

- 단계는 **밝기 순서**. 중간 숫자는 비워 둔다 → 나중에 사이 색을 넣을 자리.
- 내 파일에 이 표에 없는 hex가 있으면 같은 색상 이름에 밝기 순서로 단계를 붙인다.

---

## 3. Color — `속성/역할/변형`

**SDS 실제 이름 예:** `background/brand/default`, `text/brand/on-brand`, `border/danger/default`

| 자리 | 고르는 값 |
|---|---|
| 속성 (어디에 칠하나) | `background` · `text` · `icon` · `border` |
| 역할 (무슨 뜻인가) | `default`(기본 화면) · `brand`(주인공 색) · `neutral`(어두운 반전 영역) · `positive` · `warning` · `danger` · `disabled` · `utilities` |
| 변형 (그 안에서 무엇이 다른가) | `default` · `secondary` · `tertiary` · `hover` · `on-brand`(그 색 위의 글자) · `on-neutral` · `on-danger` |

### ‘하루’에 만들 Color 변수

| 이름 | → Color Primitives | 쓰는 곳 |
|---|---|---|
| `background/default/default` | brown/100 | 입력칸, 확인창, 체크박스 안 |
| `background/default/secondary` | brown/200 | 카드 · 배너 · 탭 묶음, neutral 버튼 |
| `background/default/secondary-hover` | brown/100 | neutral 버튼 마우스 올림 |
| `background/default/tertiary` | brown/400 | 화면 전체 바탕 |
| `background/brand/default` | green/700 | primary 버튼, 체크됨, 고른 탭 |
| `background/brand/hover` | green/500 | primary 버튼 마우스 올림 |
| `background/brand/pressed` | green/900 | primary 버튼 누름 (SDS에 없는 상태라 같은 규칙으로 추가) |
| `background/neutral/default` | brown/900 | tab-bar 바탕 |
| `background/danger/default` | red/600 | 삭제 버튼 |
| `background/disabled/default` | gray/200 | 못 누르는 버튼 |
| `text/default/default` | brown/900 | 일반 글자 (크림 위 11.6 ✅) |
| `text/default/secondary` | gray/600 | 보조 글자 (약 8.5 ✅) |
| `text/brand/default` | green/900 | 초록 강조 글자, subtle 버튼 글자 (약 8.9 ✅) |
| `text/brand/on-brand` | white/1000 | 초록 버튼 위 글자 (5.2 ✅) |
| `text/neutral/on-neutral` | brown/200 | tab-bar 위 글자 |
| `text/danger/default` | red/600 | 오류 문구 (약 4.8 ✅) |
| `text/danger/on-danger` | white/1000 | 삭제 버튼 글자 |
| `text/disabled/default` | gray/400 | 못 누르는 글자 (대비 기준 예외) |
| `icon/default/default` | brown/900 | ▲▼ · ← 아이콘 |
| `icon/brand/on-brand` | white/1000 | 체크 표시 ✓ |
| `icon/neutral/on-neutral` | brown/200 | tab-bar 아이콘 |
| `icon/disabled/default` | gray/400 | 못 누르는 아이콘 |
| `border/default/default` | brown/900 | 카드 · 버튼 · 입력칸 테두리 |
| `border/brand/default` | green/700 | 빈 체크박스 테두리, 초록 칩 테두리 |
| `border/danger/default` | red/600 | 오류 난 입력칸, 틀린 예 테두리 |
| `border/disabled/default` | gray/400 | 못 누르는 버튼 테두리 |

- **글자색 짝 규칙:** 색 바탕 위 글자는 `on-역할` → 초록 위 = `text/brand/on-brand`, 빨강 위 = `text/danger/on-danger`.
- **아이콘은 `icon/`으로 따로** 칠한다.
- **그림자 색은 변수로 만들지 않는다.** Effect 스타일(`drop-shadow/100`)로 둔다 → 6장.
- **hover 방향:** SDS는 한 단계 진하게(brand/800 → 900). ‘하루’는 지금 디자인대로 밝게 두되, 바꾸려면 `background/brand/hover`의 연결만 바꾼다.

---

## 4. Size — `종류/단계` (100 = 4px)

SDS 실제 값 그대로, 쓰는 것만 만든다. **이름의 숫자 = 값 ÷ 4 × 100** (표에 없는 값도 이 규칙).

| 이름 | 값 | 쓰는 곳 | Scoping |
|---|---|---|---|
| `space/100` | 4 | 아이콘 ↔ 숫자 | Gap · Padding |
| `space/200` | 8 | 버튼 안 아이콘 ↔ 글자, 버튼 ↔ 버튼 | Gap · Padding |
| `space/300` | 12 | 버튼 안쪽 여백, 할 일 행 ↔ 행 | Gap · Padding |
| `space/400` | 16 | 카드 · 알림 안쪽, 화면 양옆 | Gap · Padding |
| `space/600` | 24 | 카드 ↔ 카드 | Gap · Padding |
| `space/800` | 32 | 큰 덩어리 사이 | Gap · Padding |
| `space/1200` | 48 | 버튼 높이 (누르는 영역) | Width · Height |
| `radius/100` | 4 | 체크박스 | Corner radius |
| `radius/200` | 8 | 버튼 · 입력칸 · 카드 · 알림 | Corner radius |
| `radius/400` | 16 | 확인창 | Corner radius |
| `radius/full` | 9999 | 알약 배지 | Corner radius |
| `stroke/border` | 2 | 테두리 굵기 (SDS는 1, ‘하루’ 디자인은 2) | Stroke |
| `stroke/focus-ring` | 2 | 키보드 포커스 테두리 | Stroke |
| `icon/small` | 24 | 아이콘 | Width · Height |

---

## 5. Component 층 — 지금은 만들지 않는다. 만들 때의 이름

- SDS는 부품 전용 값을 코드에서만 만든다: `--button-background-color`, `--button-padding-x`.
- Material 3 이름 순서: **부품 → 상태 → 부분 → 속성** (예: `md.comp.filled-button.hover.label-text.color`).
- ‘하루’에서 필요해지면 `toggle/selected/track/color` 처럼 `부품/상태/부분/속성`으로 짓고, 값은 Color 변수를 가리킨다.

---

## 6. 스타일

### 텍스트 스타일 — SDS 이름 순서 (소문자 · / 로 묶음)
| 이름 | 크기 / 줄 높이 | 굵기 | SDS 이름 | 쓰는 곳 |
|---|---|---|---|---|
| `heading` | 24 / 32 | regular | Heading | 화면 큰 제목 |
| `subheading` | 20 / 28 | regular | Subheading | 카드 제목, 화면 header 제목 |
| `body/base` | 16 / 24 | regular | Body Base | 본문, 할 일 제목 |
| `body/strong` | 16 / 24 | bold | Body Strong | 강조 본문 |
| `body/small` | 14 / 20 | regular | Body Small | 보조 글자 (09:00) |
| `single-line/body-base` | 16 / 16 | regular | Single Line/Body Base | 버튼 · 탭 글자 |

- 지금 이름 → 새 이름: `heading/large` → `heading`, `heading/medium` → `subheading`, `body/regular` → `body/base`, `caption` → `body/small`, `button` → `single-line/body-base`.

### Effect 스타일
| 이름 | 쓰는 곳 |
|---|---|
| `drop-shadow/100` | 버튼 · 카드 그림자 (X 0, Y 2, Blur 0, 색 brown/900) |
| `drop-shadow/200` | 확인창처럼 더 떠 있는 것 |

---

## 7. 컴포넌트 이름 — SDS 컴포넌트 이름을 따른다

Figma 도움말: 생김새가 아니라 무엇인지로 짓고, 개발 용어와 맞춘다 (`Button` ↔ `<Button>`).

| ‘하루’ 부품 | 컴포넌트 이름 | SDS 이름 | 지금 이름 |
|---|---|---|---|
| 버튼 | `button` | Button | button |
| 삭제 버튼 | `button-danger` (따로 만든다) | Button Danger | button `Type=danger` |
| 아이콘만 있는 버튼 (▲▼, ←) | `icon-button` | Icon Button | reorder-button / reader-button |
| 체크박스 | `checkbox` | Checkbox | checkbox |
| 입력칸 | `input-field` | Input Field | input · field |
| 확인창 | `dialog` | Dialog | dialog |
| 버튼 묶음 (취소 + 삭제) | `button-group` | Button Group | actions |
| 잠깐 뜨는 알림 | `notification` | Notification | toast |
| 칩 · 배지 | `tag` | Tag | – |
| 탭 하나 | `tab` | Tab | tabs/tab |
| 할 일 한 줄 | `list-item` | (Material 3 List item) | todo/row |
| 아이콘 | `icon/check` · `icon/arrow-up` · `icon/arrow-left` | Icon | icon/… |

- `/`는 Assets 폴더다. 2단계까지만 쓴다.

---

## 8. 컴포넌트 속성 — SDS 속성 이름을 따른다

| 속성 | 종류 | 값 | SDS 근거 | 지금 이름 |
|---|---|---|---|---|
| `variant` | Variant | `primary` · `neutral` · `subtle` | Button `Variant` = Primary · Neutral · Subtle | Type = Primary · Secondary · Tertiary |
| `state` | Variant | `default` · `hover` · `pressed` · `disabled` | Button `State` (pressed는 Material 3 상태) | State |
| `size` | Variant | `medium` · `small` | Button `Size` | – |
| `label` | Text | 버튼 글자 | Button `Label` | Label |
| `has icon start` | Boolean | true · false | Button `Has Icon Start` | show icon |
| `icon start` | Instance swap | 아이콘 | Button `Icon Start` | icon |
| `value type` | Variant | `unchecked` · `checked` | Checkbox `Value Type` | state = unchecked · checked |
| `has description` | Boolean | true · false | Checkbox · Input `Has Description` | – |

| variant | 배경 | 테두리 | 글자 |
|---|---|---|---|
| `primary` | background/brand/default | border/brand/default | text/brand/on-brand |
| `neutral` | background/default/secondary | border/default/default | text/default/default |
| `subtle` | 없음 | 없음 | text/brand/default |
| (모든 variant) `state=disabled` | background/disabled/default | border/disabled/default | text/disabled/default |

- 베이지 버튼 = `neutral`, 글자만 있는 ‘되돌리기’ = `subtle`. 회색 버튼은 SDS에 없는 종류라 없애고 `neutral`로 바꾼다.
- Boolean은 `has ○○` 한 가지 방식만 쓴다.

---

## 9. 레이어 이름

Figma 도움말: 구조상 뜻이 있는 레이어는 `card-thumbnail`처럼 이름을 붙이고 `Rectangle 4`, `Frame 22`는 남기지 않는다.

| 어디 | 이름 | 근거 |
|---|---|---|
| 화면 칸 | `header` · `content` · `footer` (탭이면 `tab-bar`) | HTML 구조 이름 |
| 버튼 안 | `icon-start` · `label` · `icon-end` | SDS Button 속성 |
| 입력칸 안 | `label` · `input` · `description` · `error` | SDS Input Field 속성 |
| 할 일 한 줄 안 | `leading` · `content`(`headline` · `supporting-text`) · `trailing` | Material 3 List item |
| 목록 안 여러 줄 | `item-1` · `item-2` · `item-3` (Smart animate는 같은 이름끼리 움직인다) | 그 밖 규칙 |
| 확인창 안 | `heading` · `body` · `button-group` | SDS Dialog · Button Group |
| 알림(notification) 안 | `icon` · `title` · `body` | SDS Notification |
| 문서 카드 | `button-guide` · `rule-table` · `rule-row` · `examples` · `do` · `dont` · `changelog` | 그 밖 규칙 (SDS 문서의 Do / Don’t) |
| 그 밖 | 무엇인지 + 하이픈: `add-bar` · `date-text` · `settings-list` | Figma 도움말 예시 형식 |

- 한국어: 페이지 · 화면 Frame(‘화면-상태’) · Flow · Section 이름만 (코드로 가지 않는다).

---

## 10. 하루v02 지금 이름 → 새 이름 (11/23 08:20 ⓐ~ⓕ에서 바꾼다)

| 지금 | 새 이름 |
|---|---|
| 컬렉션 Primitives | Size (간격 · 모서리만 남긴다. 색은 Color Primitives를 새로 만든다) |
| 컬렉션 Semantic (Segmantic) | Color |
| spacing/… · radius/… · border/width | space/(값÷4×100) · radius/100 · 200 · 400 · full · stroke/border |
| bg/screen/screen · bg/screen/surface · bg/screen/inverse | background/default/tertiary · background/default/secondary · background/neutral/default |
| border/strong | border/default/default |
| status/error | border/danger/default (+ background/danger/default 새로) |
| padding/… · gap/… · radius/control (Color 안 숫자) | 지운다 → Size 변수로 다시 연결 (11/28) |
| text/primary · action/… · text/on-… · shadow/strong (다른 파일 변수) | Color 변수 · drop-shadow/100으로 다시 연결 (11/28) |
| 글자 스타일 heading/medium · body/regular | subheading · body/base |
| button 속성 Type=Primary · Secondary · Tertiary · danger | variant=primary · (지움→neutral) · neutral · danger(→ button-danger 분리 11/28) |
| button 속성 State=Default · Hover · Pressed · Disabled | state=default · hover · pressed · disabled |
| toast · actions · field · 행-1~3 | notification · button-group · input-field · item-1~3 |
| todo/row (다른 파일 부품) | list-item — 이 파일에서 못 바꾼다(원본 파일에서) |

Figma에서 변수 · 스타일 · 레이어 이름을 바꾸면 **연결된 레이어는 그대로 따라온다** → 이름만 바꾸면 된다. 다른 컬렉션에 새로 만든 변수만 다시 연결한다.

---

## 근거 자료
- Figma Simple Design System: https://github.com/figma/sds — `scripts/tokens/tokens.json`, `scripts/tokens/styles.json`, `src/figma/primitives/button/Button.figma.ts`
- Atlassian Design · Color: https://atlassian.design/foundations/color
- Primer · Token names: https://primer.style/foundations/primitives/token-names
- Figma 도움말 · Update 1: Tokens, variables, and styles: https://help.figma.com/hc/en-us/articles/18490793776023
- Material Web · Theming: https://material-web.dev/theming/material-theming
