# 단계 카드 안에 넣는 작은 화면 그림 (Figma 화면을 단순하게 그린 HTML)
# 블록 글에서 '그림:키' 한 줄로 부른다. 앱 폭 420에 맞춰 최대 360px.
import html
E = html.escape

BLUE = '#0D99FF'      # Figma 선택 색
HL = '#E5F4FF'        # 선택 줄 바탕
LINE = '#E6E6E6'
SUB = '#6B7280'
INK = '#1F2937'
NEW = '#15803D'       # 새 이름 글자
OLD = '#9CA3AF'       # 옛 이름 글자

# 이름이 사는 곳 4가지 — 색으로 구분 (카드 위 ‘어디’ 칩과 같은 색)
PLACE = {
    '변수 창': ('#7C3AED', '#F3E8FF'),
    '레이어 패널': ('#1D4ED8', '#DBEAFE'),
    '글자 스타일': ('#047857', '#D1FAE5'),
    '속성': ('#B45309', '#FEF3C7'),
    '캔버스': ('#374151', '#F3F4F6'),
    '앱 기입표': ('#374151', '#F3F4F6'),
}
def place_color(text):
    for k, v in PLACE.items():
        if text.startswith(k) or k in text.split(' ›')[0]:
            return v
    return PLACE['캔버스']

def chip(text, fg, bg, bold=True):
    return (f'<span style="display:inline-block;padding:2px 8px;border-radius:999px;background:{bg};color:{fg};'
            f'font-size:.85em;{"font-weight:700;" if bold else ""}white-space:nowrap">{E(text)}</span>')

def win(title, body, place=None):
    fg, bg = PLACE.get(place, ('#374151', '#F3F4F6')) if place else ('#374151', '#F3F4F6')
    return (f'<div style="max-width:360px;border:1px solid #D1D5DB;border-radius:8px;overflow:hidden;background:#fff;'
            f'font-size:13px;line-height:1.4;margin:6px 0;box-shadow:0 1px 2px rgba(0,0,0,.06)">'
            f'<div style="display:flex;align-items:center;gap:6px;padding:5px 8px;background:{bg};border-bottom:1px solid {LINE};color:{fg};font-weight:700">'
            f'<span style="width:8px;height:8px;border-radius:4px;background:{fg}"></span>{E(title)}</div>{body}</div>')

def rename(old, new):
    """옛 이름 → 새 이름 (더블클릭해서 바꾸는 칸)"""
    return (f'<span style="color:{OLD};text-decoration:line-through">{E(old)}</span>'
            f' <span style="color:{SUB}">→</span> '
            f'<span style="color:{NEW};font-weight:700;border:1.5px solid {BLUE};border-radius:3px;padding:0 3px;background:#fff">{E(new)}</span>')

def tag(text):
    return f'<span style="margin-left:auto;font-size:11px;color:#fff;background:#F97316;border-radius:4px;padding:0 5px;white-space:nowrap">{E(text)}</span>'

def row(left, right='', hl=False, note='', indent=0):
    bg = HL if hl else '#fff'
    return (f'<div style="display:flex;align-items:center;gap:8px;padding:4px 8px {4}px {8 + indent * 14}px;'
            f'border-bottom:1px solid #F3F4F6;background:{bg}">'
            f'<span style="min-width:0;flex:1">{left}</span>'
            + (f'<span style="color:{SUB};white-space:nowrap">{right}</span>' if right else '')
            + (tag(note) if note else '') + '</div>')

def sw(hexv):
    return f'<span style="display:inline-block;width:12px;height:12px;border-radius:3px;border:1px solid #D1D5DB;background:#{hexv};vertical-align:-2px;margin-right:4px"></span>'

def ic(kind):
    """레이어 패널 아이콘: # Frame · T 글자 · ◆ 원본 · ◇ Instance · ❖ 세트"""
    m = {'frame': '#', 'text': 'T', 'comp': '◆', 'inst': '◇', 'set': '❖'}
    col = '#7C3AED' if kind in ('comp', 'inst', 'set') else SUB
    return f'<span style="display:inline-block;width:14px;text-align:center;color:{col};font-weight:700;margin-right:4px">{m[kind]}</span>'

def caption(t):
    return f'<div style="font-size:12px;color:{SUB};margin:-2px 0 6px">{E(t)}</div>'

MINI = {}
def mini(key):
    def deco(fn):
        MINI[key] = fn; return fn
    return deco

