import datetime as dt, html, sys
from validate import WEEKS
from res import R
from figures import FIG
import templates as TPL

E = html.escape
from stepfmt import fmt as EB
WD = '월화수목금토일'
KIND = {'강의': ('#1D4ED8', '#DBEAFE'), '제작': ('#047857', '#D1FAE5'), '조사': ('#0F766E', '#CCFBF1'), '분석': ('#6D28D9', '#EDE9FE'),
        '검증': ('#B45309', '#FEF3C7'), 'AI': ('#4338CA', '#E0E7FF'), '훈련': ('#BE185D', '#FCE7F3'), '점검': ('#374151', '#E5E7EB')}
PHASE = {'A': ('Figma 집중', '#2563EB'), 'B': ('CASE01 학원 업무 개선', '#16A34A'), 'C': ('CASE02 콘텐츠·소비자 과업', '#7C3AED'),
         'D': ('CASE03 인터랙션', '#D97706'), 'E': ('사이트·과제형·지원', '#374151')}
fig_no = [0]

def d2(s):
    d = dt.date.fromisoformat(s); return d, f'{d.month}/{d.day}', WD[d.weekday()]

def figure(key):
    fn, cap = FIG[key]; fig_no[0] += 1
    return f'<figure class="fig"><div class="figbox">{fn().svg()}</div><figcaption><b>그림 {fig_no[0]}</b> {E(cap)}</figcaption></figure>'

def mins(t):
    a, b = t.split('-'); h1, m1 = map(int, a.split(':')); h2, m2 = map(int, b.split(':')); return h1*60+m1, h2*60+m2

def block_html(b, weekend):
    fg, bg = KIND[b.kind]
    a, z = mins(b.t)
    br = (840, 850) if weekend else (600, 610)
    inc = a < br[0] and z > br[1]
    t = b.t.replace('-', '–')
    res = ''
    if b.res:
        items = []
        for k in b.res:
            name, url, ln = R[k]
            items.append(f'<div class="res"><span class="rk">자료</span><a href="{E(url)}">{E(name)}</a><span class="len">{E(ln)}</span></div>')
        res = ''.join(items)
    steps = ''
    if b.steps:
        if len(b.steps) == 1:
            steps = f'<p class="st">{EB(b.steps[0])}</p>'
        else:
            steps = '<div class="st">' + ''.join(f'<div style="margin:0 0 8px">{EB(x)}</div>' for x in b.steps) + '</div>'
    if getattr(b, 'show_fixed', False):
        for f in TPL.fields(b.kind, b.out, b.title, getattr(b, 'when', '')):
            if f.get('fixed'):
                tip = f'<div class="fxt">{E(f["tip"])}</div>' if f.get('tip') else ''
                steps += f'<div class="fx"><div class="fxh">표 ‘{E(f["label"])}’</div><ul>' + ''.join(f'<li>{E(x)}</li>' for x in f['fixed']) + f'</ul>{tip}</div>'
            elif f.get('tip') and f['key'] != 'out':
                steps += f'<div class="fx"><div class="fxh">표 ‘{E(f["label"])}’</div><div class="fxt">{E(f["tip"])}</div></div>'
    rows = []
    if b.out: rows.append(('결과물', b.out, 'o'))
    if b.chk: rows.append(('확인', b.chk, 'c'))
    if b.early: rows.append(('일찍 끝나면', b.early, 'e'))
    if b.guide: rows.append(('예시', b.guide, 'n'))
    if b.note and not b.note.endswith('휴식을 포함한다.'): rows.append(('참고', b.note, 'n'))
    meta = ''.join(f'<div class="mrow {c}"><span class="ml">{E(l)}</span><span class="mv">{E(v)}</span></div>' for l, v, c in rows)
    incl = f'<div class="incl">{"10:00" if not weekend else "14:00"} 휴식 10분 포함</div>' if inc else ''
    fightml = figure(b.fig) if b.fig else ''
    why = f'<div class="why"><span class="wyl">학습 목표</span>{E(b.why)}</div>' if b.why else ''
    return (f'<div class="bf"><div class="blk"><div class="bl"><div class="bt">{t}</div><span class="tag" style="color:{fg};background:{bg}">{E(b.kind)}</span>{incl}</div>'
            f'<div class="br"><div class="bh">{E(b.title)}</div>{why}{res}{steps}{meta}</div></div>{fightml}</div>')

def break_row(t):
    return f'<div class="brk"><span>{t}</span> 휴식</div>'

def day_html(d):
    date, md, wd = d2(d.date)
    weekend = date.weekday() >= 5
    out = [f'<div class="day"><div class="dh"><span class="dd">{md} ({wd})</span><span class="dt">{E(d.title)}</span></div>']
    prev = None
    for b in d.blocks:
        a, z = mins(b.t)
        if b.kind != 'AI' and prev is not None and a > prev:
            if not weekend and prev == 600: out.append(break_row('10:00–10:10'))
            elif weekend and prev == 840: out.append(break_row('14:00–14:10'))
            elif weekend and prev == 660: out.append('<div class="lunch">11:00–13:00 쉬는 시간</div>')
        if b.kind == 'AI':
            out.append('<div class="ai-sep">저녁</div>')
        out.append(block_html(b, weekend))
        if b.kind != 'AI': prev = z
    out.append('</div>')
    return ''.join(out)

def week_html(w):
    d0, md0, _ = d2(w.days[0].date); d1, md1, _ = d2(w.days[-1].date)
    ph, pc = PHASE[w.phase]
    outs = ''.join(f'<tr><td class="on">{E(o)}</td><td>{E(c)}</td></tr>' for o, c in w.outputs)
    summ = ''.join(f'<tr><td class="sd">{d2(d.date)[1]} {d2(d.date)[2]}</td><td>{E(d.title)}</td></tr>' for d in w.days)
    note = getattr(w, 'note', '')
    nb = f'<div class="wnote">{E(note)}</div>' if note else ''
    figtop = figure(w.fig) if w.fig else ''
    return (f'<section class="week" id="w{w.n:02d}"><div class="wtop"><span class="phase" style="background:{pc}">{E(ph)}</span>'
            f'<span class="wdate">{md0} – {md1} · 25시간</span></div>'
            f'<h1 class="wt"><span class="wn">{w.n}주차</span> {E(w.title)}</h1>'
            f'<p class="goal">{E(w.goal)}</p>'
            f'<div class="hire"><div class="hl">채용 기준과의 연결</div><div>{E(w.hire)}</div></div>{nb}'
            f'<div class="two"><div><div class="sh">이번 주 결과물</div><table class="otab"><thead><tr><th>결과물</th><th>확인 기준</th></tr></thead><tbody>{outs}</tbody></table></div>'
            f'<div><div class="sh">요일별 작업</div><table class="stab"><tbody>{summ}</tbody></table></div></div>{figtop}'
            + ''.join(day_html(d) for d in w.days) + '</section>')

CSS = open('style.css').read()

def front(toc_pages):
    from front import FRONT
    return FRONT(toc_pages, figure)

def build(toc_pages=None):
    fig_no[0] = 0
    body = front(toc_pages or {}) + ''.join(week_html(w) for w in WEEKS)
    return f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>UI/UX 취업 준비 24주 루틴</title><style>{CSS}</style></head><body>{body}</body></html>'

if __name__ == '__main__':
    import json
    toc = json.load(open(sys.argv[1])) if len(sys.argv) > 1 else {}
    open('plan.html', 'w').write(build(toc))
    print('figures', fig_no[0])
