from svg import *

FIG = {}
def wrap(t, maxw, size):
    words=t.split(' '); lines=['']
    for w_ in words:
        cand=(lines[-1]+' '+w_).strip()
        if tw(cand,size)<=maxw: lines[-1]=cand
        else: lines.append(w_)
    return lines
def fig(key, caption):
    def deco(fn):
        FIG[key] = (fn, caption); return fn
    return deco

def mini_lines(s, x, y, w, n=3, c='#E5E7EB', gap=9, h=5):
    for i in range(n):
        s.rect(x, y+i*gap, w*(1 - 0.18*(i%3)), h, c, c, 2)

# ───────────────────────── 로드맵
@fig('roadmap', '24주 전체 지도 · 단계와 주요 마감')
def roadmap():
    s = S(680, 330)
    x0, x1 = 40, 660; per = (x1-x0)/24
    s.text(x0, 18, '주차', 10.5, 600, SUB)
    for i in range(24):
        x = x0 + i*per
        s.rect(x+1, 26, per-2, 18, BG if i else '#E5E7EB', BG, 3)
        s.text(x+per/2, 39, str(i+1), 9.5, 600 if i else 400, SUB if i else MUTE, 'middle')
    months = [('11월',1),('12월',5),('1월',9.15),('2월',13.6),('3월',17.6),('4월',22.1)]
    for m, w in months:
        s.text(x0+(w-1)*per+2, 60, m, 10, 500, MUTE)
    phases = [('완료','✓',1,1,'#E5E7EB',MUTE),
              ('A','Figma · 하루',2,4,BLUE_L,BLUE),
              ('B','CASE01 학원 업무 개선 → 실제 출시',4.6,12,GREEN_L,GREEN),
              ('C','CASE02 콘텐츠 과업',13,18,PURPLE_L,PURPLE),
              ('D','CASE03',19,21,AMBER_L,AMBER),
              ('E','사이트·지원',22,24,'#E5E7EB','#374151')]
    y = 72
    for i,(k,label,a,b,bg,fg) in enumerate(phases):
        xa = x0+(a-1)*per; xb = x0+b*per
        yy = y + (i%2)*34
        s.rect(xa, yy, xb-xa, 26, bg, fg, 6, 1)
        s.text(xa+(xb-xa)/2 if b-a<1 else xa+7, yy+17, label, 10.5, 700, fg, 'middle' if b-a<1 else 'start')
    s.text(x1, 14, '1주차(입문 코스)는 완료 · 이 계획은 2주차(11/9)부터', 9.5, 500, MUTE, 'end')
    # gates
    gates = [(4,'11/29','‘하루’ 완료'),(10.72,'1/15','학원 도구 출시'),(12,'1/24','CASE01 1차'),(16.3,'2/23','동작 링크'),(18,'3/7','CASE02 1차'),(21,'3/28','CASE03'),(21.45,'3/31','사이트 배포'),(23.3,'4/13','지원 시작')]
    gy = 156
    s.line(x0, gy, x1, gy, LINE, 1.2)
    for i,(wk,d,lab) in enumerate(gates):
        x = x0 + wk*per - 4
        s.add(f'<path d="M{x},{gy-6} L{x+6},{gy} L{x},{gy+6} L{x-6},{gy} z" fill="{INK}"/>')
        yy = gy+22 + (i%2)*30
        s.line(x, gy+6, x, yy-11, LINE, 1, '2,2')
        s.text(x, yy, d, 10, 700, INK, 'middle')
        s.text(x, yy+13, lab, 9.5, 400, SUB, 'middle')
    # threads
    ty = 238
    s.text(x0, ty-8, '매주 반복', 10.5, 700, SUB)
    threads = [('토 09–11  UI 완성도 훈련 (18회)',2,20,'#FCE7F3','#BE185D'),
               ('화·목 22–23  AI 실습 (46회)',2,24,'#E0E7FF','#4338CA'),
               ('일 14:10–15  주간 점검',2,24,BG,SUB),
               ('평일 08–09  대표 사례 보완',19,21,AMBER_L,AMBER)]
    for i,(lab,a,b,bg,fg) in enumerate(threads):
        xa = x0+(a-1)*per; xb = x0+b*per; yy = ty + i*22
        s.rect(xa, yy, xb-xa, 16, bg, bg, 8)
        if tw(lab, 9.8) + 16 > xb-xa:
            s.text(xa-8, yy+12, lab, 9.8, 600, fg, 'end')
        else:
            s.text(xa+8, yy+12, lab, 9.8, 600, fg)
    return s

# ───────────────────────── W2 점검 페이지
@fig('inventory', '예시 · ‘하루’ 점검 페이지. 같은 역할 요소를 열로 모으고 불일치에 빨간 메모를 붙인다')
def inventory():
    s = S(680, 300)
    s.rect(0, 0, 680, 300, '#FAFAFA', LINE, 8)
    s.text(16, 24, '점검 페이지', 13, 700, INK); s.text(100, 24, '(Figma 파일 ‘하루_연습’ › 점검 페이지)', 11, 400, MUTE)
    cols = ['버튼', '입력', '목록 행', '체크', '빈 상태', '확인창']
    cw = 102
    for i, c in enumerate(cols):
        x = 16 + i*(cw+8)
        s.rect(x, 38, cw, 248, WHITE, LINE, 6)
        s.text(x+10, 58, c, 12, 700, INK)
        s.text(x+cw-10, 58, ['4곳','3곳','6곳','2곳','2곳','2곳'][i], 10, 500, MUTE, 'end')
    # 버튼 열
    x = 16
    for j, (lab, w, h, r) in enumerate([('추가', 70, 30, 8), ('저장', 70, 34, 6), ('저장', 82, 30, 15), ('취소', 70, 30, 8)]):
        yy = 72 + j*44
        s.rect(x+10, yy, w, h, BLUE if lab != '취소' else WHITE, BLUE, r)
        s.text(x+10+w/2, yy+h/2+4, lab, 11, 600, WHITE if lab != '취소' else BLUE, 'middle')
    # 입력
    x = 16 + 1*(cw+8)
    for j in range(3):
        yy = 72 + j*52
        s.text(x+10, yy+8, '제목' if j < 2 else '할 일', 9.5, 500, SUB)
        s.rect(x+10, yy+13, 82, 26, WHITE, '#9CA3AF' if j != 1 else '#D1D5DB', 5 if j != 2 else 0)
    # 목록 행
    x = 16 + 2*(cw+8)
    for j in range(5):
        yy = 70 + j*32
        s.rect(x+8, yy, 86, 28, WHITE, '#E5E7EB', 4)
        s.rect(x+14, yy+8, 12, 12, WHITE, '#9CA3AF', 3 if j != 3 else 6)
        mini_lines(s, x+32, yy+8, 54 if j != 4 else 40, 2, '#D1D5DB', 8, 4)
    # 체크
    x = 16 + 3*(cw+8)
    s.rect(x+14, 76, 18, 18, WHITE, '#6B7280', 4); s.rect(x+44, 76, 18, 18, BLUE, BLUE, 4)
    s.text(x+53, 89, '✓', 12, 700, WHITE, 'middle')
    s.rect(x+14, 108, 18, 18, WHITE, '#6B7280', 9); s.rect(x+44, 108, 18, 18, GREEN, GREEN, 9)
    # 빈 상태
    x = 16 + 4*(cw+8)
    s.rect(x+10, 72, 82, 76, BG, BG, 6); s.text(x+51, 104, '할 일이', 9.5, 500, SUB, 'middle'); s.text(x+51, 118, '없어요', 9.5, 500, SUB, 'middle')
    s.rect(x+10, 158, 82, 50, WHITE, '#E5E7EB', 6); s.text(x+51, 186, '(문구 없음)', 9, 400, MUTE, 'middle')
    # 확인창
    x = 16 + 5*(cw+8)
    s.rect(x+10, 72, 82, 70, WHITE, '#9CA3AF', 8); mini_lines(s, x+18, 84, 60, 2); s.rect(x+18, 116, 30, 18, BG, BG, 4); s.rect(x+54, 116, 30, 18, RED, RED, 4)
    # 빨간 메모
    notes = [(16+8, 240, '모서리 6·8·15\n세 가지'), (16+(cw+8)+6, 240, '레이블 있는\n화면/없는 화면'), (16+2*(cw+8)+6, 240, '체크 모양\n2종 섞임'), (16+4*(cw+8)+6, 240, '빈 상태 문구\n화면마다 다름')]
    for (nx, ny, t) in notes:
        s.rect(nx, ny, 92, 38, RED_L, RED, 4)
        for k, ln in enumerate(t.split('\n')):
            s.text(nx+7, ny+15+k*14, ln, 9.5, 600, RED)
    return s

# ───────────────────────── 할 일 행 해부도
@fig('row_anatomy', '예시 · 할 일 행 컴포넌트 구조. 체크·버튼은 중첩 인스턴스, 간격은 Auto layout 값으로 정한다')
def row_anatomy():
    s = S(680, 312)
    X, Y, W, H = 20, 56, 410, 84
    P, T = 12, 44                    # 행 안쪽 여백, 터치 영역(버튼 프레임)
    s.text(X, 16, '할 일 행 (원본 컴포넌트)', 12.5, 700, INK)
    s.rect(X, Y, W, H, WHITE, BLUE, 8, 1.5)
    cy = Y + P + T/2                 # 버튼 프레임 가운데 = 제목 첫 줄 가운데
    s.line(X-6, cy, X+W+6, cy, '#93C5FD', 1, '3,3')
    # 체크: 44×44 버튼 프레임(점선) 안에 22×22 아이콘
    s.rect(X+P, Y+P, T, T, 'none', '#A78BFA', 6, 1, '3,2')
    s.rect(X+P+11, cy-11, 22, 22, WHITE, '#6B7280', 5, 1.5)
    TX = X+P+T+8
    s.text(TX, cy+5, '토요일 오전 UI 완성도 훈련 자료', 13, 600, INK)
    s.text(TX, cy+23, '정리하고 레퍼런스 캡처하기', 13, 600, INK)
    s.text(TX, cy+39, '11/14 · 09:00', 10.5, 400, SUB)
    # 더보기: 44×44 버튼 프레임
    MX = X+W-P-T
    s.rect(MX, Y+P, T, T, 'none', '#A78BFA', 6, 1, '3,2'); s.text(MX+T/2, cy+6, '⋯', 22, 700, '#4B5563', 'middle')
    # 치수
    dy = Y+H+14
    ORG = '#B45309'
    for x1, x2, t, c in [(X, X+P, '12', ORG), (X+P, X+P+T, '44', RED), (X+P+T, TX, '8', ORG), (MX, MX+T, '44', RED), (MX+T, X+W, '12', ORG)]:
        s.line(x1, dy, x2, dy, c, 1); s.line(x1, dy-4, x1, dy+4, c, 1); s.line(x2, dy-4, x2, dy+4, c, 1)
        s.text((x1+x2)/2, dy+14, t, 10, 700, c, 'middle')
    s.line(X+W+12, Y, X+W+12, Y+P, ORG, 1); s.text(X+W+17, Y+10, '12', 10, 700, ORG)
    s.text(X, dy+32, '빨강 = 기준(꼭 지킴): 누르는 영역 44×44(보라 점선, 눈에 안 보임)', 10, 700, RED); s.text(X+330, dy+32, '주황 = 시작값(바꿔도 됨): 여백 12 · 간격 8 · 체크 22 · 점 24', 10, 700, ORG)
    s.line(X+P+T/2, Y+P, X+P+T/2, 42, MUTE, 1, '2,2'); s.text(X+P+T/2, 38, '중첩 인스턴스: 체크', 10, 600, BLUE, 'middle')
    s.line(MX+T/2, Y+P, MX+T/2, 42, MUTE, 1, '2,2'); s.text(MX+T/2, 38, '중첩 인스턴스: 더보기 버튼', 10, 600, BLUE, 'middle')
    s.text(X+W+20, cy+4, '← 점선: 두 버튼과 제목 첫 줄의', 9.5, 500, '#2563EB')
    s.text(X+W+28, cy+17, '가운데를 한 줄에 맞춘다', 9.5, 500, '#2563EB')
    s.text(X, 208, '확인할 것', 11, 700, INK)
    s.text(X, 225, '· 누르는 영역은 44×44(iOS 기준, Android는 48×48). 보이는 아이콘은 작아도 되고, 버튼 프레임 크기로 영역을 확보한다.', 10.5, 400, SUB)
    s.text(X, 241, '· 제목이 세 줄이 되면 행 높이만 늘고, 두 버튼은 첫 줄 높이에 그대로 있다. 원본을 고치면 6개 행이 모두 바뀐다.', 10.5, 400, SUB)
    PX, PY = 20, 258
    s.rect(PX, PY, 640, 46, BG, LINE, 8)
    s.text(PX+12, PY+19, '오늘 만들 것: 체크 원본 · 더보기 버튼 원본 → 둘을 넣은 할 일 행 원본 1개 → 목록에 인스턴스 6개', 10.5, 700, INK)
    s.text(PX+12, PY+36, '완료 상태로 바꾸기, 제목만 바꾸는 칸 같은 설정은 내일(11/10) 강의에서 배우고 그때 붙인다.', 10, 500, SUB)
    return s

