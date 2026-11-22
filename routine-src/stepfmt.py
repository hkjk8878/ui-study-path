# 할 일 글 → HTML
# - '| 순서 | … |' 표 → 단계 카드 (한 줄에 동작 하나, ‘성공’ 줄은 ✓ 강조)
# - '| Frame | Auto layout 방향 | … |' 표 → 완성 구조 그림 (안팎으로 겹친 상자)
# - 그 밖의 표 → 가로로 밀어 볼 수 있는 표 (칸이 좁아 글자가 한 자씩 꺾이지 않게)
# - 'N단계 …' 줄 → 소제목
import html, re
E = html.escape
TD = 'style="border:1px solid #D1D5DB;padding:6px 8px;vertical-align:top;text-align:left;min-width:7em;line-height:1.5"'
TH = 'style="border:1px solid #D1D5DB;padding:6px 8px;background:#F3F4F6;text-align:left;font-weight:700;min-width:7em;white-space:nowrap"'
TIME = re.compile(r'\s*\((\d+)분\)\s*$')
STAGE = re.compile(r'^(\d+단계)\s*(.*)$')

def split_arrows(s):
    """괄호 밖의 ‘ → ’로만 나눈다."""
    out, buf, depth, i = [], '', 0, 0
    while i < len(s):
        c = s[i]
        if c in '(（[': depth += 1
        elif c in ')）]': depth = max(0, depth - 1)
        if depth == 0 and s.startswith(' → ', i):
            out.append(buf.strip()); buf = ''; i += 3; continue
        buf += c; i += 1
    if buf.strip(): out.append(buf.strip())
    return out

def merge(parts, short=16):
    """짧은 동작(‘Esc’, ‘Shift+A’)은 앞뒤와 한 줄로 묶어 줄 수를 줄인다. ‘성공’ 줄은 따로 둔다."""
    out = []
    for p in parts:
        if out and '성공' not in p and '성공' not in out[-1] and (len(out[-1]) < short or len(p) < 8) and len(out[-1]) + len(p) < 46:
            out[-1] += ' → ' + p
        else:
            out.append(p)
    return out

def cells(r):
    return [c.strip() for c in r.strip().strip('|').split('|')]

def step_cards(rows):
    head = cells(rows[0])
    h = '<div class="step-cards" style="display:flex;flex-direction:column;gap:10px;margin:8px 0">'
    for r in rows[1:]:
        c = cells(r)
        if not c or not c[0]: continue
        num, body = c[0], c[-1]
        title = c[1] if len(c) >= 3 else ''
        m = TIME.search(body); mins = ''
        if m: mins = m.group(1) + '분'; body = body[:m.start()]
        acts = merge(split_arrows(body))
        li = ''
        for a in acts:
            ok = '성공' in a
            st = 'color:#166534;font-weight:700' if ok else ''
            mark = '✓ ' if ok else ''
            li += f'<li style="margin:2px 0;{st}">{mark}{E(a)}</li>'
        badge = f'<span style="margin-left:auto;font-size:.85em;color:#6B7280;white-space:nowrap">{mins}</span>' if mins else ''
        tt = f'<b style="font-size:1.02em">{E(title)}</b>' if title else ''
        h += ('<div style="border:1px solid #D1D5DB;border-radius:10px;padding:10px 12px;background:#fff">'
              f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:4px"><span style="display:inline-grid;place-items:center;min-width:26px;height:26px;border-radius:13px;background:#1F2937;color:#fff;font-weight:700">{E(num)}</span>{tt}{badge}</div>'
              f'<ol style="margin:0;padding-left:1.4em;line-height:1.6">{li}</ol></div>')
    return h + '</div>'

def _base(name):
    return re.sub(r'\s*\(.*?\)\s*$', '', name).strip()

