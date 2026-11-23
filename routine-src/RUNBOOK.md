# 매일 밤 다음 날 블록 점검 — 작업 순서

목적: 내일 할 블록을 사용자가 읽자마자 막힘없이 하고, 그 결과가 포트폴리오와 취업에 바로 쓰이게 만든다.

## 1. 준비
```
cd routine-src
python3 -c "import pypdf, reportlab" || pip install --break-system-packages pypdf reportlab
python3 validate.py          # 블록 데이터 생성(오류 없으면 total work minutes 출력)
```
- 블록 내용 원본: `w02_04.py` · `w05_12.py` · `w13_18.py` · `w19_24.py`(기본) → `clarify.py`(표 · Figma 기능 · 이름) → `aiplan.py`(화·목 AI) → `detail.py` · `detail2.py`(하는 법 · 순서표 · `OVERRIDE` = 블록 전체 교체) → `forms.py`(할 일 속 기입표를 앱 기입표로) → `forms2.py`(블록별 전용 기입표)
- 블록 하나를 다시 쓸 때는 `detail2.OVERRIDE[('MM-DD','HH:MM')]`에 할 일 전체를 넣는 것이 가장 확실하다.

## 2. 점검 기준 (블록마다 전부)
| # | 기준 | 확인 |
|---|---|---|
| 1 | 취업에 맞나 | 이 블록 결과가 포트폴리오 사례 · 면접 답 · 채용 공고 요구(토스 · 토스뱅크 · 당근 · LINE 등, 2026 AI 활용 · 코드 프로토타입 · 데이터 근거)에 실제로 쓰이나 |
| 2 | 실무에서 쓰는 방식인가 | 현업 디자이너가 실제로 이렇게 하나. 결과물 형식이 실무 문서 형식(명세 · 테스트 계획 · 결과표 등)과 같은가 |
| 3 | 자료가 사실인가 | 강의가 따라 하는 실습인지 보기만 하는 설명인지, 예제 파일이 있는지, 루틴에 적은 내용이 강의에 실제로 있는지 → 강의 페이지 · Figma Learn을 직접 확인 |
| 4 | Figma 조작이 최신인가 | 단축키 · 메뉴 이름 · 버튼 위치 · 무료(Starter) 플랜 가능 여부를 Figma Learn 공식 문서로 확인. 확인 못 하면 “확인 필요”라고 적는다 |
| 5 | 순서대로 하면 결과가 나오나 | 앞 단계 결과가 다음 단계에 필요한 순서인가, 빠진 단계 없나, 전날 만든 것을 이어 받나, 날짜 참조(“11/20에”)가 맞나 |
| 6 | 무엇을 · 어디서 · 끝 기준 | 할 일 한 줄 → 순서표(순서 · 어디서 · 하는 일) → 용어표 → 확인. 끝났는지 아는 기준이 있나 |
| 7 | 기입표가 그 과제에 맞나 | 앱 ‘결과물 기입표’가 그 블록 과제에서 실제로 적을 것인가. 할 일 속 채울 표는 forms.py가 기입표로 옮긴다. 일반 표(‘제작 기록’ · ‘글 작성 기록’ · ‘강의 메모’ 등)가 붙어 있으면 forms2.FORMS에 그 과제 전용 표(칸 이름 · 예시 · 미리 적힌 줄)를 만든다. 매주 같은 형식이 필요한 것(주간 기록, AI 활용 기록)만 같은 표를 쓴다 |
| 8 | 이름 규칙(확정판) | `naming_guide.md`(Figma 이름 기준 확정판 — 공개 디자인 시스템 8곳 다수결, 11/23 고정)대로인가: 컬렉션 Primitives · Semantic · Size, 색 `속성/역할/변형` 3단(background/default/default · background/surface/default · background/brand/hover · text/default/subtle · text/on-brand/default · border/danger/default), Primitives `green/500` · `white`, 크기 `space/100`=4px(값÷4×100) · radius/200 · border-width/default, 글자 heading/large · heading/medium · body/medium · body/small · label/medium, 효과 shadow/100, 컴포넌트 button · icon-button · checkbox · text-field · dialog · button-group · toast · list-item · tab, 속성 variant=primary · secondary · tertiary · danger / state=default · hover · pressed · disabled / size / label / show icon / icon / checked, 레이어 영어 소문자-하이픈(dialog 안 title · description · button-group), 한국어는 페이지 · 화면 Frame · Section · Flow만 |
| 9 | 시간 배분 | 순서표의 분 합계가 블록 시간 안에 드나. 강의 길이가 블록보다 길면 주말 15:00–16:00 예비로 넘긴다고 적는다(강의는 줄이지 않는다) |
| 10 | 읽기 쉬운가 | 필요 없는 문장 · 번역투 · 같은 블록 안 중복 삭제. 용어는 원래 이름 + [뜻]. 필요한 설명은 다른 날과 겹쳐도 그날 블록에 다시 쓴다 |
| 11 | 학습 목표 | 목표 문장과 실제 할 일이 맞나 |

