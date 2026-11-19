"""PDF 루틴(2~24주)을 UI Study 앱 데이터로 변환한다. 1주차 날짜·기록 키는 건드리지 않는다."""
import json, base64, gzip, html, sys, datetime as dt, copy
import os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from validate import WEEKS
from res import R
from figures import FIG
from templates import fields as out_fields
from js_patch import patch as js_patch, forms_patch

E = html.escape
from stepfmt import fmt as EB
import forms as FORMS
REPO = sys.argv[1]
pay = json.loads(gzip.decompress(base64.b64decode(open(f'{REPO}/payload.txt').read().strip())))
old = pay['plan']; plan = copy.deepcopy(old)

CAT = {'강의': ('lesson', '강의'), '제작': ('build', '제작'), '조사': ('prep', '조사'), '분석': ('evidence', '분석'),
       '검증': ('practice', '검증'), 'AI': ('ai', 'AI 실습'), '훈련': ('practice', 'UI 완성도 훈련'), '점검': ('submit', '주간 점검')}
TD = 'padding:8px;text-align:left;vertical-align:top;border-bottom:1px solid #d4dfe7;overflow-wrap:anywhere;'
TH = TD + 'background:#eff5f9'

def mins(t):
    a, b = t.split('-'); f = lambda s: int(s[:2])*60+int(s[3:]); return f(a), f(b)

def sched(b, weekend, steps=None):
    steps = list(b.steps) if steps is None else steps
    out = []
    if getattr(b, 'why', ''):
        out.append(f'<section class="sx sx-why" style="background:#FFF7E6;border-left:4px solid #F59E0B;border-radius:6px;padding:8px 12px;margin:0 0 10px"><h4 style="margin:0 0 4px;color:#B45309">학습 목표</h4><p style="margin:0">{E(b.why)}</p></section>')
    if b.res:
        rows = ''.join(f'<tr><td style="{TD}"><a target="_blank" rel="noopener noreferrer" href="{E(R[k][1])}">{E(R[k][0])}</a></td><td style="{TD}">{E(R[k][2])}</td></tr>' for k in b.res)
        out.append(f'<section class="sx sx-res"><h4>강의·자료</h4><table style="width:100%;table-layout:fixed;border-collapse:collapse;margin:10px 0"><thead><tr><th style="{TH}">자료 · 제목을 누르면 열림</th><th style="{TH};width:34%">길이·범위</th></tr></thead><tbody>{rows}</tbody></table></section>')
    if steps:
        out.append('<section class="sx sx-steps"><h4>할 일</h4>' + ('<p>' + EB(steps[0]) + '</p>' if len(steps) == 1 else '<ol>' + ''.join(f'<li>{EB(s)}</li>' for s in steps) + '</ol>') + '</section>')
    if b.fig:
        fn, cap = FIG[b.fig]
        out.append(f'<figure class="study-example" aria-label="{E(cap)}"><figcaption><span class="example-kind">예시 그림</span>{E(cap)}</figcaption><div class="fig-scroll"><div class="fig-inner">{fn().svg().replace('style="display:block"','style="display:block;width:100%;height:auto;stroke:none;fill:#111827"',1)}</div></div></figure>')
    out.append(f'<section class="sx sx-out"><h4>결과물</h4><p>{E(b.out)}</p></section>')
    if b.chk: out.append(f'<section class="sx sx-chk"><h4>확인</h4><p>{E(b.chk)}</p></section>')
    if b.early: out.append(f'<section class="sx sx-early"><h4>일찍 끝나면</h4><p>{E(b.early)}</p></section>')
    if getattr(b,'guide',''): out.append(f'<section class="sx sx-note"><h4>예시</h4><p>{E(b.guide)}</p></section>')
    if b.note and not b.note.endswith('휴식을 포함한다.'): out.append(f'<section class="sx sx-note"><h4>참고</h4><p>{E(b.note)}</p></section>')
    a, z = mins(b.t); br = (840, 850) if weekend else (600, 610)
    if b.kind != 'AI' and a < br[0] and z > br[1]:
        out.insert(1 if getattr(b, 'why', '') else 0, f'<p class="sx-break">이 블록은 {"14:00" if weekend else "10:00"}–{"14:10" if weekend else "10:10"} 휴식 10분을 포함한다.</p>')
    return ''.join(out)

def minutes(b, weekend):
    a, z = mins(b.t); br = (840, 850) if weekend else (600, 610)
    return z - a - (10 if (b.kind != 'AI' and a < br[0] and z > br[1]) else 0)