def structure(rows):
    head = cells(rows[0])
    data = [cells(r) for r in rows[1:]]
    idx = {k: i for i, k in enumerate(head)}
    ci = idx.get('안에 들어가는 것', len(head) - 1)
    nodes = []
    for c in data:
        names = [_base(x) for x in _base(c[0]).split(' · ')] if ' · ' in _base(c[0]) else [_base(c[0])]
        nodes.append({'label': c[0], 'names': names, 'dir': c[1] if len(c) > 1 else '', 'w': c[2] if len(c) > 2 else '',
                      'h': c[3] if len(c) > 3 else '', 'kids': c[ci] if len(c) > ci else ''})
    byname, allnames = {}, {}
    for n in nodes:
        for nm in n['names']: allnames[nm] = n
    for n in nodes:
        for nm in n['names']: byname.setdefault(nm, n)
    used = set()
    def find(item):
        b = _base(item)
        b = re.sub(r'^.*?(\S+)\s*\d+개$', r'\1', b)  # ‘행 4개’ → 행
        for nm, n in byname.items():
            if b == nm or b.startswith(nm + ' ') or b.endswith(' ' + nm): return n
        return None
    def box(n, depth):
        used.add(id(n))
        for nm in n['names']:
            byname.pop(nm, None)
        kids = ''
        for it in [x for x in n['kids'].split(' · ') if x.strip()]:
            k = find(it)
            if k is not None and id(k) not in used and depth < 6:
                kids += box(k, depth + 1)
            elif k is None and _base(it) in allnames:
                continue  # 같은 상자에 이미 이름이 들어 있음(맞는-예 · 틀린-예)
            else:
                kids += f'<span style="display:inline-block;margin:3px 4px 0 0;padding:2px 8px;border-radius:12px;background:#F3F4F6;border:1px dashed #9CA3AF;font-size:.88em">{E(it.strip())}</span>'
        col = ['#2563EB', '#16A34A', '#D97706', '#9333EA', '#DB2777', '#0891B2'][depth % 6]
        arrow = '↓' if '↓' in n['dir'] or 'Vertical' in n['dir'] else ('→' if '→' in n['dir'] or 'Horizontal' in n['dir'] else '')
        flex = 'column' if arrow == '↓' else 'row'
        meta = ' · '.join(x for x in [n['dir'], 'W ' + n['w'] if n['w'] else '', 'H ' + n['h'] if n['h'] else ''] if x)
        return (f'<div style="border:2px solid {col};border-radius:8px;padding:6px 8px;margin:4px 0;background:#fff;min-width:0">'
                f'<div style="font-weight:700;color:{col}">{E(n["label"])} <span style="font-size:1.1em">{arrow}</span></div>'
                f'<div style="font-size:.82em;color:#4B5563;margin-bottom:4px">{E(meta)}</div>'
                f'<div style="display:flex;flex-direction:{flex};flex-wrap:wrap;gap:4px;align-items:flex-start">{kids}</div></div>')
    roots = ''.join(box(n, 0) for n in nodes if id(n) not in used)
    return ('<figure style="margin:8px 0;padding:10px;border:1px solid #E5E7EB;border-radius:10px;background:#F9FAFB">'
            '<figcaption style="font-weight:700;margin-bottom:6px">완성 구조 그림 — 다 만들면 이렇게 겹쳐 있다 (↓ 세로 · → 가로)</figcaption>'
            f'<div style="overflow-x:auto">{roots}</div></figure>')

def row_cards(rows):
    head = cells(rows[0])
    h = '<div style="display:flex;flex-direction:column;gap:8px;margin:6px 0">'
    for r in rows[1:]:
        c = cells(r)
        h += '<div style="border:1px solid #D1D5DB;border-radius:10px;padding:8px 12px;background:#fff">'
        h += f'<div style="font-weight:800;margin-bottom:4px">{E(c[0])}</div>'
        for k, v in zip(head[1:], c[1:]):
            if v: h += f'<div style="margin:3px 0;line-height:1.5"><span style="display:inline-block;font-size:.82em;color:#4B5563;background:#F3F4F6;border-radius:6px;padding:0 6px;margin-right:6px">{E(k)}</span>{E(v)}</div>'
        h += '</div>'
    return h + '</div>'

def table(rows):
    h = '<div style="overflow-x:auto;margin:6px 0"><table style="border-collapse:collapse;font-size:.95em;min-width:100%">'
    for i, r in enumerate(rows):
        tag, st = ('th', TH) if i == 0 else ('td', TD)
        h += '<tr>' + ''.join(f'<{tag} {st}>{E(c)}</{tag}>' for c in cells(r)) + '</tr>'
    return h + '</table></div>'

def fmt(text):
    out, rows = [], []
    def flush():
        if not rows: return
        head = cells(rows[0])
        if head and head[0] == '순서' and len(rows) > 1:
            out.append(step_cards(rows))
        elif head and head[0] == 'Frame' and any('Auto layout' in x for x in head):
            out.append(structure(rows))
        elif len(head) >= 4 and len(rows) > 1:
            out.append(row_cards(rows))
        else:
            out.append(table(rows))
        rows.clear()
    for line in text.split('\n'):
        if line.strip().startswith('|'):
            rows.append(line)
        else:
            flush()
            m = STAGE.match(line.strip())
            if m:
                out.append(f'<div style="font-weight:800;font-size:1.05em;margin:12px 0 2px;padding-top:6px;border-top:2px solid #E5E7EB">{E(m.group(1))} <span style="font-weight:600">{E(m.group(2))}</span></div>')
            elif line.strip().startswith('만들 구조'):
                continue  # 구조 그림이 제목을 대신한다
            else:
                out.append(E(line) + '<br>')
    flush()
    s = ''.join(out)
    return s[:-4] if s.endswith('<br>') else s