# ───────────────────────── 입력창 5상태
@fig('input_states', '예시 · 입력창 5가지 상태. 오류는 색만이 아니라 아이콘·문구로 원인과 고치는 방법을 알린다')
def input_states():
    s = S(680, 226)
    states = [('기본', '#9CA3AF', 1, '', '', WHITE), ('포커스', BLUE, 2, '', '', WHITE), ('입력됨', '#9CA3AF', 1, '포트폴리오 사례 목차', '', WHITE),
              ('오류', RED, 2, '', '제목을 입력해 주세요.\n한 글자 이상 필요해요.', WHITE), ('비활성', '#E5E7EB', 1, '', '', BG)]
    for i, (name, bc, sw, val, err, bg) in enumerate(states):
        x = 10 + i*134
        s.badge(x, 8, name, INK if name != '오류' else RED, BG if name != '오류' else RED_L)
        s.text(x, 52, '할 일 제목', 11, 600, INK if name != '비활성' else MUTE)
        s.text(x+60, 52, '*필수', 9.5, 600, RED if name != '비활성' else MUTE)
        s.rect(x, 60, 124, 36, bg, bc, 7, sw)
        if val: s.text(x+10, 83, val, 10.5, 500, INK)
        elif name == '포커스': s.line(x+12, 69, x+12, 87, BLUE, 1.5)
        else: s.text(x+10, 83, '예: 레퍼런스 정리', 10.5, 400, '#9CA3AF' if name != '비활성' else '#C4C8CF')
        if err:
            s.circle(x+7, 110, 6, RED, RED); s.text(x+7, 114, '!', 9, 800, WHITE, 'middle')
            for k, ln in enumerate(err.split('\n')):
                s.text(x+17, 114+k*14, ln, 10, 600, RED)
        else:
            s.text(x, 114, '40자 이내', 10, 400, SUB if name != '비활성' else '#C4C8CF')
    s.rect(10, 150, 660, 68, BG, BG, 8)
    s.text(22, 170, '규칙', 11, 700, INK)
    s.text(60, 170, '레이블은 입력창 위에 항상 보이게, 오류 문구는 그 입력창 바로 아래. 오류에서도 이미 입력한 날짜·메모는 지우지 않는다.', 10.5, 400, SUB)
    s.text(60, 206, '실제 크기: 입력창 높이 48 · 레이블 14 · 입력 글자 16 · 안내·오류 문구 13', 10.5, 600, INK)
    s.text(60, 188, '오류 문구가 두 줄이 되면 아래 입력창이 자동으로 내려가야 한다(Auto layout 세로 흐름).', 10.5, 400, SUB)
    return s

# ───────────────────────── 경로 4개
@fig('flow4', '예시 · 일요일 프로토타입의 경로 4개. 상자는 화면, 화살표 위 글자는 그 화면에서 누르는 곳이다. 각 경로를 발표 모드에서 처음부터 끝까지 눌러 본다')
def flow4():
    s = S(680, 430)
    W, H, G = 104, 40, 30
    def row(y, title, nodes, labels, color, note=''):
        s.text(10, y, title, 11.5, 700, INK)
        yb = y + 26
        for k, (t, kind) in enumerate(nodes):
            x = 10 + k*(W+G)
            bg, bc, c = WHITE, LINE, INK
            if kind == 'err': bg, bc, c = RED_L, RED, RED
            if kind == 'ok': bg, bc, c = GREEN_L, GREEN, GREEN
            s.rect(x, yb, W, H, bg, bc, 7, 1.3)
            s.text(x+W/2, yb+H/2+4, t, 11, 700, c, 'middle')
            if k < len(nodes)-1:
                ax = x+W+2
                s.arrow(ax, yb+H/2, ax+G-4, yb+H/2, color, 1.8)
                s.text(ax+(G-4)/2, yb-6, labels[k], 9.5, 600, color, 'middle')
        if note:
            s.text(10+len(nodes)*(W+G)-G+12, yb+H/2+4, note, 10, 500, SUB)
    row(16, '① 빈 제목으로 저장했다가 고쳐서 저장',
        [('목록',''),('추가-빈칸',''),('추가-오류','err'),('추가-입력됨',''),('목록+1','ok')],
        ['추가','저장','입력칸','저장'], BLUE)
    row(116, '② 취소', [('목록',''),('추가-빈칸',''),('목록','')], ['추가','취소'], AMBER, '행 개수 그대로')
    row(216, '③ 완료 체크·해제 (화면 이동 없음)', [('목록',''),('그 행 완료',''),('원래대로','')], ['체크박스','체크박스'], PURPLE)
    row(316, '④ 빈 목록에서 첫 할 일 추가', [('빈 목록',''),('추가-입력됨',''),('목록 1개','ok')], ['추가','저장'], GREEN)
    s.text(340, 418, '상자 = 화면 · 화살표 위 글자 = 그 화면에서 누르는 곳', 10.5, 500, SUB, 'middle')
    return s

# ───────────────────────── 토큰 구조
@fig('tokens', '예시 · 변수 3층 구조. 값은 왼쪽(Primitives)에서만 바꾸고, 컴포넌트는 역할 이름(semantic)만 쓴다')
def tokens():
    s = S(680, 250)
    cols = [('Primitives', '값', 20, ['blue/600 = #2563EB', 'gray/500 = #6B7280', 'red/600 = #DC2626', 'space/16 = 16px', 'radius/8 = 8px']),
            ('Semantic', '역할', 250, ['action/primary', 'text/secondary', 'status/error', 'space/inset-md', 'radius/control']),
            ('컴포넌트', '쓰는 곳', 480, ['버튼 배경', '할 일 행 날짜 글자', '입력창 오류 테두리', '할 일 행 안쪽 여백', '버튼·입력창 모서리'])]
    for (t, sub, x, items) in cols:
        s.text(x, 24, t, 13, 700, INK); s.text(x+tw(t, 13)+8, 24, sub, 10.5, 500, MUTE)
        for i, it in enumerate(items):
            y = 38 + i*38
            bg = [BLUE_L, BG, '#F5F3FF'][[20, 250, 480].index(x)]
            s.rect(x, y, 180, 28, bg, bg, 6)
            if x == 20 and i < 3:
                s.rect(x+8, y+7, 14, 14, ['#2563EB', '#6B7280', '#DC2626'][i], WHITE, 3)
                s.text(x+30, y+18, it, 10.5, 600, INK)
            else:
                s.text(x+10, y+18, it, 10.5, 600, INK)
            if x < 480:
                s.arrow(x+182, y+14, x+228, y+14, MUTE, 1.2)
    s.rect(20, 232-10, 640, 24, AMBER_L, AMBER_L, 6)
    s.text(30, 238, 'blue/600 값 하나를 바꾸면 → action/primary를 쓰는 모든 버튼·링크·체크가 함께 바뀐다. 화면에 색을 직접 입력한 곳은 0개여야 한다.', 10.3, 600, '#92400E')
    return s

# ───────────────────────── 개발 전달
@fig('handoff', '예시 · 개발 전달 명세. 화면에 번호를 달고, 옆에 조건·동작·오류를 문장으로 적는다(무료 플랜용 직접 만든 주석)')
def handoff():
    s = S(680, 345)
    s.phone(20, 10, 190, 310, '할 일 추가')
    x = 32
    s.text(x, 66, '할 일 제목  *필수', 10.5, 600, INK); s.rect(x, 72, 166, 32, WHITE, RED, 6, 1.6)
    s.text(x+4, 118, '제목을 입력해 주세요.', 9.5, 600, RED)
    s.text(x, 144, '날짜', 10.5, 600, INK); s.rect(x, 150, 166, 32, WHITE, '#9CA3AF', 6); s.text(x+10, 171, '11/15 (오늘)', 10, 500, INK)
    s.text(x, 202, '메모', 10.5, 600, INK); s.rect(x, 208, 166, 46, WHITE, '#9CA3AF', 6)
    s.rect(x, 270, 68, 34, WHITE, BLUE, 7); s.text(x+34, 292, '취소', 11, 600, BLUE, 'middle')
    s.rect(x+90, 270, 68, 34, BLUE, BLUE, 7); s.text(x+124, 292, '저장', 11, 600, WHITE, 'middle')
    pins = [(204, 88, 1, BLUE), (204, 118, 2, RED), (204, 166, 3, BLUE), (111, 287, 4, PURPLE), (204, 287, 5, PURPLE)]
    for (px, py, n, c) in pins: s.num(px, py, n, c, 9)
    notes = [(1, BLUE, '조건', '제목 필수, 1~40자. 41자째는 입력되지 않고 안내문이 “40자까지”로 바뀐다.'),
             (2, RED, '오류', '저장을 눌렀는데 제목이 비면 입력창 아래 표시. 포커스를 제목 입력창으로 옮긴다.'),
             (3, BLUE, '조건', '날짜 기본값은 오늘. 과거 날짜 선택 가능(지난 할 일 기록용).'),
             (4, PURPLE, '동작', '취소 → 목록으로. 입력한 내용은 저장하지 않음. 내용이 있으면 “나갈까요?” 확인.'),
             (5, PURPLE, '동작', '저장 → 목록으로 이동, 새 항목을 해당 날짜 맨 위에 넣고 1초간 강조.')]
    for i, (n, c, kind, t) in enumerate(notes):
        y = 14 + i*62
        s.rect(240, y, 420, 54, WHITE, LINE, 7)
        s.num(258, y+18, n, c, 9)
        s.badge(274, y+8, kind, c, {BLUE: BLUE_L, RED: RED_L, PURPLE: PURPLE_L}[c])
        for k, ln in enumerate(wrap(t, 392, 10.3)[:2]):
            s.text(256, y+38+k*13, ln, 10.3, 500, INK)
    s.text(240, 338, '주석 종류: 조건 · 동작 · 오류 · 접근성  — 색으로 구분하고 범례를 페이지 위에 둔다', 9.8, 500, SUB)
    return s

# ───────────────────────── CASE01 범위
@fig('case01_scope', '예시 · 업무 후보 비교표. 관찰할 수 있고 자주 일어나며 막히는 장면이 분명한 업무를 고른다(내용은 예시)')
def case01_scope():
    s = S(680, 200)
    hdr = ['업무 후보', '담당자', '빈도', '쓰는 도구', '막히는 장면(들은 것)', '관찰 가능']
    xs = [10, 160, 245, 300, 400, 610]
    s.rect(10, 10, 660, 30, BG, BG, 6)
    for h, x in zip(hdr, xs): s.text(x+8, 30, h, 10.5, 700, INK)
    rows = [('수업 일정 변경·전달·확인', '직원·강사', '주 3~5회', '학원 도구, 카톡', '전달 대상을 손으로 골라 빠뜨림', '가능', True),
            ('신규 상담 기록', '원장·직원', '주 2회', '노트, 엑셀', '이전 상담 내용 찾기 어려움', '일부', False),
            ('보강 일정 잡기', '직원', '월 4회', '카톡, 달력', '가능한 시간 맞추기 반복', '어려움', False)]
    for i, r in enumerate(rows):
        y = 46 + i*42
        sel = r[6]
        s.rect(10, y, 660, 36, GREEN_L if sel else WHITE, GREEN if sel else LINE, 6, 1.5 if sel else 1)
        for v, x in zip(r[:6], xs):
            s.text(x+8, y+23, v, 10.5, 700 if (sel and x == 10) else 500, INK)
        if sel: s.badge(560, y-8, '선택', WHITE, GREEN)
    s.text(10, 186, '선택 이유를 한 줄로 남긴다: “자주 일어나고(주 3~5회), 실제 처리 장면을 볼 수 있으며, 빠뜨림이라는 결과가 분명하다.”', 10.5, 500, SUB)
    return s

# ───────────────────────── 기록 양식/카드
@fig('note_card', '예시 · 세션 기록 양식과 원문 카드. 본 것·들은 말·내 해석을 다른 칸에 쓴다(내용은 가상 예시)')
def note_card():
    s = S(680, 250)
    hdr = ['시간', '관찰한 행동', '한 말(그대로)', '내 해석', '후속 질문']
    xs = [10, 62, 218, 384, 530]; ws = [52, 156, 166, 146, 140]
    s.rect(10, 10, 660, 28, BG, BG, 6)
    for h, x in zip(hdr, xs): s.text(x+8, 29, h, 10.5, 700, INK)
    rows = [('14:05', ['반 목록에서 학생 이름을', '하나씩 체크함(약 2분)'], ['“이거 매번 다시', '골라야 돼요.”'], ['저장된 그룹이', '없는 듯(확인 필요)'], ['전에 빠뜨린 적이', '있나요?']),
            ('14:08', ['카톡으로 같은 문구를', '두 방에 붙여넣음'], ['“강사님 방이랑', '학부모 방이 달라서요.”'], ['채널이 둘이라', '두 번 보냄'], ['어느 방을 먼저', '보내나요?'])]
    for i, r in enumerate(rows):
        y = 44 + i*58
        s.rect(10, y, 660, 52, WHITE, LINE, 6)
        s.text(18, y+21, r[0], 10.5, 600, SUB)
        for j, cell in enumerate(r[1:]):
            x = xs[j+1]+8
            col = [INK, INK, PURPLE, BLUE][j]
            for k, ln in enumerate(cell): s.text(x, y+21+k*15, ln, 10.3, 500 if j != 1 else 600, col)
    s.text(10, 176, '원문 카드 (한 장에 사실 하나)', 11.5, 700, INK)
    cards = [('P1-07', '반 목록에서 학생을 매번 다시 골라 전달 대상을 만든다.'), ('P1-08', '강사 방과 학부모 방에 같은 문구를 두 번 보낸다.'), ('O1-03', '전달 대상 고르기에 약 2분 걸림(관찰).')]
    for i, (code, t) in enumerate(cards):
        x = 10 + i*222
        s.rect(x, 186, 212, 56, '#FFFBEB', '#F59E0B', 4)
        s.text(x+10, 204, code, 10.5, 800, AMBER)
        for k, ln in enumerate(wrap(t, 192, 10.3)[:2]):
            s.text(x+10, 221+k*14, ln, 10.3, 500, INK)
    return s

