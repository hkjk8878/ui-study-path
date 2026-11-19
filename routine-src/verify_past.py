"""배포 전 확인: 오늘(KST)까지의 블록은 기록 칸(recordSections)과 id가 바뀌면 안 된다.
사용: python3 verify_past.py <이전 plan-final.json> <새 plan-final.json> [허용할 날짜 시간 ...]"""
import json, sys, datetime as dt
old, new = json.load(open(sys.argv[1])), json.load(open(sys.argv[2]))
allow = set(sys.argv[3:])
today = (dt.datetime.now(dt.timezone.utc) + dt.timedelta(hours=9)).date().isoformat()
def idx(p): return {(d['date'], b['time']): b for d in p['days'] for b in d['blocks']}
O, N = idx(old), idx(new)
bad = [k for k in O if k[0] <= today and f'{k[0]} {k[1][:5]}' not in allow and
       (O[k].get('recordSections') != N.get(k, {}).get('recordSections') or O[k].get('id') != N.get(k, {}).get('id'))]
if set(O) != set(N): bad.append(('블록 목록이 달라짐', str(set(O) ^ set(N))))
print('OK' if not bad else 'FAIL', bad)
sys.exit(1 if bad else 0)
