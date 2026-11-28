"""앱 JS에 '결과물 기입표'(table 기록 종류)를 추가한다. 이미 적용돼 있으면 그대로 둔다. 저장 구조는 그대로(taskRecords[블록][필드])."""
MARK = '/* FILL-TABLE v3 */'

FN = r'''function renderFillTable(field, values, date, taskId) {
  const base = field.columns || [];
  const prefix = field.key + '.';
  let used = 0, ncol = base.length;
  for (const k of Object.keys(values)) {
    if (!k.startsWith(prefix) || !values[k]) continue;
    const rest = k.slice(prefix.length);
    if (rest.startsWith('h.')) { ncol = Math.max(ncol, parseInt(rest.slice(2), 10) + 1); continue; }
    const [r, c] = rest.split('.').map(x => parseInt(x, 10));
    if (r >= 0) used = Math.max(used, r + 1);
    if (c >= 0) ncol = Math.max(ncol, c + 1);
  }
  const fixed = field.fixed || null;
  const n = fixed ? Math.max(fixed.length, used) : Math.max(field.rows || 5, used + 1);
  const cols = Array.from({length: ncol}, (_, c) => c);
  const cell = (r, c) => `<td><textarea rows="1" aria-label="${esc((base[c] || '추가 열') + ' ' + (r + 1) + '행')}" data-task-record="${esc(taskId)}" data-record-date="${esc(date)}" data-record-field="${esc(prefix + r + '.' + c)}">${esc(values[prefix + r + '.' + c] ?? '')}</textarea></td>`;
  const head = c => c < base.length ? `<th scope="col">${esc(base[c])}</th>`
    : `<th scope="col" class="ft-extra-head"><textarea rows="1" placeholder="열 이름" aria-label="추가 열 이름" data-task-record="${esc(taskId)}" data-record-date="${esc(date)}" data-record-field="${esc(prefix + 'h.' + c)}">${esc(values[prefix + 'h.' + c] ?? '')}</textarea></th>`;
  const row = r => `<tr><th scope="row" class="ft-num">${r + 1}</th>${cols.map(c => fixed && c === 0 && r < fixed.length ? `<td class="ft-fixed">${esc(fixed[r])}</td>` : cell(r, c)).join('')}</tr>`;
  const ex = field.example || [];
  return `<div class="fill-table-wrap" data-ft-cols="${ncol}" data-ft-prefix="${esc(prefix)}" data-ft-task="${esc(taskId)}" data-ft-date="${esc(date)}">
    <div class="ft-head"><strong>${esc(field.label)}</strong>${field.tip ? `<p class="ft-tip">${esc(field.tip)}</p>` : ''}${ncol >= 4 ? '<p class="ft-scroll-hint">열이 화면보다 넓으면 표를 옆으로 밀어 보세요 →</p>' : ''}</div>
    <div class="ft-scroll"><table class="fill-table" style="min-width:${Math.max(480, ncol * 128 + 48)}px">
    <thead><tr><th scope="col" class="ft-num">#</th>${cols.map(head).join('')}</tr></thead>
    <tbody>${ex.some(v => v) ? `<tr class="ft-example"><th scope="row" class="ft-num">예시</th>${cols.map(c => `<td>${esc(ex[c] ?? '')}</td>`).join('')}</tr>` : ''}
    ${Array.from({length: n}, (_, r) => row(r)).join('')}</tbody></table></div>
    <div class="ft-actions"><button type="button" class="ft-add" data-ft-add>+ 줄 추가</button><button type="button" class="ft-add" data-ft-addcol>+ 열 추가</button></div></div>`;
}
'''

