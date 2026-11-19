# 이름 규칙을 ‘하루_연습’ 파일 실제 규칙(영어 전부 소문자, 컬렉션만 첫 글자 대문자)에 맞춘다
import re
TOK = ['Todo/Row','Todo/Card','Todo','Icon/Check','Icon/More','Icon/Close','Icon/Play','Card/Thumbnail','List/Row','Button/Like','Button/Reader','Button/Blue',
       'Annotation/Spec','Annotation/Note','Button','Checkbox','Input','Toast','Dialog','Badge','Annotation','Progress',
       'State','Type','Size','Status','Default','Hover','Pressed','Focused','Disabled','Error','Filled','Selected','Loading','Unchecked','Checked','Done',
       'Primary','Secondary','Small','Large','Off','On','Sent','Partly confirmed','All confirmed','Canceled','Action','Condition','Accessibility',
       'Label','Show icon','Show badge','Number','Description','Title','Thumbnail','Icon']
_pat = re.compile('|'.join(r'(?<![A-Za-z/\-])' + re.escape(t) + r'(?![A-Za-z\-])' for t in sorted(TOK, key=len, reverse=True)))
LINE = [
 ('[영어, 첫 글자 대문자]', '[영어 소문자]'),
 ('· Main component: 첫 글자 대문자, 폴더는 슬래시', '· Main component: 소문자, 폴더는 슬래시'),
 ('· Variant: Figma 형식 ‘속성=값’, 첫 글자 대문자', '· Variant: Figma 형식 ‘속성=값’, 소문자'),
 ('· Variant: Figma 형식 ‘속성=값’, 둘 다 첫 글자 대문자', '· Variant: Figma 형식 ‘속성=값’, 소문자'),
 ('· 화면에 놓인 Instance(◇)는 이름을 바꾸지 않는다. Main component 이름을 그대로 따라간다', '· 화면에 놓인 Instance(◇) 이름은 바꾸지 않아도 된다(바꿔도 원본 연결은 안전하다)'),
 ('· 팁: 화면에 놓인 Instance(◇)는 이름을 바꾸지 않는다 → 바꾸면 어느 Main component인지 안 보인다', '· 팁: 화면에 놓인 Instance(◇) 이름은 바꾸지 않아도 된다. 바꿔도 원본 연결은 안전하다'),
 ('◆ Main component와 Variant가 맞는가', '◆ Main component와 Variant가 소문자인가'),
]
def fix(s):
    if not (s.startswith('이름') or s.startswith('· 이름')): return s
    s = s.replace('[영어, 첫 글자 대문자] 컬렉션', '[[KEEPCOL]]')
    for a, b in LINE: s = s.replace(a, b)
    s = s.replace('[[KEEPCOL]]', '[영어, 첫 글자 대문자] 컬렉션')
    s = re.sub(r'· 대문자 시작은 컴포넌트와 Variant만[^\n]*', '· 영어는 모두 소문자. 첫 글자 대문자는 변수 컬렉션 이름(Primitives · Semantic)뿐', s)
    s = s.replace('컬렉션 이름만 Primitives처럼 첫 글자 대문자', '컬렉션 이름만 Primitives처럼 첫 글자 대문자(영어 중 유일한 대문자)')
    return _pat.sub(lambda m: m.group(0).lower(), s)
