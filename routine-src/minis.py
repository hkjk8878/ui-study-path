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
