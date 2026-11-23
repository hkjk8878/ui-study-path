# 11/23 밤 사용자와 정한 일정 변경 (11/24부터 적용)
# 1) 밀린 11/19~11/23 실습 중 기술 블록만 이번 주에 다시 넣는다(원래 블록은 기록으로 그대로 둔다).
#    '하루' 파일 이름 정리·문서 작업은 하지 않는다. 이름 기준은 CASE01 키트(12/21~)에서 처음부터 적용한다.
# 2) 월·수·금 22:00 'UI 따라 만들기'(11/27~4/16), 일 15:10 '앱 뜯어보기'(12/6~), 월 1회 토 15:10 '3시간 디자인 과제'.
#    이 블록들은 b.extra = True → validate.py 주간 시간 계산에서 뺀다(기존 루틴 시간은 그대로).
import copy, datetime as dt
from model import B
from detail import T

NAME_NOTE = ('파일 이름이 이 블록에 적힌 이름과 달라도(예: Type=Primary · field · 행-1) 바꾸지 않는다. '
             '파일에 보이는 이름을 그대로 고르고 넘어간다. 이름 정리는 12/21 CASE01 키트를 새로 만들 때 처음부터 확정판 이름으로 한다.')

# ---------- 앱 화면 보는 곳 (App Store 페이지 = 화면 사진이 바로 보인다) ----------
APPS = {
    'toss': ('토스', 'https://apps.apple.com/kr/app/id839333328'),
    'daangn': ('당근', 'https://apps.apple.com/kr/app/id1018769995'),
    'baemin': ('배달의민족', 'https://apps.apple.com/kr/app/id378084485'),
    '29cm': ('29CM', 'https://apps.apple.com/kr/app/id789634744'),
    'coupang': ('쿠팡', 'https://apps.apple.com/kr/app/id454434967'),
    'tide': ('Tide Guide', 'https://apps.apple.com/kr/app/id1406371071'),
    'moonlitt': ('Moonlitt', 'https://apps.apple.com/kr/app/id6444718902'),
    'guitarwiz': ('Guitar Wiz', 'https://apps.apple.com/kr/app/id6740015002'),
    'grug': ('grug', 'https://apps.apple.com/kr/app/id6751649802'),
    'structured': ('Structured', 'https://apps.apple.com/kr/app/id1499198946'),
}
ADA = {'tide': '2026 Apple Design Award 시각·그래픽 부문 수상', 'moonlitt': '2026 Apple Design Award 인터랙션 부문 수상',
       'guitarwiz': '2026 Apple Design Award 포용성 부문 수상', 'grug': '2026 Apple Design Award 즐거움 부문 수상',
       'structured': '2026 Apple Design Award 포용성 부문 최종 후보'}

def add_res(R):
    for k, (n, u) in APPS.items():
        R['app_' + k] = (f'{n} · App Store 화면 사진', u,
                         ADA.get(k, '화면 사진 6~10장 · 실제 화면은 내 휴대폰에서 캡처'))

# ---------- 1단계: 똑같이 만들기 (12회) ----------
S1 = [
    ('toss', '홈', '큰 숫자(잔액) 위계, 카드 사이 간격', '계좌 카드 행'),
    ('toss', '송금 금액 입력', '한 화면에 할 일 하나, 숫자 키패드와 아래 고정 버튼', '키패드 버튼'),
    ('daangn', '홈 목록', '목록 행(사진 · 제목 · 동네 · 가격) 컴포넌트', '상품 목록 행'),
    ('daangn', '상품 상세', '큰 사진 아래 정보 순서, 아래 고정 채팅 버튼', '아래 고정 바'),
    ('daangn', '채팅방', '말풍선 Auto layout, 아래 고정 입력창', '말풍선(내 것 · 상대 것)'),
    ('baemin', '가게 목록', '필터 칩 가로 스크롤, 가게 카드', '필터 칩'),
    ('baemin', '메뉴 옵션 선택', '필수 · 선택 옵션의 라디오 · 체크박스 상태', '옵션 행'),
    ('29cm', '상품 목록(2열)', '2열 그리드, 사진 비율, 글자 위계', '상품 카드'),
    ('29cm', '상품 상세', '사진 중심 레이아웃, 가격 · 할인 표시', '가격 묶음'),
    ('coupang', '장바구니', '정보가 많은 화면에서 가격 강조와 체크 묶음', '장바구니 상품 행'),
    ('toss', '주식 종목 화면', '차트와 숫자, 기간 탭', '기간 탭'),
    ('toss', '설정(전체 메뉴)', '설정 목록 패턴, 구분선과 묶음 제목', '설정 행'),
]
# ---------- 2단계: 규칙 찾기 → 원본에 없는 화면 ----------
S2_APPS = [('toss', '모임통장 설정'), ('daangn', '동네 행사 상세'), ('baemin', '포장 주문 완료'),
           ('29cm', '브랜드 소개'), ('coupang', '반품 신청 완료')]