### 따라 하기 점검 A~L (블록마다 꼭, 처음 하는 사람이라 생각하고)
| # | 점검 | 통과 기준 |
|---|---|---|
| A | 한 줄씩 확인 | 순서표 줄마다 ① 무엇을 선택 ② 어디서(패널·메뉴 이름) ③ 무엇을 입력·고름 ④ 하고 나면 보이는 것. 하나라도 없으면 채운다 (나쁜 예: “Shift+A → 가로 Auto layout” — 무엇을 선택하는지·어디서 방향을 고르는지·결과가 없음) |
| B | 새 것 / 있는 것 | 블록에 나오는 Frame·화면·부품마다 “새로 만듦” 또는 “이미 있음(○/○에 만든 ○○)”이 적혀 있다 (나쁜 예: “390 목록 화면의 할 일 행”) |
| C | 그대로 따라 하기 | 순서표를 글자 그대로 따라 했을 때 생기는 레이어 구조를 직접 적어 본다. 블록 목표 화면과 다르면(겹침·안 늘어남·없는 것을 고르라고 함) 빠진 단계를 넣는다 (나쁜 예: list에 세로 Auto layout을 켜는 단계가 없어 행이 겹침) |
| D | 구조표 | Frame 안에 Frame이 2단계 이상 들어가면 순서표 위에 ‘Frame / Auto layout 방향 / W / H / 안에 들어가는 것’ 표가 있다 |
| E | 그림 범위 | 예시 그림의 부분마다 이 블록 것인지 다른 블록 것인지 표시가 있다 (나쁜 예: 768 블록 그림에 1280이 표시 없이 같이 있음) |
| G | 화면 요소 이름 | 누를 아이콘·버튼·칸마다 Figma 공식 이름(영문 그대로) + 위치(어느 패널·어느 칸·줄 앞/뒤) + 모양 + 보이는 조건(무엇을 선택해야 나타나나)을 쓴다. 이름은 Figma Learn에서 확인한다 (나쁜 예: “설정 아이콘” → 좋은 예: “Layout guide 칸에 새로 생긴 줄 앞의 격자 모양 아이콘(Layout guide settings)”) |
| H | 칸이 나타나는 순서 | 어떤 값을 골라야 다른 칸이 나타나면 그 값을 먼저 고르게 쓴다 (예: Margin · Gutter는 Type을 Stretch로 바꾼 뒤에만 보인다 → Type 먼저) |
| I | 보기 형식·분량 | 할 일은 ‘| 순서 | 만드는 것 | 하는 일 (시간) |’ 순서표 하나로 쓴다(앱에서 단계 카드로 보인다). 카드 하나 = 만드는 것 하나, 동작은 ‘ → ’로 나누고 카드당 8줄 안팎, 마지막에 ‘○○이 보이면 성공’. 구조는 ‘| Frame | Auto layout 방향 | W | H | 안에 들어가는 것 |’ 표로만 쓴다(앱에서 완성 구조 그림으로 그려진다) — 같은 구조를 글로 다시 설명하지 않는다. ‘이미 있는 것 / 새로 만드는 것’은 각 1줄, 이름만. 같은 뜻 문장 반복·괄호 속 긴 설명 금지. 4칸 이상 표는 줄 카드로 보이니 칸 이름을 짧게 |
| J | 예시 그림·자료 속 영상 | 만드는 블록(제작·훈련)은 완성 구조 그림 또는 figures.py 그림이 꼭 있다(없으면 만든다). ‘강의·자료’ 페이지마다 안에 든 영상 개수와 길이를 WebFetch로 확인해 자료 표 ‘길이·범위’에 ‘영상 n개 · 총 m분’으로 쓰고, 순서표에 ‘영상 보기’ 카드와 시간을 넣는다. 시간이 넘치면 예비 시간으로 옮긴다 |
| K | 줄 나누기 | 순서표 ‘하는 일’ 칸은 ‘ ¶ ’로 줄을 직접 나눈다(앱은 ¶ 기준으로 줄을 만든다). 한 줄 = 대상 하나에 하는 일 하나를 끝까지(무엇을 선택 → 어디서 → 무엇을 고름). ‘T’ · ‘radius/md’ · ‘이름 dialog’처럼 무엇에 하는지 모르는 조각 줄 금지 — 이름 바꾸기는 ‘감싼 Frame 이름 더블클릭 → actions’처럼 대상을 쓴다. 고르는 값은 그 칸과 같은 줄(‘Corner radius 칸 ◇ → radius/md’). 카드 첫 줄은 [어느 페이지](예: [‘컴포넌트’ 페이지])로 시작한다. 한 요소(글자 하나·버튼 하나)를 만드는 동작은 한 줄에 모은다(T → 클릭 → 입력 → Esc → 스타일). Auto layout 안에 넣는 동작은 놓을 자리(파란 선이 어디에 보일 때)와 잘못 들어갔을 때 고치는 줄을 쓴다. 글자 정렬(Align left 등)처럼 결과 모양을 바꾸는 설정은 빠뜨리지 않는다. 성공 줄은 완성 모습을 위치 · 순서까지 쓴다(예: ‘왼쪽에 글자, 오른쪽 끝에 버튼’). 표 칸 안 글에는 ‘|’를 쓰지 않는다(칸이 갈라져 글이 사라진다 — 나쁜 예: 11/22 상세 ‘수정 | 삭제’). 앱 스크린샷으로 줄마다 혼자 읽어도 뜻이 통하는지, 카드에 빠진 줄이 없는지 본다 |
| L | 앞 블록 결과 확인 | 이전 블록에서 만든 것을 쓰는 줄(복사 · 복제 · ‘이미 있는 것’)마다, 그 블록 지시에 그것을 실제로 만들라고 쓰여 있는지 원본(detail2 · clarify · w*.py)을 찾아 확인한다. 확인이 안 되거나 선택 사항이었으면 ‘없으면 이렇게 만든다’ 줄을 넣거나 처음부터 새로 만들게 쓴다(나쁜 예: 11/22 상세 ⑤ ‘수정 · 삭제 버튼 선택’ — 11/20 detail에 버튼을 넣었다는 보장이 없었음) |
| F | 자료 성격 | 강의·문서가 따라 하는 실습인지 보기만 하는 설명인지 확인하고 루틴에 그대로 쓴다 (나쁜 예: 보기만 하는 Habitz 강의를 ‘따라 만들기’로 씀) |
- 점검 대상: 내일과 모레 블록. 모레 것은 이틀 전에 한 번, 전날 밤에 한 번 보게 된다.
- 보고: 블록마다 A~F와 기준 1~11 결과를 표로.

