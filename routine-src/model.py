from dataclasses import dataclass, field

@dataclass
class Block:
    t: str            # '08:00-09:10'
    kind: str         # 강의 / 제작 / 조사 / 분석 / 검증 / AI / 훈련 / 점검
    title: str
    res: tuple = ()   # 자료 키
    steps: tuple = ()
    out: str = ''
    chk: str = ''
    early: str = ''
    fig: str = ''     # 그림 키
    note: str = ''
    guide: str = ''
    why: str = ''

@dataclass
class Day:
    date: str   # '2026-11-09'
    title: str
    blocks: list

@dataclass
class Week:
    n: int
    title: str
    goal: str
    hire: str
    outputs: list   # [(결과물, 확인 기준)]
    days: list
    fig: str = ''
    phase: str = ''

def B(t, kind, title, res=(), steps=(), out='', chk='', early='', fig='', note=''):
    return Block(t, kind, title, tuple(res), tuple(steps), out, chk, early, fig, note)