# ───────────────────────── 기준선 측정표
@fig('baseline', '예시 · 기준선 측정표. “무엇을 보면 1로 센다”까지 정의해야 12주차에 같은 방식으로 다시 잴 수 있다(숫자는 가상 예시)')
def baseline():
    s = S(680, 240)
    hdr = ['세션', '처리 시간', '단계 수', '도구 전환', '다시 묻기', '실수·수정']
    xs = [10, 100, 210, 310, 420, 530]
    s.rect(10, 10, 660, 28, BG, BG, 6)
    for h, x in zip(hdr, xs): s.text(x+10, 29, h, 10.5, 700, INK)
    rows = [('O1', '11분 20초', '9', '4', '2', '1 (대상 누락)'), ('O2', '8분 05초', '8', '3', '1', '0'), ('기준선', '9분 43초', '8.5', '3.5', '1.5', '0.5')]
    for i, r in enumerate(rows):
        y = 44 + i*34
        last = i == 2
        s.rect(10, y, 660, 28, AMBER_L if last else WHITE, AMBER if last else LINE, 6)
        for v, x in zip(r, xs): s.text(x+10, y+19, v, 10.5, 700 if last else 500, INK)
    s.text(530+10, 44+2*34+19+0, '', 1)
    s.text(10, 166, '정의', 11, 700, INK)
    defs = ['처리 시간: 변경 요청을 받은 순간 ~ 마지막 사람에게 전달 완료까지',
            '도구 전환: 학원 도구 ↔ 카톡 ↔ 엑셀 사이를 오간 횟수   ·   다시 묻기: 같은 정보를 다른 사람에게 다시 확인한 횟수',
            '기준선 옆에는 반드시 측정 횟수를 쓴다(예: “관찰 2회 평균”). 2회로 “평균적으로”라고 일반화하지 않는다.']
    for i, d in enumerate(defs): s.text(10, 186+i*18, '· ' + d, 10.3, 500, SUB)
    return s

# ───────────────────────── 어피니티
@fig('affinity', '예시 · 어피니티 다이어그램. 같은 단어가 아니라 같은 상황·원인끼리 묶고, 묶음마다 근거 수를 적는다')
def affinity():
    s = S(680, 270)
    s.rect(10, 8, 660, 32, INK, INK, 6)
    s.text(22, 29, '초점 질문 · 일정 변경을 모두에게 정확히 알리기까지 무엇이 시간을 잡아먹고 빠뜨림을 만드는가?', 11, 600, WHITE)
    groups = [('전달 대상을 매번 손으로 골라서 빠뜨린다', '카드 9 · 참여자 3', GREEN, ['P1-07', 'P2-03', 'O1-03', 'P3-11']),
              ('채널이 둘이라 같은 내용을 두 번 보낸다', '카드 6 · 참여자 3', GREEN, ['P1-08', 'O2-05', 'P3-02']),
              ('누가 확인했는지 몰라 다시 묻는다', '카드 7 · 참여자 2', GREEN, ['P2-09', 'O1-07', 'O2-02']),
              ('사유 문구를 매번 새로 쓴다', '카드 2 · 1인 근거', AMBER, ['P2-14'])]
    for i, (name, cnt, c, cards) in enumerate(groups):
        x = 10 + i*167
        s.rect(x, 52, 157, 206, WHITE, c, 8, 1.4)
        for k, ln in enumerate(wrap(name, 137, 10.5)[:2]):
            s.text(x+10, 72+k*15, ln, 10.5, 700, INK)
        s.badge(x+10, 96, cnt, c, GREEN_L if c == GREEN else AMBER_L, 9.5)
        for j, cd in enumerate(cards):
            yy = 124 + j*32
            s.rect(x+10, yy, 137, 26, '#FFFBEB', '#F59E0B', 3)
            s.text(x+18, yy+17, cd, 10, 700, AMBER)
            mini_lines(s, x+62, yy+8, 76, 2, '#FCD34D', 8, 3)
    return s

# ───────────────────────── 문제 후보표
@fig('problem_table', '예시 · 문제 후보표. 후보마다 근거·반례·아직 모르는 것을 같은 칸에 적어 비교한다(내용은 예시)')
def problem_table():
    s = S(680, 210)
    hdr = ['문제 후보', '누가·언제', '영향', '근거', '반례', '모르는 것']
    xs = [10, 190, 300, 400, 470, 560]
    s.rect(10, 10, 660, 28, BG, BG, 6)
    for h, x in zip(hdr, xs): s.text(x+8, 29, h, 10.5, 700, INK)
    rows = [(['전달 대상을 손으로 골라', '빠뜨림'], ['직원 · 당일', '변경 시'], ['학부모 미통보', '월 2~3건(말)'], ['P1-07 외', '8장'], ['P3: 반이', '작으면 없음'], ['실제 누락', '빈도'], True),
            (['누가 확인했는지', '몰라 다시 물음'], ['직원·강사', ''], ['확인 전화', '1~2회/건'], ['P2-09 외', '6장'], ['없음', ''], ['확인 기능', '필요성'], False)]
    for i, r in enumerate(rows):
        y = 44 + i*60
        sel = r[6]
        s.rect(10, y, 660, 54, GREEN_L if sel else WHITE, GREEN if sel else LINE, 6, 1.4 if sel else 1)
        for cell, x in zip(r[:6], xs):
            for k, ln in enumerate(cell): s.text(x+8, y+22+k*15, ln, 10.3, 600 if x == 10 else 500, INK)
    s.text(10, 182, '빈도·영향·반복성으로 비교해 하나를 고르고, 고르지 않은 후보와 이유를 남긴다. 숫자가 “말”에서 나온 것인지 “관찰”에서 나온 것인지 구분한다.', 10.3, 500, SUB)
    return s

# ───────────────────────── 스윔레인
@fig('swimlane', '예시 · 현재 흐름(As-is). 담당자별 줄에 단계·도구·막히는 지점(빨간 표시+근거 번호)을 놓는다')
def swimlane():
    s = S(680, 280)
    lanes = ['원장', '직원', '강사', '학부모']
    for i, l in enumerate(lanes):
        y = 10 + i*62
        s.rect(10, y, 660, 58, BG if i % 2 == 0 else WHITE, LINE, 4)
        s.text(22, y+34, l, 11.5, 700, INK)
    def step(x, lane, t, tool, w=96):
        y = 10 + lane*62 + 10
        s.rect(x, y, w, 38, WHITE, '#9CA3AF', 6)
        s.text(x+8, y+16, t, 10.2, 600, INK); s.text(x+8, y+31, tool, 9, 500, MUTE)
        return (x, y, w)
    a = step(70, 0, '변경 결정', '구두')
    b = step(180, 1, '변경 입력', '학원 도구')
    c = step(290, 1, '대상 고르기', '수동 선택')
    d = step(400, 1, '문구 작성·전송', '카톡 2개 방')
    e = step(400, 2, '확인 답장', '카톡')
    f = step(510, 3, '확인(일부)', '카톡')
    g = step(560, 1, '확인 전화', '전화', 100)
    for (p, q) in [(a, b), (b, c), (c, d)]:
        s.arrow(p[0]+p[2], p[1]+19, q[0]-2, q[1]+19, SUB, 1.3)
    s.arrow(d[0]+48, d[1]+38, e[0]+48, e[1]-2, SUB, 1.3)
    s.path(f'M{d[0]+96},{d[1]+28} C470,{f[1]-30} 520,{f[1]-20} {f[0]+20},{f[1]-2}', SUB, 1.3, head=True)
    s.path(f'M{f[0]+70},{f[1]} C{f[0]+70},{g[1]+60} {g[0]+60},{g[1]+60} {g[0]+60},{g[1]+40}', RED, 1.3, head=True, dash='4,3')
    for (x, y, n, t) in [(c[0]+80, c[1]-6, 'P1-07', '빠뜨림'), (d[0]+80, d[1]-6, 'P1-08', '두 번 전송'), (g[0]+84, g[1]-6, 'P2-09', '다시 묻기')]:
        s.circle(x, y, 9, RED, RED); s.text(x, y+4, '!', 10, 800, WHITE, 'middle')
    s.text(10, 270, '빨간 표시 = 막히는 지점(근거: P1-07 대상 빠뜨림 · P1-08 두 번 전송 · P2-09 확인 위해 다시 연락). 점선 = 기다림 뒤 일어나는 일', 9.8, 500, SUB)
    return s

# ───────────────────────── 발산
@fig('diverge', '예시 · 넓게 탐색하고 좁히기. 방향(HMW)마다 흐름 썸네일 4개 → 평가 → 정보 순서가 다른 두 안(A/B)')
def diverge():
    s = S(680, 300)
    hmws = ['HMW ① 대상 고르기를 없앨 수 있을까', 'HMW ② 확인을 자동으로 모을 수 있을까', 'HMW ③ 변경·전달을 한곳에서 끝낼까']
    for r, h in enumerate(hmws):
        y = 10 + r*72
        s.text(10, y+14, h, 10.5, 700, INK)
        for c in range(4):
            x = 10 + c*86
            sel = (r, c) in [(0, 1), (0, 3), (2, 2)]
            s.rect(x, y+22, 78, 44, WHITE, BLUE if sel else '#9CA3AF', 4, 1.8 if sel else 1)
            for k in range(3):
                s.rect(x+6+k*24, y+30, 18, 28, BG, '#D1D5DB', 2)
                if k < 2: s.arrow(x+24+k*24, y+44, x+30+k*24, y+44, MUTE, 0.8)
            s.text(x+5, y+33, f'{"①②③"[r]}-{c+1}', 8.5, 700, BLUE if sel else SUB, halo=True)
    # 평가표
    s.text(370, 24, '평가 (각 1~3점, 높을수록 좋음 · 합계 상위 3안)', 10.5, 700, INK)
    hdr = ['안', '문제 해결', '부담 적음', '반영 가능', '위험 낮음', '합계']
    for j, h in enumerate(hdr): s.text(372 + j*49, 46, h, 9.3, 600, SUB)
    rows = [('①-2', 3, 2, 3, 3, 11, True), ('③-3', 3, 2, 2, 3, 10, True), ('①-4', 2, 3, 2, 2, 9, True), ('②-1', 2, 2, 2, 2, 8, False), ('③-1', 1, 3, 2, 2, 8, False)]
    for i, r in enumerate(rows):
        y = 56 + i*26
        s.rect(366, y, 296, 22, BLUE_L if r[6] else WHITE, BLUE if r[6] else LINE, 4)
        for j, v in enumerate(r[:6]): s.text(374 + j*49, y+16, str(v), 10.3, 700 if j in (0, 5) else 500, INK)
    s.rect(366, 200, 140, 86, BLUE_L, BLUE, 8, 1.5); s.text(380, 222, 'A안 ← ①-2 + ①-4', 11.5, 800, BLUE)
    s.lines(380, 242, ['한 화면에서', '변경 + 대상 + 전달', '(단계 3)'], 10.3, 500, INK, 15)
    s.rect(522, 200, 140, 86, PURPLE_L, PURPLE, 8, 1.5); s.text(536, 222, 'B안 ← ③-3', 11.5, 800, PURPLE)
    s.lines(536, 242, ['변경 → 대상 확인', '→ 전달 (단계 4)', '확인 현황 강조'], 10.3, 500, INK, 15)
    s.text(10, 240, '실질적으로 다른 안 = 정보 순서·단계·', 10.3, 600, INK); s.text(10, 256, '누가 하는지가 다르다. 색만 바꾼 것은 같은 안.', 10.3, 600, INK)
    s.text(10, 280, '탈락한 아이디어 중 아까운 것은 “나중에” 목록에.', 10, 500, SUB)
    return s

# ───────────────────────── 상태표 (CASE01)
@fig('states', '예시 · 일정 변경 한 건의 상태. 상태마다 누가 무엇을 보고 다음에 무엇을 할 수 있는지 정한다')
def states():
    s = S(680, 230)
    nodes = {'작성 중': (20, 70, INK, BG), '전달됨': (180, 70, BLUE, BLUE_L), '일부 확인': (340, 70, AMBER, AMBER_L), '모두 확인': (500, 70, GREEN, GREEN_L),
             '취소됨': (20, 170, GRAY_D, BG), '전달 실패': (180, 170, RED, RED_L)}
    for k, (x, y, c, bg) in nodes.items():
        s.rect(x, y, 140, 44, bg, c, 22, 1.5); s.text(x+70, y+27, k, 11.5, 700, c, 'middle')
    s.arrow(160, 92, 178, 92, SUB, 1.4); s.arrow(320, 92, 338, 92, SUB, 1.4); s.arrow(480, 92, 498, 92, SUB, 1.4)
    s.arrow(90, 114, 90, 168, GRAY_D, 1.3); s.text(72, 146, '취소', 9.8, 600, GRAY_D, 'end')
    s.arrow(196, 114, 150, 168, GRAY_D, 1.3)
    s.arrow(230, 114, 230, 168, RED, 1.4); s.text(236, 146, '일부 실패', 9.5, 600, RED)
    s.arrow(290, 168, 290, 116, RED, 1.4, '4,3'); s.text(296, 146, '다시 보내기', 9.5, 600, RED)
    s.text(20, 30, '상태마다 정할 것', 11, 700, INK)
    s.text(130, 30, '보이는 정보 · 할 수 있는 행동 · 누가(원장/직원/강사/학부모)', 10.5, 500, SUB)
    s.text(20, 48, '예) 일부 확인: 직원은 “확인 안 한 3명”과 다시 알리기 버튼을 본다. 학부모는 확인 버튼만 본다.', 10.3, 500, SUB)
    return s