## 3. 고친 뒤 확인 · 배포
```
python3 build.py                                  # PDF (google-chrome 필요)
qpdf --object-streams=generate --compress-streams=y --recompress-flate --compression-level=9 UIUX_24주_루틴_20261108.pdf ../assets/final-plan.pdf   # 무손실 압축. Cloudflare 파일 1개 한도 25MiB를 넘으면 배포 실패
git show HEAD:data/plan-final.json > /tmp/prev.json
python3 to_app.py ..                              # 앱 데이터
python3 verify_past.py /tmp/prev.json ../data/plan-final.json   # 오늘까지 기록 칸이 바뀌면 FAIL → 배포 금지
python3 md_gen.py                                 # out_md/ → 프로젝트 문서
```
- `../sw.js`의 캐시 이름 숫자를 1 올린다(ui-study-path-vNN).
- 커밋 → `git push origin main` → `gh api repos/hkjk8878/ui-study-path/commits/<sha>/check-runs`로 배포 성공 확인.
- 프로젝트 문서: `out_md/`의 해당 주차 파일을 같은 이름(`claude/UIUX_24주_루틴_20261117_…`)으로 덮어쓴다.

## 11/23 밤 일정 조정 (사용자 결정 · extra_plan.py)
- ‘하루’ 이름 정리는 멈춘다. ‘하루’ 블록에 ‘이름 바로잡기’ 카드를 넣지 않는다. 파일 이름이 블록과 달라도 보이는 이름 그대로 고르게 한다(NAME_NOTE). 확정판 이름은 12/21 CASE01 키트부터 처음부터 적용한다.
- 밀린 11/19~11/23 중 기술 블록만 다시 넣었다: 화 11/24 = 11/22 프로토타입 + 강의 2개, 수 11/25 = 원래 11/24 모션 + 밤 강의 2개, 토 11/28 오후 = 원래 11/25 명세, 일 11/29 15:10~ = 11/20 반응형. 원래 블록은 기록으로 그대로 둔다. 문서 · 규칙 · 색 규칙 · 버튼 다시 만들기 · ‘하루’ 정리는 뺐다.
- 추가 블록(b.extra = True, 주간 시간 계산에서 뺌): 월·수·금 22:00 ‘UI 따라 만들기’(1단계 똑같이 12회 → 2단계 규칙 찾기 ~1/29 → 3단계 수상작 5회 + 다시 설계하기), 일 15:10 ‘앱 뜯어보기’(12/6~), 토 15:10 ‘3시간 디자인 과제’(12/19 · 1/16 · 2/20 · 3/20). 고칠 때는 extra_plan.py를 고친다.
- 11/24 0시: 이번 주 ‘하루’ 실습 블록(화 프로토타입 · 화 AI · 수 모션 2 · 토 명세 3 · 일 반응형 2)을 새 빈 파일 ‘기능 연습’에서 처음부터 하는 블록으로 다시 썼다(extra_plan.rewrite_week). ‘하루’ 파일 상태에 기대는 줄을 쓰지 않는다. 11/26 10:10에 동의 두 번 나누기(CONSENT) 추가 — 사용자는 이직 준비 중이라 포트폴리오 공개 허락은 1월 마무리 때 받는다. 참여자 2명 예정.
- verify_past.py의 ‘블록 목록이 달라짐’은 이 조정 커밋에서만 의도된 차이다(오늘 이전 날짜 차이 없음 확인함).