# ───────────── 오늘 바꾸는 이름은 4군데에 산다
@mini('name_map')
def name_map():
    def cell(num, place, where, what, ex):
        fg, bg = PLACE[place]
        return (f'<div style="border:2px solid {fg};border-radius:8px;padding:6px 8px;background:{bg}">'
                f'<div style="display:flex;gap:6px;align-items:center"><b style="color:{fg}">{num} {E(place)}</b></div>'
                f'<div style="font-size:12px;color:{INK};margin-top:2px">{E(where)}</div>'
                f'<div style="font-size:12px;margin-top:4px"><b>바꾸는 것:</b> {E(what)}</div>'
                f'<div style="font-size:12px;color:{SUB}">예: {ex}</div></div>')
    grid = ('<div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;padding:8px">'
            + cell('①', '변수 창', '맨 왼쪽 세로 아이콘 줄 → Variables 아이콘', '컬렉션 이름 · 변수 이름', rename('spacing/2', 'space/200'))
            + cell('②', '글자 스타일', '캔버스 빈 곳 클릭 → 오른쪽 Text styles', '글자 스타일 이름 + 크기 · 굵기', rename('caption', 'body/small'))
            + cell('③', '레이어 패널', '화면 왼쪽 Layers 목록', '레이어(칸 · 글자) 이름', rename('actions', 'button-group'))
            + cell('④', '속성', '부품 세트 선택 → 오른쪽 Properties', '속성 이름 · 값 이름', rename('Type', 'variant'))
            + '</div>')
    fig = ('<div style="display:grid;grid-template-columns:70px 1fr 90px;gap:4px;padding:8px 8px 0;font-size:11px;text-align:center">'
           f'<div style="border:2px solid {PLACE["레이어 패널"][0]};border-radius:4px;height:70px;padding-top:4px;color:{PLACE["레이어 패널"][0]}">③ Layers</div>'
           f'<div style="border:1px dashed #D1D5DB;border-radius:4px;height:70px;padding-top:4px;color:{SUB};position:relative">캔버스'
           f'<div style="position:absolute;left:12px;top:22px;border:2px solid {PLACE["변수 창"][0]};border-radius:4px;background:#fff;padding:2px 6px;color:{PLACE["변수 창"][0]}">① Variables 창</div></div>'
           f'<div style="display:flex;flex-direction:column;gap:4px"><div style="border:2px solid {PLACE["속성"][0]};border-radius:4px;height:33px;color:{PLACE["속성"][0]}">④ Properties</div>'
           f'<div style="border:2px solid {PLACE["글자 스타일"][0]};border-radius:4px;height:33px;color:{PLACE["글자 스타일"][0]}">② Text styles</div></div></div>')
    return win('Figma 화면 — 이름이 사는 4군데', fig + grid)

# ───────────── ⓐ 컬렉션 이름
@mini('var_collections')
def var_collections():
    left = (row('<b>Collections</b>')
            + row('Primitives', '그대로')
            + row(rename('Segmantic', 'Semantic'), hl=True, note='더블클릭')
            + row('Size', '그대로'))
    return win('① 변수 창 (Variables) — 왼쪽 컬렉션 목록', left, '변수 창')

# ───────────── ⓑ Size 변수
@mini('var_size')
def var_size():
    b = (row('<b>Name</b>', '<b>Value</b>')
         + row(rename('spacing/1', 'space/100'), '4', hl=True, note='이름 칸 더블클릭')
         + row(rename('spacing/2', 'space/200'), '8')
         + row(rename('spacing/4', 'space/400'), '16')
         + row(rename('radius/md', 'radius/200'), '8')
         + row(rename('border/width', 'border-width/default'), '2'))
    return win('① 변수 창 › Size 컬렉션 — 값을 보고 이름을 정한다', b, '변수 창') + caption('이름 숫자 = 값 ÷ 4 × 100 (8 → 200, 16 → 400). 값 칸은 건드리지 않는다')

# ───────────── ⓒ Primitives 그룹
@mini('var_groups')
def var_groups():
    groups = (row('<b>Groups</b>')
              + row('All')
              + row(f'<span style="color:{OLD}">color</span> <span style="color:{SUB};font-size:11px">(끌어낸 뒤 빈 그룹 삭제)</span>', indent=0)
              + row('green', indent=1, note='끌어서 All 아래로')
              + row(rename('netral', 'gray'), indent=1, hl=True, note='더블클릭'))
    rows = (row('<b>Name</b>', '<b>Value</b>')
            + row(rename('green/50', 'green/300'), sw('D2E077') + 'D2E077', hl=True)
            + row(rename('green/100', 'green/400'), sw('A4C263') + 'A4C263')
            + row(rename('green/200', 'green/500'), sw('6DC458') + '6DC458'))
    return (win('① 변수 창 › Primitives — 왼쪽 Groups', groups, '변수 창')
            + win('① 변수 창 › Primitives — 오른쪽 이름 칸', rows, '변수 창')
            + caption('밝을수록 작은 숫자. 값(색)은 그대로라 Semantic 쪽 연결도 그대로 따라온다'))

# ───────────── ⓓ Semantic 변수 이름 + 새로 만들기
@mini('var_color')
def var_color():
    b = (row('<b>Name</b>', '<b>Value</b>')
         + row(rename('bg/screen/screen', 'background/default/default'), sw('C49A6C'), hl=True, note='더블클릭')
         + row(rename('border/strong', 'border/default/default'), sw('645552'))
         + row(rename('status/error', 'border/danger/default'), sw('CF4843')))
    return win('① 변수 창 › Semantic 컬렉션 — 이름만 바꾼다', b, '변수 창') + caption('값 칸(색 동그라미)은 누르지 않는다 → 가리키던 색이 그대로 남는다')

