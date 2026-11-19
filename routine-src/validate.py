import datetime as dt, sys
from w02_04 import W02, W03, W04
from w05_12 import W05, W06, W07, W08, W09, W10, W11, W12
from w13_18 import W13, W14, W15, W16, W17, W18
from w19_24 import W19, W20, W21, W22, W23, W24
from res import R
import figplan
WEEKS=[W02,W03,W04,W05,W06,W07,W08,W09,W10,W11,W12,W13,W14,W15,W16,W17,W18,W19,W20,W21,W22,W23,W24]
figplan.apply(WEEKS)
import whyplan
whyplan.apply(WEEKS)
import clarify
clarify.apply(WEEKS)

def m(s):
    h,mi=s.split(':'); return int(h)*60+int(mi)

def block_minutes(b, weekend):
    a,z=[m(x) for x in b.t.split('-')]
    mins=z-a
    br=(14*60,14*60+10) if weekend else (10*60,10*60+10)
    if a<br[0] and z>br[1]: mins-=10
    if (a<br[1] and z>br[0]) and not (a<br[0] and z>br[1]) and not (a>=br[1] or z<=br[0]):
        return None  # 휴식과 일부만 겹침
    return mins

errs=[]; start=dt.date(2026,11,9)
total=0
for wi,w in enumerate(WEEKS):
    if w.n!=wi+2: errs.append(f'week number {w.n}')
    if len(w.days)!=7: errs.append(f'W{w.n} days {len(w.days)}')
    wk=0
    for di,d in enumerate(w.days):
        exp=start+dt.timedelta(days=wi*7+di)
        if d.date!=exp.isoformat(): errs.append(f'W{w.n} day{di} {d.date}!={exp}')
        weekend=exp.weekday()>=5
        day=0; ai=0; prev=None
        for b in d.blocks:
            a,z=[m(x) for x in b.t.split('-')]
            if b.kind=='AI':
                if (a,z)!=(22*60,23*60): errs.append(f'{d.date} AI time {b.t}')
                ai+=60; continue
            if prev is not None and a<prev:
                errs.append(f'{d.date} overlap {b.t}')
            if prev is not None:
                gap=a-prev
                okgap = gap==0 or (not weekend and prev==600 and a==610) or (weekend and ((prev==660 and a==780) or (prev==840 and a==850)))
                if not okgap: errs.append(f'{d.date} gap {prev}->{a} at {b.t}')
            prev=z
            bm=block_minutes(b,weekend)
            if bm is None: errs.append(f'{d.date} partial break overlap {b.t}')
            else: day+=bm
            for k in b.res:
                if k not in R: errs.append(f'{d.date} unknown res {k}')
            if not b.out: errs.append(f'{d.date} {b.t} no output')
            for s in b.steps:
                if len(s)<14: print('SHORT', w.n, d.date, b.t, repr(s))
        exp_day=230 if weekend else 170
        if day!=exp_day: errs.append(f'{d.date} work {day} != {exp_day}')
        wd=exp.weekday()
        if wd in (1,3) and ai!=60: errs.append(f'{d.date} missing AI')
        if wd not in (1,3) and ai: errs.append(f'{d.date} extra AI')
        wk+=day+ai
    if wk!=1430: errs.append(f'W{w.n} weekly {wk}')
    total+=wk
    for o,c in w.outputs:
        if not c: print('EMPTY OUTPUT CRIT', w.n, o)
print('\n'.join(errs) if errs else 'OK')
print('total work minutes', total, total/60, 'h; scheduled incl breaks', len(WEEKS)*25)