# ───────────────────────── 테스트 기록
@fig('test_sheet', '예시 · 테스트 계획과 기록 양식. 과업 문장에 버튼 이름을 넣지 않고, 성공 기준을 미리 정한다')
def test_sheet():
    s = S(680, 260)
    s.rect(10, 10, 660, 70, BLUE_L, BLUE_L, 8)
    s.text(22, 32, '과업 1', 11, 800, BLUE)
    s.text(80, 32, '“내일 3시 중등A반 수업이 4시로 바뀌었어요. 담당 강사님과 학부모님께 알려 주세요.”', 11, 600, INK)
    s.text(22, 54, '성공 기준', 10.5, 700, INK); s.text(90, 54, '도움 없이 완료 · 대상 누락 0 · 3분 이내', 10.5, 500, INK)
    s.text(22, 72, '나쁜 예', 10.5, 700, RED); s.text(90, 72, '“변경 버튼을 눌러 전달하세요” (경로를 알려줌)', 10.5, 500, RED)
    hdr = ['시간', '행동(본 것)', '발언(그대로)', '도움', '결과']
    xs = [10, 70, 290, 500, 580]
    s.rect(10, 92, 660, 26, BG, BG, 6)
    for h, x in zip(hdr, xs): s.text(x+8, 110, h, 10.5, 700, INK)
    rows = [('0:12', '반 목록 대신 “공지”를 먼저 누름', '“여기서 하는 건가…”', '없음', '진행'), ('0:48', '대상에서 학부모 탭을 못 찾음', '“학부모는 어디 있지?”', '질문 1', '막힘'), ('1:55', '전달 완료 화면 확인', '“다 보낸 거죠?”', '없음', '성공')]
    for i, r in enumerate(rows):
        y = 124 + i*34
        s.rect(10, y, 660, 28, WHITE, LINE, 6)
        for v, x in zip(r, xs):
            c = RED if v == '막힘' else GREEN if v == '성공' else PURPLE if x == 290 else INK
            s.text(x+8, y+19, v, 10.3, 600 if x in (290, 580) else 500, c)
    s.text(10, 244, '막혔을 때는 “지금 무엇을 찾고 계세요?”만 묻는다. 해석(“탭 이름이 모호한 듯”)은 정리할 때 다른 칸에 쓴다.', 10.3, 500, SUB)
    return s

# ───────────────────────── 심각도
@fig('severity', '예시 · 문제 목록과 심각도(0~4). 빈도·영향·반복성으로 매기고, 3 이상부터 고친다')
def severity():
    s = S(680, 240)
    ox, oy, W, H = 50, 200, 280, 170
    s.line(ox, oy, ox+W, oy, SUB, 1.2); s.line(ox, oy, ox, oy-H, SUB, 1.2)
    s.text(ox+W/2, oy+32, '빈도 (몇 명이 겪었나) →', 10, 600, SUB, 'middle')
    s.add(f'<text x="{ox-30}" y="{oy-H/2}" font-size="10" font-weight="600" fill="{SUB}" font-family="{FONT}" text-anchor="middle" transform="rotate(-90 {ox-30} {oy-H/2})">영향 (막힘 정도) →</text>')
    # (번호, 겪은 사람 수, 영향 0~1, 심각도, 문제, 근거)
    pts = [(1, 3, 0.88, 4, '학부모 탭 못 찾음', 'U1,U2,U4'), (2, 2, 0.68, 3, '완료 확인 모호', 'U2,U3'), (3, 1, 0.52, 2, '사유 입력칸 작음', 'U5'),
           (4, 1, 0.24, 1, '아이콘 의미', 'U1'), (5, 1, 0.12, 1, '정렬 순서', 'U3')]
    cols = {4: RED, 3: AMBER, 2: '#CA8A04', 1: MUTE}
    for p in (1, 2, 3):
        x = ox + p/3.4*W; s.line(x, oy, x, oy+4, SUB, 1); s.text(x, oy+14, f'{p}명', 9, 500, SUB, 'middle')
    for (no, ppl, fy, sev, lab, ev) in pts:
        x = ox + ppl/3.4*W + (12 if no == 5 else 0); y = oy - fy*H
        s.circle(x, y, 11, cols[sev], WHITE, 2); s.text(x, y+4, str(no), 10, 800, WHITE, 'middle')
    s.text(ox+8, oy-H+4, '원 안 숫자 = 표의 문제 번호 · 색 = 심각도', 9.3, 500, SUB)
    hdr = ['#', '문제', '근거', '심각도']
    xs = [360, 384, 540, 610]
    s.rect(356, 14, 314, 26, BG, BG, 6)
    for h, x in zip(hdr, xs): s.text(x, 32, h, 10.3, 700, INK)
    for i, (no, ppl, fy, sev, lab, ev) in enumerate(pts):
        y = 46 + i*30
        s.rect(356, y, 314, 26, WHITE, LINE, 5)
        s.text(362, y+18, str(no), 10, 600, SUB); s.text(384, y+18, lab, 10.3, 600, INK)
        s.text(540, y+18, ev, 9.8, 500, SUB)
        s.badge(612, y+4, str(sev), WHITE, cols[sev], 10)
    s.text(356, 214, '0 문제 아님 · 1 외관 · 2 경미 · 3 중대 · 4 치명적(출시 전 반드시)', 9.8, 500, SUB)
    s.text(356, 230, '(NN/g 심각도 척도)', 9.5, 400, MUTE)
    return s

# ───────────────────────── 사례 페이지
@fig('case_layout', '예시 · 사례 페이지 구조. 섹션마다 “하나만 기억한다면” 한 줄을 정하고, 그 문장을 돕는 그림만 남긴다')
def case_layout():
    s = S(680, 340)
    s.rect(10, 10, 300, 322, WHITE, '#9CA3AF', 10)
    secs = [('1', '한 줄 결과 + 대표 화면', 44, BLUE_L, BLUE), ('2', '문제와 근거(원문 1~2줄)', 30, BG, INK), ('3', '내 역할 · AI·동료 도움 구분', 24, BG, INK),
            ('4', '탐색과 선택(12안→A/B→선택)', 36, BG, INK), ('5', '최종 UI(상태 포함)', 44, BG, INK), ('6', '검증과 수정(전후)', 32, BG, INK),
            ('7', '출시와 결과(측정 횟수)', 30, GREEN_L, GREEN), ('8', '배운 것 · 다시 한다면', 24, BG, INK)]
    y = 20; mids = {}
    for n, t, h, bg, c in secs:
        s.rect(22, y, 276, h, bg, bg, 5)
        s.text(32, y+16, n, 10.5, 800, c); s.text(48, y+16, t, 10.3, 600, INK)
        mids[n] = y + min(h, 30)/2 + 2
        y += h + 6
    notes = [('1', '첫 화면 30초: 누가 무엇 때문에 얼마나 손해 봤고, 무엇을 바꿔 얼마나 나아졌나'),
             ('2', '인터뷰 3·관찰 2와 원문 번호. 문제마다 실제 장면 1개'),
             ('4', '탐색 그림 1장 + 선택 이유 3줄. 포기한 장점도 쓴다'),
             ('6', '수정 전후는 같은 과업·같은 기준으로 비교한다'),
             ('7', '기준선 대비 결과와 한계. 측정하지 않은 전환율·매출은 넣지 않는다')]
    ys = [30, 92, 154, 216, 278]
    for (n, t), ny in zip(notes, ys):
        my = mids[n]
        s.path(f'M298,{my} C318,{my} 316,{ny+16} 334,{ny+16}', MUTE, 1, head=True)
        s.rect(338, ny, 332, 40, WHITE, LINE, 6)
        for k, ln in enumerate(wrap(t, 312, 10)[:2]):
            s.text(348, ny+16+k*14, ln, 10, 500, INK)
    return s

# ───────────────────────── 경쟁 리뷰
@fig('competitive', '예시 · 경쟁 서비스 리뷰 매트릭스. 같은 과업을 직접 해 보며 단계·찾은 위치·막힘을 기록한다(서비스명은 실제로 쓴 앱으로 채운다)')
def competitive():
    s = S(680, 266)
    svcs = ['서비스 A', '서비스 B', '서비스 C', '서비스 D']
    steps = ['앱 열기 → 이어볼 작품 찾기', '회차 확인(어디까지 봤나)', '찜 목록에서 고르기', '재생 시작']
    s.rect(10, 10, 660, 28, BG, BG, 6)
    s.text(18, 29, '과업: 어제 보던 작품 이어보기', 10.5, 700, INK)
    for j, sv in enumerate(svcs): s.text(250 + j*105 + 46, 29, sv, 10.5, 700, INK, 'middle')
    data = [[('홈 첫 줄', 'ok'), ('홈 2번째 줄', 'ok'), ('보관함 안', 'warn'), ('검색 필요', 'bad')],
            [('진행률 막대', 'ok'), ('회차 번호만', 'warn'), ('표시 없음', 'bad'), ('진행률', 'ok')],
            [('정렬 1종', 'warn'), ('필터 3종', 'ok'), ('최근 순', 'ok'), ('없음', 'bad')],
            [('1탭', 'ok'), ('2탭', 'ok'), ('광고 후', 'warn'), ('1탭', 'ok')]]
    cm = {'ok': (GREEN_L, GREEN), 'warn': (AMBER_L, AMBER), 'bad': (RED_L, RED)}
    for i, st in enumerate(steps):
        y = 46 + i*40
        s.rect(10, y, 230, 34, WHITE, LINE, 6); s.text(20, y+22, st, 10.3, 600, INK)
        for j, (v, k) in enumerate(data[i]):
            bg, fg = cm[k]
            s.rect(250 + j*105, y, 95, 34, bg, bg, 6); s.text(250 + j*105 + 47, y+22, v, 10.2, 600, fg, 'middle')
    s.text(10, 222, '색: 초록 = 바로 됨 · 노랑 = 찾는 데 단계가 더 걸림 · 빨강 = 막힘(찾지 못하거나 정보 없음)', 10.3, 600, INK)
    s.text(10, 240, '셀마다 캡처 번호를 붙이고, 막힘(빨강)에는 해당 휴리스틱(예: 상태 가시성, 기억보다 인식)을 적는다.', 10.3, 500, SUB)
    s.text(10, 258, '마지막 줄에 “아무도 잘 풀지 못한 지점”을 적으면 CASE02의 기회가 된다.', 10.3, 600, INK)
    return s

# ───────────────────────── CASE03 상태 다이어그램
@fig('state_diagram', '예시 · CASE03 상태 다이어그램. 상태·전환·트리거를 정하고, 각 전환에 어떤 움직임으로 알릴지 붙인다')
def state_diagram():
    s = S(680, 290)
    s.text(10, 18, '트리거: 사용자(보내기·다시) / 시스템(응답·실패)', 10.3, 600, INK)
    s.text(10, 36, '모든 상태에 “지금 상태 문구 + 다음 행동”이 있어야 한다', 10.3, 500, SUB)
    N = {'대기': (10, 120, INK, BG), '보내는 중': (190, 120, BLUE, BLUE_L), '모두 성공': (420, 56, GREEN, GREEN_L),
         '일부 실패': (420, 186, RED, RED_L), '다시 보내는 중': (420, 250, BLUE, BLUE_L)}
    W = 130
    for k, (x, y, c, bg) in N.items():
        s.rect(x, y, W, 40, bg, c, 20, 1.6); s.text(x+W/2, y+25, k, 11.5, 700, c, 'middle')
    s.arrow(140, 140, 188, 140, SUB, 1.5); s.text(164, 132, '보내기', 9.5, 600, SUB, 'middle', halo=True)
    s.path('M320,132 C370,110 380,80 418,76', SUB, 1.5, head=True); s.text(360, 98, '전부 응답', 9.5, 600, GREEN, 'middle', halo=True)
    s.path('M320,150 C370,170 380,200 418,206', SUB, 1.5, head=True); s.text(362, 196, '일부 실패', 9.5, 600, RED, 'middle', halo=True)
    s.path('M485,226 L485,248', SUB, 1.5, head=True); s.text(492, 242, '다시', 9.5, 600, SUB, halo=True)
    s.path('M552,270 C640,270 640,76 552,76', GREEN, 1.4, head=True, dash='4,3'); s.text(646, 176, '성공', 9.5, 600, GREEN, 'end', halo=True)
    notes = [(10, 196, '보내는 중', '진행 표시가 대상 수만큼 채워짐'), (10, 222, '모두 성공', '체크가 그려짐 150ms'), (10, 248, '일부 실패', '실패한 사람만 남고 접힘 250ms')]
    for (x, y, st, t) in notes:
        lab = f'모션({st}) · {t}'
        w = tw(lab, 9.3) + 14
        s.rect(x, y, w, 20, PURPLE_L, PURPLE_L, 5)
        s.text(x+7, y+14, lab, 9.3, 600, PURPLE)
    return s

