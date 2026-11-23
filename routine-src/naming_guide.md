# Figma 이름 기준 — 확정판 (2026-11-23 고정 · 다시 바꾸지 않는다)

> 이 문서가 ‘하루’ 파일(하루v02)과 루틴 전체(앱 · 매일 밤 점검 포함)의 **유일한 이름 기준**이다. 앞선 문서(가이드 v2 · SDS판)와 다르면 이 문서를 따른다.
> **정한 방법: 특정 회사 하나가 아니라, 공개된 실무 디자인 시스템 8곳에서 가장 많이 쓰는 방식(다수결).**
> 8곳: Google Material 3 · Atlassian · GitHub Primer · Shopify Polaris · IBM Carbon · Figma SDS(Figma 공식 예제) · 당근 SEED(국내) · 정부 KRDS(국내).
> 국내 회사가 가장 많이 쓰는 방식을 보여 주는 통계는 없다. 이름 규칙을 전부 공개한 국내 기준은 SEED · KRDS 둘뿐이라 8곳에 함께 넣었다(토스 TDS는 일부만 공개).
>
> **고정 규칙**
> 1. 여러 방식이 있으면 8곳 중 **가장 많이 쓰는 방식**. 표마다 ‘근거’ 칸에 어느 곳이 그렇게 쓰는지 적었다.
> 2. 표가 갈리거나 8곳에 없으면 **Figma 도움말**, 그다음 **Material 3**.
> 3. 다른 강의 · 예제에서 다른 이름을 봐도 **이 문서를 바꾸지 않는다.** 고치는 경우는 둘뿐: 근거와 다르게 적은 것을 찾았을 때, 아직 없는 것을 새로 정할 때(이 문서 규칙으로 짓고 여기에 추가).
> 4. 표기: **영어 소문자 + 하이픈(-)**, 묶음은 **/**. 컬렉션 이름만 첫 글자 대문자. 한국어는 페이지 · 화면 Frame(‘화면-상태’) · Section · Flow만.
> 5. 이름을 적는 모든 곳(이 문서 · 루틴 블록)에는 값과 쓰는 곳을 함께 적는다.

---

## 1. 변수 컬렉션 — `Primitives` · `Semantic` · `Size`

| 컬렉션 | 하는 일 | 부품에 직접 연결? | 근거 |
|---|---|---|---|
| `Primitives` | 색 실제 값 | ✗ (Scoping 끄기) | 층 이름 primitive · semantic: KRDS 컬렉션 이름 · Figma 도움말 · 대부분의 토큰 글 |
| `Semantic` | 색 쓰임 (Primitives를 가리킴) | ✓ | 같음 |
| `Size` | 간격 · 모서리 · 테두리 굵기 · 아이콘 크기 (한 층, 값을 바로 넣음) | ✓ | 간격 값을 바로 쓰는 곳: Atlassian · Polaris · SDS · SEED |
| (Component 층) | 만들지 않는다. 부품 전용 값은 개발 코드에서 | – | Figma 도움말: 큰 시스템용 |

---

## 2. Primitives — `색상/단계`

- 단계: **100 단위, 숫자가 클수록 진함** (50도 써도 됨). 근거: SDS · SEED · Atlassian · Tailwind · 토스(grey50~900).
- 색상 이름: `gray` · `green` · `brown` · `red` …. 회색은 `gray`(SDS · SEED · KRDS · Tailwind).
- 흰색 · 검정은 단계 없이 `white` · `black` (Primer · Tailwind · SEED static-white).
- 컬렉션이 색만 담으므로 `color/` 묶음은 쓰지 않는다.

하루v02 실제 색 (11/23 사용자 화면 기준, 밝기로 단계를 정함):

| 지금 이름 | 값 | 새 이름 |
|---|---|---|
| color/green/50 · 100 · 200 | D2E077 · A4C263 · 6DC458 | `green/300` · `green/400` · `green/500` |
| color/brown/50 · 100 · 300 | F3E5C2 · E8CFA6 · C49A6C | `brown/200` · `brown/300` · `brown/400` |
| color/brown/400 · 600 · 700 · 800 | AA7959 · 8C7369 · 7B6762 · 645552 | `brown/500` · `brown/600` · `brown/700` · `brown/800` |
| color/netral/0 | FFFFFF | `white` |
| color/netral/200 · 500 | C1C8B9 · 6B7470 | `gray/300` · `gray/500` |
| color/red/300 | CF4843 | `red/500` |

---

## 3. Semantic — `속성/역할/변형` (늘 3단)

| 자리 | 값 | 근거 (가장 많이 쓰는 말) |
|---|---|---|
| 속성 (어디에 칠하나) | `background` · `text` · `icon` · `border` | Atlassian · SDS · Polaris · Carbon · KRDS (SEED만 bg/fg/stroke) |
| 역할 (무슨 뜻인가) | `default` 기본 · `surface` 카드처럼 올라온 면 · `inverse` 어두운 반전 면 · `brand` 주인공 색 · `neutral` 회색 · `danger` 위험 · `success` 완료 · `warning` 주의 · `information` 안내 · `disabled` 못 누름 · `on-brand` · `on-danger` · `on-inverse` (그 색 바탕 위) | brand: Atlassian · SDS · Polaris · SEED / danger: Atlassian · Primer · SDS · Carbon · KRDS / success: Atlassian · Primer · Polaris · Carbon · KRDS / surface: Atlassian · Polaris · Material · KRDS / inverse: Atlassian · Polaris · Material · KRDS / on-: Material · SDS · SEED · KRDS |
| 변형 (그 안에서 무엇이 다른가) | `default` · `subtle`(옅게) · `strong`(진하게) · `raised`(더 떠 있는 면) · `hover` · `pressed` | subtle: Atlassian · KRDS · SEED / hover · pressed: Material · Atlassian · SEED · KRDS |

### ‘하루’ Semantic 변수 (이 표의 이름이 기준)

| 이름 | 가리킬 Primitives | 쓰는 곳 |
|---|---|---|
| `background/default/default` | brown/400 | 화면 전체 바탕 |
| `background/surface/default` | brown/200 | 카드 · 배너 · tertiary 버튼 |
| `background/surface/hover` | brown/300 | tertiary 버튼 마우스 올림 |
| `background/surface/raised` | white 또는 가장 밝은 갈색 | 입력칸 · 확인창 · 체크박스 안 |
| `background/inverse/default` | brown/800 | tab-bar 같은 어두운 바탕 |
| `background/brand/default` · `hover` · `pressed` | green/500 · green/400 · green 더 진한 단계 | primary 버튼, 체크됨, 고른 탭 |
| `background/neutral/default` · `hover` · `pressed` | gray/500 계열 | secondary 버튼(회색) |
| `background/danger/default` | red/500 | 삭제 버튼 |
| `background/disabled/default` | gray/300 | 못 누르는 버튼 |
| `text/default/default` | brown/800 | 일반 글자 |
| `text/default/subtle` | gray/500 | 보조 글자 (09:00 · 개수) |
| `text/brand/default` | green 진한 단계 | 초록 강조 글자 |
| `text/danger/default` | red/500 | 오류 문구 |
| `text/disabled/default` | gray/300 | 못 누르는 글자 |
| `text/on-brand/default` | white | 초록 버튼 위 글자 |
| `text/on-danger/default` | white | 삭제 버튼 글자 |
| `text/on-inverse/default` | brown/200 | 어두운 바탕 위 글자 |
| `icon/default/default` · `icon/on-brand/default` · `icon/disabled/default` | text와 같은 값 | 아이콘 (글자와 따로 칠한다) |
| `border/default/default` | brown/800 | 카드 · 버튼 · 입력칸 테두리 |
| `border/brand/default` | green/500 | 빈 체크박스 · 초록 칩 테두리 |
| `border/danger/default` | red/500 | 오류 난 입력칸 · 틀린 예 테두리 |
| `border/disabled/default` | gray/300 | 못 누르는 버튼 테두리 |

- 값 칸은 예다. **하루v02에서는 이미 연결된 값을 그대로 두고 이름만 바꾼다.** 새로 만드는 변수만 위 표의 가까운 단계를 고르고 대비 플러그인으로 다시 잰다.
- 색 바탕 위 글자 · 아이콘은 `on-역할`: 초록 위 `text/on-brand/default`, 빨강 위 `text/on-danger/default`.
- 그림자 색은 변수로 만들지 않는다 → Effect 스타일 `shadow/100` (6장).

---

## 4. Size — `종류/단계` (100 = 4px)

간격은 8px 기준(Material · Android 8dp 격자), 작은 곳만 4px. 이름 숫자 = **값 ÷ 4 × 100** (4px 단위: Polaris · SDS · SEED · Tailwind. Atlassian만 8px 단위).

| 이름 | 값 | 쓰는 곳 | Scoping |
|---|---|---|---|
| `space/100` | 4 | 아이콘 ↔ 숫자 | Gap · Padding |
| `space/200` | 8 | 버튼 안 아이콘 ↔ 글자, 버튼 ↔ 버튼 | Gap · Padding |
| `space/300` | 12 | 버튼 안쪽 여백, 할 일 행 ↔ 행 | Gap · Padding |
| `space/400` | 16 | 카드 · toast 안쪽, 화면 양옆 | Gap · Padding |
| `space/600` | 24 | 카드 ↔ 카드 | Gap · Padding |
| `space/800` | 32 | 큰 덩어리 사이 | Gap · Padding |
| `space/1200` | 48 | 버튼 높이 (누르는 영역) | Width · Height |
| `radius/100` | 4 | 체크박스 | Corner radius |
| `radius/200` | 8 | 버튼 · 입력칸 · 카드 · toast | Corner radius |
| `radius/400` | 16 | 확인창 | Corner radius |
| `radius/full` | 9999 | 알약 배지 | Corner radius |
| `border-width/default` | 2 | 모든 테두리 굵기 | Stroke |
| `border-width/focus` | 2 | 키보드 포커스 테두리 | Stroke |
| `icon-size/medium` | 24 | 아이콘 | Width · Height |

- border-width: Atlassian `border.width` · Polaris `border-width` · KRDS `border-width` (SDS만 stroke).

---

## 5. 스타일

### 글자 스타일 — `역할/크기` (굵기가 다르면 끝에 `-bold`)
근거: Material(display · headline · title · body · label + large · medium · small) · Atlassian(heading · body) · Polaris(heading · body) · KRDS(heading · body + large · medium · small). 역할 `heading` · `body` · `label`, 크기 `large` · `medium` · `small`.

| 이름 | 크기 / 줄 높이 | 굵기 | 쓰는 곳 |
|---|---|---|---|
| `heading/large` | 24 / 32 | Bold | 메인 화면 맨 위 큰 제목 (‘오늘’) |
| `heading/medium` | 20 / 28 | Bold | 상세 · 수정 header 제목, 확인창 질문, 규칙 카드 제목 |
| `body/medium` | 16 / 24 | Regular | 본문, 할 일 제목, 입력칸 글자, 확인창 설명 |
| `body/medium-bold` | 16 / 24 | Bold | 본문 안 강조 (필요할 때만) |
| `body/small` | 14 / 20 | Regular | 보조 글자 (09:00 · 날짜 · 개수 · 안내 · 오류 문구) |
| `label/medium` | 16 / 16 | Bold | 버튼 · 탭 글자 (한 줄만 쓰는 곳) |

- 지금 이름 → 새 이름: `subheading` → `heading/medium`, `body/regular` · `body/base` → `body/medium`, `body/strong` → `body/medium-bold`, `caption` → `body/small`, `button` → `label/medium`. 글꼴에 Bold가 없으면 Regular로 두고 이름은 그대로.

### Effect 스타일 — `shadow/단계`
| 이름 | 쓰는 곳 | 근거 |
|---|---|---|
| `shadow/100` | 버튼 · 카드 그림자 (X 0, Y 2, Blur 0, 색 brown/800) | Polaris shadow-100 · SDS drop-shadow/100 · SEED shadow s1 |
| `shadow/200` | 확인창처럼 더 떠 있는 것 (필요할 때) | 같음 |

---

## 6. 컴포넌트 이름 — 무엇인지로 (생김새 말고)

| ‘하루’ 부품 | 이름 | 근거 (가장 많이 쓰는 이름) | 지금 이름 |
|---|---|---|---|
| 버튼 (삭제 버튼 포함) | `button` | 8곳 모두 | button |
| 아이콘만 있는 버튼 | `icon-button` | Material · Atlassian · Primer · SDS | – |
| 체크박스 | `checkbox` | 8곳 모두 | checkbox |
| 입력칸 | `text-field` | Material · Atlassian · Polaris (SDS input-field · SEED text-input) | input · field |
| 확인창 | `dialog` | Material · Primer · SDS · SEED(alert-dialog) | dialog |
| 버튼 묶음 | `button-group` | Atlassian · Polaris · SDS | actions |
| 잠깐 뜨는 알림 | `toast` | Polaris · Carbon · Primer (Material · SEED snackbar) | toast |
| 할 일 한 줄 | `list-item` | Material · SEED | todo/row |
| 탭 하나 | `tab` | 8곳 대부분 | – |
| 아이콘 | `icon/check` · `icon/arrow-left` | 공통 | – |
| 개발 전달 번호 주석 (11/25 추가) | `annotation` | Figma 도움말 Annotations(번호 · 설명으로 개발 정보를 남기는 기능, 무료 플랜에 없어 부품으로 만든다) | – |

- `/`는 Assets 폴더다. 2단계까지만.

---

## 7. 컴포넌트 속성

| 속성 | 종류 | 값 | 근거 | 지금 이름 |
|---|---|---|---|---|
| `variant` | Variant | `primary` · `secondary` · `tertiary` · `danger` | 속성 이름 variant: Polaris · Primer · SDS · SEED / 값 primary·secondary·tertiary: Polaris · Carbon · KRDS / danger를 같은 속성 값으로: Carbon · Atlassian · Primer | Type = Primary · Secondary · Tertiary · danger |
| `state` | Variant | `default` · `hover` · `pressed` · `disabled` | Material · Atlassian · SEED · KRDS | State |
| `size` | Variant | `small` · `medium` · `large` | 8곳 모두 | – |
| `label` | Text | 버튼 글자 | Material · SDS · SEED | Label |
| `show icon` | Boolean | true · false | Figma 도움말 예시 방식(Show ○○), 11/19부터 쓰던 이름 | show icon |
| `icon` | Instance swap | 아이콘 | 공통 | icon |
| `checked` | Variant | `true` · `false` | HTML · Primer · Polaris · Atlassian(isChecked) | – |
| `shape` | Variant | 파일에 있는 값 그대로 소문자 | 파일에만 있는 속성 | Shape |
| `variant` (annotation) | Variant | `action` · `condition` · `error` · `accessibility` | 같은 부품 종류를 variant 값으로 나누는 방식(위 variant 줄과 같음). 값은 주석 내용 종류: 동작 · 조건 · 오류 · 접근성 (11/25 추가) | – |
| `number` · `description` (annotation) | Text | 주석 번호 · 설명 문장 | 7장 label처럼 속성 이름 = 안쪽 글자 레이어 이름 (11/25 추가) | – |
| `show description` (annotation) | Boolean | true · false (false면 번호 동그라미만 → 화면 위 표시) | show icon과 같은 ‘show ○○’ 방식 (11/25 추가) | – |

| variant | 배경 | 테두리 | 글자 |
|---|---|---|---|
| `primary` | background/brand/default | border/default/default | text/on-brand/default |
| `secondary` | background/neutral/default | border/default/default | text/on-brand/default (흰 글자 대비가 모자라면 text/default/default) |
| `tertiary` | background/surface/default | border/default/default | text/default/default |
| `danger` | background/danger/default | border/default/default | text/on-danger/default |
| (모든 variant) `state=disabled` | background/disabled/default | border/disabled/default | text/disabled/default |

---

## 8. 레이어 이름

| 어디 | 이름 | 근거 |
|---|---|---|
| 화면 칸 | `header` · `content` · `footer` (탭이면 `tab-bar`) | HTML 구조 이름 |
| 버튼 안 | `icon` · `label` | 7장 속성 이름과 같게 |
| 입력칸 안 | `label` · `input` · `helper-text` · `error-text` | Material supporting text · Polaris helpText |
| 할 일 한 줄 안 | `leading` · `content`(`title` · `description`) · `trailing` | Material List item |
| 목록 안 여러 줄 | `item-1` · `item-2` · `item-3` (Smart animate는 같은 이름끼리 움직인다) | 그 밖 규칙 |
| 확인창 안 | `title`(질문 문장) · `description`(설명 문장) · `button-group` | SEED alert-dialog · Atlassian modal · Material |
| toast 안 | `message` · 버튼 | SEED snackbar message |
| annotation 안 · 명세 (11/25 추가) | `badge`(번호 동그라미) 안 `number` 글자 · `description` 글자 / 주석 묶음 `notes` / 명세 Frame `명세-할 일 추가` | 7장 속성 이름과 같게 · 화면 Frame 한국어 ‘화면-상태’ |
| 문서 카드 | `button-guide` · `rule-table` · `rule-row` · `examples` · `do` · `dont` · `changelog` | 그 밖 규칙 |
| 그 밖 | 무엇인지 + 하이픈: `add-bar` · `date-text` · `settings-list` | Figma 도움말 예시 형식 |

---

## 9. 하루v02 지금 이름 → 확정 이름 (11/23 08:20 0단계에서 바꾼다)

| 어디 | 지금 | 확정 이름 |
|---|---|---|
| 변수 창 · 컬렉션 | Primitives · Segmantic · Size | Primitives · **Semantic** · Size |
| Primitives | color/green/50 … color/red/300 | 2장 표 (green/300 … red/500, white) |
| Size | spacing/1 · 2 · 4 …, radius/md, border/width | space/(값÷4×100), radius/200, border-width/default |
| Semantic | bg/screen/screen · bg/screen/surface · bg/screen/inverse | background/default/default · background/surface/default · background/inverse/default |
| Semantic | border/strong · status/error | border/default/default · border/danger/default |
| Semantic | (새로) | background/danger/default → red/500 (삭제 버튼) |
| 글자 스타일 | subheading · body/regular · body/base · caption · button | heading/medium · body/medium · body/medium · body/small · label/medium |
| button 속성 | Type=Primary · Secondary · Tertiary · danger / State=Default … / Shape / Label | variant=primary · secondary · tertiary · danger / state=default … / shape / label |
| 레이어 | actions · field · 행-1~3 · dialog 질문 · 설명 글자 | button-group · text-field · item-1~3 · title · description |
| 그대로 | toast · dialog · button · heading/large · heading/medium | – |
| 나중에 (11/28) | Semantic 안 padding/ · gap/ · radius/control 숫자, 다른 파일 변수 text/primary · action/… · shadow/strong, todo/row | Size 변수로 다시 연결 후 삭제 / Semantic 변수 · shadow/100으로 다시 연결 / list-item(원본 파일에서) |

Figma에서 변수 · 스타일 · 레이어 · 속성 이름을 바꾸면 **연결된 곳은 그대로 따라온다.** 새로 만든 변수만 다시 연결한다. 변수를 다른 컬렉션으로 옮기는 기능은 없다(복사만 됨).

---

## 근거 자료
- Figma Simple Design System: https://github.com/figma/sds
- 당근 SEED: https://github.com/daangn/seed-design (packages/rootage — color · dimension · radius · components)
- 정부 KRDS: https://github.com/KRDS-uiux/krds-uiux (tokens/figma_token.json) · https://www.krds.go.kr
- Atlassian Design: https://atlassian.design/foundations/color · https://atlassian.design/foundations/spacing · https://atlassian.design/foundations/elevation
- Shopify Polaris: https://polaris.shopify.com/components/actions/button · https://polaris-react.shopify.com/tokens/space
- IBM Carbon: https://carbondesignsystem.com/components/button/usage
- Material Design: https://m2.material.io/design/layout · https://m3.material.io
- GitHub Primer: https://primer.style/foundations/primitives/token-names