# ---------- 3단계: 수상작 ----------
S3_ADA = [('tide', '시간대별 차트 화면', '데이터 시각화 · 차트 위 글자 배치'),
          ('moonlitt', '오늘의 달 화면', '정보를 줄인 첫 화면 · 큰 그래픽과 작은 숫자'),
          ('guitarwiz', '코드(chord) 상세', '큰 글자 · 대비 · 색 없이 구분하는 표시'),
          ('grug', '오늘의 문장 카드', '단순한 카드에 개성(손글씨 · 색 테마) 넣기'),
          ('structured', '하루 타임라인', '세로 타임라인 · 색 구분 · 끌어서 옮기는 일정')]

MEASURE = lambda: T(['재는 곳', '원본', '내 화면'],
                    ['화면 좌우 여백', '', ''], ['제목 글자 크기 · 굵기', '', ''],
                    ['본문 글자 크기', '', ''], ['반복 행 · 카드 사이 간격', '', ''], ['버튼 높이 · 모서리', '', ''])

def copy_block(n, app, screen, learn, comp):
    name, _ = APPS[app]
    steps = [
        f'{name} ‘{screen}’ 화면 1장을 똑같이 만든다. 익히는 것: {learn}.',
        '순서표\n' + T(['순서', '만드는 것', '하는 일 (시간)'],
          ['①', '원본 캡처 놓기', f'어디: 캔버스 ¶ 휴대폰에서 {name} 앱 → ‘{screen}’ 화면 캡처(앱이 없으면 ‘강의·자료’의 App Store 화면 사진) ¶ 파일 ‘UI 따라 만들기’에 페이지 {n:02d} {name}-{screen} 만들기 → 캡처를 끌어 놓기 ¶ 캡처 선택 → W 390으로 맞추기(비율 유지) → 레이어 이름 원본 → 자물쇠(Lock) ¶ 캡처가 390 폭으로 잠겨 있으면 성공 (5분)'],
          ['②', '값 재기', '어디: 캔버스 ¶ 캡처 위에 R로 사각형을 그려 여백 · 간격 · 버튼 높이를 잰다(오른쪽 W · H 숫자) ¶ 글자는 캡처 글자 높이에 T 글자를 겹쳐 크기를 맞춰 본다 ¶ 아래 ‘결과물 기입표’ 원본 칸에 적는다 ¶ 5칸이 다 차면 성공 (10분)'],
          ['③', f'{comp} 부품', f'어디: 캔버스 ¶ 화면에서 두 번 이상 나오는 것({comp})을 먼저 Auto layout으로 만들고 Ctrl+Alt+K(Create component) ¶ 인스턴스를 복제해 반복 부분을 채운다 ¶ 레이어 패널에서 부품 앞 아이콘이 ◆이면 성공 (15분)'],
          ['④', '화면 조립', '어디: 캔버스 ¶ 캡처 오른쪽에 390×844 Frame → 위에서 아래로 Auto layout으로 쌓기 ¶ 글자는 캡처와 같은 문장 · 크기 · 굵기 ¶ 색은 스포이트(I)로 캡처에서 찍기 ¶ 화면이 캡처와 같은 순서로 다 채워지면 성공 (20분)'],
          ['⑤', '겹쳐 비교', '어디: 캔버스 ¶ 내 화면을 캡처 위로 끌어 겹치기 → 레이어 Opacity 50% ¶ 어긋난 곳을 고친다(여백 → 간격 → 글자 순서로) ¶ 기입표 내 화면 칸을 채운다 ¶ 겹쳤을 때 글자 · 버튼 위치가 4px 안으로 맞으면 성공 (10분)']),
        '결과 기록\n' + MEASURE(),
        '막히면: 그 기능 이름만 유튜브에서 찾아 5~10분 영상 하나만 본다(예: “Figma auto layout 가로 스크롤”). 강의를 처음부터 다시 듣지 않는다.',
    ]
    b = B('22:00-23:00', '훈련', f'UI 따라 만들기 {n} · {name} {screen}', ['app_' + app], steps,
          out=f'{name} {screen} 따라 만든 화면, 재기 표', chk='겹쳐 봤을 때 여백 · 간격 · 글자 크기가 원본과 같은가. 다른 곳이 남았다면 왜 다른지 한 줄.')
    b.why = '잘 만든 실제 화면을 같은 값으로 다시 만들면 피그마 조작이 손에 붙고, 간격 · 글자 위계 같은 규칙이 몸에 들어온다. 연습용이며 포트폴리오에는 넣지 않는다.'
    return b

