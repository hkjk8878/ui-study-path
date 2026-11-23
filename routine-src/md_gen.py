import validate, res, datetime as dt, os
WD='월화수목금토일'
def steps_md(s):
    out=[]; L=s.split('\n'); i=0; intable=False
    for x in L:
        if x.startswith('|'):
            if not intable:
                out.append(''); out.append(x); n=x.count('|')-1; out.append('|'+'---|'*n); intable=True
            else: out.append(x)
        else:
            if intable: out.append(''); intable=False
            out.append(x)
    return out
def block_md(b):
    o=[f"#### {b.t.replace('-','–')} · [{b.kind}] {b.title}",'']
    if b.why: o+= [f'**학습 목표:** {b.why}','']
    for k in b.res:
        if k in res.R:
            t,u,m=res.R[k]; o.append(f'- 자료: [{t}]({u}) · {m}')
    if b.res: o.append('')
    for i,s in enumerate(b.steps,1):
        L=steps_md(s)
        o.append(f'{i}. {L[0]}')
        for x in L[1:]: o.append('   '+x if x else '')
    o.append('')
    if b.out: o.append(f'- **결과물:** {b.out}')
    if b.chk: o.append(f'- **확인:** {b.chk}')
    if b.early: o.append(f'- **일찍 끝나면:** {b.early}')
    if b.guide: o.append(f'- **예시:** {b.guide}')
    o.append(''); return o
def week_md(w):
    d0=dt.date.fromisoformat(w.days[0].date); d1=dt.date.fromisoformat(w.days[-1].date)
    o=[f'## {w.n}주차 · {w.title}','',f'{d0.month}/{d0.day} – {d1.month}/{d1.day}','',w.goal,'']
    if w.hire: o+=[f'**채용 기준과의 연결** {w.hire}','']
    if w.outputs:
        o+=['**이번 주 결과물**','','| 결과물 | 확인 기준 |','|---|---|']+[f'| {a} | {b} |' for a,b in w.outputs]+['']
    for d in w.days:
        x=dt.date.fromisoformat(d.date)
        o+=[f'### {x.month}/{x.day} ({WD[x.weekday()]}) {d.title}','']
        for b in d.blocks: o+=block_md(b)
    return o
parts=[('1_개요·2주차',[2]),('1b_3주차',[3]),('2_4–6주차',[4,5,6]),('3_7–9주차',[7,8,9]),('4_10–12주차',[10,11,12]),('5_13–15주차',[13,14,15]),('6_16–18주차',[16,17,18]),('7_19–21주차',[19,20,21]),('8_22–24주차',[22,23,24])]
W={w.n:w for w in validate.WEEKS}
OUT='out_md'
os.makedirs(OUT,exist_ok=True)
allmd=['# UI/UX 취업 준비 24주 루틴 (2026-11-17판)','']
for name,ns in parts:
    o=[f'# UI/UX 24주 루틴 · {name.split("_",1)[1]}','','(2026-11-17판 · 앱 https://ui-study-path.hkjk8878.workers.dev/ 과 같은 내용)','']
    for n in ns: o+=week_md(W[n])
    if name.startswith('1_'):
        o=[open('overview.md').read().rstrip(),'','---','',open('naming_guide.md').read().replace('\n# ','\n## ',1),'']+o[4:]
    import re as _re
    open(f'{OUT}/UIUX_24주_루틴_20261117_{name}.md','w').write(_re.sub(r'그림:[a-z_]+', '[화면 그림 — 앱 · PDF에서 보기]', '\n'.join(o)))
    allmd+=o[4:]
open('UIUX_24주_루틴_20261109.md','w').write('\n'.join(allmd))
print('ok')