@mini('var_create')
def var_create():
    b = (row('<b>Name</b>', '<b>Value</b>')
         + row(f'<span style="color:{NEW};font-weight:700">background/danger/default</span>', sw('CF4843') + 'red/500', hl=True, note='새로 만듦')
         + f'<div style="padding:6px 8px;color:{BLUE};font-weight:700">+ Create variable</div>')
    fill = (row('<b>Fill</b>')
            + row(sw('CF4843') + 'background/danger/default', '⁘', hl=True, note='점 4개 아이콘'))
    return (win('① 변수 창 › Semantic — 맨 아래 + Create variable → Color', b, '변수 창')
            + win('④ 오른쪽 Design 패널 — 삭제 버튼(Type=danger) 선택 뒤 Fill 칸', fill, '속성'))

# ───────────── ⓔ-1 글자 스타일
@mini('text_style_edit')
def text_style_edit():
    lst = (row('<b>Text styles</b>')
           + row('Aa ' + rename('subheading', 'heading/medium'), hl=True, note='오른쪽 버튼 → Edit style')
           + row('Aa ' + rename('body/base', 'body/medium'))
           + row('Aa ' + rename('caption', 'body/small'))
           + row('Aa ' + rename('button', 'label/medium')))
    def fld(k, v):
        return (f'<div style="display:flex;gap:6px;align-items:center;padding:3px 8px"><span style="width:76px;color:{SUB}">{E(k)}</span>'
                f'<span style="flex:1;border:1.5px solid {BLUE};border-radius:4px;padding:1px 6px;font-weight:700;color:{NEW}">{E(v)}</span></div>')
    edit = fld('Name', 'heading/medium') + fld('Size', '20') + fld('Line height', '28') + fld('Weight', 'Bold')
    return (win('② 캔버스 빈 곳 클릭 → 오른쪽 Text styles', lst, '글자 스타일')
            + win('② Edit style 창 — 이름과 값 4칸을 표대로', edit, '글자 스타일')
            + caption('이름만 바꾸면 크기는 예전 값이 남는다 → Size · Line height · Weight도 같은 창에서 맞춘다'))

# ───────────── ⓔ-2 toast · dialog 안 레이어
@mini('layer_dialog')
def layer_dialog():
    b = (row(ic('comp') + 'toast', note='그대로')
         + row(ic('comp') + 'dialog ▾', hl=False)
         + row(ic('frame') + rename('actions', 'button-group'), indent=1)
         + row(ic('text') + rename('할 일을 삭제할까요?', 'title'), indent=1, hl=True, note='질문 문장')
         + row(ic('text') + rename('‘치킨 먹기’가 사라져요.', 'description'), indent=1, note='설명 문장'))
    return win('③ 레이어 패널 (화면 왼쪽 Layers)', b, '레이어 패널') + caption('T 줄 = 글자 레이어. Figma가 입력한 문장을 이름으로 붙여 둔 것 → 이름만 바꾸고 화면 글자는 그대로')

# ───────────── ⓔ-3 화면 레이어
@mini('layer_screens')
def layer_screens():
    b = (row(ic('frame') + '수정-기본 ▾')
         + row(ic('frame') + 'content ▾', indent=1)
         + row(ic('inst') + rename('field', 'text-field'), indent=2, hl=True, note='4개 Ctrl+클릭 → Ctrl+R')
         + row(ic('frame') + '목록 ▾')
         + row(ic('frame') + 'content ▾', indent=1)
         + row(ic('inst') + rename('행-1', 'item-1'), indent=2, note='더블클릭')
         + row(ic('inst') + rename('행-2', 'item-2'), indent=2))
    return win('③ 레이어 패널 — ‘화면’ 페이지', b, '레이어 패널')

# ───────────── ⓕ 속성 이름
@mini('props_rename')
def props_rename():
    p = (row('<b>Properties</b>')
         + row(rename('Type', 'variant'), 'primary · secondary · tertiary · danger', hl=True, note='줄 클릭')
         + row(rename('State', 'state'), 'default · hover …')
         + row(rename('Label', 'label'), 'T'))
    def fld(k, v):
        return (f'<div style="display:flex;gap:6px;align-items:center;padding:3px 8px"><span style="width:60px;color:{SUB}">{E(k)}</span>'
                f'<span style="flex:1">{v}</span></div>')
    pop = fld('Name', rename('Type', 'variant')) + fld('Values', rename('Primary', 'primary') + '<br>' + rename('Secondary', 'secondary') + '<br>' + rename('Tertiary', 'tertiary'))
    return (win('④ button 세트 선택 → 오른쪽 Design 패널 Properties', p, '속성')
            + win('④ 뜨는 창 — 이름과 값 이름', pop, '속성'))

# ───────────── 1단계 결과 모습
def _card(inner, border='#645552', bg='#F3E5C2', w=300):
    return f'<div style="width:{w}px;max-width:100%;border:2px solid {border};border-radius:8px;background:{bg};padding:10px;display:flex;flex-direction:column;gap:8px;font-size:12px">{inner}</div>'
def _lbl(name):
    return f'<span style="font-size:10px;color:{BLUE};font-weight:700">{E(name)}</span>'