# ───────────────────────── 모션 명세
@fig('motion_spec', '예시 · 모션 명세. 전환마다 길이·이징·이유·모션 줄이기 대체를 표로 쓰고, 타임라인으로 겹침을 확인한다(값은 예시)')
def motion_spec():
    s = S(680, 300)
    hdr = ['요소', '속성', '시작', '길이', '이징', '알려주는 것', '줄이기 시']
    xs = [10, 86, 170, 268, 322, 380, 560]
    s.rect(10, 10, 660, 26, BG, BG, 6)
    for h, x in zip(hdr, xs): s.text(x+6, 28, h, 10, 700, INK)
    rows = [('진행 막대', '너비', '보내기 직후', '실제', '선형', '얼마나 보냈나', '숫자만 갱신'),
            ('성공 체크', '선 그리기', '응답 완료', '150ms', '감속', '끝났다', '즉시 표시'),
            ('실패 목록', '높이·투명도', '실패 확인', '250ms', '표준', '누가 남았나', '즉시 표시'),
            ('다시 버튼', '등장', '실패 목록 뒤', '150ms', '감속', '다음 행동', '즉시 표시')]
    for i, r in enumerate(rows):
        y = 40 + i*28
        s.rect(10, y, 660, 24, WHITE, LINE, 4)
        for v, x in zip(r, xs): s.text(x+6, y+16, v, 9.8, 600 if x == 10 else 500, INK)
    # timeline
    ty = 170
    s.text(10, ty, '타임라인 (ms) · 0 = 서버 응답 도착. 결과에 따라 둘 중 하나만 재생된다', 10.5, 700, INK)
    X0, X1 = 90, 600
    for t in range(0, 501, 100):
        x = X0 + (X1-X0)*t/500
        s.line(x, ty+12, x, ty+92, '#E5E7EB', 1); s.text(x, ty+106, str(t), 9, 500, MUTE, 'middle')
    bars = [('성공 체크', 0, 150, GREEN, '모두 성공일 때'), ('실패 목록', 0, 250, RED, '일부 실패일 때'), ('다시 버튼', 250, 400, BLUE, '일부 실패일 때 (목록 뒤)')]
    for i, (lab, a, b, c, when) in enumerate(bars):
        y = ty + 18 + i*24 + (8 if i else 0)
        s.text(10, y+12, lab, 9.8, 600, INK)
        s.rect(X0 + (X1-X0)*a/500, y, (X1-X0)*(b-a)/500, 16, c, c, 4, op=0.85)
        s.text(X0 + (X1-X0)*b/500 + 6, y+12, when, 9.3, 600, c)
    s.line(10, ty+42, X1, ty+42, LINE, 1, '3,3')
    # easing curve
    return s

# ───────────────────────── 사이트 구조
@fig('site', '예시 · 포트폴리오 사이트 구조. 첫 화면에서 대표 사례 3개와 각 한 줄 결과가 바로 보이게 한다')
def site():
    s = S(680, 270)
    s.rect(10, 10, 330, 250, WHITE, '#9CA3AF', 10)
    s.rect(10, 10, 330, 22, BG, BG, 10); s.circle(24, 21, 4, '#F87171', '#F87171'); s.circle(36, 21, 4, '#FBBF24', '#FBBF24'); s.circle(48, 21, 4, '#34D399', '#34D399')
    s.text(26, 58, '이름 · Product Designer', 12.5, 800, INK)
    s.text(26, 76, '실제 업무의 막힘을 근거로 고치고, 움직임으로 상태를 알립니다', 9.8, 500, SUB)
    cards = [('CASE01', '학원 일정 변경 전달 · 출시', '전달 처리 9분 43초 → 5분대 (예시)', GREEN_L, GREEN),
             ('CASE02', '콘텐츠 이어보기·찜', '이어볼 작품 찾기 3단계 → 1단계 (예시)', PURPLE_L, PURPLE),
             ('CASE03', '상태·복구 인터랙션', '실패 상태 이해 1/4명 → 4/4명 (예시)', AMBER_L, AMBER)]
    for i, (k, t, res, bg, c) in enumerate(cards):
        y = 88 + i*50
        s.rect(26, y, 298, 44, bg, bg, 8)
        s.rect(34, y+6, 52, 32, WHITE, WHITE, 5)
        s.text(96, y+19, k, 10, 800, c); s.text(96 + tw(k, 10) + 8, y+19, t, 10.3, 700, INK)
        s.text(96, y+35, '결과 · ' + res, 9.5, 500, SUB)
    s.text(26, 250, '소개 · 연락처 · PDF 다운로드', 9.8, 500, SUB)
    # IA
    s.rect(400, 20, 120, 34, INK, INK, 8); s.text(460, 42, '첫 화면', 11, 700, WHITE, 'middle')
    for i, (t, c) in enumerate([('CASE01', GREEN), ('CASE02', PURPLE), ('CASE03', AMBER)]):
        x = 370 + i*100
        s.rect(x, 100, 90, 32, WHITE, c, 8, 1.4); s.text(x+45, 121, t, 10.5, 700, c, 'middle')
        s.arrow(460, 54, x+45, 98, MUTE, 1)
    s.rect(400, 170, 120, 30, WHITE, LINE, 8); s.text(460, 190, '소개(경력·도구)', 10.3, 600, INK, 'middle')
    s.arrow(460, 54, 460, 168, MUTE, 1, '3,3')
    s.text(370, 226, '· 로그인 잠금·과한 애니메이션·느린 로딩 금지', 10, 500, SUB)
    s.text(370, 244, '· 지원 직무에 따라 사례 순서를 바꿀 수 있게', 10, 500, SUB)
    return s

# ───────────────────────── 과제형 3일
@fig('challenge', '예시 · 과제형 전형 연습 3일. 토스 챌린지 평가 기준(문제 정의·솔루션 설계·시각적 완성도)으로 스스로 채점한다')
def challenge():
    s = S(680, 220)
    days = [('1일차 · 문제', ['주변 2명 10분 인터뷰', '문제 정의 1문장 + 근거', '해결 방향 3개'], BLUE, BLUE_L),
            ('2일차 · 설계', ['핵심 흐름 1개 와이어', '기존 키트로 고해상도', '오류·예외 상태'], PURPLE, PURPLE_L),
            ('3일차 · 제출', ['흐름이 보이는 URL', '3문항: 문제·해결·이유', '자체 평가 + 1명 평가'], GREEN, GREEN_L)]
    for i, (t, items, c, bg) in enumerate(days):
        x = 10 + i*224
        s.rect(x, 10, 212, 136, bg, c, 10, 1.4)
        s.text(x+14, 34, t, 12.5, 800, c)
        for k, it in enumerate(items):
            s.circle(x+18, 58+k*26, 3, c, c); s.text(x+28, 62+k*26, it, 10.5, 600, INK)
        if i < 2: s.arrow(x+212, 78, x+222, 78, c, 1.6)
    s.text(10, 172, '채점', 11, 700, INK)
    crit = [('문제 정의', '주어진 단서로 핵심 문제를 정의했나'), ('솔루션 설계', '문제와 해결이 화면에 분명히 드러나나'), ('시각적 완성도', '익숙한 패턴을 맥락에 맞게 다듬었나')]
    for i, (k, t) in enumerate(crit):
        x = 50 + i*210
        s.badge(x, 158, k, INK, BG, 10)
        s.text(x, 196, t, 9.8, 500, SUB)
    return s

# ───────────────────────── 11/10 컴포넌트 속성 3종
def _plus(s, cx, cy, c=WHITE, k=6):
    s.line(cx-k, cy, cx+k, cy, c, 2); s.line(cx, cy-k, cx, cy+k, c, 2)
def _trash(s, cx, cy, c=WHITE):
    s.line(cx-6, cy-5, cx+6, cy-5, c, 1.8); s.rect(cx-4.5, cy-3, 9, 9, 'none', c, 1.5, 1.6); s.line(cx-2, cy-8, cx+2, cy-8, c, 1.8)
def _btn(s, x, y, w, label, icon='plus', fill=BLUE, fg=WHITE, stroke=None):
    s.rect(x, y, w, 48, fill, stroke or fill, 10)
    tx = x + w/2
    if icon:
        (_plus if icon == 'plus' else _trash)(s, x+22, y+24, fg); tx = x + 40 + (w-40)/2 - 6
    s.text(tx, y+29.5, label, 15, 700, fg, 'middle')

@fig('props3', '예시 · 버튼 원본 1개에 속성 3개를 붙이면, 인스턴스마다 오른쪽 패널에서 글자·아이콘 켜고 끄기·아이콘 종류만 골라 쓴다')
def props3():
    s = S(680, 330)
    s.text(20, 18, '① 원본(컴포넌트) 1개', 12.5, 700, INK)
    s.rect(20, 30, 180, 80, 'none', PURPLE, 8, 1.2, '4,3')
    _btn(s, 36, 46, 148, '저장')
    s.text(20, 128, '보라 점선 = 원본. 여기서 속성을 만든다.', 10, 500, SUB)
    # 패널
    s.text(240, 18, '② 인스턴스를 고르면 오른쪽 패널에 생기는 칸', 12.5, 700, INK)
    PX, PY = 240, 30
    s.rect(PX, PY, 420, 120, BG, LINE, 8)
    rows = [('Label', '텍스트 속성', '글자만 바꾼다'), ('Show icon', '불리언 속성', '켜기/끄기 스위치'), ('Icon', '인스턴스 교체 속성', '아이콘을 다른 것으로')]
    for i, (n, kind, say) in enumerate(rows):
        y = PY + 14 + i*36
        s.text(PX+14, y+15, n, 11.5, 700, INK)
        if i == 0:
            s.rect(PX+96, y, 90, 24, WHITE, LINE, 5); s.text(PX+106, y+16, '저장', 11, 500, INK)
        elif i == 1:
            s.rect(PX+96, y+3, 36, 18, BLUE, BLUE, 9); s.circle(PX+123, y+12, 7, WHITE, WHITE)
            s.text(PX+140, y+16, '켬', 10.5, 600, SUB)
        else:
            s.rect(PX+96, y, 90, 24, WHITE, LINE, 5); s.text(PX+106, y+16, '더하기', 11, 500, INK); s.text(PX+176, y+16, '▾', 10, 500, SUB, 'end')
        s.badge(PX+200, y+3, kind, PURPLE, PURPLE_L, 10)
        s.text(PX+408, y+16, say, 10.5, 500, SUB, 'end')
    # 결과
    s.text(20, 182, '③ 같은 원본에서 나온 인스턴스 3개 (원본은 그대로)', 12.5, 700, INK)
    xs = [20, 240, 460]
    data = [('저장', 'plus', 'Label 저장 · Show icon 켬 · Icon 더하기'),
            ('다음', None, 'Label 다음 · Show icon 끔'),
            ('삭제', 'trash', 'Label 삭제 · Show icon 켬 · Icon 휴지통')]
    for x, (lb, ic, cap) in zip(xs, data):
        _btn(s, x, 196, 180, lb, ic, RED if lb == '삭제' else BLUE)
        s.text(x, 262, cap, 10, 500, SUB)
    s.rect(20, 280, 640, 42, BG, LINE, 8)
    s.text(32, 297, '빨간 삭제 버튼처럼 색까지 다르면 속성이 아니라 Variants(내일 08:30 블록)로 만든다.', 10.5, 700, INK)
    s.text(32, 314, '버튼 크기: 높이 48 · 글자 16 · 아이콘 24 안쪽 — 그림의 모양·문구는 예시라 그대로 따라 할 필요 없다.', 10, 500, SUB)
    return s

# ───────────────────────── 11/10 Variants 세트
@fig('variants4', '예시 · Variants 세트(보라 점선 틀). 속성 2개(Type, State)를 곱해 버전 4개를 만들고, 인스턴스에서는 고르기만 한다')
def variants4():
    s = S(680, 310)
    X, Y = 110, 50
    s.rect(X, Y, 420, 160, 'none', PURPLE, 10, 1.4, '5,4')
    s.badge(X, 4, '버튼 (컴포넌트 세트)', PURPLE, PURPLE_L, 10.5)
    s.text(X+120, Y-12, 'State = Default', 10.5, 700, INK, 'middle'); s.text(X+320, Y-12, 'State = Disabled', 10.5, 700, INK, 'middle')
    s.text(X-10, Y+52, 'Type =', 10.5, 700, INK, 'end'); s.text(X-10, Y+66, 'Primary', 10.5, 700, INK, 'end')
    s.text(X-10, Y+122, 'Type =', 10.5, 700, INK, 'end'); s.text(X-10, Y+136, 'Secondary', 10.5, 700, INK, 'end')
    _btn(s, X+30, Y+30, 180, '저장', None)
    _btn(s, X+230, Y+30, 180, '저장', None, '#E5E7EB', '#6B7280')
    _btn(s, X+30, Y+100, 180, '취소', None, WHITE, BLUE, BLUE)
    _btn(s, X+230, Y+100, 180, '취소', None, WHITE, '#9CA3AF', '#E5E7EB')
    # 인스턴스 패널
    s.text(560, 62, '인스턴스 패널', 11, 700, INK)
    for i, (k, v) in enumerate([('Type', 'Primary'), ('State', 'Disabled')]):
        y = 72 + i*34
        s.text(560, y+16, k, 10.5, 600, SUB); s.rect(600, y, 74, 24, WHITE, LINE, 5); s.text(606, y+16, v, 10, 500, INK)
    s.rect(X+224, Y+24, 192, 60, 'none', PURPLE, 12, 2.2)
    s.text(560, 160, '이렇게 고르면 왼쪽에서', 10, 600, PURPLE); s.text(560, 174, '굵은 보라 테두리 버전이', 10, 600, PURPLE); s.text(560, 188, '화면에 나온다.', 10, 600, PURPLE)
    s.rect(20, 230, 640, 72, BG, LINE, 8)
    s.text(32, 250, '속성과 Variants 나누기(오늘 메모할 한 줄의 예)', 11, 700, INK)
    s.text(32, 268, '· 글자·아이콘만 바뀐다 → 속성(텍스트·불리언·교체).  · 색·테두리·모양 자체가 바뀐다 → Variants.', 10.5, 500, SUB)
    s.text(32, 286, '· 비활성도 높이 48은 그대로. 비활성 글자는 대비 기준 예외지만, 왜 못 누르는지 안내문으로 알린다.', 10.5, 500, SUB)
    return s