def rule_block(n, app, new_screen, part):
    name, _ = APPS[app]
    if part == 1:
        steps = [f'{name} 화면 3~4장에서 반복되는 규칙(간격 · 글자 · 색 · 버튼)을 찾아 1장으로 정리한다. 다음 회차에 이 규칙만 보고 원본에 없는 ‘{new_screen}’ 화면을 만든다.',
                 '순서표\n' + T(['순서', '만드는 것', '하는 일 (시간)'],
                   ['①', '캡처 4장', f'어디: 캔버스 ¶ {name} 앱 화면 4장 캡처(홈 · 목록 · 상세 · 완료 같은 서로 다른 화면) ¶ 페이지 {n:02d} {name}-규칙에 나란히 놓기 ¶ 4장이 한 줄로 보이면 성공 (5분)'],
                   ['②', '규칙 재기', '어디: 캔버스 ¶ 4장 모두에서 좌우 여백 · 행 간격 · 제목/본문 글자 크기 · 주 버튼 모양을 잰다 ¶ 4장에서 같은 값이 나오면 규칙, 다르면 왜 다른지 적는다 (30분)'],
                   ['③', '규칙 1장', '어디: 캔버스 ¶ 새 Frame ‘규칙’에 아래 표 내용을 글자로 옮긴다 ¶ 다음 회차에 이 Frame만 보고 만들 수 있으면 성공 (25분)']),
                 '찾은 규칙\n' + T(['종류', '규칙', '근거(몇 장 중 몇 장)'],
                   ['여백 · 간격', '', ''], ['글자 크기 · 굵기', '', ''], ['색(강조 · 바탕 · 회색)', '', ''], ['버튼 · 모서리', '', ''])]
        title = f'규칙 찾기 {n} · {name} 규칙 정리'
        out = f'{name} 규칙 1장'
    else:
        steps = [f'지난 회차의 {name} 규칙 1장만 보고 원본 앱에 없는 ‘{new_screen}’ 화면을 만든다. 원본 앱 화면은 보지 않는다.',
                 '순서표\n' + T(['순서', '만드는 것', '하는 일 (시간)'],
                   ['①', '화면 내용 정하기', f'어디: 캔버스 ¶ ‘{new_screen}’에 들어갈 정보를 위에서 아래 순서로 5~7줄 적는다 ¶ 가장 중요한 정보 하나에 별표 (10분)'],
                   ['②', '화면 만들기', '어디: 캔버스 ¶ 390×844 Frame → 규칙 1장의 여백 · 간격 · 글자 · 버튼 값만 쓴다 ¶ 규칙에 없는 것이 필요하면 새로 정하고 규칙 1장에 추가한다 (35분)'],
                   ['③', '원본 옆에 놓고 보기', f'어디: 캔버스 ¶ 지난 회차 캡처 4장 옆에 놓는다 ¶ 같은 앱 화면처럼 보이면 성공, 튀는 곳이 있으면 1곳 고친다 (15분)']),
                 '확인\n' + T(['볼 것', '결과'], ['규칙에 없는 값을 쓴 곳', ''], ['같은 앱처럼 안 보이는 곳', ''], ['규칙 1장에 추가한 것', ''])]
        title = f'규칙 찾기 {n} · {name} 새 화면 ‘{new_screen}’'
        out = f'{new_screen} 화면, 보완한 규칙 1장'
    b = B('22:00-23:00', '훈련', title, ['app_' + app], steps, out=out,
          chk='원본에 없는 화면인데도 같은 앱 화면처럼 보이는가. 그렇게 보이는 이유를 규칙 이름으로 말할 수 있는가.')
    b.why = '규칙을 뽑아 새 화면에 적용할 수 있어야 남의 화면을 베끼는 단계를 넘어 내 화면을 만든다. 디자인 시스템 실무와 같은 생각 순서다.'
    return b