TAIL = r'''
''' + MARK + r'''
function ftGrow(t) { t.style.height = 'auto'; t.style.height = t.scrollHeight + 2 + 'px'; }
document.addEventListener('input', e => { if (e.target.matches?.('.fill-table textarea')) ftGrow(e.target); });
document.addEventListener('toggle', e => { if (e.target.matches?.('details')) e.target.querySelectorAll('.fill-table textarea').forEach(ftGrow); }, true);
new MutationObserver(() => document.querySelectorAll('.fill-table textarea:not([data-grown])').forEach(t => { if (t.value) { t.dataset.grown = '1'; ftGrow(t); } }))
  .observe(document.documentElement, {childList: true, subtree: true});
document.addEventListener('click', e => {
  const btn = e.target.closest?.('[data-ft-add]');
  if (!btn) return;
  const body = btn.closest('.fill-table-wrap').querySelector('tbody');
  const last = body.lastElementChild;
  const next = last.cloneNode(true);
  const r = body.querySelectorAll('tr:not(.ft-example)').length;
  next.querySelector('th').textContent = r + 1;
  next.querySelectorAll('td.ft-fixed').forEach(td => {
    const wrap = btn.closest('.fill-table-wrap');
    td.className = '';
    td.innerHTML = `<textarea rows="1" data-task-record="${wrap.dataset.ftTask}" data-record-date="${wrap.dataset.ftDate}" data-record-field="${wrap.dataset.ftPrefix}${r}.0"></textarea>`;
  });
  next.querySelectorAll('textarea').forEach(t => {
    t.value = ''; t.style.height = ''; delete t.dataset.grown;
    t.dataset.recordField = t.dataset.recordField.replace(/\.\d+\.(\d+)$/, '.' + r + '.$1');
    t.setAttribute('aria-label', (t.getAttribute('aria-label') || '').replace(/\d+행$/, (r + 1) + '행'));
  });
  body.appendChild(next);
  next.querySelector('textarea')?.focus();
});
document.addEventListener('click', e => {
  const btn = e.target.closest?.('[data-ft-addcol]');
  if (!btn) return;
  const wrap = btn.closest('.fill-table-wrap');
  const c = parseInt(wrap.dataset.ftCols, 10);
  wrap.dataset.ftCols = c + 1;
  const ta = (field, label) => `<textarea rows="1" aria-label="${label}" data-task-record="${wrap.dataset.ftTask}" data-record-date="${wrap.dataset.ftDate}" data-record-field="${wrap.dataset.ftPrefix}${field}"></textarea>`;
  const th = document.createElement('th'); th.scope = 'col'; th.className = 'ft-extra-head';
  th.innerHTML = ta('h.' + c, '추가 열 이름'); th.querySelector('textarea').placeholder = '열 이름';
  wrap.querySelector('thead tr').appendChild(th);
  wrap.querySelectorAll('tbody tr').forEach(tr => {
    const td = document.createElement('td');
    if (!tr.classList.contains('ft-example')) {
      const r = parseInt(tr.querySelector('th').textContent, 10) - 1;
      td.innerHTML = ta(r + '.' + c, '추가 열 ' + (r + 1) + '행');
    }
    tr.appendChild(td);
  });
  const table = wrap.querySelector('table');
  table.style.minWidth = Math.max(480, (c + 1) * 128 + 48) + 'px';
  th.querySelector('textarea').focus();
});
'''

def patch(js):
    if MARK in js: return js
    if '/* FILL-TABLE v2 */' in js:
        return upgrade_v2(js)
    if '/* FILL-TABLE v1 */' in js:
        js = strip_v1(js)
    a = 'function renderTaskRecord(fields, values, date, taskId) {\n'
    assert js.count(a) == 1
    js = js.replace(a, FN + a + "  const fillTables = fields.filter(f => f.kind === 'table').map(f => renderFillTable(f, values, date, taskId)).join('');\n  fields = fields.filter(f => f.kind !== 'table');\n  if (!fields.length) return fillTables;\n")
    b = 'return `<div class="task-record stack-sm">${checkTable}'
    assert js.count(b) == 1
    js = js.replace(b, 'return fillTables + `<div class="task-record stack-sm">${checkTable}')
    c = 'if (sections.general) return content + `<details class="task-record"><summary>이 과제의 확인·수정 기록</summary>${renderSection(sections.general)}</details>`;'
    assert js.count(c) == 1
    js = js.replace(c, '''if (sections.general || sections.output) return content
    + (sections.output ? `<details class="task-record out-record" open><summary>결과물 기입표 <span class="ft-sub">바로 적어서 쓰기 · 자동 저장</span></summary>${renderSection(sections.output)}</details>` : '')
    + (sections.general ? `<details class="task-record"><summary>이 과제의 확인·수정 기록</summary>${renderSection(sections.general)}</details>` : '');''')
    return js + TAIL

