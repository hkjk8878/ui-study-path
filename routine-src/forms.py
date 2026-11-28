# 할 일 안의 '적어 넣는 표'를 앱의 결과물 기입표로 옮긴다.
# PDF·MD에는 표를 그대로 두고, 앱에서는 할 일에 안내 한 줄만 남긴다.
import re

SKIP_FIRST = ('순서', '이름', '용어', '좋은 카드', '점수', '어디', '무엇', '기준', '칸')
START = '2026-11-20'
EXTRA_DAYS = {('2026-11-19', '08:00'), ('2026-11-19', '08:15'), ('2026-11-19', '09:00'), ('2026-11-19', '10:10'), ('2026-11-19', '22:00')}

def _cells(line):
    return [re.sub(r'\s*\[[^\]]*\]', '', c).strip() for c in line.strip().strip('|').split('|')]

def _is_form(head, rows):
    h0 = head[0]
    if head == ['적을 것', '예']:
        return True
    if any(h0.startswith(s) for s in SKIP_FIRST) and h0 not in ('칸',):
        return False
    if h0 == '칸':
        return any(any(c == '' for c in r[1:]) for r in rows)
    if any(any(c == '' for c in r[1:]) for r in rows):
        return True
    return len(rows) == 1 and len(head) >= 2

def convert(b, date, base_fields):
    """returns (instructions, fields or None)"""
    key = (date, b.t[:5])
    if not (date >= START or key in EXTRA_DAYS):
        return list(b.steps), None
    out_steps, forms = [], []
    for s in b.steps:
        lines = s.split('\n'); new = []; i = 0
        while i < len(lines):
            if lines[i].startswith('|'):
                j = i
                while j < len(lines) and lines[j].startswith('|'): j += 1
                tbl = [_cells(l) for l in lines[i:j]]
                head, rows = tbl[0], tbl[1:]
                if rows and _is_form(head, rows):
                    cap = ''
                    if new and not new[-1].startswith(('·', '|', '작업:', '→')) and len(new[-1]) <= 40:
                        cap = new[-1]
                        if not re.match(r'^(\d단계|기록 \()', cap):
                            new.pop()
                    label = (cap or b.title).split(' (')[0].rstrip(':').strip()
                    label = re.sub(r'^\d단계\s*', '', label)
                    if head == ['적을 것', '예']:
                        label = 'AI 활용 기록'
                        f = {'key': 'airec', 'label': label, 'kind': 'table', 'columns': ['적을 것', '내용'],
                             'example': ['', ''], 'rows': len(rows), 'tip': ' · '.join(f'{r[0]}: {r[1]}' for r in rows),
                             'fixed': [r[0] for r in rows]}
                        forms.append(f)
                        new.append('→ 아래 ‘결과물 기입표’의 「AI 활용 기록」에 적는다')
                        i = j
                        continue
                    filled = [r for r in rows if all(c for c in r)]
                    blank = [r for r in rows if not all(c for c in r[1:])]
                    ex = filled[0] if filled else [''] * len(head)
                    f = {'key': f'st{len(forms)+1}', 'label': label, 'kind': 'table', 'columns': head,
                         'example': ex, 'rows': 5, 'tip': ''}
                    if len(blank) >= 2 and all(r[0] for r in rows):
                        f['fixed'] = [r[0] for r in rows]
                        f['rows'] = len(rows)
                    forms.append(f)
                    new.append(f'→ 아래 ‘결과물 기입표’의 「{label}」에 적는다' + (' (예시 한 줄 있음)' if filled else ''))
                else:
                    new.extend(lines[i:j])
                i = j
            else:
                new.append(lines[i]); i += 1
        out_steps.append('\n'.join(new))
    if not forms:
        return list(b.steps), None
    return out_steps, forms