def ada_block(n, app, screen, learn):
    b = copy_block(n, app, screen, learn, '반복되는 부분')
    name = APPS[app][0]
    b.title = f'수상작 따라 만들기 {n} · {name} {screen}'
    b.steps = (b.steps[0] + f' ({ADA[app]}.) 이 앱은 해외 앱이라 휴대폰에 없으면 App Store 화면 사진으로 한다.',) + tuple(b.steps[1:])
    b.why = '수상작은 국내 앱에 적은 시각 표현 · 움직임 · 접근성을 보여 준다. 무엇이 화면을 ‘완성도 있게’ 만드는지 값으로 확인한다.'
    return b

def redesign_block(n, cyc, part):
    if part == 1:
        steps = ['자주 쓰는 앱에서 불편했던 화면 1개를 고르고, 무엇이 왜 불편한지 근거와 함께 적는다. (이번 묶음 3회 중 1회)',
                 '순서표\n' + T(['순서', '만드는 것', '하는 일 (시간)'],
                   ['①', '화면 고르기', '어디: 휴대폰 ¶ 최근 1주 안에 실제로 막히거나 헤맨 화면 1개를 캡처 ¶ 후보가 없으면 가족 · 친구 1명에게 “최근 앱 쓰다 짜증 났던 순간”을 묻는다 (10분)'],
                   ['②', '문제 적기', '어디: 캔버스 ¶ 캡처 옆에: 누가 · 무엇을 하려다 · 어디서 막혔나 ¶ 막힌 이유를 NN/g 10가지 원칙 중 하나로 이름 붙인다 (25분)'],
                   ['③', '바꿀 목표 1줄', '어디: 캔버스 ¶ “○○하는 사람이 △△를 □초 안에 끝낸다”처럼 잴 수 있는 목표 1줄 ¶ 목표가 숫자로 끝나면 성공 (25분)']),
                 '문제 정리\n' + T(['칸', '내용'], ['누가 · 무엇을 하려다', ''], ['막힌 곳 · 이유(원칙 이름)', ''], ['바꿀 목표(숫자로)', ''])]
        title, out = f'다시 설계하기 {cyc}-1 · 불편한 화면 고르기', '고른 화면, 문제 정리, 목표 1줄'
    elif part == 2:
        steps = ['지난 회차에 고른 화면을 내 방식으로 다시 설계한다. 2안을 만들어 비교한다.',
                 '순서표\n' + T(['순서', '만드는 것', '하는 일 (시간)'],
                   ['①', '두 방향', '어디: 캔버스 ¶ 같은 문제를 푸는 서로 다른 방향 2개를 한 줄씩(예: 단계를 줄인다 / 순서를 바꾼다) (10분)'],
                   ['②', 'A안 · B안', '어디: 캔버스 ¶ 390×844 Frame 2개 ¶ 원래 앱의 글자 · 색 규칙은 지키고 구조만 바꾼다 (40분)'],
                   ['③', '고르기', '어디: 캔버스 ¶ 목표 1줄 기준으로 A · B 중 하나를 고르고 이유 1줄 (10분)'])]
        title, out = f'다시 설계하기 {cyc}-2 · A안 · B안', 'A안 · B안, 고른 이유'
    else:
        steps = ['고른 안을 한 사람에게 직접 해 보게 하고, 원래 화면과 비교해 결과를 1장으로 정리한다.',
                 '순서표\n' + T(['순서', '만드는 것', '하는 일 (시간)'],
                   ['①', '해 보게 하기', '어디: 휴대폰(Figma 발표 링크) ¶ 가족 · 친구 1명에게 원래 화면과 내 화면에서 같은 일을 시키고 걸린 시간 · 멈춘 곳을 적는다 (25분)'],
                   ['②', '1장 정리', '어디: 캔버스 ¶ 문제 → 바꾼 것 → 결과(시간 · 멈춘 곳) → 남은 한계 4줄 ¶ 남이 이 1장만 보고 왜 바꿨는지 알면 성공 (35분)']),
                 '비교\n' + T(['볼 것', '원래 화면', '내 화면'], ['걸린 시간', '', ''], ['멈춘 곳', '', ''])]
        title, out = f'다시 설계하기 {cyc}-3 · 해 보게 하고 1장 정리', '비교 결과, 정리 1장(포트폴리오 후보)'
    b = B('22:00-23:00', '훈련', title, ['nng_heur'] if part == 1 else [], steps, out=out,
          chk='바꾼 이유가 “예뻐서”가 아니라 문제와 목표로 설명되는가.')
    b.why = '불편한 화면을 근거로 고치고 결과를 재는 연습은 면접의 “이 앱을 개선한다면?” 질문과 신입 과제 전형에 그대로 쓰인다. 이 단계의 1장 정리는 포트폴리오 부록 후보가 된다.'
    return b