def records(b):
    r = records_check(b) or {}
    r['output'] = out_fields(b.kind, b.out, b.title, getattr(b, 'when', ''))
    for t in getattr(b, 'extra_tables', ()):
        f = {'key': t['key'], 'label': t['t'], 'kind': 'table', 'columns': t['c'], 'example': t['ex'], 'rows': t['n'], 'tip': t['tip']}
        if t['fixed']: f['fixed'] = t['fixed']
        r['output'].append(f)
    return r

def records_check(b):
    if b.kind == 'AI':
        return {'general': [{'key': 'prompt', 'label': 'AI에 보낸 요청문(처음 보낸 글을 그대로 붙여 넣기, 다시 요청한 글은 아래에 이어서)', 'kind': 'text'},
                            {'key': 'status', 'label': '실행해서 기대 결과와 비교한 결과', 'kind': 'status'},
                            {'key': 'requests', 'label': '전체 요청 횟수', 'kind': 'number'},
                            {'key': 'fixes', 'label': '수정 요청 횟수', 'kind': 'number'},
                            {'key': 'minutesSpent', 'label': '걸린 시간(분)', 'kind': 'number'},
                            {'key': 'judgement', 'label': '직접 판단한 것과 확인하지 못한 것', 'kind': 'text'}]}
    if b.chk:
        return {'general': [{'key': 'status', 'label': '확인: ' + b.chk, 'kind': 'status'},
                            {'key': 'evidence', 'label': '실패했거나 고친 내용', 'kind': 'text'}]}
    return None

def attach(b):
    if b.kind == 'AI': return {'html': True, 'images': True}
    if b.kind in ('제작', '훈련', '검증', '분석', '조사'): return {'html': False, 'images': True}
    return None

PH = {'A': 'foundation', 'B': 'case01', 'C': 'case02', 'D': 'case03', 'E': 'submission'}
start = dt.date(2026, 11, 2)
days = plan['days']
assert days[7]['date'] == '2026-11-09'
for w in WEEKS:
    for di, d in enumerate(w.days):
        idx = (w.n-1)*7 + di
        date = dt.date.fromisoformat(d.date); assert days[idx]['date'] == d.date
        weekend = date.weekday() >= 5
        phase = 'case01' if w.n >= 5 and w.n <= 12 else PH[w.phase]
        blocks = []
        for bi, b in enumerate(d.blocks):
            cat, lab = CAT[b.kind]
            instr, sforms = FORMS.convert(b, d.date, None)
            blk = {'id': f'w{w.n:02d}d{di}b{bi}', 'label': b.title, 'time': b.t.replace('-', '–'), 'minutes': minutes(b, weekend),
                   'category': cat, 'categoryLabel': lab, 'instructions': instr, 'output': b.out,
                   'resourceKeys': list(b.res), 'scheduleHtml': sched(b, weekend, instr), 'acceptance': b.chk}
            rs = records(b)
            import forms2 as FORMS2
            fk = (d.date[5:], b.t[:5])
            if (d.date >= '2026-11-20' or d.date == '2026-11-19') and fk in FORMS2.FORMS:
                sforms = (sforms or []) + FORMS2.FORMS[fk]
            if d.date >= '2026-11-20' and b.title.startswith('주간 기록') and rs:
                import re as _re
                first = b.steps[0] if b.steps else ''
                parts = [p.strip(' .') for p in _re.split(r',\s*', first.split('을 확인한다')[0].split('.')[0]) if p.strip()]
                third = next((p for p in parts if '다음 주' in p), '다음 주에 준비할 것').replace('을 적는다', '').replace('를 적는다', '')
                for f in rs.get('output', []):
                    if f['label'] == '주간 기록' and f['columns'] == ['항목', '내용']:
                        f['fixed'] = ['실제 걸린 시간 · 넘친 블록', '못 끝낸 것', third, '이름 점검 결과']
                        f['rows'] = 4
                        f['tip'] = '채용 기준 칸과 사례에 쓸 결정 4줄은 앱 ‘주간 회고’에 적는다'
            if sforms:
                rs = rs or {}
                extra = [f for f in rs.get('output', []) if f['key'] not in [x['key'] for x in out_fields(b.kind, b.out, b.title, getattr(b, 'when', ''))]]
                rs['output'] = sforms + extra
            if rs: blk['recordSections'] = rs
            at = attach(b)
            if at: blk['attachments'] = at
            blocks.append(blk)
        days[idx] = {'date': d.date, 'weekday': '월화수목금토일'[date.weekday()], 'week': w.n, 'phase': phase, 'title': d.title, 'blocks': blocks}
    wk = plan['weeks'][w.n-1]
    outs = ' / '.join(o for o, c in w.outputs)
    crit = ' / '.join(f'{o}: {c}' for o, c in w.outputs)
    res_keys = []
    for d in w.days:
        for b in d.blocks:
            for k in b.res:
                if k not in res_keys: res_keys.append(k)
    wk.update({'title': w.title, 'phase': 'case01' if 5 <= w.n <= 12 else PH[w.phase], 'output': outs, 'purpose': w.hire,
               'coreOutput': w.goal, 'qualityCriterion': crit, 'reviewChecklist': [f'{o} — {c}' for o, c in w.outputs],
               'evidenceMap': w.hire, 'resources': res_keys, 'aiResources': ['pair', 'ms_hai'], 'learningGuide': None, 'feedback': None,
               'aiOutput': ' / '.join(b.title for d in w.days for b in d.blocks if b.kind == 'AI')})

