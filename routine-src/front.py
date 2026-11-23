import re
import html
from res import R
E = html.escape

def L(k, text=None):
    name, url, _ = R[k]
    return f'<a href="{E(url)}">{E(text or name)}</a>'

KINDS = [('강의', '영상·문서를 보고 예제를 따라 만든다'), ('제작', 'Figma·HTML로 화면과 흐름을 만든다'), ('조사', '실제 사람을 만나 듣고 본다'),
         ('분석', '기록을 묶고 문제를 정의한다'), ('검증', '테스트·점검으로 확인하고 고친다'), ('AI', '화·목 저녁, AI로 만들고 직접 확인한다'),
         ('훈련', '토요일 오전 UI 완성도 훈련'), ('점검', '일요일 주간 점검·기록')]


def naming_html():
    import markdown
    md = open('naming_guide.md').read()
    md = re.sub(r'^# (.*)$', r'## \1', md, count=1, flags=re.M)
    h = markdown.markdown(md, extensions=['tables'])
    h = h.replace('<h2>', '<h2 class="fp-h">').replace('<h3>', '<h3 class="fp-h3">').replace('<table>', '<table class="ftab">').replace('<blockquote>', '<div class="note">').replace('</blockquote>', '</div>')
    return h


def FRONT(toc, figure):
    from render import KIND, WEEKS
    cover = f'''<section class="cover">
<div class="cv-top">UI/UX · 프로덕트 디자이너 취업 준비</div>
<h1 class="cv-t">24주 루틴</h1>
<div class="cv-s">2주차 ~ 24주차 일별 계획 · 2026.11.9 (월) – 2027.4.18 (일)</div>
<div class="cv-grid">
<div><div class="cv-n">25<small>시간</small></div><div class="cv-l">매주 배정</div></div>
<div><div class="cv-n">23<small>시간 50분</small></div><div class="cv-l">매주 실제 작업(휴식 70분 제외)</div></div>
<div><div class="cv-n">548<small>시간 10분</small></div><div class="cv-l">23주 작업 합계 (배정 575시간)</div></div>
<div><div class="cv-n">3<small>개</small></div><div class="cv-l">포트폴리오 사례 (대표 2 + 심화 1)</div></div>
</div>
<div class="cv-goal"><b>목표</b> 신입·주니어 UI/UX·프로덕트 디자이너 채용에서 서류와 면접을 통과할 수 있는 실력과 포트폴리오를 만든다. 기준은 채용공고와 기업이 직접 밝힌 평가 기준이다.</div>
<div class="cv-foot">2026년 11월 8일 작성 · 공고 내용은 지원 전에 다시 확인한다</div>
</section>'''

    crit = [
     ('대표 사례 2개를 깊게', f'{L("toss_bank","토스뱅크 신입 전형")}: 대표 프로젝트 2개만 넣고, 면접에서 직접 고른 2개 사례를 깊게 묻는다', 'CASE01·02를 대표로 완성, CASE03은 그중 하나의 심화', '5–18주'),
     ('실제 사용자 데이터로 개선', '토스뱅크 신입 자격요건: 개인 취향이 아닌 정량·정성 사용자 데이터로 제품을 개선한 경험', '원문 카드 번호, 기준선 측정, 같은 방법으로 전후 비교', '5–6 · 12 · 14주'),
     ('출시·피드백·동작 링크', '토스뱅크: 설계·출시하거나 피드백을 받은 경험 / 당근 인턴(11/3 확인): 출시·실제 반응·동작 링크', '학원 내부 도구에 실제 반영 후 측정, CASE02 웹 링크 배포', '11–12 · 17주'),
     ('시각적 완성도', f'토스뱅크: 정보 위계를 고려한 시각적 완성도 / {L("toss_ch","토스 챌린지")} 평가 기준 / {L("brunch_mistake","국내 첨삭 2026")}: 화면 완성도 부족이 1순위 실수', '토요일 UI 완성도 훈련 18회, 사례마다 고해상도 UI 1~2주', '2–20주'),
     ('넓은 탐색과 선택 이유', f'{L("kolko","Kolko, ACM Interactions 2025")}: 실질적으로 다른 해결안 10~15개 탐색 후 1~2개로 좁혀 테스트', '해결안 12개 이상 → 평가 → A/B → 테스트 → 선택 기록', '7–8 · 15주'),
     ('흐름이 보이는 제출물', '토스 챌린지: 결과 화면이 아닌 실제 사용자 흐름을 URL로 제출, 문제 정의 필수', '모든 사례에 프로토타입·동작 링크, 23주차 과제형 연습', '2 · 17 · 20 · 23주'),
     ('도구·협업·전달', 'LINE Pay(11/3 확인): 흐름 설계·디자인 시스템·AI 프로토타입 / 토스플레이스: PO·개발자와 함께 문제 해결', '컴포넌트·변수·디자인 시스템, 개발 전달 명세, 크리틱 받기', '2–4 · 9 · 11 · 16 · 18주'),
     ('AI 활용과 판단', '토스 챌린지: 전 단계 AI 허용 / LINE Pay: AI 프로토타입·생산성 개선', '화·목 AI 46회: 요청문 직접 작성, 실행 확인, 요청·수정 횟수 기록', '매주'),
    ]
    rows = ''.join(f'<tr><td class="c1">{E(a)}</td><td>{b}</td><td>{E(c)}</td><td class="c4">{E(d)}</td></tr>' for a, b, c, d in crit)
    basis = f'''<section class="fp"><div class="fp-k">기준</div><h1 class="fp-t">이 루틴이 맞춘 채용 기준</h1>
<p class="lead">아래 기준은 기업이 공고·전형 페이지에 직접 쓴 내용과 디자인 리더의 글에서 가져왔다. 주차별 과제는 모두 이 표의 어느 칸을 채우기 위한 것이다.</p>
<table class="ctab"><thead><tr><th style="width:17%">기준</th><th style="width:38%">근거</th><th style="width:31%">이 루틴에서 만드는 증거</th><th style="width:14%">주차</th></tr></thead><tbody>{rows}</tbody></table>
<div class="note"><b>라프텔</b>은 장기 목표로 둔다. 2026년 공고 기준 프로덕트 디자이너는 경력 3년 이상 또는 그에 준하는 실력을 요구한다. 첫 지원은 직원 50명 이상의 신입·주니어 지원 가능 포지션(콘텐츠 플랫폼과 일반 서비스)을 중심으로 하고, CASE02에서 콘텐츠 플랫폼 과업을 다뤄 연결 고리를 만든다.</div>
</section>'''


    nums = '''<section class="fp"><div class="fp-k">숫자</div><h1 class="fp-t">숫자 읽는 법 (크기·글자·색)</h1>
<p class="lead">루틴에 나오는 숫자는 세 종류다. <b>기준</b>은 꼭 지킨다. <b>기본값</b>은 많이 쓰는 값이라 처음엔 그대로 쓴다. <b>시작값</b>은 이 루틴이 정한 값이라 이유가 있으면 바꿔도 된다. Figma에는 단위 없이 숫자만 입력하며, 그 숫자가 px(1배 화면 기준)이다.</p>
<table class="ctab"><thead><tr><th style="width:19%">숫자</th><th style="width:31%">무엇인가</th><th style="width:9%">종류</th><th style="width:22%">출처</th><th>바꿔도 되나</th></tr></thead><tbody><tr><td><b>누르는 영역 44×44</b></td><td>손가락으로 누르는 버튼 프레임의 크기. 아이콘보다 커도 되고, 배경을 꺼서 눈에 안 보여도 된다.</td><td><span class="nk nk-s">기준</span></td><td>Apple 디자인 가이드(iOS). Android는 48×48</td><td>작게 하면 안 됨(더 크게는 가능)</td></tr><tr><td><b>웹 최소 24×24</b></td><td>웹 접근성에서 허용하는 가장 작은 누르는 영역</td><td><span class="nk nk-s">기준</span></td><td>WCAG 2.2 (2.5.8)</td><td>작게 하면 안 됨</td></tr><tr><td><b>글자 대비 4.5:1</b></td><td>글자색과 배경색의 밝기 차이. 대비 계산기에 두 색을 넣으면 숫자가 나온다. 큰 글자(24 이상, 굵게는 19 이상)와 아이콘은 3:1</td><td><span class="nk nk-s">기준</span></td><td>WCAG 2.2 (1.4.3 · 1.4.11)</td><td>낮추면 안 됨</td></tr><tr><td><b>입력창 글자 16 이상</b></td><td>입력창 안에 사용자가 치는 글자 크기</td><td><span class="nk nk-s">기준(웹)</span></td><td>iPhone 웹에서 16보다 작으면 입력할 때 화면이 자동 확대된다</td><td>낮추면 안 됨</td></tr><tr><td><b>버튼·입력창 높이 48</b></td><td>누르는 버튼과 입력칸의 세로 크기</td><td><span class="nk nk-d">기본값</span></td><td>Google Material</td><td>44 이상이면 바꿔도 됨</td></tr><tr><td><b>본문 16 / 줄 간격 24</b></td><td>“16/24”는 글자 크기 16, 줄 간격(Line height) 24라는 뜻</td><td><span class="nk nk-d">기본값</span></td><td>Material 3 Body Large. iOS 기본 본문은 17</td><td>16~17 사이에서 선택</td></tr><tr><td><b>보조 13 · 가장 작은 글자 12</b></td><td>날짜·안내문 같은 작은 글자</td><td><span class="nk nk-d">기본값</span></td><td>iOS Footnote 13 · Material Body Small 12</td><td>12보다 작게는 쓰지 않음</td></tr><tr><td><b>아이콘 24</b></td><td>아이콘이 들어가는 정사각형 크기</td><td><span class="nk nk-d">기본값</span></td><td>Material 기본 아이콘 크기</td><td>20~24에서 선택, 한 화면에서는 통일</td></tr><tr><td><b>여백 12 · 간격 8 · 체크 아이콘 22</b></td><td>할 일 행 안쪽 여백, 체크와 제목 사이, 체크 모양 크기</td><td><span class="nk nk-m">시작값</span></td><td>이 루틴이 정한 값</td><td>바꿔도 됨. 바꾸면 정렬(점선)도 다시 맞춘다</td></tr><tr><td><b>간격 단계 4·8·12·16·24·32</b></td><td>여백·간격에 쓸 숫자 목록</td><td><span class="nk nk-m">시작값</span></td><td>4의 배수로 맞추는 흔한 관례</td><td>바꿔도 됨. 목록 밖 숫자는 쓰지 않는다</td></tr></tbody></table>
<h2 class="fp-h">Figma 용어 (Figma 화면에 나오는 영어 이름 그대로 쓴다)</h2>
<table class="ftab"><tbody>
<tr><td><b>Frame</b></td><td>화면이나 칸을 담는 상자. 이 루틴의 ‘화면’ = 390×844 Frame 하나</td></tr>
<tr><td><b>Section</b></td><td>여러 화면을 한 영역으로 묶어 캔버스를 정리하는 틀</td></tr>
<tr><td><b>Auto layout</b></td><td>Frame 안 요소를 자동으로 줄 세우고 여백·간격을 지키게 하는 설정</td></tr>
<tr><td><b>Main component</b></td><td>‘컴포넌트’ 페이지에 만든 원본(보라색 ◆). 이걸 고치면 Instance가 모두 바뀐다. 루틴의 ‘원본’은 이것을 말한다</td></tr>
<tr><td><b>Instance</b></td><td>Main component를 화면에 가져다 쓴 복사본(◇)</td></tr>
<tr><td><b>Variant · Property</b></td><td>한 컴포넌트의 상태 버전(예: state=default · error) · 그 버전을 고르는 오른쪽 패널 항목</td></tr>
<tr><td><b>Detach instance</b></td><td>Instance와 Main component의 연결을 끊는 메뉴. 쓰지 않는다</td></tr>
<tr><td><b>Prototype 탭 · Flow · Present</b></td><td>화면 연결 패널 · Present에서 고르는 시작점 · 발표 모드(오른쪽 위 ▶)</td></tr>
</tbody></table>
''' + naming_html() + '''<div class="note"><b>Figma에서 넣는 곳</b> · 누르는 영역·높이: 프레임의 W·H를 Fixed로 · 여백: Auto layout의 Padding · 간격: Auto layout의 Gap · 글자 크기·줄 간격: 텍스트 선택 후 Typography의 Size·Line height(px로) · 대비: 두 색을 대비 계산기(예: WebAIM Contrast Checker)나 Figma 대비 플러그인에 넣어 숫자 확인</div>
</section>'''
    tags = ''.join(f'<div class="kd"><span class="tag" style="color:{KIND[k][0]};background:{KIND[k][1]}">{E(k)}</span><span>{E(v)}</span></div>' for k, v in KINDS)
    rules = f'''<section class="fp"><div class="fp-k">규칙</div><h1 class="fp-t">시간표와 진행 규칙</h1>
<table class="ttab"><thead><tr><th>요일</th><th>시간</th><th>휴식</th><th>작업 시간</th></tr></thead><tbody>
<tr><td>월–금</td><td>08:00 – 11:00</td><td>10:00 – 10:10</td><td>하루 2시간 50분</td></tr>
<tr><td>토·일</td><td>09:00 – 11:00 · 13:00 – 15:00</td><td>14:00 – 14:10</td><td>하루 3시간 50분</td></tr>
<tr><td>화·목 저녁</td><td>22:00 – 23:00 (AI)</td><td>없음</td><td>1시간</td></tr>
<tr><td>토·일 예비</td><td>15:00 – 16:00</td><td>없음</td><td>밀린 일이 있을 때만</td></tr>
<tr class="sum"><td>주간</td><td colspan="2">배정 25시간 · 23주 575시간</td><td>23시간 50분 · 23주 548시간 10분</td></tr>
</tbody></table>
<h2 class="fp-h">블록을 진행하는 방법</h2>
<ol class="rules">
<li><b>결과물이 있어야 끝난 것이다.</b> 각 블록의 ‘결과물’이 저장돼 있지 않으면 시간이 지나도 끝난 것이 아니다.</li>
<li><b>일찍 끝나면</b> 그 블록의 ‘일찍 끝나면’ 항목을 한다. 항목이 없으면 그 주 ‘결과물 확인 기준’을 다시 실행해 실패한 것을 고친다. 영상을 하나 더 보는 것으로 채우지 않는다.</li>
<li><b>못 끝내면</b> 다음 날 일정은 건드리지 않고, 그 주 토·일 15:00–16:00 예비 시간에 한다. 밀린 일이 없으면 예비 시간은 쉰다. 강의·튜토리얼은 줄이지 않는다. 예비 시간으로도 모자라면 시간을 더 써서라도 끝까지 본다.</li>
<li><b>인터뷰·관찰·테스트는 상대의 시간에 맞춘다.</b> 공부 시간 밖에서 진행했다면 그 블록을 기록 정리로 바꾸고 주간 총 시간은 유지한다.</li>
<li><b>개인정보:</b> 실제 이름·학생 정보·연락처는 기록에서 지우고 AI에 올리지 않는다. AI가 만든 발언·관찰을 조사 결과로 쓰지 않는다. 본인 점검과 실제 사용자 확인을 구분해 적는다.</li>
<li><b>AI 저녁(화·목):</b> ① 무엇을 만드는지 정한다 ② 요청문은 직접 쓴다 ③ 실행해 기대 결과와 비교한다 ④ 틀린 부분만 고치게 하고 같은 조작으로 다시 확인한다 ⑤ 전체 요청 횟수·수정 요청 횟수·걸린 시간을 적는다.</li>
<li><b>Figma 무료(Starter) 플랜 기준:</b> 컴포넌트 라이브러리 게시 불가 → 같은 파일 안 페이지로 관리. 변수 모드는 컬렉션당 1개. 프로토타입 안의 변수·조건은 유료 → 그 로직은 HTML로 구현해 동작 링크로 쓴다. 주석 기능·Dev Mode는 유료 → 직접 만든 주석 컴포넌트로 전달 명세를 만든다.</li>
<li><b>토요일 오전 레퍼런스 훈련</b>에서 다시 만든 남의 화면은 포트폴리오에 내 작업처럼 넣지 않는다.</li>
<li><b>매일 · 매주 기록:</b> 매일 앱 ‘오늘의 공부 기록’에 결정과 근거 · 증거 파일 · 막힌 곳을 남기고, 매주 ‘주간 회고’에 채용 기준 중 채운 칸과 사례에 쓸 결정(문제 → 선택지 → 고른 이유 → 결과)을 적는다. 면접의 “왜 이렇게 했나요?”와 포트폴리오 과정 이미지는 그날 남기지 않으면 다시 만들 수 없다.</li>
<li><b>학습 목표:</b> 할 일만 봐서는 목적이 잘 안 보이는 블록에는 맨 위에 ‘학습 목표’ 줄이 있다. 시작하기 전에 먼저 읽고, 끝난 뒤 그 목표를 이뤘는지로 스스로 점검한다.</li>
<li><b>예시 그림:</b> Figma 기능을 처음 배우는 블록과 처음 보는 결과물 형식(표·문서·다이어그램)에는 예시 그림이 있다. 그림은 1분 보고 닫은 뒤 직접 만들고, 끝나면 비교한다. 화면 디자인을 정하는 블록에는 일부러 그림을 넣지 않았다(‘예시’ 줄에 표시). 그림 속 문구·숫자는 형식 예시다.</li>
</ol>
<h2 class="fp-h">블록 종류</h2><div class="kinds">{tags}</div>
<h2 class="fp-h">파일</h2>
<table class="ftab"><tbody>
<tr><td>Figma <code>하루_연습</code></td><td>2–4주 기초 연습. 페이지: 점검 / 컴포넌트 / 기초 / 화면 / 프로토타입 / 전달 / 주간 기록. 포트폴리오 사례가 아니다.</td></tr>
<tr><td>Figma <code>CASE01</code> · <code>CASE02</code> · <code>CASE03</code></td><td>사례별 파일. 조사 카드는 FigJam 또는 같은 파일의 조사 페이지.</td></tr>
<tr><td>폴더 <code>CASE0n/</code></td><td>원문 기록(익명) · 측정표 · 테스트 기록 · 사례 원고 · HTML 프로토타입</td></tr>
<tr><td><code>날짜_AI.html</code> · <code>날짜_AI_기록.md</code></td><td>AI 저녁 결과물과 요청·수정 횟수 기록</td></tr>
</tbody></table>
</section>'''

    cases = [('CASE01', '학원 직원의 실제 업무 개선', '기본 후보: 수업 일정 변경 → 전달 → 확인', '4주 목 – 12주 (11/26 – 1/24)<br>보완 19–21주', '실제 근거로 문제 정의, 넓은 탐색과 선택, 고해상도 UI, 사용성 테스트, <b>학원 도구에 실제 출시</b>와 전후 측정', '원문 카드·기준선 측정표·A/B 선택 기록·테스트 전후·출시 후 측정·사례 페이지·7분 발표'),
             ('CASE02', '소비자 앱의 핵심 과업 개선', '기본 후보: 콘텐츠 앱의 작품 탐색·찜·이어보기', '13 – 18주 (1/25 – 3/7)<br>보완 19–21주', '경쟁 서비스 리뷰, 소비자 선택 기준을 반영한 정보 설계, 앱·웹 반응형, <b>동작 링크</b>', '경쟁 리뷰 매트릭스·조사 결과·A/B·앱+웹 UI·배포 링크·테스트 전후·사례 페이지'),
             ('CASE03', '상태 이해와 오류 복구 인터랙션', 'CASE01·02에서 관찰된 헷갈리는 상태 흐름 하나', '19 – 21주 (3/8 – 3/28)', '상태 설계, 모션 명세(길이·이징·이유), 모션 줄이기 대안, 실제 동작과 영상', '상태 다이어그램·모션 명세·동작 링크·After Effects 시연 영상·테스트 결과')]
    crows = ''.join(f'<tr><td class="cn">{a}<div class="cs">{E(b)}</div></td><td>{E(c)}</td><td>{d}</td><td>{e}</td><td>{E(f)}</td></tr>' for a, b, c, d, e, f in cases)
    mapp = f'''<section class="fp"><div class="fp-k">지도</div><h1 class="fp-t">24주 지도와 포트폴리오 3개</h1>
{figure('roadmap')}
<table class="castab"><thead><tr><th style="width:17%">사례</th><th style="width:17%">대상</th><th style="width:15%">기간</th><th style="width:27%">보여줄 역량</th><th>남는 증거</th></tr></thead><tbody>{crows}</tbody></table>
<div class="note">‘하루’(개인 일정관리 앱)는 2–4주 Figma 기초 연습 소재다. 실제 ‘하루’ 앱 코드는 수정하지 않는다. 22주차에 세 사례를 담은 웹사이트와 PDF판을 만들고, 23주차에 과제형 전형을 연습한 뒤 24주차에 지원을 시작한다.</div>
</section>'''

    trs = ''
    for w in WEEKS:
        p = toc.get(f'w{w.n:02d}', '')
        trs += f'<tr><td class="tn"><a href="#w{w.n:02d}">{w.n}주차</a></td><td><a href="#w{w.n:02d}">{E(w.title)}</a></td><td class="td">{w.days[0].date[5:].replace("-","/")} – {w.days[-1].date[5:].replace("-","/")}</td><td class="tp">{p}</td></tr>'
    toc_html = f'''<section class="fp"><div class="fp-k">목차</div><h1 class="fp-t">주차별 목차</h1><table class="toc"><tbody>{trs}</tbody></table></section>'''
    return cover + basis + rules + nums + mapp + toc_html