# ---------- 일요일 앱 뜯어보기 ----------
TEAR = [('toss', '송금'), ('daangn', '판매글 쓰기'), ('baemin', '장바구니 담기'), ('29cm', '좋아요(찜)'),
        ('coupang', '주문 배송 조회'), ('toss', '만보기'), ('daangn', '동네 인증'), ('baemin', '배달 현황(라이더 위치)'),
        (None, '카카오톡 선물하기'), (None, '네이버 지도 길찾기'), ('toss', '주식 주문'), ('daangn', '채팅'),
        ('baemin', '리뷰 쓰기'), ('29cm', '검색'), ('coupang', '장바구니'), ('structured', '일정 끌어서 옮기기'),
        ('moonlitt', '달 위치 찾기(나침반)'), ('tide', '차트 종류 바꾸기'), ('guitarwiz', '색 없이 구분하는 표시')]

def tear_block(n, app, feat):
    name = APPS[app][0] if app else ''
    label = f'{name} {feat}'.strip()
    steps = [f'{label} 기능 하나를 직접 써 보고, 이 기능이 어떤 문제를 풀려고 만들어졌는지 5가지 질문으로 정리한다.',
             '순서표\n' + T(['순서', '만드는 것', '하는 일 (시간)'],
               ['①', '직접 써 보기', f'어디: 휴대폰 ¶ {label} 기능을 처음부터 끝까지 한 번 써 본다 ¶ 화면마다 캡처 (10분)'],
               ['②', '5가지 질문', '어디: 메모장 ¶ 아래 표를 채운다. 모르는 것은 “추측:”을 붙인다 (20분)']),
             '뜯어보기\n' + T(['질문', '내 답'], ['어떤 문제를 풀려고 만들었을까', ''], ['누구를 위한 것인가', ''],
                             ['다른 방법은 무엇이 있었을까', ''], ['무엇을 포기했을까', ''], ['무엇으로 성공을 쟀을까', ''])]
    b = B('15:10-15:40', '분석', f'앱 뜯어보기 {n} · {label}', ['app_' + app] if app else [], steps,
          out='뜯어보기 5문답', chk='답마다 화면에서 본 근거가 있는가, 추측은 추측이라고 적었는가.')
    b.why = '큰 회사 면접은 “좋아하는 앱의 기능을 분석해 보세요”처럼 문제 → 해결 → 지표로 생각하는지 본다. 매주 30분씩 쌓으면 바로 답할 거리가 된다.'
    return b

# ---------- 월 1회 3시간 과제 ----------
TASKS = [('2026-12-19', '동네 도서관 좌석 예약: 처음 온 사람이 빈 좌석을 2분 안에 예약한다'),
         ('2027-01-16', '모임 회비 나눠 내기: 5명이 각자 낼 돈을 확인하고 한 번에 보낸다'),
         ('2027-02-20', '부모님 약 먹을 시간 알림: 놓친 약을 가족이 알 수 있게 한다'),
         ('2027-03-20', '중고 거래 사기 의심 알리기: 거래 전에 위험 신호를 알아챈다')]