## 4. 하지 말 것
- 오늘까지의 블록 기록 칸(recordSections) · 블록 id · 블록 순서 바꾸기
- 실제 ‘하루’ 앱 코드 수정, 사용자 개인정보를 AI에 올리기
- 확인하지 않은 단축키 · 메뉴를 확실한 것처럼 쓰기

## 사용자 Figma 파일 (하루v02) — 지시는 이 파일에 실제로 있는 것만 쓴다
- 링크: https://www.figma.com/design/XiPq1RgXThHHkxW9p1NASr/ (fileKey XiPq1RgXThHHkxW9p1NASr)
- 파일 상태는 Figma MCP로 읽지 않는다(11/23 사용자 결정 — Starter 플랜 MCP 읽기 한도가 매우 작아 밤 점검이 한도를 다 쓴다). 대신 사용자가 claude.ai 프로젝트에 올린 캡처(이름에 figma가 든 이미지 · 날짜가 가장 최근 것)를 project_info → project_read → Read로 본다. 캡처가 이 목록보다 새로우면 캡처를 기준으로 하고 이 목록을 고친다. 캡처가 없거나 해당 화면이 안 찍혀 있으면 이 목록을 기준으로 하고, 파일 상태에 따라 달라지는 줄에 ‘○○가 안 보이면: …’ 대체 카드를 넣는다.
- 11/23 08:20 0단계(확정판 이름 바로잡기)를 했다면: 컬렉션 Primitives(색만: green/300~500 · brown/200~800 · white · gray/300 · gray/500 · red/500) · Semantic(옛 Segmantic: background/default/default · background/surface/default · background/inverse/default · border/default/default · border/danger/default + 새 background/danger/default → red/500) · Size(space/ · radius/ · border-width/), 글자 스타일 heading/large · heading/medium · body/medium · body/small · label/medium, button 속성 variant(primary · secondary · tertiary · danger) · state · shape · label 소문자, 레이어 toast(그대로) · button-group · text-field · item-1~3 · dialog 안 title · description. 11/28 13:00에 남은 정리(Semantic 안 padding/gap/radius 숫자 · 다른 파일 변수 다시 연결 · Primitives Scoping 끄기). (11/23 08:44 사용자 답: 오전에 가이드 v2 ⓐ~ⓕ는 하지 않았음)
- 2026-11-23 19:50 점검: Figma MCP 호출 한도(Starter 플랜)로 파일을 읽지 못함 → 11/23 08:20 0단계 · 11/22 ⑧(목록 · 목록-삭제됨)이 실제로 됐는지 확인 못 함. 그래서 11/24 08:40 ⓪-2 · 10:10 ①-2에 ‘없을 때만 만든다’ 카드를 넣었다. 11/25 08:20에서 새로 생길 것: 페이지 ‘전달’, 부품 annotation(variant=action · condition · error · accessibility, 속성 number · description · show description), 화면 Frame 추가-기본 · 명세-할 일 추가, Semantic background/brand/default · background/neutral/default · text/default/default · text/on-brand/default · text/on-danger/default · text/on-inverse/default, Size radius/full(없을 때만).
- 2026-11-22 19:50 확인한 상태(ⓐ~ⓕ 전) (17:45와 같음 — 11/22 ⑧ 목록 · 목록-삭제됨과 Prototype 연결 · Flow는 아직 없음)
  - 페이지: 점검(비어 있음) · 컴포넌트 · 화면 · 프로토타입(비어 있음)
  - 컴포넌트 페이지: button(속성 Type · State · Shape · Label, 값이 Primary · Secondary · Tertiary · danger 처럼 대문자 섞임, danger는 State=Disabled 하나), dialog, toast, 이름 없는 Frame 1(사각형 9개)과 참고 이미지 8장. checkbox · todo/row · input 원본은 이 파일에 없음
  - todo/row: 다른 파일(라이브러리)의 부품. 화면의 Instance 속성 State(Off …) · Text · 날짜Text, 안에 checkbox Instance · title Frame(글자 2) · move Frame(reader-button 2). 부품 자체에 On click → Change to(다른 State) 연결이 있음
  - 화면 페이지: 상세 · 상세-수정됨 · 수정-기본 · 수정-입력됨 · 삭제-확인창. 모두 header(‘←’ · heading/medium 글자) · content · footer(button 2) 구조, 수정 화면 content는 field Frame 2개. ‘목록’ · ‘목록-삭제됨’ 화면 없음. 화면 사이 Prototype 연결 · Flow 없음(버튼 hover만)
  - 변수 컬렉션: Primitives(color/green · brown · netral · red, spacing/0-5~7, radius/sm~3xl, border/width) · Segmantic(철자 틀림 — 11/23 ⓪에서 Semantic으로 고침: bg/screen/screen · surface · inverse, border/strong, status/error, padding/control · card · screen, gap/inline · list · section, radius/control)
  - 화면에 쓰인 변수 이름에는 이 파일 컬렉션에 없는 text/primary · action/* · text/on-* · shadow/strong도 보인다(다른 파일 변수일 수 있음)
  - 글자 스타일 · 효과 스타일: 없음(heading/medium · body/regular는 레이어 이름) — 11/23 ⓪에서 만든다
- 이 목록에 없는 것을 쓰게 하려면 ‘먼저 만든다’ 줄을 넣는다. 파일 상태가 바뀌면 이 목록을 고친다.

## 이름은 naming_guide.md(확정판) 기준으로 — 다시 바꾸지 않는다
- 유일한 기준: `routine-src/naming_guide.md` = 프로젝트 문서 `claude/Figma_이름짓기_가이드.md`(확정판, 11/23 고정). 정한 방법: 특정 회사가 아니라 공개 디자인 시스템 8곳(Material 3 · Atlassian · Primer · Polaris · Carbon · Figma SDS · 당근 SEED · 정부 KRDS)에서 가장 많이 쓰는 방식, 갈리면 Figma 도움말 → Material 3. 사용자가 정한 원칙: 기준을 못 박고 중구난방으로 쓰지 않는다.
- 다른 강의 · 예제 · 이전 문서(가이드 v2 · SDS판)의 이름을 봐도 기준을 바꾸지 않는다. 고치는 경우는 근거와 다르게 적은 것을 찾았을 때 · 아직 없는 것을 새로 정할 때뿐이고, 그때도 확정판 규칙으로 짓고 문서에 추가한다.
- 루틴 지시에 나오는 이름(변수 · 스타일 · 컴포넌트 · 속성 · 레이어)은 모두 확정판 이름으로 쓴다. 이름을 적는 곳에는 값과 쓰는 곳을 같이 적는다.
- 파일 속 이름이 확정판과 다르면 그 이름을 처음 쓰는 블록 맨 앞에 ‘이름 바로잡기’ 카드(지금 → 확정 이름 · 어디서 바꾸나 · 왜 한 줄)를 넣는다. 확정판 9장 표가 하루v02 바꾸기 목록이다.
- 변수를 다른 컬렉션으로 옮기는 기능은 Figma에 없다(복사만 됨 → 다시 연결 필요). 그래서 옮기기 대신 이름 바꾸기 · 새로 만들기 · 다시 연결 순서로 쓴다.
- 기록 칸(forms2 · recordSections)의 이름은 과거 블록이면 바꾸지 않는다(verify_past).

## 보기 형식: 그림 + 짧은 줄 (11/23 사용자 요청)
- 그림으로 보여야 하는 것(어느 창 · 어느 칸 · 다 만든 모습)은 그림으로, 꼭 글이어야 하는 것(값 · 이름 · 이유 · 순서)은 글로. 그림을 넣는다고 내용을 빼지 않는다.
- 단계 카드 '하는 일' 칸에 쓰는 특수 줄 (stepfmt.py가 그린다):
  - `어디: 변수 창 › Size 컬렉션` → 카드 위 색 칩. 앞 단어로 색이 정해진다: 변수 창(보라) · 글자 스타일(초록) · 레이어 패널(파랑) · 속성(주황) · 캔버스 · 앱 기입표(회색)
  - `바꾸는 것: 레이어 패널 · 레이어 이름` → 진한 색 칩. 이름을 바꾸는 카드에는 반드시 넣어 변수 이름인지 레이어 이름인지 스타일 이름인지 헷갈리지 않게 한다
  - `그림:키` → minis.py의 화면 그림(MINI). 카드 밖 글 줄에도 쓸 수 있다. 필요한 그림이 없으면 minis.py에 함수를 새로 만든다(win · row · rename · ic · chip 도우미 사용, 폭 360 이하)
  - `왜: …` → 회색 메모 줄
- 줄 하나 = 동작 하나(약 40자 이내). 한 카드가 10줄을 넘거나 창이 바뀌면 카드를 쪼갠다(ⓓ-1 · ⓓ-2처럼).
- 이름을 붙이는 줄은 어디의 이름인지 쓴다: ‘레이어 이름 rule-row’, ‘변수 이름 칸’, ‘Edit style 창 Name 칸’.
- 고친 뒤 420px 스크린샷으로 칩 · 그림 · 줄이 잘 보이는지 확인한다.
