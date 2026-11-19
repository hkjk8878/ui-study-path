"""앱 JS에 '결과물 기입표'(table 기록 종류)를 추가한다. 이미 적용돼 있으면 그대로 둔다. 저장 구조는 그대로(taskRecords[블록][필드])."""
MARK = '/* FILL-TABLE v2 */'

FN = r'''function renderFillTable(field, values, date, taskId) {
  const cols = field.columns || [];
  const prefix = field.key + '.';
  let used = 0;
  for (const k of Object.keys(values)) {
    if (!k.startsWith(prefix) || !values[k]) continue;
    const r = parseInt(k.slice(prefix.length), 10);
    if (r >= 0) used = Math.max(used, r + 1);
  }
  const fixed = field.fixed || null;
  const n = fixed ? fixed.length : Math.max(field.rows || 5, used + 1);
  const cell = (r, c) => `<td><textarea rows="1" aria-label="${esc(cols[c] + ' ' + (r + 1) + '행')}" data-task-record="${esc(taskId)}" data-record-date="${esc(date)}" data-record-field="${esc(prefix + r + '.' + c)}">${esc(values[prefix + r + '.' + c] ?? '')}</textarea></td>`;
  const row = r => `<tr><th scope="row" class="ft-num">${r + 1}</th>${cols.map((_, c) => fixed && c === 0 ? `<td class="ft-fixed">${esc(fixed[r])}</td>` : cell(r, c)).join('')}</tr>`;
  return `<div class="fill-table-wrap" data-ft-cols="${cols.length}">
    <div class="ft-head"><strong>${esc(field.label)}</strong>${field.tip ? `<p class="ft-tip">${esc(field.tip)}</p>` : ''}${cols.length >= 4 ? '<p class="ft-scroll-hint">열이 화면보다 넓으면 표를 옆으로 밀어 보세요 →</p>' : ''}</div>
    <div class="ft-scroll"><table class="fill-table" style="min-width:${Math.max(480, cols.length * 128 + 48)}px">
    <thead><tr><th scope="col" class="ft-num">#</th>${cols.map(c => `<th scope="col">${esc(c)}</th>`).join('')}</tr></thead>
    <tbody><tr class="ft-example"><th scope="row" class="ft-num">예시</th>${(field.example || []).map(v => `<td>${esc(v)}</td>`).join('')}</tr>
    ${Array.from({length: n}, (_, r) => row(r)).join('')}</tbody></table></div>
    ${fixed ? '' : '<button type="button" class="ft-add" data-ft-add>+ 줄 추가</button>'}</div>`;
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
  next.querySelectorAll('textarea').forEach(t => {
    t.value = ''; t.style.height = ''; delete t.dataset.grown;
    t.dataset.recordField = t.dataset.recordField.replace(/\.\d+\.(\d+)$/, '.' + r + '.$1');
    t.setAttribute('aria-label', t.getAttribute('aria-label').replace(/\d+행$/, (r + 1) + '행'));
  });
  body.appendChild(next);
  next.querySelector('textarea')?.focus();
});
'''

def patch(js):
    if MARK in js: return js
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

def strip_v1(js):
    """v1 패치를 걷어내고 원래 코드로 되돌린다(v2를 다시 넣기 위해)."""
    a = js.index('function renderFillTable('); b = js.index('function renderTaskRecord(')
    js = js[:a] + js[b:]
    js = js.replace("  const fillTables = fields.filter(f => f.kind === 'table').map(f => renderFillTable(f, values, date, taskId)).join('');\n  fields = fields.filter(f => f.kind !== 'table');\n  if (!fields.length) return fillTables;\n", '')
    js = js.replace('return fillTables + `<div class="task-record stack-sm">${checkTable}', 'return `<div class="task-record stack-sm">${checkTable}')
    i = js.index('if (sections.general || sections.output) return content'); k = js.index("</details>` : '');", i) + len("</details>` : '');")
    js = js[:i] + 'if (sections.general) return content + `<details class="task-record"><summary>이 과제의 확인·수정 기록</summary>${renderSection(sections.general)}</details>`;' + js[k:]
    js = js[:js.index('\n/* FILL-TABLE v1 */')]
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
