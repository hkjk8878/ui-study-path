# 영어 이름·Figma 용어 옆에 (한국어 뜻)을 붙인다 — 블록마다 처음 나올 때 한 번
import re
G = [
 # 이름(슬래시 묶음) — 긴 것부터
 ('Todo/Row','할 일/행'), ('Todo/Card','할 일/카드'), ('Icon/Check','아이콘/체크'), ('Icon/More','아이콘/더보기'), ('Icon/Close','아이콘/닫기'), ('Icon/Play','아이콘/재생'),
 ('Card/Thumbnail','카드/썸네일'), ('List/Row','목록/행'), ('Button/Like','버튼/찜'), ('Button/Reader','버튼/읽기'),
 ('Annotation/Spec','주석/명세'), ('Annotation/Note','주석/메모'),
 ('text/primary','글자/주요'), ('text/secondary','글자/보조'), ('text/disabled','글자/비활성'), ('bg/surface','배경/바탕면'),
 ('border/default','테두리/기본'), ('action/primary','누르는 것/주요'), ('heading/large','제목/크게'), ('heading/medium','제목/중간'),
 ('body/regular','본문/보통'), ('body/strong','본문/굵게'), ('shadow/small','그림자/작게'), ('shadow/medium','그림자/중간'),
 ('gray/500','회색/중간 진하기'), ('blue/500','파랑/중간 진하기'), ('space/16','간격/16px'), ('radius/8','모서리/8px'),
 # Figma 용어
 ('Main component','원본 부품'), ('Instance','복사본'), ('Auto layout','자동 정렬'), ('Smart animate','같은 이름끼리 자동 움직임'),
 ('Navigate to','화면 이동'), ('Change to','상태 바꾸기'), ('On click','누르면'), ('Open overlay','위에 띄우기'), ('Overlay','위에 띄우는 창'),
 ('Absolute position','자유 위치'), ('Layout guide','열 그리드'), ('Constraints','폭이 바뀔 때 붙는 방향'),
 ('Add min width','최소 너비'), ('Add max width','최대 너비'), ('Detach instance','원본과 연결 끊기'), ('Export','내보내기'),
 ('Variables','변수'), ('Primitives','기본값 모음'), ('Semantic','쓰임새 모음'), ('Section','구역'), ('Flow','흐름 시작점'),
 ('Present','발표 모드'), ('Assets','부품 모음 패널'), ('Padding','안쪽 여백'), ('Gap','사이 간격'), ('Hug','내용에 맞춤'),
 ('Variant','종류·상태 버전'), ('Property','속성'),
 # 부품
 ('Button','버튼'), ('Checkbox','체크박스'), ('Input','입력창'), ('Toast','잠깐 뜨는 알림'), ('Dialog','확인창'), ('Badge','배지'), ('Annotation','주석'), ('Progress','진행 표시'),
 # 속성 이름 · 값
 ('State','상태'), ('Type','종류'), ('Size','크기'), ('Status','진행 상태'), ('Label','글자'), ('Show icon','아이콘 보이기'), ('Show badge','배지 보이기'),
 ('Default','기본'), ('Hover','마우스 올림'), ('Pressed','누른 순간'), ('Focused','입력 중'), ('Disabled','비활성·못 누름'), ('Error','오류'),
 ('Filled','입력됨'), ('Selected','선택됨'), ('Loading','불러오는 중'), ('Unchecked','체크 안 됨'), ('Checked','체크됨'), ('Done','완료'),
 ('Primary','주요'), ('Secondary','보조'), ('Small','작게'), ('Large','크게'),
 ('bg/subtle','배경/옅게'), ('status/error','상태/오류'), ('status/success','상태/성공'),
 ('Close when clicking outside','바깥 누르면 닫기'), ('Scroll behavior','스크롤할 때 동작'), ('Show version history','버전 기록 보기'),
 ('Anyone with the link','링크 있는 누구나'), ('can view','보기만 가능'), ('Flow starting point','흐름 시작점 정하기'),
 ('Prototype','화면 연결'), ('Overflow','넘치는 내용'), ('Vertical','세로 스크롤'), ('Fixed','고정'), ('Center','가운데'),
 ('Frame','틀'), ('Fill','남은 공간 채우기'), ('Typography','글자 설정'), ('Plugins','플러그인'),
 ('Share','공유'), ('Columns','열 수'), ('Gutter','열 사이 간격'), ('Margin','바깥 여백'), ('Scale','비율대로 늘리기'),
 ('label','글자'), ('icon','아이콘'), ('title','제목'), ('date','날짜'), ('list','목록'),
 ('todo/row','할 일/행'), ('todo/card','할 일/카드'), ('icon/check','아이콘/체크'), ('icon/more','아이콘/더보기'), ('icon/close','아이콘/닫기'),
 ('card/thumbnail','카드/썸네일'), ('list-item','목록/행'), ('button/like','버튼/찜'), ('button/reader','버튼/읽기'), ('button/blue','버튼/파랑'),
 ('annotation/spec','주석/명세'), ('annotation/note','주석/메모'), ('action/primary-hover','누르는 것/주요-마우스 올림'),
 ('border/subtle','테두리/옅게'), ('border/strong','테두리/진하게'), ('text/on-action','글자/누르는 것 위'),
 ('status/warning','상태/주의'), ('status/info','상태/안내'),
 ('button','버튼'), ('checkbox','체크박스'), ('input','입력창'), ('toast','잠깐 뜨는 알림'), ('dialog','확인창'), ('badge','배지'),
 ('annotation','주석'), ('progress','진행 표시'), ('thumbnail','썸네일'), ('meta','작은 정보'),
 ('type','종류'), ('state','상태'), ('size','크기'), ('status','진행 상태'), ('show icon','아이콘 보이기'),
 ('default','기본'), ('hover','마우스 올림'), ('pressed','누른 순간'), ('focused','입력 중'), ('disabled','비활성·못 누름'),
 ('error','오류'), ('filled','입력됨'), ('selected','선택됨'), ('loading','불러오는 중'), ('unchecked','체크 안 됨'), ('checked','체크됨'), ('done','완료'),
 ('primary','주요'), ('secondary','보조'), ('tertiary','가장 약함'), ('danger','위험'), ('subtle','옅게'), ('strong','진하게'),
 ('leading','앞쪽'), ('trailing','뒤쪽'), ('headline','제목 줄'), ('supporting-text','보조 글'), ('reorder','순서 바꾸기'),
 # 안쪽 레이어
 ('header','위 칸'), ('content','본문 칸'), ('footer','아래 칸'), ('text-group','글자 묶음'), ('more-button','더보기 버튼'), ('add-bar','추가 줄'),
 ('caption','작은 설명 글자'),
]
_pat = re.compile('(' + '|'.join(r'(?<![A-Za-z/\-(])' + re.escape(t) + r'(?![A-Za-z/\-])' for t, _ in G) + r')(\()?')
_mean = dict(G)

def annotate(steps):
    seen = set(); out = []
    for s0 in steps:
      lines = []
      for s in s0.split('\n'):
        if s.strip().startswith(('|', '“')) or s.startswith('이름 짓기') or s.startswith('이름 상식'):
            lines.append(s); continue
        def rep(m, s=s):
            t = m.group(1); par = m.group(2)
            if t in seen: return m.group(0)
            seen.add(t)
            if par and s[m.end():].startswith(_mean[t]): return m.group(0)
            if s[m.end():].startswith(' [') or s[m.end():].startswith(' variable'): return m.group(0)
            after = s[m.end():]; before = s[:m.start()]
            if after.startswith(('=', '/')) or before.endswith(('=', '/')): seen.discard(t); return m.group(0)
            mean = _mean[t]
            if after.startswith(' 칸') and mean.endswith(' 칸'): mean = mean[:-2]
            return f'{t} [{mean}] (' if par else f'{t} [{mean}]'
            return f'{t} [{_mean[t]}] (' if par else f'{t} [{_mean[t]}]'
        lines.append(_pat.sub(rep, s))
      out.append('\n'.join(lines))
    return tuple(out)