# resources: 기존 목록 유지 + 새 키 추가(같은 키는 새 값으로)
existing = {r['key']: r for r in plan['resources']}
for k, (name, url, ln) in R.items():
    existing[k] = {'key': k, 'title': name, 'url': url, 'note': ln, 'kind': existing.get(k, {}).get('kind', 'doc')}
plan['resources'] = list(existing.values())

ph = {p['id']: p for p in plan['phases']}
ph['foundation'].update({'label': 'Figma 집중 · ‘하루’', 'short': '컴포넌트·변수·디자인 시스템·전달', 'endWeek': 4, 'end': '2026-11-29'})
ph['case01'].update({'label': 'CASE01 · 학원 직원의 실제 업무 개선', 'short': '실제 조사 → 출시 → 전후 측정'})
ph['case02'].update({'label': 'CASE02 · 콘텐츠·소비자 과업 개선', 'short': '경쟁 리뷰 → 앱·웹 UI → 동작 링크'})
ph['case03'].update({'label': 'CASE03 · 상태 이해와 오류 복구 인터랙션', 'short': '모션 명세 → 동작 링크·영상 → 테스트', 'endWeek': 21, 'end': '2027-03-28'})
ph['submission'].update({'label': '사이트·과제형 연습·지원', 'short': '포트폴리오 사이트 · 과제 · 이력서 · 지원', 'startWeek': 22, 'start': '2027-03-29'})

plan['gates'] = [
 {'id': 'g1', 'date': '2026-11-29', 'title': '‘하루’ 기초 완료 + CASE01 준비', 'check': '컴포넌트·변수·문서화·전달 명세, 조사 계획·질문지·세션 일정'},
 {'id': 'g2', 'date': '2026-12-13', 'title': 'CASE01 문제 정의 확정', 'check': '인터뷰 3·관찰 2, 원문 카드, 기준선, 문제 정의·성공 기준'},
 {'id': 'g3', 'date': '2027-01-15', 'title': '학원 도구에 실제 출시', 'check': '전달 명세·검증표 통과·직원 안내·측정 시작'},
 {'id': 'g4', 'date': '2027-01-24', 'title': 'CASE01 1차 완료', 'check': '출시 후 측정·사례 페이지·7분 발표·외부 피드백'},
 {'id': 'g5', 'date': '2027-02-23', 'title': 'CASE02 동작 링크 배포', 'check': '찜·이어보기 상태 동작, 모바일 확인'},
 {'id': 'g6', 'date': '2027-03-07', 'title': 'CASE02 1차 완료', 'check': '사례 페이지·전달 명세·두 사례 연속 발표'},
 {'id': 'g7', 'date': '2027-03-28', 'title': 'CASE03 완료', 'check': '모션 명세·동작 링크·시연 영상·테스트·사례 페이지'},
 {'id': 'g8', 'date': '2027-04-04', 'title': '포트폴리오 사이트·PDF판', 'check': '배포·외부 리뷰 2명 반영·기기별 확인'},
 {'id': 'g9', 'date': '2027-04-13', 'title': '지원 시작', 'check': '과제형 연습·이력서·모의 면접·공고별 맞춤 지원'}]

