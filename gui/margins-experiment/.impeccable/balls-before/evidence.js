/* Exact-record inspection. Court geometry is symbolic; these are the frozen MCP records. */
(() => {
  'use strict';
  function init() {
    const $ = selector => document.querySelector(selector);
    const $$ = selector => [...document.querySelectorAll(selector)];
    const names = ['Roger Federer', 'Novak Djokovic'];
    const rows = Object.freeze(window.MARGINS_RECORDS.map(raw => Object.freeze({
      raw, id: Number(raw.Pt), winner: Number(raw.PtWinner), server: Number(raw.Svr),
      set: 1 + Number(raw.Set1) + Number(raw.Set2),
      tb: Number(raw.Gm1) === Number(raw.Gm2) && Number(raw.Gm1) === (Number(raw.Set1) + Number(raw.Set2) === 4 ? 12 : 6)
    })));
    const subsets = {all: rows, set2: rows.filter(r => r.set === 2), tb: rows.filter(r => r.tb), rest: rows.filter(r => r.set !== 2 && !r.tb), other: rows.filter(r => r.set !== 2)};
    const subsetNames = {all: 'All points', set2: 'Set two', tb: 'Three tiebreaks', rest: 'Neither set two nor a tiebreak', other: 'Other four sets'};
    for (let set = 1; set <= 5; set++) { subsets['set' + set] = rows.filter(r => r.set === set); subsetNames['set' + set] = 'Set ' + set; }
    Object.values(subsets).forEach(Object.freeze); Object.freeze(subsets);
    const stats = records => ({n: records.length, f: records.filter(r => r.winner === 1).length, d: records.filter(r => r.winner === 2).length});
    const state = {filter: 'all', point: 1};
    const selectedRows = () => subsets[state.filter];
    const scoreFor = record => { const parts = record.raw.Pts.split('-'); return record.server === 1 ? parts : [parts[1], parts[0]]; };
    function refreshMarks() {
      const ids = new Set(selectedRows().map(record => record.id));
      $$('.point').forEach(node => { const selected = ids.has(Number(node.dataset.id)); node.classList.toggle('is-muted', !selected); node.classList.toggle('is-selected', selected); node.classList.toggle('is-pinned', Number(node.dataset.id) === state.point); node.dataset.selected = String(selected); });
    }
    function render() {
      const record = rows[state.point - 1], raw = record.raw, selected = selectedRows(), totals = stats(selected), score = scoreFor(record);
      $('#point-number').value = record.id;
      $('#record-position').textContent = `${selected.findIndex(r => r.id === record.id) + 1} of ${selected.length} in selection`;
      $('#subset-line').textContent = `${subsetNames[state.filter]} · ${totals.n}/422 · Federer ${totals.f} / Djokovic ${totals.d}`;
      const note = record.id === 359 || record.id === 360 ? 'Championship point for Federer. Outside the tiebreaks.' : record.id === 81 ? 'A score-orientation check: Djokovic serves at 3–2.' : record.tb ? 'Tiebreak point. This is score context, not a pressure rating.' : `Set ${record.set} · ${record.set === 2 ? 'part of the 38-point second set' : 'outside the second set'}`;
      $('#record-detail').innerHTML = `<p class="record-callout">${note}</p><div class="record-state"><dl><dt>Before point ${record.id} · Federer / Djokovic</dt><dd class="record-score">${score[0]} – ${score[1]}</dd></dl><dl><dt>Completed sets · games in this set</dt><dd>${raw.Set1}–${raw.Set2} sets<br>${raw.Gm1}–${raw.Gm2} games</dd></dl></div><div class="record-meta"><span>Serving <strong>${names[record.server - 1]}</strong></span><span>Won by <strong>${names[record.winner - 1]}</strong></span></div>`;
      const dl = document.createElement('dl'); dl.className = 'raw-fields';
      Object.entries(raw).forEach(([key, value]) => { const cell = document.createElement('div'), dt = document.createElement('dt'), dd = document.createElement('dd'); dt.textContent = key; dd.textContent = value === '' ? '(empty)' : String(value); cell.append(dt, dd); dl.append(cell); });
      $('#raw-record').replaceChildren(dl);
      $('#prev-point').disabled = selected[0].id === record.id;
      $('#next-point').disabled = selected.at(-1).id === record.id;
      $$('#filters [data-filter]').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.filter === state.filter)));
      refreshMarks();
      window.MarginsCourt?.selectPoint(record.id);
    }
    function selectFilter(filter) {
      if (!Object.hasOwn(subsets, filter)) return;
      state.filter = filter;
      if (!selectedRows().some(r => r.id === state.point)) state.point = selectedRows()[0].id;
      render();
    }
    function pinPoint(id) {
      if (!Number.isInteger(id) || id < 1 || id > rows.length) { $('#point-number').value = state.point; return; }
      if (!selectedRows().some(r => r.id === id)) state.filter = 'all';
      state.point = id; render();
    }
    function stepPoint(delta) { const selected = selectedRows(), index = selected.findIndex(r => r.id === state.point); pinPoint(selected[Math.max(0, Math.min(selected.length - 1, index + delta))].id); }
    function revealInspector() { $('#inspection').scrollIntoView({block: 'start', behavior: 'instant'}); $('#point-number').focus({preventScroll: true}); }
    $$('#filters [data-filter]').forEach(button => button.addEventListener('click', () => selectFilter(button.dataset.filter)));
    $$('[data-point]').forEach(button => button.addEventListener('click', () => pinPoint(Number(button.dataset.point))));
    $('#restore').addEventListener('click', () => selectFilter('all'));
    $('#point-number').addEventListener('change', event => pinPoint(Number(event.target.value)));
    $('#prev-point').addEventListener('click', () => stepPoint(-1));
    $('#next-point').addEventListener('click', () => stepPoint(1));
    $('#record-detail').tabIndex = 0;
    $('#record-detail').setAttribute('aria-label', 'Selected point details. Use left and right arrows to step through selected records.');
    $('#record-detail').addEventListener('keydown', event => { if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') { event.preventDefault(); stepPoint(event.key === 'ArrowRight' ? 1 : -1); } if (event.key === 'Escape') $('#point-number').focus(); });
    document.addEventListener('click', event => {
      const group = event.target.closest('[data-inspect-filter]');
      if (group) { selectFilter(group.dataset.inspectFilter); revealInspector(); return; }
      const node = event.target.closest('#point-ledger .point');
      if (node) { pinPoint(Number(node.dataset.id)); revealInspector(); }
    });
    window.MarginsEvidence = Object.freeze({rows, subsets, stats, selectFilter, pinPoint, refreshMarks, snapshot: () => ({...state, selected: selectedRows().map(r => r.id)})});
    selectFilter('all');
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, {once: true}); else init();
})();