# ───────────────────────── 11/10 ‘하루’ 체크·행 상태
def _check(s, x, y, done):
    if done:
        s.rect(x, y, 22, 22, BLUE, BLUE, 5); s.path(f'M{x+5},{y+11.5} L{x+9.5},{y+16} L{x+17},{y+7}', WHITE, 2.2)
    else:
        s.rect(x, y, 22, 22, WHITE, '#6B7280', 5, 1.5)

@fig('haru_states', '예시 · ‘하루’ 체크·할 일 행 상태. 패널에서 State만 바꾸면 체크·글자색·취소선이 함께 바뀌고 제목은 그대로 남는다')
def haru_states():
    s = S(680, 352)
    s.text(20, 18, '체크 Variants', 12, 700, INK)
    s.rect(20, 28, 150, 70, 'none', PURPLE, 8, 1.2, '4,3')
    for i, (d, n) in enumerate([(False, '미완료'), (True, '완료')]):
        x = 36 + i*70
        s.rect(x, 36, 44, 44, 'none', '#A78BFA', 6, 1, '3,2'); _check(s, x+11, 47, d)
        s.text(x+22, 92, n, 10, 600, SUB, 'middle')
    s.text(200, 18, '할 일 행 Variants (State)', 12, 700, INK)
    s.rect(200, 28, 460, 150, 'none', PURPLE, 8, 1.2, '4,3')
    for i, (d, st) in enumerate([(False, 'State = 기본'), (True, 'State = 완료')]):
        y = 40 + i*68
        s.text(212, y+10, st, 10, 700, PURPLE)
        s.rect(212, y+16, 436, 44, WHITE, LINE, 8)
        _check(s, 223, y+27, d)
        c = '#6B7280' if d else INK
        s.text(256, y+37, '레퍼런스 캡처 3장 모으기', 13, 600, c)
        if d: s.line(256, y+32, 256+tw('레퍼런스 캡처 3장 모으기', 13)*0.84, y+32, c, 1.3)
        s.text(256, y+53, '11/14 · 09:00', 10, 400, SUB)
        s.text(640, y+43, '⋯', 18, 700, '#4B5563', 'end')
    # 규칙표
    s.text(20, 204, '상태별 표시 규칙 표 (오늘 결과물 예)', 12, 700, INK)
    cols = [20, 140, 300, 500, 660]
    hd = ['상태', '체크', '제목 글자색', '취소선']
    rows = [['기본', '빈 칸(테두리 회색)', '#111827 (진한 검정)', '없음'], ['완료', '파랑 채움 + 흰 체크', '#6B7280 (흰 배경 대비 4.8:1)', '있음']]
    s.rect(20, 214, 640, 28, BG, LINE, 0)
    for j, h in enumerate(hd): s.text(cols[j]+10, 233, h, 10.5, 700, INK)
    for i, r in enumerate(rows):
        y = 242 + i*28; s.rect(20, y, 640, 28, WHITE, LINE, 0)
        for j, v in enumerate(r): s.text(cols[j]+10, y+19, v, 10.5, 500, INK)
    s.text(20, 322, '완료 글자를 #9CA3AF(연회색)로 하면 대비 2.5:1이라 기준(4.5:1) 미달 → 더 진한 회색을 쓴다.', 10.5, 600, RED)
    s.text(20, 340, '체크·더보기 누르는 영역 44×44, 제목 16/24, 날짜 13 — 월요일 행 원본 그대로.', 10, 500, SUB)
    return s

# ═════════════════════════ 추가 예시 그림 (전체 점검 후)
def _cap(s, x, y, t, c=SUB, size=10, w=500): return s.text(x, y, t, size, w, c)
def _box(s, x, y, w, h, title=None, fill=WHITE, stroke=LINE, r=8):
    s.rect(x, y, w, h, fill, stroke, r)
    if title: s.text(x+10, y+18, title, 11, 700, INK)

@fig('slot_vs_swap', '예시 · 인스턴스 교체와 슬롯의 차이. 교체는 정해진 자리 하나의 부품만 바꾸고, 슬롯은 빈 자리에 원하는 것을 여러 개 넣는다')
def slot_vs_swap():
    s = S(680, 270)
    for col, (title, sub) in enumerate([('인스턴스 교체', '자리 1개 · 부품만 바꿈'), ('슬롯', '빈 자리 · 아무거나 여러 개')]):
        X = 20 + col*340
        s.text(X, 18, title, 13, 700, PURPLE); s.text(X+tw(title,13)*0.86+10, 18, sub, 10.5, 500, SUB)
        for i in range(2):
            y = 32 + i*104
            s.rect(X, y, 300, 92, WHITE, LINE, 10)
            s.text(X+14, y+24, '카드 제목', 12, 700, INK); s.text(X+14, y+41, '설명 한 줄', 10.5, 400, SUB)
            if col == 0:
                s.rect(X+246, y+12, 40, 40, 'none', PURPLE, 6, 1.2, '3,2')
                s.text(X+266, y+39, '♥' if i == 0 else '★', 20, 700, RED if i == 0 else AMBER, 'middle')
                s.text(X+14, y+76, 'Icon = 하트' if i == 0 else 'Icon = 별', 10, 600, PURPLE)
            else:
                s.rect(X+12, y+50, 276, 34, 'none', PURPLE, 6, 1.2, '3,2')
                if i == 0:
                    s.rect(X+18, y+55, 120, 24, BLUE, BLUE, 6); s.text(X+78, y+71, '확인', 10.5, 700, WHITE, 'middle')
                    s.rect(X+144, y+55, 120, 24, WHITE, BLUE, 6); s.text(X+204, y+71, '취소', 10.5, 700, BLUE, 'middle')
                else:
                    s.rect(X+18, y+55, 70, 24, BG, LINE, 4); s.text(X+53, y+71, '이미지', 9.5, 500, SUB, 'middle')
                    s.text(X+96, y+71, '안내 문구 + 이미지', 10, 500, INK)
    s.rect(20, 244-6, 640, 30, BG, LINE, 8)
    s.text(32, 257, '보라 점선 = 인스턴스에서 바꿀 수 있는 자리. 메모할 한 줄 예: “아이콘 하나만 바꾸면 교체, 안에 넣을 것이 매번 다르면 슬롯.”', 10, 600, INK)
    return s

@fig('interactive', '예시 · 상호작용 컴포넌트. Variants 2개를 서로 ‘On click → Change to’로 연결하면, 화면마다 따로 연결하지 않아도 눌렀을 때 바뀐다')
def interactive():
    s = S(680, 250)
    s.rect(20, 20, 300, 120, 'none', PURPLE, 10, 1.4, '5,4'); s.badge(20, 0, '체크 (컴포넌트 세트)', PURPLE, PURPLE_L, 10)
    for i, (d, n) in enumerate([(False, 'Unchecked'), (True, 'Checked')]):
        x = 50 + i*160
        s.rect(x, 50, 60, 60, WHITE, LINE, 8)
        if d: s.rect(x+19, 69, 22, 22, BLUE, BLUE, 5); s.path(f'M{x+24},{80.5} L{x+28.5},{85} L{x+36},{76}', WHITE, 2.2)
        else: s.rect(x+19, 69, 22, 22, WHITE, '#6B7280', 5, 1.5)
        s.text(x+30, 128, n, 10, 600, SUB, 'middle')
    s.path('M112,62 C150,40 170,40 208,62', BLUE, 1.6, head=True); s.text(160, 44, 'On click', 9.5, 700, BLUE, 'middle')
    s.path('M208,100 C170,122 150,122 112,100', BLUE, 1.6, head=True); s.text(160, 132, 'On click', 9.5, 700, BLUE, 'middle')
    # 패널
    PX = 350
    s.text(PX, 18, 'Prototype 탭 (Unchecked를 고른 상태)', 11, 700, INK)
    s.rect(PX, 28, 310, 112, BG, LINE, 8)
    for i, (k, v) in enumerate([('Interaction', 'On click'), ('Action', 'Change to'), ('Destination', 'Checked')]):
        y = 40 + i*32
        s.text(PX+14, y+16, k, 10.5, 600, SUB); s.rect(PX+120, y, 176, 24, WHITE, LINE, 5); s.text(PX+130, y+16, v, 10.5, 600, INK)
    s.rect(20, 160, 640, 82, BG, LINE, 8)
    s.text(32, 180, '확인 순서', 11, 700, INK)
    s.text(32, 198, '① 세트 안 Unchecked → Checked, Checked → Unchecked 두 개를 연결한다 (Prototype 탭).', 10.5, 500, SUB)
    s.text(32, 216, '② 인스턴스 5개를 한 프레임에 놓고 발표 모드(▶)에서 하나씩 누른다.', 10.5, 500, SUB)
    s.text(32, 234, '③ 누른 것 하나만 바뀌면 성공. 안 바뀌면 연결을 세트 안 Variants가 아닌 화면 프레임에 걸었는지 확인한다.', 10.5, 500, SUB)
    return s