def upgrade_v2(js):
    """v2 → v3: 함수와 줄 추가 처리만 바꿔 끼운다(뒤에 붙은 다른 패치는 그대로 둔다)."""
    a = js.index('function renderFillTable('); b = js.index('function renderTaskRecord(')
    js = js[:a] + FN + js[b:]
    i = js.index("document.addEventListener('click', e => {\n  const btn = e.target.closest?.('[data-ft-add]');")
    k = js.index("\n});\n", i) + len("\n});\n")
    new = TAIL[TAIL.index("document.addEventListener('click', e => {"):]
    js = js[:i] + new + js[k:]
    return js.replace('/* FILL-TABLE v2 */', MARK, 1)

def strip_v1(js, ver='v1'):
    """v1 패치를 걷어내고 원래 코드로 되돌린다(v2를 다시 넣기 위해)."""
    a = js.index('function renderFillTable('); b = js.index('function renderTaskRecord(')
    js = js[:a] + js[b:]
    js = js.replace("  const fillTables = fields.filter(f => f.kind === 'table').map(f => renderFillTable(f, values, date, taskId)).join('');\n  fields = fields.filter(f => f.kind !== 'table');\n  if (!fields.length) return fillTables;\n", '')
    js = js.replace('return fillTables + `<div class="task-record stack-sm">${checkTable}', 'return `<div class="task-record stack-sm">${checkTable}')
    i = js.index('if (sections.general || sections.output) return content'); k = js.index("</details>` : '');", i) + len("</details>` : '');")
    js = js[:i] + 'if (sections.general) return content + `<details class="task-record"><summary>이 과제의 확인·수정 기록</summary>${renderSection(sections.general)}</details>`;' + js[k:]
    js = js[:js.index(f'\n/* FILL-TABLE {ver} */')]
    return js