def task_block(n, prob):
    steps = [f'과제: {prob}. 3시간 안에 문제 정의부터 주요 화면까지 끝낸다. 시간 제한 과제 전형 연습이다.',
             '순서표\n' + T(['순서', '만드는 것', '하는 일 (시간)'],
               ['①', '문제 · 가정', '어디: 메모장 ¶ 누가 · 언제 · 왜 이 일을 하나, 확인 안 된 가정 3개 (20분)'],
               ['②', '사용자 · 시나리오', '어디: 메모장 ¶ 주 사용자 1명과 성공 시나리오 1개, 실패 상황 2개 (30분)'],
               ['③', '흐름 · 와이어', '어디: 캔버스 ¶ 화면 흐름 1줄 → 회색 와이어 3~5장 (40분)'],
               ['④', '주요 화면 2~3장', '어디: 캔버스 ¶ 가장 중요한 화면만 완성도 있게 ¶ 오류 · 빈 상태 1장 포함 (70분)'],
               ['⑤', '정리 1장', '어디: 캔버스 ¶ 문제 → 결정 3개와 이유 → 화면 → 다음에 확인할 것 ¶ 3시간 안에 끝나면 성공 (20분)'])]
    b = B('15:10-18:10', '제작', f'3시간 디자인 과제 {n}', [], steps, out='과제 정리 1장, 주요 화면',
          chk='결정마다 이유가 있는가, 3시간을 넘기지 않았는가(넘겼다면 어디서).')
    b.why = '큰 회사 채용에는 짧은 시간 안에 문제를 정의하고 화면까지 내는 과제 전형이 있다. 시간을 재고 해 봐야 실전에서 시간 배분을 할 수 있다.'
    return b

def _evening_dates():
    d, out = dt.date(2026, 11, 27), []
    while d <= dt.date(2027, 4, 16):
        if d.weekday() in (0, 2, 4): out.append(d.isoformat())
        d += dt.timedelta(days=1)
    return out

def _sundays():
    d, out = dt.date(2026, 12, 6), []
    while d <= dt.date(2027, 4, 11):
        out.append(d.isoformat()); d += dt.timedelta(days=7)
    return out