@fig('comp_page', '예시 · 정리된 ‘컴포넌트’ 페이지. 부품마다 이름·사용 설명 한 줄·세트를 한 칸에 모으고, 속성 순서를 통일한다')
def comp_page():
    s = S(680, 300)
    s.rect(20, 10, 640, 200, '#FAFAFA', LINE, 10)
    s.text(36, 34, '컴포넌트', 14, 800, INK)
    items = [('Button', '화면의 주요 행동. 한 화면에 Primary는 1개.', 'Type · State · Label · Show icon'),
             ('Checkbox', '할 일 완료 표시. 누르는 영역 44×44.', 'State'),
             ('Input', '글자 입력. 레이블은 항상 위에 보인다.', 'State · Label · Help text · Show help'),
             ('TodoRow', '목록의 할 일 한 줄. 제목은 세 줄까지.', 'State · Title')]
    for i, (n, d, p) in enumerate(items):
        x = 36 + (i % 2)*312; y = 48 + (i//2)*78
        s.rect(x, y, 296, 70, WHITE, LINE, 8)
        s.text(x+12, y+20, n, 12, 700, INK); s.text(x+12, y+38, d, 10, 500, SUB)
        s.text(x+12, y+58, '속성: ' + p, 9.5, 600, PURPLE)
    s.text(20, 232, '이름 규칙 예', 11, 700, INK)
    s.text(20, 250, '· 원본 이름은 영어 한 단어(Button, Input) · 속성 이름도 같은 말로(State, Label) · 값은 Default/Disabled처럼 통일', 10.5, 500, SUB)
    s.text(20, 268, '· 속성 순서: 모양을 바꾸는 것(Type, State) → 글자(Label) → 켜고 끄기(Show …) → 교체(Icon)', 10.5, 500, SUB)
    s.text(20, 286, '· 안 쓰는 Variants·이름 없는 레이어(Frame 12 등)는 지운다. 영어 대신 한국어로 통일해도 된다 — 섞지만 않으면 된다.', 10.5, 500, SUB)
    return s

@fig('measure', '예시 · 재는 방법. 캡처 위에 여백·행 높이·글자 크기를 빨간 선으로 재고 옆에 표로 적는다(그림 속 화면과 숫자는 예시다. 실제로는 09:00에 고른 내 레퍼런스를 잰다)')
def measure():
    s = S(680, 330)
    s.phone(20, 10, 200, 310, '오늘 할 일')
    for i in range(4):
        y = 52 + i*62
        s.circle(46, y+20, 9, WHITE, '#6B7280', 1.4)
        s.rect(64, y+10, 110, 8, '#374151', '#374151', 3); s.rect(64, y+26, 70, 6, '#9CA3AF', '#9CA3AF', 3)
        s.line(30, y+48, 210, y+48, '#E5E7EB')
    R = RED
    s.line(20, 76, 36, 76, R, 1.2); s.text(28, 70, '16', 9, 700, R, 'middle')
    s.line(214, 52, 214, 114, R, 1.2); s.line(209, 52, 219, 52, R); s.line(209, 114, 219, 114, R); s.text(222, 87, '62', 9, 700, R)
    s.rect(62, 60, 114, 12, 'none', R, 0, 1); s.text(180, 70, '17', 9, 700, R)
    s.rect(62, 77, 74, 10, 'none', R, 0, 1); s.text(140, 86, '13', 9, 700, R)
    # 표
    TX = 260
    s.text(TX, 22, '치수 표 (재서 적은 값)', 12, 700, INK)
    rows = [('항목', '값', '메모'), ('좌우 여백', '16', '모든 행 같음'), ('행 높이', '62', '두 줄 제목이면 늘어남'), ('제목', '17 / 22 · Semibold', '가장 진함'),
            ('보조 글자', '13 / 18 · Regular', '회색'), ('구분선', '1 · #E5E7EB', '행 사이에만'), ('색 개수', '글자 2 · 강조 1 · 선 1', '강조색은 체크에만')]
    for i, r in enumerate(rows):
        y = 32 + i*30
        s.rect(TX, y, 400, 30, BG if i == 0 else WHITE, LINE, 0)
        for j, (v, cx) in enumerate(zip(r, [10, 110, 250])):
            s.text(TX+cx, y+20, v, 10.5, 700 if i == 0 else 500, INK)
    s.text(TX, 262, '재는 법: 요소 선택 → Alt(Option) 누른 채 다른 요소에 마우스 → 거리 숫자가 나온다.', 10, 600, INK)
    s.text(TX, 280, '글자 크기는 캡처를 실제 화면 폭(예: 390)에 맞춘 뒤 글자 높이로 어림한다.', 10, 500, SUB)
    s.text(TX, 298, '정확한 값보다 “제목과 보조 글자의 차이”, “여백이 모두 같은가”를 보는 게 목적이다.', 10, 500, SUB)
    return s

@fig('type_scale', '예시 · 텍스트 스타일 표. 이름·크기/줄 간격·굵기·쓰는 곳을 한 줄씩 정하고, 모든 글자에 이 중 하나를 적용한다')
def type_scale():
    rows = [('제목(대)', 24, 32, 700, '화면 맨 위 제목'), ('제목', 20, 28, 700, '구역 제목'), ('본문', 16, 24, 400, '할 일 제목, 설명'),
            ('본문(강조)', 16, 24, 600, '강조할 본문'), ('보조', 13, 18, 400, '날짜·안내문'), ('버튼', 16, 24, 600, '버튼 글자')]
    s = S(680, 60 + sum(r[2] + 10 for r in rows) + 40)
    s.text(20, 18, '스타일 이름', 10.5, 700, SUB); s.text(140, 18, '크기 / 줄 간격 · 굵기', 10.5, 700, SUB); s.text(300, 18, '보기', 10.5, 700, SUB); s.text(560, 18, '쓰는 곳', 10.5, 700, SUB)
    y = 30
    for n, sz, lh, w, use in rows:
        s.line(20, y, 660, y, LINE)
        s.text(20, y + lh/2 + 9, n, 11.5, 700, INK)
        s.text(140, y + lh/2 + 9, f'{sz} / {lh} · ' + {400: 'Regular', 600: 'Semibold', 700: 'Bold'}[w], 11, 500, INK)
        s.rect(300, y+5, 240, lh, BLUE_L, BLUE_L, 2, op=0.6)
        s.text(304, y + 5 + lh/2 + sz*0.36, '레퍼런스 정리하기', sz, w, INK)
        s.text(560, y + lh/2 + 9, use, 10.5, 500, SUB)
        y += lh + 10
    s.line(20, y, 660, y, LINE)
    s.text(20, y+20, '파란 칸 높이 = 줄 간격. Figma: 텍스트 선택 → 오른쪽 Typography → 스타일(네 점 아이콘) → + 로 등록.', 10, 600, INK)
    s.text(20, y+36, '이 숫자는 시작값이다. 화면 글자는 12보다 작게 쓰지 않는다.', 10, 500, SUB)
    return s

@fig('foundations_page', '예시 · ‘기초’ 문서 페이지 배치. 원칙·색·글자·간격·모서리를 위에서 아래로 놓고, 항목마다 실제 화면 조각을 붙인다')
def foundations_page():
    s = S(680, 420)
    s.rect(20, 6, 640, 408, '#FAFAFA', LINE, 10)
    s.text(36, 32, '‘하루’ 기초', 15, 800, INK)
    y = 48
    s.text(36, y+14, '원칙', 11.5, 700, INK)
    for i, t in enumerate(['장식보다 남은 할 일', '빠른 입력보다 실수 방지', '새 기능보다 같은 규칙']):
        s.rect(100 + i*180, y, 170, 36, WHITE, LINE, 6); s.text(110 + i*180, y+22, t, 10, 600, INK)
    y = 100
    s.text(36, y+14, '색', 11.5, 700, INK)
    for i, (n, c) in enumerate([('text/primary', '#111827'), ('text/secondary', '#6B7280'), ('action/primary', BLUE), ('status/error', RED), ('bg/subtle', BG)]):
        x = 100 + i*104
        s.rect(x, y, 30, 30, c, LINE, 6); s.text(x+36, y+13, n, 8.5, 600, INK); s.text(x+36, y+26, c, 8.5, 400, SUB)
    s.text(100, y+48, '각 색 옆에 쓰는 곳(예: 오류 문구, 체크 완료)과 대비 비율을 적는다.', 9.5, 500, SUB)
    y = 166
    s.text(36, y+14, '글자', 11.5, 700, INK)
    for i, (n, sz, w) in enumerate([('제목(대) 24/32', 20, 700), ('본문 16/24', 14, 400), ('보조 13/18', 11, 400)]):
        s.text(100, y+16 + i*24, '오늘 할 일', sz, w, INK); s.text(240, y+16 + i*24, n, 10, 500, SUB)
    y = 248
    s.text(36, y+14, '간격', 11.5, 700, INK)
    xx = 100
    for v in [4, 8, 12, 16, 24, 32]:
        s.rect(xx, y+2, v*1.6, 14, BLUE_L, BLUE, 2); s.text(xx, y+32, str(v), 9.5, 600, INK); xx += v*1.6 + 24
    s.text(100, y+50, '어디에 쓰는지 한 줄씩: 8 = 체크와 제목 사이, 12 = 행 안쪽 여백, 16 = 화면 좌우 여백 …', 9.5, 500, SUB)
    y = 320
    s.text(36, y+14, '모서리', 11.5, 700, INK)
    for i, r in enumerate([4, 8, 12, 999]):
        s.rect(100 + i*80, y, 50, 30, WHITE, INK, min(r, 15), 1.2); s.text(125 + i*80, y+44, str(r), 9.5, 600, INK, 'middle')
    s.rect(470, 300, 170, 100, WHITE, LINE, 8); s.text(480, 318, '실제 화면 조각', 10, 700, INK)
    s.rect(480, 328, 150, 30, WHITE, LINE, 6); s.rect(488, 335, 16, 16, WHITE, '#6B7280', 4); s.rect(512, 338, 80, 7, '#374151', '#374151', 3)
    s.text(480, 380, '규칙이 쓰인 곳을 캡처해 붙임', 9.5, 500, SUB)
    return s

@fig('breakpoints', '예시 · 오늘 다룰 세 너비. 390은 이미 있는 ‘목록’ 화면(새로 만들지 않음), 768은 08:30 이 블록에서 목록(280~360)+상세(남는 공간)로 만들고, 1280은 10:10 블록에서 가운데 960 안에 같은 2단을 놓는다')
def breakpoints():
    s = S(680, 300)
    def list_col(x, y, w, n=4):
        for i in range(n):
            s.rect(x, y + i*30, w, 26, WHITE, LINE, 4); s.rect(x+6, y+8 + i*30, 10, 10, WHITE, '#6B7280', 2); s.rect(x+22, y+10 + i*30, min(70, w-30), 6, '#374151', '#374151', 2)
    # 390
    s.text(20, 16, '390 · 이미 있음', 10, 700, INK)
    s.rect(20, 24, 110, 200, WHITE, '#9CA3AF', 10); list_col(28, 36, 94, 5)
    # 768
    s.text(150, 16, '768 · 08:30 지금 만듦', 10, 700, INK)
    s.rect(150, 24, 220, 200, WHITE, '#9CA3AF', 8); list_col(156, 36, 84, 5)
    s.rect(246, 32, 118, 184, BG, LINE, 6); s.text(254, 50, '상세', 10, 700, INK); s.rect(254, 58, 90, 6, '#374151', '#374151', 2); s.rect(254, 70, 70, 5, '#9CA3AF', '#9CA3AF', 2)
    s.text(198, 238, '목록 최소 280', 9, 600, ORG if False else '#B45309', 'middle'); s.text(305, 238, '상세 = Fill', 9, 600, '#B45309', 'middle')
    # 1280
    s.text(390, 16, '1280 · 10:10 블록에서 만듦', 10, 700, INK)
    s.rect(390, 24, 270, 200, WHITE, '#9CA3AF', 8)
    s.rect(410, 30, 230, 188, 'none', RED, 4, 1, '4,3')
    list_col(416, 40, 84, 5); s.rect(506, 38, 128, 174, BG, LINE, 6); s.text(514, 56, '상세', 10, 700, INK)
    s.text(525, 238, '가운데 최대 폭 960 (빨간 점선)', 9, 600, RED, 'middle')
    s.rect(20, 252, 640, 42, BG, LINE, 8)
    s.text(32, 269, '너비별 규칙 표에 적을 것: 요소 / 390 / 768 / 1280. 예) 상세: 새 화면으로 이동 / 오른쪽에 표시 / 오른쪽에 표시', 10, 600, INK)
    s.text(32, 286, '모양은 예시다. 목록·상세의 최소·최대 폭을 정해 두면 너비만 바꿔도 손으로 위치를 다시 맞출 필요가 없다.', 10, 500, SUB)
    return s

@fig('usage_rule', '예시 · 11/23 08:20에 만드는 button 규칙 카드(전부 이 블록 것). 버튼 모양은 11/19에 만든 button Instance, 빨간 테두리는 11/22 status/error 변수. 오른쪽 글씨는 레이어 이름 안내')
def usage_rule():
    s = S(680, 560)
    G = '#3F7A31'
    s.rect(20, 10, 400, 540, WHITE, LINE, 10)
    s.text(44, 42, 'button 규칙', 15, 800, INK)
    rows = [('언제 쓰나', '화면의 행동(저장 · 추가 · 삭제). primary는 한 화면에 1개'),
            ('쓰지 않을 때', '다른 화면으로 이동만 할 때(→ 목록 행 · ←)'),
            ('상태', 'default · hover · pressed · disabled(필수 칸이 빔)'),
            ('문구', '하는 일 그대로 동사(저장 · 삭제). ‘확인’만 쓰지 않는다')]
    for i, (k, v) in enumerate(rows):
        y = 62 + i*26
        s.text(44, y+14, k, 10.5, 700, INK); s.text(140, y+14, v, 10, 500, SUB)
    s.rect(36, 58, 368, 108, 'none', BLUE, 4, 1, '4,3')
    for j, (ok, lab, a1, a2, note) in enumerate([(True, '○ 맞는 예', '취소', '저장', 'primary는 하나'),
                                                  (False, '✕ 틀린 예', '확인', '저장', 'primary가 둘이라 무엇을 누를지 모름')]):
        Y = 182 + j*176
        s.rect(44, Y, 352, 164, BG, RED if not ok else LINE, 8, 2 if not ok else 1)
        s.text(60, Y+22, lab, 11, 700, GREEN if ok else RED)
        if ok: _btn(s, 60, Y+32, 110, a1, None, WHITE, INK, LINE)
        else:  _btn(s, 60, Y+32, 110, a1, None, G)
        _btn(s, 60, Y+86, 110, a2, None, G)
        s.text(60, Y+152, note, 10, 600, SUB)
    s.rect(36, 174, 368, 356, 'none', BLUE, 4, 1, '4,3')
    for y, t in [(46, '← 제목 글자 (heading/medium)'), (112, '← 규칙-표 = 행 4개 (세로)'), (128, '   행 = 칸 이름(W 96) + 내용(W Fill)'),
                 (196, '← 예시 (세로)'), (214, '   맞는-예 = 표시 글자 · button 2개 · 설명'), (382, '← 틀린-예 (Stroke status/error)')]:
        s.text(432, y, t, 10, 600, BLUE if t.startswith('←') else SUB)
    s.text(432, 480, '카드 바깥: button 규칙', 10.5, 700, INK)
    s.text(432, 498, 'Vertical · W Fixed 360 · H Hug', 10, 500, SUB)
    s.text(432, 516, '컴포넌트 페이지 button 세트 오른쪽', 10, 500, SUB)
    return s

@fig('easing', '예시 · 길이와 이징. 같은 300ms라도 처음이 빠른지 끝이 빠른지에 따라 느낌이 다르다. 들어오는 것은 감속(ease-out)이 기본')
def easing():
    s = S(680, 280)
    X, Y, W, H = 50, 30, 260, 180
    s.rect(X, Y, W, H, 'none', LINE, 0); s.text(X, Y-10, '진행(위치) ↑', 10, 600, SUB); s.text(X+W, Y+H+18, '시간 →', 10, 600, SUB, 'end')
    s.path(f'M{X},{Y+H} L{X+W},{Y}', MUTE, 1.6)
    s.path(f'M{X},{Y+H} C{X},{Y+H} {X+W*0.58},{Y} {X+W},{Y}', BLUE, 2.2)
    s.path(f'M{X},{Y+H} C{X+W*0.42},{Y+H} {X+W},{Y} {X+W},{Y}', RED, 2.2)
    s.path(f'M{X},{Y+H} C{X+W*0.42},{Y+H} {X+W*0.58},{Y} {X+W},{Y}', GREEN, 2.2)
    for i, (c, n, d) in enumerate([(BLUE, 'ease-out (감속)', '빠르게 시작해 천천히 멈춤 → 나타나는 것'), (RED, 'ease-in (가속)', '천천히 시작해 빠르게 끝남 → 사라지는 것'),
                                   (GREEN, 'ease-in-out', '양 끝이 느림 → 화면 안에서 옮겨 가는 것'), (MUTE, 'linear', '일정한 속도 → 기계적으로 보임')]):
        y = 40 + i*36
        s.line(340, y, 366, y, c, 3); s.text(374, y+4, n, 11, 700, INK); s.text(374, y+20, d, 10, 500, SUB)
    s.text(340, 196, '길이: 보통 100~500ms 사이에서 고른다(NN/g).', 10.5, 600, INK)
    s.text(340, 214, '작고 가까운 변화는 짧게, 크게 움직이면 길게.', 10.5, 500, SUB)
    s.rect(20, 236, 640, 36, BG, LINE, 8)
    s.text(32, 258, 'Figma: 연결선 선택 → Animation: Smart animate → Easing 목록에서 고르고 길이(ms)를 입력. 고른 값과 이유를 함께 적는다.', 10, 600, INK)
    return s

@fig('research_plan', '예시 · 조사 계획 1쪽 양식. 칸 이름과 채우는 방법을 보여 주는 예이며, 내용은 직접 정한다')
def research_plan():
    s = S(680, 380)
    s.rect(20, 6, 640, 368, WHITE, LINE, 10)
    s.text(36, 32, 'CASE01 조사 계획 (1쪽)', 14, 800, INK); s.text(644, 32, '작성일 · 버전', 10, 500, SUB, 'end')
    rows = [('배경', '왜 이 업무를 보는가. 지금 알고 있는 것 2~3줄.'),
            ('알고 싶은 것', '질문 3개. 예) 일정이 바뀌면 누가, 어떤 순서로 알리는가?'),
            ('방법', '인터뷰 ○명(각 40분) + 실제 업무 관찰 ○회. 왜 이 방법인지 한 줄.'),
            ('참여자', '역할만 적는다(예: 상담 직원 A). 실명·연락처는 따로 보관.'),
            ('일정', '날짜 · 시간 · 장소. 상대가 가능한 시간에 맞춘다.'),
            ('기록·동의', '녹음 여부를 먼저 묻는다. 거절하면 메모만. 기록은 익명으로.'),
            ('측정할 것', '기준선: 걸린 시간, 다시 묻는 횟수 등 — 정의를 함께 적는다.'),
            ('끝나면 나올 것', '원문 카드 40장+, 기준선 측정표, As-is 흐름.')]
    for i, (k, v) in enumerate(rows):
        y = 48 + i*40
        s.rect(36, y, 608, 36, BG if i % 2 == 0 else WHITE, LINE, 4)
        s.text(48, y+23, k, 11, 700, INK); s.text(160, y+23, v, 10.5, 500, SUB)
    return s

@fig('ui_kit', '예시 · UI 키트 v0 페이지. 중간 해상도 화면에 필요한 최소 부품만 회색 위주로 모은다(색·꾸밈은 9주차 v1에서)')
def ui_kit():
    s = S(680, 300)
    s.rect(20, 6, 640, 288, '#FAFAFA', LINE, 10)
    s.text(36, 30, '학원 UI 키트 v0', 14, 800, INK)
    s.text(36, 56, '색', 11, 700, INK)
    for i, c in enumerate(['#111827', '#6B7280', '#D1D5DB', '#F3F4F6', BLUE, RED]):
        s.rect(80 + i*36, 44, 28, 20, c, LINE, 4)
    s.text(320, 56, '글자', 11, 700, INK)
    for i, (t, sz) in enumerate([('제목 20', 15), ('본문 16', 12.5), ('보조 13', 10.5)]):
        s.text(364 + i*92, 58, t, sz, 600 if i == 0 else 400, INK)
    s.text(36, 96, '버튼', 11, 700, INK)
    for i, (lb, f, fg, st) in enumerate([('보내기', '#374151', WHITE, None), ('취소', WHITE, '#374151', '#9CA3AF'), ('비활성', '#E5E7EB', '#6B7280', None)]):
        s.rect(80 + i*110, 80, 100, 32, f, st or f, 6); s.text(130 + i*110, 101, lb, 11, 700, fg, 'middle')
    s.text(36, 146, '입력', 11, 700, INK)
    s.rect(80, 130, 210, 32, WHITE, '#9CA3AF', 6); s.text(90, 151, '수업 이름', 10.5, 400, '#6B7280')
    s.text(320, 146, '상태', 11, 700, INK)
    for i, (t, c, bg) in enumerate([('전달됨', SUB, BG), ('확인함', GREEN, GREEN_L), ('전달 실패', RED, RED_L)]):
        s.badge(364 + i*86, 134, t, c, bg, 10.5)
    s.text(36, 196, '표 행', 11, 700, INK)
    s.rect(80, 180, 560, 30, WHITE, LINE, 0)
    for j, w in enumerate([120, 160, 90]): s.rect(90 + sum([0, 140, 320][:j+1]) if False else [90, 230, 410][j], 192, w*0.6, 7, '#9CA3AF', '#9CA3AF', 3)
    s.badge(560, 186, '확인함', GREEN, GREEN_L, 10)
    s.text(36, 240, '규칙', 11, 700, INK)
    s.text(80, 240, '버튼·입력 높이 48(그림은 축소) · 글자 최소 12 · 상태는 색 + 글자로 함께 표시', 10.5, 500, SUB)
    s.text(80, 262, '부품마다 컴포넌트로 만든다. 새 부품이 필요하면 화면에서 그리지 말고 키트에 먼저 추가한다.', 10.5, 500, SUB)
    s.text(80, 282, '내용(문구·상태 이름)은 예시다. 조사에서 나온 실제 말로 바꾼다.', 10, 500, SUB)
    return s

@fig('journey', '예시 · 현재 여정도 양식. 단계(열) × 하는 일·생각·감정·문제(행)로 나누고, 칸마다 근거 카드 번호를 붙인다')
def journey():
    s = S(680, 340)
    stages = ['찾기', '고르기', '찜하기', '다시 보기']
    rowsn = ['하는 일', '생각·말', '감정', '문제', '기회']
    X0, CW, Y0, RH = 100, 140, 30, 54
    for j, st in enumerate(stages):
        s.rect(X0 + j*CW, 6, CW-6, 22, PURPLE_L, PURPLE_L, 4); s.text(X0 + j*CW + (CW-6)/2, 21, st, 11, 700, PURPLE, 'middle')
    for i, rn in enumerate(rowsn):
        y = Y0 + i*RH
        s.text(20, y+30, rn, 11, 700, INK)
        s.line(20, y, 660, y, LINE)
    cells = {(0, 0): '홈에서 넘겨 봄', (0, 1): '썸네일·평점 비교', (0, 2): '찜 누름', (0, 3): '찜 목록 찾기',
             (1, 0): '“뭘 볼지 모르겠다” C2-04', (1, 1): '“줄거리가 길다” C3-11', (1, 2): '“나중에 볼게” C1-07', (1, 3): '“어디 있지?” C4-02',
             (3, 0): '', (3, 1): '비교 정보 부족 · 카드 4장', (3, 2): '', (3, 3): '찜 위치 못 찾음 · 카드 5장',
             (4, 1): '핵심 정보만 비교', (4, 3): '이어 볼 것 먼저'}
    for (i, j), t in cells.items():
        if t: s.text(X0 + j*CW + 4, Y0 + i*RH + 22, t, 9.5, 500, INK if i != 3 else RED)
    ys = [2, 3.4, 1.4, 4]
    pts = ' '.join(f'{X0 + j*CW + 60},{Y0 + 2*RH + 8 + v*9}' for j, v in enumerate(ys))
    s.add(f'<polyline points="{pts}" fill="none" stroke="{BLUE}" stroke-width="2"/>')
    for j, v in enumerate(ys): s.circle(X0 + j*CW + 60, Y0 + 2*RH + 8 + v*9, 4, BLUE, BLUE)
    s.line(20, Y0 + 5*RH, 660, Y0 + 5*RH, LINE)
    s.text(20, 318, '감정은 위가 좋음, 아래가 나쁨. 카드 번호(C2-04 등)가 없는 칸은 비워 둔다 — 추측으로 채우지 않는다.', 10, 600, INK)
    s.text(20, 334, '단계·문구·번호는 모두 형식 예시다. 실제 내용은 내 인터뷰 카드에서 가져온다.', 10, 500, SUB)
    return s

@fig('storyboard', '예시 · 인터랙션 스토리보드. 장면마다 화면 스케치 + 무슨 일이 일어나는지 한 줄 + 바뀌는 상태 이름을 적는다')
def storyboard():
    s = S(680, 280)
    scenes = [('1 상황', '직원이 변경 공지를 보낸다', '보내는 중'), ('2 실패', '한 명에게 전달 실패', '전달 실패'),
              ('3 알림', '실패한 사람만 표시되고 이유가 보인다', '전달 실패'), ('4 복구', '다시 보내기 → 전달됨으로 바뀜', '전달됨')]
    for i, (t, d, st) in enumerate(scenes):
        x = 20 + i*162
        s.text(x, 16, t, 11.5, 700, INK)
        s.rect(x, 24, 150, 150, WHITE, '#9CA3AF', 10)
        for k in range(3):
            y = 40 + k*36
            s.rect(x+10, y, 130, 28, WHITE, LINE, 5); s.rect(x+18, y+10, 60, 6, '#9CA3AF', '#9CA3AF', 2)
            c, bg, lab = (SUB, BG, '…')
            if i == 0: lab = '보내는 중'
            elif k == 1 and i in (1, 2): c, bg, lab = RED, RED_L, '실패'
            else: c, bg, lab = SUB, BG, '전달됨'
            if i == 3 and k == 1: c, bg, lab = GREEN, GREEN_L, '전달됨'
            s.rect(x+92, y+6, 42, 16, bg, bg, 8); s.text(x+113, y+18, lab, 8.5, 700, c, 'middle')
        if i == 2: s.rect(x+10, 148, 130, 20, RED_L, RED_L, 4); s.text(x+75, 162, '번호 없음 · 다시 보내기', 8.5, 700, RED, 'middle')
        for k, ln in enumerate(wrap(d, 148, 10)): s.text(x, 192 + k*15, ln, 10, 500, SUB)
        s.badge(x, 222, '상태: ' + st, PURPLE, PURPLE_L, 9.5)
        if i < 3: s.arrow(x+152, 99, x+160, 99, MUTE, 1.4)
    s.text(20, 266, '그림은 손그림 수준이면 충분하다. 장면 수는 4~6개, 각 장면에서 “무엇이 바뀌는가”를 한 가지만 보여 준다.', 10, 600, INK)
    return s

@fig('check_btn', '예시 · ‘하루’ 체크·버튼 Variants와 속성 이름 목록. 체크는 상태 2개, 버튼은 상태 2개 + 글자·아이콘 켜고 끄기 속성을 붙인다')
def check_btn():
    s = S(680, 360)
    s.text(20, 18, '체크 (컴포넌트 세트)', 12, 700, INK)
    s.rect(20, 28, 170, 92, 'none', PURPLE, 8, 1.2, '4,3')
    for i, (d, n) in enumerate([(False, 'State=Unchecked'), (True, 'State=Checked')]):
        x = 34 + i*76
        s.rect(x, 40, 44, 44, 'none', '#A78BFA', 6, 1, '3,2'); _check(s, x+11, 51, d)
        s.text(x+22, 104, n.split('=')[1], 9.5, 600, SUB, 'middle')
    s.text(210, 18, '버튼 (컴포넌트 세트)', 12, 700, INK)
    s.rect(210, 28, 450, 92, 'none', PURPLE, 8, 1.2, '4,3')
    _btn(s, 226, 44, 200, '저장')
    _btn(s, 444, 44, 200, '저장', 'plus', '#E5E7EB', '#6B7280')
    s.text(326, 108, 'State=Default', 9.5, 600, SUB, 'middle'); s.text(544, 108, 'State=Disabled · 높이 48 그대로', 9.5, 600, SUB, 'middle')
    # 속성 이름 목록
    s.text(20, 148, '속성 이름 목록 (오늘 결과물 예)', 12, 700, INK)
    cols = [20, 100, 210, 320, 470, 660]
    hd = ['컴포넌트', '속성 이름', '종류', '값', '이유']
    rows = [('체크', 'State', 'Variant', 'Unchecked / Checked', '모양이 달라서'),
            ('버튼', 'State', 'Variant', 'Default / Disabled', '색이 달라서'),
            ('버튼', 'Label', 'Text', '저장, 추가 …', '글자만 바꿔 씀'),
            ('버튼', 'Show icon', 'Boolean', '켬 / 끔', '아이콘 없는 버튼도 씀')]
    s.rect(20, 158, 640, 26, BG, LINE, 0)
    for j, h in enumerate(hd): s.text(cols[j]+8, 175, h, 10.5, 700, INK)
    for i, r in enumerate(rows):
        y = 184 + i*26; s.rect(20, y, 640, 26, WHITE, LINE, 0)
        for j, v in enumerate(r): s.text(cols[j]+8, y+17, v, 10.5, 500 if j else 600, INK)
    s.rect(20, 300, 640, 52, BG, LINE, 8)
    s.text(32, 320, '③ 교체하는 법: 월요일 행 원본 안의 체크를 이 체크 세트의 인스턴스로 바꾼다(체크 선택 → 오른쪽 패널 위쪽 이름 옆 ▾ → 체크 세트 고르기).', 10, 600, INK)
    s.text(32, 338, '원본 한 곳만 바꾸면 6개 행이 모두 따라온다. 행에서 체크 상태는 오른쪽 패널의 State로 고른다.', 10, 500, SUB)
    return s