@mini('rule_row')
def rule_row_fig():
    r = (f'<div style="border:1px dashed {BLUE};padding:4px;display:flex;gap:16px">{_lbl("rule-row")}'
         '<span style="width:96px;font-weight:700">언제 쓰나</span><span style="flex:1">화면의 행동(저장 · 추가 · 삭제)</span></div>')
    return win('캔버스 — 다 만들면 (가로로 두 글자)', f'<div style="padding:8px">{r}</div>', '캔버스')

@mini('dodont')
def dodont_fig():
    def btn(t, prim):
        return (f'<span style="display:inline-block;padding:4px 10px;border-radius:6px;border:1.5px solid #645552;'
                f'background:{"#6DC458" if prim else "#F3E5C2"};color:{"#fff" if prim else "#1F2937"};font-weight:700">{t}</span>')
    do = f'<div style="border:1px solid #D1D5DB;border-radius:6px;padding:6px;background:#fff">{_lbl("do")}<div>○ 맞는 예</div><div style="display:flex;gap:6px;margin:4px 0">{btn("취소",0)}{btn("저장",1)}</div><div>primary는 한 화면에 하나</div></div>'
    dont = f'<div style="border:2px solid #CF4843;border-radius:6px;padding:6px;background:#fff">{_lbl("dont")}<div>✕ 틀린 예</div><div style="display:flex;gap:6px;margin:4px 0">{btn("확인",1)}{btn("저장",1)}</div><div>primary가 둘</div></div>'
    return win('캔버스 — 다 만들면 (dont만 빨간 테두리)', f'<div style="padding:8px;display:flex;flex-direction:column;gap:6px">{do}{dont}</div>', '캔버스')

@mini('guide_card')
def guide_card_fig():
    rows = ''.join(f'<div style="display:flex;gap:10px"><b style="width:70px">{a}</b><span>{b}</span></div>' for a, b in
                   [('언제 쓰나', '화면의 행동'), ('쓰지 않을 때', '이동만 할 때'), ('상태', 'default · hover …'), ('문구', '동사로')])
    inner = (f'{_lbl("button-guide")}<b style="font-size:15px">button 규칙</b>'
             f'<div style="border:1px dashed {BLUE};padding:4px;display:flex;flex-direction:column;gap:3px">{_lbl("rule-table")}{rows}</div>'
             f'<div style="border:1px dashed {BLUE};padding:4px;display:flex;gap:4px">{_lbl("examples")} do · dont</div>')
    return win('캔버스 — button-guide 완성 모습', f'<div style="padding:8px">{_card(inner)}</div>', '캔버스')

@mini('settings_screen')
def settings_fig():
    def r(t):
        return (f'<div style="display:flex;align-items:center;gap:8px;border:1px dashed {BLUE};padding:6px">{_lbl("settings-row")}'
                f'<span style="flex:1">{t}</span><span style="width:40px;height:22px;border:2px solid #CF4843;border-radius:4px"></span></div>')
    inner = (f'<div style="border:1px dashed {BLUE};padding:4px;display:flex;gap:6px;align-items:center">{_lbl("header")}<b>←</b><b style="font-size:15px">설정</b></div>'
             f'<div style="display:flex;flex-direction:column;gap:6px">{r("알림")}{r("완료한 할 일 숨기기")}</div>')
    return win('캔버스 — 설정 화면 완성 모습 (빨간 칸 = 아직 없는 toggle)', f'<div style="padding:8px">{_card(inner, bg="#C49A6C", w=230)}</div>', '캔버스')

# ═════════════ 11/24 · 11/25 그림 ═════════════
PLACE.setdefault('Prototype 탭', ('#BE185D', '#FCE7F3'))

def _phone(title, rows, w=150, extra='', fs=11):
    """작은 휴대폰 화면: rows = [(체크, 글자, 줄긋기, 강조)]"""
    r = ''
    for chk, t, strike, hl in rows:
        box = (f'<span style="display:inline-grid;place-items:center;width:14px;height:14px;border:2px solid #6DC458;border-radius:3px;'
               f'background:{"#6DC458" if chk else "#fff"};color:#fff;font-size:10px">{"✓" if chk else ""}</span>')
        st = 'text-decoration:line-through;color:#6B7280;' if strike else ''
        r += (f'<div style="display:flex;gap:6px;align-items:center;padding:5px 6px;border:1.5px solid {"#0D99FF" if hl else "#645552"};'
              f'border-radius:6px;background:#F3E5C2;margin-top:5px;white-space:nowrap">{box}<span style="{st}">{E(t)}</span></div>')
    return (f'<div style="width:{w}px;border:1px solid #9CA3AF;border-radius:10px;background:#C49A6C;padding:6px;font-size:{fs}px;position:relative;overflow:hidden;min-height:150px">'
            f'<div style="font-weight:700;color:#fff;font-size:10px">{E(title)}</div>{r}{extra}</div>')

def _arrow(t):
    return (f'<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;font-size:10px;color:#BE185D;'
            f'text-align:center;min-width:44px">→<br>{t}</div>')

