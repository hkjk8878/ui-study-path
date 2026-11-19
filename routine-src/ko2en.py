# 한국어로 옮겨 쓴 Figma·개발 용어를 ‘원래 말 [뜻]’로 바꾼다 — 블록마다 처음 나올 때 한 번
import re
K = [  # (한국어, 원래 말) — 긴 것부터
 ('CSS 변수', 'CSS variable'), ('의미 변수', 'Semantic variable'), ('기본값 변수', 'Primitive variable'), ('숫자 변수', 'Number variable'),
 ('색 변수', 'Color variable'), ('텍스트 스타일', 'Text style'), ('글자 스타일', 'Text style'), ('효과 스타일', 'Effect style'),
 ('상호작용 컴포넌트', 'Interactive component'), ('열 그리드', 'Layout guide'), ('발표 모드', 'Present'), ('버전 기록', 'Version history'),
 ('내보내기', 'Export'), ('댓글', 'Comment'), ('주석', 'Annotation'), ('오토 레이아웃', 'Auto layout'), ('인스턴스', 'Instance'),
 ('변수', 'Variable'), ('참조', 'Alias'), ('속성', 'Property'),
]
_pat = re.compile('|'.join(r'(?<![가-힣A-Za-z\[])' + re.escape(k) for k, _ in K))
_en = dict(K)

def apply(steps):
    seen = set(); out = []
    blob = '\n'.join(steps)
    for s0 in steps:
        lines = []
        for s in s0.split('\n'):
            if s.strip().startswith(('|', '“')):
                lines.append(s); continue
            def rep(m, s=s):
                k = m.group(0); e = _en[k]
                if k in seen or e in seen: return k
                seen.add(k); seen.add(e)
                if e.lower() in s.lower(): return k   # 같은 줄에 이미 원래 말이 있으면 그대로
                if k == '원본' and re.match(r'\s*(파일|기록|자료|문서|데이터)', s[m.end():]): return k
                return f'{e} [{k}]'
            lines.append(_pat.sub(rep, s))
        out.append('\n'.join(lines))
    return tuple(out)

_kv = re.compile(r'^· ([^:|]{1,22}): (.+)$')
def kv_tables(steps):
    """‘· 이름: 설명’ 줄이 2개 이상 이어지면 표로 바꾼다"""
    out = []
    for s0 in steps:
        lines = s0.split('\n'); res = []; run = []
        def flush():
            if len(run) >= 2:
                res.append('| 항목 | 내용 |')
                res.extend(f'| {a} | {b.replace("|", "/")} |' for a, b in run)
            else:
                res.extend(f'· {a}: {b}' for a, b in run)
            run.clear()
        for ln in lines:
            m = _kv.match(ln)
            if m: run.append((m.group(1), m.group(2)))
            else: flush(); res.append(ln)
        flush(); out.append('\n'.join(res))
    return tuple(out)