def evening_plan():
    dates = _evening_dates(); plan = {}; i = 0
    for n, (app, scr, learn, comp) in enumerate(S1, 1):
        plan[dates[i]] = copy_block(n, app, scr, learn, comp); i += 1
    n = 1
    while dates[i] <= '2027-01-29':
        app, new = S2_APPS[((n - 1) // 2) % len(S2_APPS)]
        plan[dates[i]] = rule_block(n, app, new, 1 if n % 2 else 2); i += 1; n += 1
    for k, (app, scr, learn) in enumerate(S3_ADA, 1):
        plan[dates[i]] = ada_block(k, app, scr, learn); i += 1
    cyc, part = 1, 1
    while i < len(dates):
        plan[dates[i]] = redesign_block(i, cyc, part); i += 1
        part += 1
        if part == 4: cyc, part = cyc + 1, 1
    return plan

def _find(weeks, date, t):
    for w in weeks:
        for d in w.days:
            if d.date == date:
                for b in d.blocks:
                    if b.t[:5] == t: return d, b
    raise KeyError((date, t))

def _day(weeks, date):
    for w in weeks:
        for d in w.days:
            if d.date == date: return d
    raise KeyError(date)

def _clone(weeks, date, t, new_t, note=True):
    _, b = _find(weeks, date, t)
    c = copy.deepcopy(b); c.t = new_t
    c.steps = tuple(c.steps)
    if note:
        c.steps = (c.steps[0], NAME_NOTE) + tuple(c.steps[1:]) if c.steps else (NAME_NOTE,)
    c.note = (f'원래 {date[5:].replace("-", "/")} 블록이다. 11/23 일정 조정으로 옮겼다.' + (' ' + c.note if c.note else '')).strip()
    return c

def _extra(b):
    b.extra = True
    return b

def apply(weeks):
    # --- 이번 주 재배치 ---
    tue = _day(weeks, '2026-11-24'); wed = _day(weeks, '2026-11-25')
    sat = _day(weeks, '2026-11-28'); sun = _day(weeks, '2026-11-29'); fri = _day(weeks, '2026-11-27')
    old_tue = {b.t[:5]: b for b in tue.blocks}
    old_wed = {b.t[:5]: b for b in wed.blocks}
    # 화: 밀린 프로토타입 + 강의 2개 + 원래 AI
    p = _clone(weeks, '2026-11-22', '09:00', '08:00-10:00')
    p.steps = tuple(x.replace('11/24 모션 블록', '11/25 모션 블록') for x in p.steps)
    l1 = _clone(weeks, '2026-11-23', '08:00', '10:10-10:30', note=False)
    l2 = _clone(weeks, '2026-11-20', '08:00', '10:30-11:00', note=False)
    ai = old_tue['22:00']
    ai.steps = tuple(s.replace('수요일에 쓸', '토요일에 쓸').replace('수요일 명세', '토요일 명세') for s in ai.steps)
    tue.blocks = [p, l1, l2, ai]
    tue.title = '밀린 실습 · 상세·수정·삭제 프로토타입'
    # 수: 원래 화요일 모션 3블록(시간 같음) + 저녁 강의 2개
    mo = []
    for t in ('08:00', '08:40', '10:10'):
        b = old_tue[t]
        b.steps = tuple(x.replace('11/22', '11/24') for x in b.steps)
        b.steps = (b.steps[0], NAME_NOTE) + tuple(b.steps[1:]) if t != '08:00' else b.steps
        b.note = ('원래 11/24 블록이다. 11/23 일정 조정으로 하루 미뤘다.' + (' ' + b.note if b.note else '')).strip()
        mo.append(b)
    e1 = _extra(_clone(weeks, '2026-11-19', '08:00', '22:00-22:15', note=False))
    e2 = _extra(_clone(weeks, '2026-11-19', '08:15', '22:15-23:00', note=False))
    wed.blocks = mo + [e1, e2]
    wed.title = '상태를 알리는 모션 + 밤 강의 2개'
    # 토: 오후 '하루' 정리 대신 개발 전달 명세(원래 11/25)
    s0 = sat.blocks[0]
    h = old_wed['08:00']; h.t = '13:00-13:20'
    m = old_wed['08:20']; m.t = '13:20-15:00'
    m.steps = (m.steps[0], NAME_NOTE) + tuple(m.steps[1:])
    c = old_wed['10:10']; c.t = '15:10-16:00'; _extra(c)
    for b in (h, m, c):
        b.note = ('원래 11/25 블록이다. 11/23 일정 조정으로 토요일로 옮겼다.' + (' ' + b.note if b.note else '')).strip()
    sat.blocks = [s0, h, m, c]
    sat.title = 'UI 완성도 훈련 3회 + 개발 전달 명세'
    # 일: 오후 끝에 밀린 반응형 2블록
    r1 = _extra(_clone(weeks, '2026-11-20', '08:30', '15:10-16:40'))
    r2 = _extra(_clone(weeks, '2026-11-20', '10:10', '16:40-17:30'))
    sun.blocks = sun.blocks + [r1, r2]
    sun.title = sun.title + ' + 밀린 반응형 768·1280'
    # --- 저녁 · 주말 추가 블록 ---
    ev = evening_plan()
    for date, b in ev.items():
        d = _day(weeks, date); d.blocks.append(_extra(b))
    for n, date in enumerate(_sundays(), 1):
        app, feat = TEAR[(n - 1) % len(TEAR)]
        _day(weeks, date).blocks.append(_extra(tear_block(n, app, feat)))
    for n, (date, prob) in enumerate(TASKS, 1):
        _day(weeks, date).blocks.append(_extra(task_block(n, prob)))
    for w in weeks:
        for d in w.days:
            if d.date >= '2026-11-24':
                d.blocks.sort(key=lambda b: b.t)
            for b in d.blocks:
                if not hasattr(b, 'when'):
                    b.when = f'{d.date[5:]} {b.t[:5]}'