@mini('done_frames')
def done_frames():
    a = _phone('목록-미완료', [(0, '치킨 먹기', 0, 1), (0, '우유 사기', 0, 0), (0, '운동하기', 0, 0)], w=135)
    b = _phone('목록-완료됨', [(0, '우유 사기', 0, 0), (0, '운동하기', 0, 0), (1, '치킨 먹기', 1, 1)], w=135)
    body = f'<div style="display:flex;gap:4px;padding:8px;align-items:stretch">{a}{_arrow("item-1 누르면<br>Smart animate<br>Ease out<br>150ms")}{b}</div>'
    return win('캔버스 — 다 만들면 (파란 테두리 = item-1)', body, '캔버스') + caption('두 화면 모두 행 레이어 이름이 item-1 · item-2 · item-3 → 같은 이름끼리 자리를 옮겨 움직인다')

@mini('list_layers')
def list_layers():
    b = (row(ic('frame') + '목록 ▾')
         + row(ic('frame') + 'header ▸', indent=1)
         + row(ic('frame') + 'content ▾', indent=1)
         + row(ic('inst') + 'item-1', '치킨 먹기', indent=2, hl=True)
         + row(ic('inst') + 'item-2', '우유 사기', indent=2)
         + row(ic('inst') + rename('todo/row', 'item-3'), '운동하기', indent=2, note='이렇게 남았으면 더블클릭'))
    return win('레이어 패널 — ‘화면’ 페이지 목록', b, '레이어 패널')

@mini('type_settings')
def type_settings():
    ty = (row('<b>Typography</b>')
          + row('body/medium', '<span style="border:1.5px solid #0D99FF;border-radius:3px;padding:0 4px">⚙</span>', hl=True, note='Type settings'))
    pop = (row('<b>Basics</b> · <span style="color:#9CA3AF">Details</span>')
           + row('Decoration', '— &nbsp; U &nbsp; <span style="border:1.5px solid #0D99FF;border-radius:3px;padding:0 4px;text-decoration:line-through">S</span>', hl=True, note='Strikethrough'))
    return (win('오른쪽 Design 패널 — 치킨 먹기 글자 선택 뒤', ty, '속성')
            + win('뜨는 창 Type settings', pop, '속성'))

@mini('move_item')
def move_item():
    b = (row(ic('frame') + 'content ▾')
         + row(ic('inst') + 'item-2', '우유 사기', indent=1)
         + row(ic('inst') + 'item-3', '운동하기', indent=1)
         + f'<div style="height:0;border-top:2px solid #0D99FF;margin:0 8px 0 22px"></div>'
         + row(ic('inst') + 'item-1', '치킨 먹기', indent=1, hl=True, note='여기로 끌어 놓기'))
    return win('레이어 패널 — 목록-완료됨 content', b, '레이어 패널') + caption('파란 가로선이 item-3 아래에 보일 때 놓는다. content 밖으로 나가면 Ctrl+Z')

@mini('proto_interaction')
def proto_interaction():
    def fld(k, v, hl=False):
        return row(f'<span style="color:{SUB}">{E(k)}</span>', f'<b style="color:{NEW if hl else INK}">{E(v)}</b>', hl=hl)
    b = (fld('Trigger', 'On click') + fld('Action', 'Navigate to') + fld('도착(Destination)', '목록-완료됨', True)
         + fld('Animation', 'Smart animate', True) + fld('이징', 'Ease out') + fld('시간', '150ms', True))
    return win('Prototype 탭 › Interactions 줄을 눌러 뜨는 창', b, 'Prototype 탭')

@mini('after_delay')
def after_delay():
    def fld(k, v, hl=False):
        return row(f'<span style="color:{SUB}">{E(k)}</span>', f'<b style="color:{NEW if hl else INK}">{E(v)}</b>', hl=hl)
    b = (fld('Trigger', 'After delay · 1ms', True) + fld('Action', 'Navigate to') + fld('도착', '목록-삭제됨', True)
         + fld('Animation', 'Smart animate · Ease out · 200ms', True))
    return win('Prototype 탭 — 목록-삭제직후 Frame 선택 뒤 + 를 눌러 뜨는 창', b, 'Prototype 탭') + caption('Frame 자체에 거는 연결이라 안쪽 레이어는 아무것도 선택하지 않는다')

@mini('delete_flow')
def delete_flow():
    toast = lambda y: (f'<div style="position:absolute;left:6px;right:6px;top:{y}px;background:#F3E5C2;border:1.5px solid #645552;'
                       'border-radius:5px;padding:2px 4px;display:flex;gap:3px;justify-content:space-between;white-space:nowrap;font-size:7px;left:3px;right:3px"><span>삭제했어요</span><b>되돌리기</b></div>')
    a = _phone('목록-삭제직후', [(0, '우유 사기', 0, 0), (0, '운동하기', 0, 0)], w=100,
               extra=toast(170) + '<div style="position:absolute;left:6px;top:120px;font-size:8px;color:#fff">↓ toast는 화면 밖</div>', fs=9)
    b = _phone('목록-삭제됨', [(0, '우유 사기', 0, 0), (0, '운동하기', 0, 0)], w=100, extra=toast(122), fs=9)
    c = _phone('목록', [(0, '치킨 먹기', 0, 1), (0, '우유 사기', 0, 0), (0, '운동하기', 0, 0)], w=100, fs=9)
    body = (f'<div style="display:flex;gap:2px;padding:8px;align-items:stretch;font-size:10px">{a}{_arrow("1ms 뒤<br>Smart<br>Ease out<br>200")}'
            f'{b}{_arrow("되돌리기<br>Smart<br>Ease in<br>and out<br>250")}{c}</div>')
    return win('캔버스 — 확인창 ‘삭제’ 다음에 이어지는 3화면', body, '캔버스') + caption('목록-삭제직후는 사용자가 거의 못 보는 화면: toast 출발 자리만 화면 아래 바깥으로 둔다')