plan['deliverables'] = {
 'foundation': [{'title': '‘하루’ 컴포넌트·Variants·상호작용', 'week': 2}, {'title': '변수 3층 구조·텍스트 스타일·기초 문서', 'week': 3}, {'title': '사용 규칙·모션 2개·개발 전달 명세', 'week': 4}, {'title': 'CASE01 조사 계획·질문지 v2·세션 일정', 'week': 4}],
 'case01': [{'title': '인터뷰 3·관찰 2 원문 카드 + 기준선', 'week': 5}, {'title': '어피니티·문제 정의·성공 기준', 'week': 6}, {'title': '해결안 12개+·평가·A/B 와이어', 'week': 7}, {'title': 'A/B 비교 테스트·선택 기록', 'week': 8},
            {'title': '고해상도 UI·상태·접근성·크리틱', 'week': 9}, {'title': '사용성 테스트 3~5명·수정·재확인', 'week': 10}, {'title': '학원 도구 실제 반영·검증표·출시', 'week': 11}, {'title': '출시 후 측정·사례 페이지·7분 발표', 'week': 12}],
 'case02': [{'title': '후보 비교·경쟁 리뷰·모집', 'week': 13}, {'title': '조사 5~6회·문제 정의·기준선', 'week': 14}, {'title': '탐색·A/B·비교 테스트·선택', 'week': 15}, {'title': '앱·웹 고해상도 UI·크리틱', 'week': 16},
            {'title': '동작 링크 배포·테스트·수정', 'week': 17}, {'title': '사례 페이지·전달 명세·발표', 'week': 18}],
 'case03': [{'title': '상태 다이어그램·정적 대안·모션 명세', 'week': 19}, {'title': '동작 링크·시연 영상·모션 줄이기', 'week': 20}, {'title': '테스트·수정·사례 페이지', 'week': 21}],
 'submission': [{'title': '포트폴리오 사이트·PDF판·외부 리뷰', 'week': 22}, {'title': '과제형 연습 3일·이력서·모의 면접', 'week': 23}, {'title': '최종 점검·지원 5곳 이상·다음 4주 계획', 'week': 24}]}

pg = plan.get('projectProductionGuides', {})
pg['case01'] = {**pg.get('case01', {}), 'period': '4주 목 준비 / 5–12주 조사·설계·테스트·실제 출시 / 19–21주 평일 첫 시간 보완',
                'production': [f'{w.n}주: {w.title.split("·",1)[-1].strip()} — {w.goal}' for w in WEEKS if 5 <= w.n <= 12]}
pg['case02'] = {**pg.get('case02', {}), 'period': '13–18주 / 19–21주 평일 첫 시간 보완',
                'production': [f'{w.n}주: {w.title.split("·",1)[-1].strip()} — {w.goal}' for w in WEEKS if 13 <= w.n <= 18]}
pg['case03'] = {**pg.get('case03', {}), 'period': '19–21주',
                'production': [f'{w.n}주: {w.title.split("·",1)[-1].strip()} — {w.goal}' for w in WEEKS if 19 <= w.n <= 21]}
plan['projectProductionGuides'] = pg

_je = [j for j in (plan.get('jobEvidence') or []) if j.get('resource') != 'toss_bank']  # 실행할 때마다 쌓이던 중복 제거
plan['jobEvidence'] = _je + [
 {'company': '토스뱅크', 'role': 'Product Designer (신입 전형, 2026.9 게시)', 'scope': '디자인 경력 2년 이하',
  'facts': '정량·정성 사용자 데이터로 제품을 개선한 경험, 설계·출시 또는 피드백 경험, 정보 위계를 고려한 시각적 완성도. 대표 프로젝트 2개, 면접에서 2개 사례를 깊게.',
  'interpretation': 'CASE01·02를 대표로, 기준선 측정·실제 출시·고해상도 UI를 보강.', 'resource': 'toss_bank'}]
plan['executionPolicy'] = '월–금 08:00–11:00(휴식 10:00–10:10), 토·일 09:00–11:00·13:00–15:00(휴식 14:00–14:10), 화·목 AI 22:00–23:00. 주 25시간 배정, 작업 23시간 50분. 2–24주 작업 합계 548시간 10분.'
plan['aiPolicy'] = '화·목 저녁 46회. 만드는 것을 정하고 요청문은 직접 쓰며, 실행해 기대 결과와 비교하고 전체 요청·수정 요청 횟수와 시간을 기록한다. 실제 이름·학생 정보는 AI에 올리지 않는다.'
m = plan['meta']
m.update({'source': 'UIUX_24주_루틴_20261108.pdf', 'sourceVersion': '2026-11-08', 'revision': '2026-11-08-routine',
          'status': '2–24주 일별 루틴(109쪽 PDF)과 일치. 1주차는 기존 기록 유지', 'taskHours': 548.17 + 0, 'breakHours': 26.83})
plan['researchCheckedAt'] = '2026-11-08'

pay['plan'] = plan
pay['js'] = forms_patch(js_patch(pay['js']))
css = pay['css']
mk = '/* READABILITY-OVERRIDE'
if mk in css: css = css[:css.index(mk)].rstrip('\n')
pay['css'] = css + '\n' + open(os.path.join(HERE, 'readability.css')).read()
raw = json.dumps(pay, ensure_ascii=False, separators=(',', ':')).encode()
open(f'{REPO}/payload.txt', 'w').write(base64.b64encode(gzip.compress(raw, 9)).decode())
json.dump(plan, open(f'{REPO}/data/plan-final.json', 'w'), ensure_ascii=False, indent=1)
print('ok', len(plan['days']), sum(len(d['blocks']) for d in plan['days'][7:]))
