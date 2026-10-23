/* The complete cohorts behind this one set's comparison. No spatial inference. */
(() => {
  'use strict';
  const $ = selector => document.querySelector(selector);
  const data = window.TACTICAL_DATA;
  const ids = {drop: new Set(data.dropIds), sv: new Set(data.serveVolleyIds)};
  const names = {1: 'Djokovic', 2: 'Medvedev'};
  let kind = 'drop', scope = window.tacticalSnapshot().scope;
  const expanded = new Set();
  function element(tag, text, className) {
    const node = document.createElement(tag);
    if (text !== undefined) node.textContent = text;
    if (className) node.className = className;
    return node;
  }
  function classify(record) {
    // A faulted first serve is not the counted serve. c is a let, not a stroke.
    const code = (record['2nd'] || record['1st']).replace(/^c+/, '');
    const strokes = code.match(/[fbrsvzopuylmhijktq][^fbrsvzopuylmhijktq]*/g) || [];
    const shots = strokes.map((token, index) => ({token, actor: index % 2 ? +record.Svr : 3 - +record.Svr}));
    const ownDrop = shots.findIndex(shot => shot.actor === 1 && /^[uy]/.test(shot.token));
    return {code, shots, ownDrop};
  }
  function inclusion(record) {
    const {shots, ownDrop} = classify(record);
    const p = element('p');
    if (kind === 'sv') {
      p.append('Djokovic comes forward behind his serve. An approach counts even if a missed return means he never has to volley.');
    } else {
      const drop = shots[ownDrop];
      p.append('Djokovic plays a ', drop.token[0] === 'u' ? 'forehand' : 'backhand', ' drop shot. ');
      if (shots.slice(0, ownDrop).some(shot => shot.actor === 2 && /^[uy]/.test(shot.token))) {
        p.append('Medvedev plays a drop shot first: Djokovic’s reply is a counter-drop. ');
      }
      p.append(ownDrop < shots.length - 1 ? 'The rally continues after it.' : 'The drop shot ends this point.');
    }
    return p;
  }
  function render() {
    const records = data.records.filter(r => ids[kind].has(+r.Pt) && (scope === 'all' || +r.Svr === 1));
    const won = records.filter(r => +r.PtWinner === 1).length;
    $('#ledger-result').textContent = `${won} of ${records.length} points won by Djokovic${scope === 'serve' || kind === 'sv' ? ' · on his serve' : ' · whole second set'}.`;
    $('#ledger-definition').textContent = kind === 'drop'
      ? 'Points containing his drop shot; the rally may continue afterward. Open a point to see what happened.'
      : 'Points where he follows his serve forward, whether or not a volley follows. Open a point to see what happened.';
    document.querySelectorAll('[data-ledger-kind]').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.ledgerKind === kind)));
    document.querySelectorAll('[data-ledger-scope]').forEach(button => {button.setAttribute('aria-pressed', String(button.dataset.ledgerScope === scope));button.hidden = button.dataset.ledgerScope === scope;});
    const fragment = document.createDocumentFragment();
    for (const r of records) {
      const details = element('details'); details.dataset.sourcePoint = r.Pt;
      details.open = expanded.has(r.Pt);
      details.addEventListener('toggle', () => {if (details.open) expanded.add(r.Pt); else expanded.delete(r.Pt);});
      const scores = r.Pts.split('-'); if (+r.Svr === 2) scores.reverse();
      const summary = element('summary');
      summary.append(element('span', r.Pt, 'ledger-id'), element('span', `${r.Gm1}–${r.Gm2}`), element('span', scores.join('–')), element('span', names[r.PtWinner], +r.PtWinner === 1 ? 'ledger-won' : 'ledger-lost'));
      summary.setAttribute('aria-label', `Source point ${r.Pt}. Before: games ${r.Gm1}–${r.Gm2}, points ${scores.join('–')}, Djokovic / Medvedev. ${names[r.Svr]} serving. ${names[r.PtWinner]} won. Inspect inclusion and original record.`);
      const body = element('div', undefined, 'ledger-record');
      body.append(element('p', `${names[r.Svr]} serving · ${names[r.PtWinner]} won the point.`), inclusion(r));
      const original = element('dl');
      for (const [key, value] of Object.entries(r)) {
        const pair = element('div');
        if (['1st', '2nd', 'Notes', 'match_id'].includes(key)) pair.className = 'ledger-code';
        const dd = element('dd'); dd.append(element('code', value || '(empty)'));
        pair.append(element('dt', key), dd); original.append(pair);
      }
      const source = element('details', undefined, 'ledger-original');
      source.open = expanded.has('original-' + r.Pt);
      source.addEventListener('toggle', () => {if (source.open) expanded.add('original-' + r.Pt); else expanded.delete('original-' + r.Pt);});
      const classification = classify(r);
      const proof = kind === 'sv' ? 'Counted serve: ' + classification.code.match(/^[456]\+/)[0] + '. The + marks the approach.' : 'His drop-shot fragment: ' + classification.shots[classification.ownDrop].token + '. u = forehand drop shot; y = backhand drop shot.';
      source.append(element('summary', 'Inspect charting codes and original record'), element('p', proof), element('p', 'Pts is server / returner order; empty fields are shown explicitly.', 'ledger-original-label'), original);
      body.append(source);
      details.append(summary, body); fragment.append(details);
    }
    $('#ledger-points').replaceChildren(fragment);
  }
  document.querySelectorAll('[data-ledger-kind]').forEach(button => button.addEventListener('click', () => {kind = button.dataset.ledgerKind;render();}));
  document.querySelectorAll('[data-ledger-scope]').forEach(button => button.addEventListener('click', () => {document.dispatchEvent(new CustomEvent('comparison-scope-request', {detail:button.dataset.ledgerScope}));document.querySelector('[data-ledger-scope]:not([hidden])').focus({preventScroll:true});}));
  document.addEventListener('comparison-scope', event => {if (scope === event.detail) return;scope = event.detail;render();});
  render();
})();