def _badge(n, bg, fg):
    return (f'<span style="display:inline-grid;place-items:center;width:20px;height:20px;border-radius:10px;background:#{bg};'
            f'color:#{fg};font-size:11px;font-weight:700;flex:none">{n}</span>')

@mini('annotation_variants')
def annotation_variants():
    v = [('action', '6DC458', 'FFFFFF', '누르면 어디로 · 몇 ms'), ('condition', '645552', 'F3E5C2', '입력 조건 · 기본값'),
         ('error', 'CF4843', 'FFFFFF', '오류 문구와 위치'), ('accessibility', '6B7280', 'FFFFFF', '라벨 · 누르는 크기')]
    rows_ = ''.join(f'<div style="display:flex;gap:6px;align-items:flex-start;padding:5px 8px;border-bottom:1px solid #F3F4F6">'
                    f'{_badge(i + 1, bg, fg)}<span style="flex:1">{E(d)}</span><span style="font-size:10px;color:{BLUE};font-weight:700">variant={k}</span></div>'
                    for i, (k, bg, fg, d) in enumerate(v))
    return win('캔버스 — annotation 세트 (variant 4개)', rows_, '캔버스') + caption('왼쪽 동그라미 = badge(안에 number 글자), 오른쪽 글 = description 글자')

@mini('annotation_props')
def annotation_props():
    p = (row('<b>annotation</b> ◇', note='Instance 선택')
         + row('variant', 'action ▾', hl=True)
         + row('number', '1')
         + row('description', '제목은 꼭 입력 · 최대 40자')
         + row('show description', '● 켬'))
    return win('오른쪽 Design 패널 — annotation Instance 속성', p, '속성') + caption('화면 위 번호 표시는 같은 부품에서 show description만 끈 것')

@mini('spec_done')
def spec_done():
    marks = (f'<div style="position:absolute;right:4px;top:30px">{_badge(1, "645552", "F3E5C2")}</div>'
             f'<div style="position:absolute;left:4px;top:30px">{_badge(8, "6B7280", "FFFFFF")}</div>'
             f'<div style="position:absolute;right:4px;top:62px">{_badge(2, "645552", "F3E5C2")}</div>'
             f'<div style="position:absolute;left:4px;bottom:28px">{_badge(6, "6DC458", "FFFFFF")}</div>'
             f'<div style="position:absolute;right:4px;bottom:28px">{_badge(5, "6DC458", "FFFFFF")}</div>')
    field = lambda t, y: f'<div style="position:absolute;left:26px;right:26px;top:{y}px;border:1.5px solid #645552;border-radius:5px;background:#fff;padding:2px 4px">{t}</div>'
    phone = (f'<div style="width:120px;height:170px;border:1px solid #9CA3AF;border-radius:10px;background:#C49A6C;position:relative;font-size:9px;flex:none">'
             f'<div style="padding:5px;color:#fff;font-weight:700">← 할 일 추가</div>{field("제목을 입력하세요", 30)}{field("09:00", 62)}'
             f'<div style="position:absolute;left:26px;right:26px;bottom:8px;display:flex;gap:4px"><span style="flex:1;background:#6B7280;color:#fff;border-radius:4px;text-align:center">취소</span>'
             f'<span style="flex:1;background:#6DC458;color:#fff;border-radius:4px;text-align:center">저장</span></div>{marks}</div>')
    notes = ''.join(f'<div style="display:flex;gap:4px;align-items:flex-start;margin-bottom:3px">{_badge(n, bg, fg)}<span>{E(t)}</span></div>'
                    for n, bg, fg, t in [(1, '645552', 'F3E5C2', '제목 필수 · 최대 40자'), (2, '645552', 'F3E5C2', '시간 기본값 없음'),
                                         (3, '645552', 'F3E5C2', '저장 버튼 늘 누를 수 있음'), (4, 'CF4843', 'FFFFFF', '빈 제목 오류 문구'),
                                         (5, '6DC458', 'FFFFFF', '저장 → 목록 맨 아래'), (6, '6DC458', 'FFFFFF', '취소 → 입력값 버림'),
                                         (7, '645552', 'F3E5C2', '빈 목록 문구'), (8, '6B7280', 'FFFFFF', '라벨 · 버튼 48')])
    body = (f'<div style="padding:8px"><div style="border:1px dashed {BLUE};border-radius:8px;background:#F3E5C2;padding:8px;display:flex;gap:10px;font-size:10px">'
            f'{phone}<div style="flex:1;min-width:0">{_lbl("notes")}{notes}</div></div></div>')
    return win('캔버스 — 명세-할 일 추가 완성 모습 (‘전달’ 페이지)', body, '캔버스') + caption('왼쪽 = 추가-기본 화면 + 번호 표시, 오른쪽 = notes(annotation 8개)')