# ---- 하루·주간 기록 양식: 실무·채용에 쓰이는 항목으로 (기존 저장 키 유지, 새 키 추가) ----
FORM_MARK = '/* FORMS v1 */'
FORM_REPL = [
 ('<label for="learnt">오늘 배운 것</label><textarea id="learnt" name="learnt" placeholder="오늘 익힌 UX 개념 또는 Figma 기능">${esc(e.learnt)}</textarea></div>',
  '<label for="learnt">오늘 배운 것과 쓴 곳</label><textarea id="learnt" name="learnt" placeholder="기능·개념 이름 + 어디에 썼나 (예: Variant — 체크 상태 2개를 할 일 행에 적용)">${esc(e.learnt)}</textarea></div>'
  '<div class="field"><label for="decision">오늘의 결정과 근거</label><textarea id="decision" name="decision" placeholder="무엇을 골랐고 왜 골랐나. 근거는 기준·자료·사용자 말 (예: 저장 버튼을 비활성 대신 누르면 오류 표시 — 이유를 알려 줘야 고칠 수 있다). 면접 ‘왜 이렇게 했나요?’의 재료">${esc(e.decision||\'\')}</textarea></div>'),
 ('<label for="hard">막혔던 점·궁금한 점</label><textarea id="hard" name="hard" placeholder="어느 강의의 어느 부분이 어려웠는지">',
  '<label for="hard">막힌 곳</label><textarea id="hard" name="hard" placeholder="어느 자료의 어느 단계에서, 무엇을 하다가 막혔나 (예: 3-2 문서 Change to 단계에서 연결이 안 됨)">'),
 ('<label for="day-note">근거 자료·링크·메모</label><textarea id="day-note" name="note" placeholder="Figma 링크, 테스트 기록, 작업 파일 위치 등">',
  '<label for="day-note">증거 파일·링크</label><textarea id="day-note" name="note" placeholder="전후 캡처·녹화 파일 이름, Figma 링크 (포트폴리오 과정 이미지로 쓴다)">'),
 ('<label for="next">다음에 이어 할 일</label><textarea id="next" name="next" placeholder="오늘 못 끝낸 부분이나 후속 과제">',
  '<label for="next">다음에 이어 할 일</label><textarea id="next" name="next" placeholder="못 끝낸 것과 언제 할지 (예: 토요일 15:00 예비 시간)">'),
 ('<label for="review-goal">이번 주 목표</label><textarea id="review-goal" name="goal" placeholder="이번 주에 달성하려던 구체적인 목표">',
  '<label for="review-goal">이번 주 목표</label><textarea id="review-goal" name="goal" placeholder="이번 주 결과물 한 줄 (일정 화면의 ‘이번 주 목표’ 참고)">'),
 ('<label for="review-what">이번 주 완성한 것</label><textarea id="review-what" name="what" placeholder="완성 파일, 실습 결과, 포트폴리오 근거 자료">',
  '<label for="review-what">이번 주 완성한 것</label><textarea id="review-what" name="what" placeholder="만든 것 + 파일 이름·링크 (예: 할 일 추가 흐름 프로토타입 4경로, flow-01~04.mp4)">'),
 ('<label for="review-good">어떤 점이 개선됐나? (증거 포함)</label><textarea id="review-good" name="good" placeholder="강의 이해도, 과제 개선, 사용자 피드백 등 확인된 사실">${esc(e.good)}</textarea></div>',
  '<label for="review-good">어떤 점이 개선됐나? (증거 포함)</label><textarea id="review-good" name="good" placeholder="전과 비교한 사실 + 파일 (예: 할 일 행을 원본 하나로 — 고칠 곳 6군데 → 1군데, 1109_row.png)">${esc(e.good)}</textarea></div>'
  '<div class="field"><label for="review-hire">채용 기준 중 채운 칸 / 빈 칸</label><textarea id="review-hire" name="hire" placeholder="8칸: 대표 사례 깊이 · 사용자 데이터로 개선 · 출시·동작 링크 · 시각적 완성도 · 넓은 탐색과 선택 이유 · 흐름이 보이는 제출물 · 도구·협업·전달 · AI 활용 (예: 시각적 완성도 ✓ 1114 전후 캡처 / 빈 칸: 사용자 데이터 → 5주차 조사)">${esc(e.hire||\'\')}</textarea></div>'
  '<div class="field"><label for="review-decision">사례에 쓸 결정 (문제 → 선택지 → 고른 이유 → 결과)</label><textarea id="review-decision" name="decision" placeholder="이번 주 ‘오늘의 결정’ 중 1~2개 (예: 빈 제목 저장 → A 비활성 / B 오류 표시 → B, 이유를 알려 줘야 고칠 수 있다 → 오류 화면 추가)">${esc(e.decision||\'\')}</textarea></div>'),
 ('<label for="confidence">개념 이해도 (1~5점)</label>', '<label for="confidence">혼자 처음부터 만들 수 있나 (1 따라 하기만 · 3 일부 막힘 · 5 자료 없이 끝까지)</label>'),
 ('<label for="quality">결과물 완성도 (1~5점)</label>', '<label for="quality">결과물 완성도 (1 동작 안 함 · 3 점검표 일부 통과 · 5 모두 통과)</label>'),
 ("for(const key of ['learnt','hard','note','next'])obj[key]", "for(const key of ['learnt','decision','hard','note','next'])obj[key]"),
 ("for(const key of ['goal','what','good','next'])obj[key]", "for(const key of ['goal','what','good','hire','decision','next'])obj[key]"),
 ("obj.next=f.next.value.trim();putEntry('day:'+d,obj)", "obj.next=f.next.value.trim();obj.decision=f.decision.value.trim();putEntry('day:'+d,obj)"),
 ("obj.next=f.elements.next.value.trim();obj.confidence=", "obj.next=f.elements.next.value.trim();obj.hire=f.elements.hire.value.trim();obj.decision=f.elements.decision.value.trim();obj.confidence="),
]

def forms_patch(js):
    if FORM_MARK in js: return js
    for a, b in FORM_REPL:
        assert js.count(a) == 1, a[:60]
        js = js.replace(a, b)
    return js + '\n' + FORM_MARK + '\n'
