# 매일 밤 다음 날 블록 점검 — 작업 순서

목적: 내일 할 블록을 사용자가 읽자마자 막힘없이 하고, 그 결과가 포트폴리오와 취업에 바로 쓰이게 만든다.

## 1. 준비
```
cd routine-src
python3 -c "import pypdf, reportlab" || pip install --break-system-packages pypdf reportlab
python3 validate.py          # 블록 데이터 생성(오류 없으면 total work minutes 출력)
```
- 블록 내용 원본: `w02_04.py` · `w05_12.py` · `w13_18.py` · `w19_24.py`(기본) → `clarify.py`(표 · Figma 기능 · 이름) → `aiplan.py`(화·목 AI) → `detail.py` · `detail2.py`(하는 법 · 순서표 · `OVERRIDE` = 블록 전체 교체) → `forms.py`(할 일 속 기입표를 앱 기입표로)
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
| 7 | 기입표가 맞나 | 할 일 속 “채울 표”가 앱 ‘결과물 기입표’로 들어가나(forms.py). 할 일과 상관없는 일반 기입표가 붙어 있지 않나 |
| 8 | 이름 규칙(실무) | 영어는 모두 소문자(button · state=default · text/primary · heading/large), 컬렉션만 Primitives · Semantic, 페이지 · 화면 Frame · Section · Flow는 한국어(‘화면-상태’), / = 폴더, - = 단어 잇기 |
| 9 | 시간 배분 | 순서표의 분 합계가 블록 시간 안에 드나. 강의 길이가 블록보다 길면 주말 15:00–16:00 예비로 넘긴다고 적는다(강의는 줄이지 않는다) |
| 10 | 읽기 쉬운가 | 필요 없는 문장 · 번역투 · 같은 블록 안 중복 삭제. 용어는 원래 이름 + [뜻]. 필요한 설명은 다른 날과 겹쳐도 그날 블록에 다시 쓴다 |
| 11 | 학습 목표 | 목표 문장과 실제 할 일이 맞나 |

## 3. 고친 뒤 확인 · 배포
```
python3 build.py                                  # PDF (google-chrome 필요)
cp UIUX_24주_루틴_20261108.pdf ../assets/final-plan.pdf
git show HEAD:data/plan-final.json > /tmp/prev.json
python3 to_app.py ..                              # 앱 데이터
python3 verify_past.py /tmp/prev.json ../data/plan-final.json   # 오늘까지 기록 칸이 바뀌면 FAIL → 배포 금지
python3 md_gen.py                                 # out_md/ → 프로젝트 문서
```
- `../sw.js`의 캐시 이름 숫자를 1 올린다(ui-study-path-vNN).
- 커밋 → `git push origin main` → `gh api repos/hkjk8878/ui-study-path/commits/<sha>/check-runs`로 배포 성공 확인.
- 프로젝트 문서: `out_md/`의 해당 주차 파일을 같은 이름(`claude/UIUX_24주_루틴_20261117_…`)으로 덮어쓴다.

## 4. 하지 말 것
- 오늘까지의 블록 기록 칸(recordSections) · 블록 id · 블록 순서 바꾸기
- 실제 ‘하루’ 앱 코드 수정, 사용자 개인정보를 AI에 올리기
- 확인하지 않은 단축키 · 메뉴를 확실한 것처럼 쓰기