# ═════════════ 11/27~ UI 따라 만들기 그림 ═════════════
def _shot(title, w=110, op=1.0, dashed=False, lock=False):
    """회색 덩어리로 그린 화면 (원본 캡처 · 내 화면 공통). 특정 앱 모양이 아니라 위치만 보여 준다."""
    bars = ''.join(f'<div style="height:{h}px;margin:{m}px 8px 0;border-radius:4px;background:{c}"></div>'
                   for h, m, c in ((10, 8, '#9CA3AF'), (22, 6, '#4B5563'), (26, 8, '#D1D5DB'), (26, 6, '#D1D5DB'), (26, 6, '#D1D5DB')))
    bd = '2px dashed #0D99FF' if dashed else '1px solid #9CA3AF'
    lk = '<span style="float:right">🔒</span>' if lock else ''
    return (f'<div style="width:{w}px;min-height:170px;border:{bd};border-radius:10px;background:#fff;opacity:{op};padding-bottom:8px">'
            f'<div style="font-size:9px;color:#374151;padding:3px 6px;border-bottom:1px solid #E5E7EB">{E(title)}{lk}</div>{bars}</div>')

@mini('copy_canvas')
def copy_canvas():
    a = _shot('원본 (캡처 · 390)', lock=True)
    b = _shot('홈-기본 (Frame 390×844)', dashed=True)
    s1 = f'<div style="display:flex;gap:10px;padding:8px;align-items:flex-start">{a}{_arrow("④ 오른쪽에<br>새로 만듦")}{b}</div>'
    over = (f'<div style="position:relative;width:110px;height:200px;margin:8px auto">'
            f'<div style="position:absolute;inset:0">{_shot("원본", lock=True)}</div>'
            f'<div style="position:absolute;left:4px;top:3px">{_shot("홈-기본 50%", op=.5, dashed=True)}</div></div>')
    return (win('캔버스 — ①~④ 다 하면 (나란히)', s1, '캔버스')
            + win('캔버스 — ⑤ 겹쳐 보기 (내 화면 투명도 50%)', over, '캔버스')
            + caption('어긋난 만큼 두 겹으로 보인다. 여백 → 간격 → 글자 순서로 맞춘다'))

# ───────────── 11/25 전체 흐름 한 장 — 다 만든 예시
@mini('flow_example')
def flow_example():
    groups = [
        ('Discover', '넓게 조사', '#1D4ED8', '#DBEAFE', [('조사', '인터뷰 메모 · 관찰 기록', '나와 팀 → 진짜 문제 찾기', '')]),
        ('Define', '좁혀서 정하기', '#1D4ED8', '#DBEAFE', [('문제 정의', '문제 정의 1장 · 성공 기준', '팀 · 기획자 → 무엇을 풀지', '')]),
        ('Develop', '넓게 만들어 보기', '#047857', '#D1FAE5', [
            ('아이디어', '스케치 · 비교표', '팀 → 어느 안으로 갈지', ''),
            ('설계(와이어)', '흐름도 · 와이어', '기획자 · 개발자 → 화면 순서', ''),
            ('화면 완성', '디자인 시안 · 컴포넌트', '개발자 → 만들 화면', ''),
            ('테스트', '테스트 결과 · 문제 목록', '팀 → 무엇을 고칠지', '')]),
        ('Deliver', '좁혀서 완성', '#047857', '#D1FAE5', [
            ('개발 전달', '명세 · 주석', '개발자 → 그대로 구현', ''),
            ('출시·측정', '바뀐 점 공지 · 측정 결과', '사용자 · 팀 → 잘 됐는지', '')]),
    ]
    def dia(l, r, fg, bg):
        half = lambda t: (f'<div style="flex:1;display:grid;place-items:center;font-size:11px;font-weight:700;color:{fg}">{E(t)}</div>')
        return (f'<div style="position:relative;width:150px;height:60px">'
                f'<div style="position:absolute;left:52px;top:7px;width:46px;height:46px;transform:scale(2.2,.9) rotate(45deg);'
                f'background:{bg};border:1.5px solid {fg}"></div>'
                f'<div style="position:absolute;inset:0;display:flex">{half(l)}<div style="width:0;border-left:1.5px dashed {fg};margin:6px 0"></div>{half(r)}</div></div>')
    svg = (f'<div style="display:flex;justify-content:center;gap:4px;padding:8px 0 4px">'
           f'{dia("Discover", "Define", "#1D4ED8", "#DBEAFE")}{dia("Develop", "Deliver", "#047857", "#D1FAE5")}</div>'
           f'<div style="display:flex;justify-content:space-around;font-size:11px;color:{SUB};padding:4px 10px 6px">'
           '<span>넓힘 → 좁힘 (문제)</span><span>넓힘 → 좁힘 (해결)</span></div>')
    rows = ''
    for g, gk, fg, bg, stages in groups:
        rows += (f'<div style="margin:6px 8px 0;padding:3px 8px;border-radius:6px;background:{bg};color:{fg};font-weight:700;font-size:12px">'
                 f'{E(g)} · {E(gk)}</div>')
        for name, doc, who, date in stages:
            rows += (f'<div style="display:flex;gap:6px;margin:4px 8px 0 16px;padding:5px 7px;border:1px solid {LINE};border-left:3px solid {fg};border-radius:6px">'
                     f'<div style="flex:1"><b>{E(name)}</b><div style="font-size:12px;color:{INK}">📄 {E(doc)}</div>'
                     f'<div style="font-size:12px;color:{SUB}">👀 {E(who)}</div></div>'
                     f'<div style="font-size:11px;color:{SUB};white-space:nowrap">{E(date)}</div></div>')
    return (win('예시 — 다 만든 흐름 한 장', svg + rows + '<div style="height:8px"></div>', '캔버스')
            + caption('📄 그 단계에서 나오는 문서 · 👀 누가 읽고 무엇을 정하나 — 실무에서 흔한 예'))

