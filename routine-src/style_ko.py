# 11/24 사용자 요청: 번역투 대신 자연스러운 한국어. 11/25 이후 블록의 기입표 칸 이름만 바꾼다(과거 기록 칸은 그대로).
COLS = {'내 말로 한 줄': '한 줄 정리', '내 작업 어디에 쓰나': '어디에 쓰나', '고친 질문(내 말로)': '고친 질문'}
def records(rs):
    for sec in rs.values():
        if not isinstance(sec, list): continue
        for f in sec:
            if 'columns' in f:
                f['columns'] = [COLS.get(c, c) for c in f['columns']]
            if 'label' in f:
                for a, b in COLS.items(): f['label'] = f['label'].replace(a, b)