# ───────────── 11/25 읽는 사람별 문서 3장 — 다 만든 예시
def _board(name, who, body):
    return (f'<div style="margin:6px 8px;border:1px solid #D1D5DB;border-radius:8px;background:#fff">'
            f'<div style="display:flex;justify-content:space-between;padding:4px 8px;background:#F3F4F6;border-bottom:1px solid {LINE};font-size:12px">'
            f'<b>{E(name)}</b><span style="color:{SUB}">읽는 사람: {E(who)}</span></div><div style="padding:6px 8px;font-size:12px">{body}</div></div>')
def _kv(rows):
    return ''.join(f'<div style="display:flex;gap:6px;padding:2px 0;border-bottom:1px dashed {LINE}"><span style="width:52px;color:{SUB}">{E(k)}</span><span style="flex:1">{v}</span></div>' for k, v in rows)
def _btn(t, bg='#E5484D', fg='#fff'):
    return f'<span style="display:inline-block;padding:3px 12px;border-radius:6px;background:{bg};color:{fg};font-weight:700;font-size:11px">{E(t)}</span>'

@mini('doc3_example')
def doc3_example():
    f = _board('foundation · 기초 값', '디자이너 · 개발자', _kv([
        ('색', f'{sw("E5484D")} 삭제 버튼 #E5484D · {sw("2B2B2B")} 알림 바탕 #2B2B2B'),
        ('글자', '제목 20 Bold · 본문 14 Regular · 버튼 14 Bold'),
        ('간격', '화면 여백 16 · 할 일 줄 사이 8 · 버튼 안쪽 12'),
        ('모서리', '버튼 8 · 확인창 12 · 알림 12')]))
    c = _board('components · button', '디자이너 / 개발자 칸을 나눔',
        f'<div style="font-weight:700;margin-bottom:2px">디자이너 칸</div>'
        + _kv([('언제', '되돌릴 수 없는 동작(삭제)에만 빨간 버튼'), ('안 쓸 때', '저장 · 확인 같은 보통 동작'),
               ('○ / ✕', f'○ {_btn("삭제")} &nbsp; ✕ {_btn("확인")} ← 무엇을 하는지 모름')])
        + f'<div style="font-weight:700;margin:6px 0 2px">개발자 칸</div>'
        + _kv([('기본', '바탕 #E5484D · 글자 #FFFFFF · 높이 40'), ('누름', '내 파일에 없으면 ‘없음’'), ('비활성', '내 파일에 없으면 ‘없음’')]))
    shot = lambda t: f'<div style="width:70px;height:96px;border:1px solid #9CA3AF;border-radius:6px;background:#F3F4F6;font-size:9px;color:{SUB};padding:3px">{E(t)}</div>'
    p = _board('patterns · 삭제 흐름', '새 팀원 · 기획자',
        f'<div style="display:flex;gap:6px;margin-bottom:4px">{shot("삭제-확인창 50%")}{shot("목록-삭제됨 50%")}</div>'
        + _kv([('규칙 1', '삭제는 바로 지우지 않고 확인창을 띄운다'), ('규칙 2', '지운 뒤 알림은 화면 아래 · 4초'), ('규칙 3', '되돌리기 → 원래 자리로 돌아온다')]))
    return (win('예시 — 다 만든 문서 3장 (흰 판 3개)', f + c + p + '<div style="height:4px"></div>', '캔버스')
            + caption('숫자는 예시다. 내 화면에서 레이어를 클릭해 오른쪽 Design 패널에서 읽은 값으로 적는다'))

@mini('discard_example')
def discard_example():
    d = (f'<div style="margin:10px auto;width:220px;border-radius:12px;background:#fff;border:1px solid #D1D5DB;padding:12px;box-shadow:0 2px 6px rgba(0,0,0,.1)">'
         f'<div style="font-weight:700;font-size:13px">수정한 내용을 버릴까요?</div>'
         f'<div style="font-size:11px;color:{SUB};margin:2px 0 10px">버리면 되돌릴 수 없어요.</div>'
         f'<div style="display:flex;gap:6px">{_btn("취소", "#E5E7EB", "#111")}{_btn("버리기")}</div></div>')
    return (win('만들 것 — 수정 취소 확인창 (삭제 확인창과 같은 모양)', d, '캔버스')
            + caption('색 · 글자 · 간격 · 모서리를 원래 화면이 아니라 문서 3장만 보고 고른다'))
