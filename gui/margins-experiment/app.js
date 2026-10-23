/* Disposable experiment: can a conserved point ledger sharpen an expert's reading?
   No model, simulated time, persistence, or live data. Original records in records.js. */
(() => {
  'use strict';
  const $ = s => document.querySelector(s);
  const $$ = s => [...document.querySelectorAll(s)];
  const raw = window.MARGINS_RECORDS;
  const names = ['Roger Federer', 'Novak Djokovic'];
  const rows = raw.map(r => Object.freeze({raw:r,id:+r.Pt,winner:+r.PtWinner,server:+r.Svr,set:1+(+r.Set1)+(+r.Set2),tb:(+r.Gm1 === +r.Gm2)&&(+r.Gm1 === ((+r.Set1)+(+r.Set2)===4?12:6))}));
  const subsets = {all:rows,set2:rows.filter(r=>r.set===2),tb:rows.filter(r=>r.tb),rest:rows.filter(r=>r.set!==2&&!r.tb),other:rows.filter(r=>r.set!==2)};
  const subsetNames = {all:'All points',set2:'Set two',tb:'Three tiebreaks',rest:'Neither set two nor a tiebreak',other:'Other four sets'};
  for(const s of [1,3,4,5]){subsets['set'+s]=rows.filter(r=>r.set===s);subsetNames['set'+s]='Set '+s;}
  const stats = a => ({n:a.length,f:a.filter(r=>r.winner===1).length,d:a.filter(r=>r.winner===2).length});
  const signed = n => n>0?'+'+n:n<0?'−'+Math.abs(n):'0';
  const state = {chapter:0,filter:'all',point:1,moving:false,paused:false,reduceOverride:false};
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const reduceMotion=()=>reduced.matches||state.reduceOverride;
  const chapters = [
    {title:'FOURTEEN<br><em>AHEAD.</em>',deck:'He won more points.<br>He lost the final.',copy:'Federer finished 218–204 ahead. But where, exactly, did that advantage accumulate?',aside:'A closer reading. About 80 seconds, at your pace.',next:'Trace the margin',label:'Full-match total'},
    {title:'FIVE SETS.<br><em>ONE SURPLUS.</em>',long:true,deck:'The advantage wasn’t<br>spread evenly.',copy:'Read each set’s contribution. Federer’s margins were −5, +14, +1, +5 and −1. The other four net to zero.',aside:'Signed margins are Federer’s points minus Djokovic’s. They are not a measure of playing quality.',next:'Hold set two apart',label:'Five set contributions'},
    {title:'ALL FOURTEEN.<br><em>IN 38 POINTS.</em>',long:true,deck:'One set holds the<br>entire net surplus.',copy:'Set two: 26–12. The other four sets, taken together: 192–192. All 422 points are still here.',aside:'<strong>This is a partition, not a match without set two.</strong> That set was real, and it counted.',next:'Keep set two. Split the rest',label:'Set two held apart'},
    {title:'EVEN.<br><em>NOT UNIFORM.</em>',long:true,deck:'192–192 in four sets.<br>Opposing margins underneath.',copy:'Set two stays. Split only the other four sets: 12–21 in the tiebreaks, 180–171 outside them. Those −9 and +9 margins cancel.',aside:'Set two counted. Federer also won more games: <strong>36–32.</strong> Equal aggregate points do not establish equal quality.',next:'Read the verdict',label:'A complete, disjoint partition'},
    {title:'REAL.<br><em>CONCENTRATED.</em>',long:true,deck:'The total is true.<br>The inference needs care.',copy:'Federer’s point advantage was real and concentrated. The full-match total alone does not establish sustained dominance.',aside:'No verdict on deservedness, nerves or intent. Inspect the evidence—and the limits—below.',next:'Inspect the evidence',label:'The bounded verdict'}
  ];
  let width = 0, height = 0, positions = new Map(), motion = null, epoch = 0, labelChapter=0;
  const nodes = new Map(), ns='http://www.w3.org/2000/svg';
  for (const r of rows) {
    const node=document.createElementNS(ns,r.winner===1?'circle':'rect');
    if(r.winner===1) node.setAttribute('r','3');
    else {const side=Math.sqrt(Math.PI*9);node.setAttribute('x',-side/2);node.setAttribute('y',-side/2);node.setAttribute('width',side);node.setAttribute('height',side);}
    node.setAttribute('class','point '+(r.winner===2?'dj':'fed'));
    node.dataset.id=r.id;node.dataset.winner=r.winner;
    $('#marks').append(node);nodes.set(r.id,node);
  }

  function groups(chapter) {
    if(chapter===0) return [{name:'All points',records:rows,filter:'all'}];
    if(chapter===1) return [1,2,3,4,5].map((s,i)=>({name:'Set '+s,records:rows.filter(r=>r.set===s),score:['6–7','6–1','6–7','6–4','12–13'][i],filter:'set'+s,accent:s===2}));
    if(chapter===2) return [{name:'Set two',records:subsets.set2,filter:'set2',accent:true},{name:'Other four sets',records:rows.filter(r=>r.set!==2),filter:'other'}];
    return [{name:'Set two',records:subsets.set2,filter:'set2',accent:true},{name:'Three tiebreaks',records:subsets.tb,filter:'tb'},{name:'Other points in those sets',records:subsets.rest,filter:'rest'}];
  }
  function layout(chapter) {
    const w=$('.visual-wrap').clientWidth;
    const gap=w<400?22:36, lane=(w-gap)/2, coords=new Map(), gs=groups(chapter);
    let y=chapter===0?20:0;
    const labels=[];
    for(const g of gs){
      const st=stats(g.records), count=Math.max(st.f,st.d);
      const pitch=chapter===0?Math.min(14,lane/Math.max(1,Math.floor(lane/12))):Math.min(9,lane/Math.max(1,Math.floor(lane/8)));
      const cols=Math.max(1,Math.floor((lane-10)/pitch));
      const labelHeight=chapter===0?0:chapter===2&&g.filter==='other'?145:75;
      const labelY=y, base=y+labelHeight;
      for(const winner of [1,2]){
        g.records.filter(r=>r.winner===winner).forEach((r,i)=>coords.set(r.id,{x:5+(winner-1)*(lane+gap)+(i%cols)*pitch,y:base+Math.floor(i/cols)*pitch}));
      }
      const blockH=Math.ceil(count/cols)*pitch;
      const extent=labelHeight+blockH;
      labels.push({...g,...st,y:labelY,h:extent});
      y+=extent+(chapter===1?25:g.filter==='set2'&&chapter>=2?43:38);
    }
    const h=Math.max(chapter===0?(w<400?260:285):0,y+5);
    return {w,h,coords,labels};
  }
  function transform(p){return `translate(${p.x}px, ${p.y}px)`;}
  function readPositions(){
    if(!motion)return new Map(positions);
    return new Map(rows.map(r=>{const m=new DOMMatrixReadOnly(getComputedStyle(nodes.get(r.id)).transform);return [r.id,{x:m.e,y:m.f}];}));
  }
  function cancelMotion(){
    if(motion){for(const a of motion.animations){a.onfinish=null;a.cancel();}motion=null;}
    state.moving=false;state.paused=false;
    $('#transfer-frame').setAttribute('visibility','hidden');
  }
  function drawLabels(l,chapter){
    labelChapter=chapter;
    $('#evidence-stage').dataset.phase=chapter;
    const container=$('#group-labels'),active=document.activeElement;
    const focusedKey=container.contains(active)?active.dataset.group:null;
    const restoreFocus=()=>{if(focusedKey){const same=[...container.querySelectorAll('button')].find(b=>b.dataset.group===focusedKey);(same||$('#next')).focus({preventScroll:true});}};
    container.replaceChildren();
    if(chapter===0){restoreFocus();return;}
    for(const g of l.labels){
      const el=document.createElement('div');el.className='group-label'+(g.accent?' accent':'');el.dataset.group=g.filter;el.style.top=g.y+'px';el.style.height=g.h+'px';
      const sample=g.score?`${g.n}/422 points · games ${g.score} (F/D)`:`${g.n}/422 points`;
      el.innerHTML=`<div><button class="group-name" type="button">${g.name}</button><span class="group-sample">${sample}</span></div><span class="group-margin">${signed(g.f-g.d)}</span><div class="group-counts"><span>Federer <b>${g.f}</b></span><span>Djokovic <b>${g.d}</b></span></div>`;
      const button=el.querySelector('button');
      button.dataset.group=g.filter||g.name;
      button.setAttribute('aria-label',`${g.name}: ${g.n} points; Federer ${g.f}, Djokovic ${g.d}; Federer margin ${signed(g.f-g.d)}. Inspect records.`);
      button.addEventListener('click',()=>{
        if(g.filter)selectFilter(g.filter);
        else {selectFilter('all');pinPoint(g.records[0].id);}
        $('#inspection').scrollIntoView({block:'start',behavior:'instant'});
        $('#point-number').focus({preventScroll:true});
      });container.append(el);
    }
    restoreFocus();
  }
  function updateChapter(){
    const c=chapters[state.chapter];
    $('#chapter-title').innerHTML=c.title;$('#chapter-title').classList.toggle('long-title',!!c.long);
    $('#chapter-title').classList.toggle('verdict-title',state.chapter===4);
    $('#chapter-title').classList.toggle('concentration-title',state.chapter===2);
    $('#chapter-deck').innerHTML=c.deck;$('#chapter-copy').textContent=c.copy;$('#chapter-aside').innerHTML=c.aside;
    $('#next').firstChild.textContent=c.next+' ';
    $('#back').disabled=state.chapter===0;
    $('#replay').disabled=state.chapter===0;
    $$('.chapter-track button').forEach((b,i)=>{if(i===state.chapter)b.setAttribute('aria-current','step');else b.removeAttribute('aria-current');});
    $('#ledger-title').textContent='All 422 recorded points: '+c.label;
    $('#ledger-description').textContent=groups(state.chapter).map(g=>{const s=stats(g.records);return `${g.name}: ${s.n} of 422 points, Federer ${s.f}, Djokovic ${s.d}.`;}).join(' ');
  }
  function updateStatus(){
    const active=document.activeElement,restorePlaybackFocus=active===$('#pause')&&!state.moving;
    const activeGroup=active.closest&&active.closest('#group-labels');
    $('#evidence-stage').classList.toggle('is-moving',state.moving);
    $('#evidence-stage').classList.toggle('is-unfolding',!!(motion&&motion.unfolding));
    $('#arrangement').textContent=state.moving?(state.paused?'Paused · same 422 points':'Moving to: '+chapters[state.chapter].label):chapters[state.chapter].label;
    $('#pause').disabled=!state.moving;$('#pause').textContent=state.paused?'Resume':'Pause';
    $('#stage-caption').textContent=state.chapter===2?'Set two: IDs 88–125. Held apart, never removed.':state.chapter>=3?'Other four sets: (12 − 21) + (180 − 171) = −9 + 9 = 0. Set two stays +14.':'One mark = one point. Ordered by point ID within each winner’s group.';
    if(state.moving)$('#stage-caption').textContent=motion&&motion.unfolding?'Set two stays fixed: IDs 88–125. Only the other 384 points rearrange.':'Same 422 records. Departure counts stay above.'+($('#transfer-frame').getAttribute('visibility')==='visible'?' The bracket follows the 38 points of set two.':'');
    $('#transition-status').textContent=state.moving?(state.paused?'Rearrangement paused.':'Rearranging the same 422 records.'):$('#ledger-description').textContent;
    if(restorePlaybackFocus)($('#replay').disabled?$('#next'):$('#replay')).focus({preventScroll:true});
    else if(state.moving&&activeGroup)$('#pause').focus({preventScroll:true});
  }
  function showDeparture(unfolding){
    const panel=$('#departure-context'),gs=groups(labelChapter);
    panel.replaceChildren();const heading=document.createElement('p');heading.textContent='Departure: '+chapters[labelChapter].label+' · F / D';panel.append(heading);
    const table=document.createElement('div');table.className='departure-groups';table.style.gridTemplateColumns=`repeat(${gs.length},minmax(0,1fr))`;
    for(const g of gs){const s=stats(g.records),cell=document.createElement('div');if(g.records===subsets.set2||g.filter==='set2')cell.className='departure-selected';cell.innerHTML=`<strong>${g.name}</strong><span>${s.n}/422</span><span>${s.f} / ${s.d}</span><b>${signed(s.f-s.d)}</b>`;table.append(cell);}panel.append(table);
    if(state.chapter===2||labelChapter===2){const label=document.createElement('p');label.className='departure-ids';label.textContent=(unfolding?'Set two held fixed':'Moving bracket: set two')+' · IDs 88–125';panel.append(label);}
  }
  function settle(token){
    if(!motion||motion.token!==token)return;
    const target=motion.target,viewportY=window.scrollY;
    const l=layout(target);
    cancelMotion();positions=l.coords;width=l.w;height=l.h;
    for(const [id,p]of positions)nodes.get(id).style.transform=transform(p);
    $('.visual-wrap').style.height=l.h+'px';$('#ledger').setAttribute('viewBox',`0 0 ${l.w} ${l.h}`);
    drawLabels(l,target);updateHalo();updateStatus();
    // Some embedded engines adjust scroll by the document-height reduction.
    // Preserve the reader’s current position, including any deliberate scroll during travel.
    if(innerWidth<=760)window.scrollTo({top:viewportY,behavior:'instant'});
  }
  function go(chapter,{instant=false}={}){
    chapter=Math.max(0,Math.min(4,chapter));
    if(motion&&motion.reversible&&(chapter===motion.startChapter||chapter===motion.endChapter)&&chapter!==state.chapter&&!instant&&!reduceMotion()){
      motion.target=chapter;state.chapter=chapter;
      const rate=chapter===motion.endChapter?1:-1;
      for(const a of motion.animations){a.updatePlaybackRate(rate);a.play();}
      state.paused=false;updateChapter();updateStatus();return;
    }
    const previous=state.chapter,wasMoving=!!motion,from=readPositions();
    cancelMotion();const token=++epoch;state.chapter=chapter;
    updateChapter();const l=layout(chapter);width=l.w;height=l.h;
    const stageH=(instant||reduceMotion()||!from.size||chapter===previous)?l.h:Math.max($('.visual-wrap').clientHeight,l.h);
    $('.visual-wrap').style.height=stageH+'px';$('#ledger').setAttribute('viewBox',`0 0 ${l.w} ${stageH}`);
    if(instant||reduceMotion()||!from.size||chapter===previous){
      positions=l.coords;for(const[id,p]of positions)nodes.get(id).style.transform=transform(p);drawLabels(l,chapter);updateHalo();updateStatus();return;
    }
    const unfolding=!wasMoving&&((previous===2&&chapter===3)||(previous===3&&chapter===2));
    state.moving=true;showDeparture(unfolding);const animations=[],duration=chapter===1?880:800;
    const same=(a,b)=>Math.abs(a.x-b.x)<.01&&Math.abs(a.y-b.y)<.01;
    const start=document.timeline.currentTime;
    for(const r of rows){const node=nodes.get(r.id);if(same(from.get(r.id),l.coords.get(r.id))){node.style.transform=transform(l.coords.get(r.id));continue;}const a=node.animate([{transform:transform(from.get(r.id))},{transform:transform(l.coords.get(r.id))}],{duration,easing:'cubic-bezier(.77,0,.175,1)',fill:'both'});a.startTime=start;animations.push(a);}
    const halo=$('#point-halo'),hp=from.get(state.point),ht=l.coords.get(state.point);
    if(!same(hp,ht)){const ha=halo.animate([{transform:transform(hp)},{transform:transform(ht)}],{duration,easing:'cubic-bezier(.77,0,.175,1)',fill:'both'});ha.startTime=start;animations.push(ha);}
    if((chapter===2||previous===2)&&!unfolding){
      const box=coords=>{const pts=subsets.set2.map(r=>coords.get(r.id)),xs=pts.map(p=>p.x),ys=pts.map(p=>p.y);return{x:Math.min(...xs)-7,y:Math.min(...ys)-7,w:Math.max(...xs)-Math.min(...xs)+14,h:Math.max(...ys)-Math.min(...ys)+14};};
      const source=box(from),destination=box(l.coords);
      const rect=$('#transfer-frame');rect.setAttribute('visibility','visible');
      const frameTransform=b=>`translate(${b.x}px, ${b.y}px) scale(${b.w}, ${b.h})`;
      const fa=rect.animate([{transform:frameTransform(source)},{transform:frameTransform(destination)}],{duration,easing:'cubic-bezier(.77,0,.175,1)',fill:'both'});fa.startTime=start;animations.push(fa);
    }
    motion={token,target:chapter,animations,startChapter:previous,endChapter:chapter,reversible:!wasMoving,unfolding};
    if(!animations.length){settle(token);return;}
    animations[0].onfinish=()=>settle(token);updateStatus();
  }
  function updateHalo(){const p=positions.get(state.point);if(p){$('#point-halo').style.transform=transform(p);$('#point-halo').setAttribute('visibility','visible');}}
  function filterRows(){return subsets[state.filter]||rows;}
  function normalizeScore(r){const parts=r.raw.Pts.split('-');return r.server===1?parts:[parts[1],parts[0]];}
  function renderRecord(){
    const r=rows[state.point-1],rr=r.raw,sel=filterRows(),st=stats(sel),score=normalizeScore(r);
    $('#point-number').value=r.id;$('#record-position').textContent=`${sel.findIndex(p=>p.id===r.id)+1} of ${sel.length} in selection`;
    $('#subset-line').textContent=`${subsetNames[state.filter]} · ${st.n}/422 · Federer ${st.f} / Djokovic ${st.d}`;
    const note=(r.id===359||r.id===360)?'Championship point for Federer. Outside the tiebreaks.':r.id===81?'A score-orientation check: Djokovic serves at 3–2.':r.tb?'Tiebreak point. This is score context, not a pressure rating.':`Set ${r.set} · ${r.set===2?'part of the 38-point second set':'outside the second set'}`;
    $('#record-detail').innerHTML=`<p class="record-callout">${note}</p><div class="record-state"><dl><dt>Before point ${r.id} · Federer / Djokovic</dt><dd class="record-score">${score[0]} – ${score[1]}</dd></dl><dl><dt>Completed sets · games in this set</dt><dd>${rr.Set1}–${rr.Set2} sets<br>${rr.Gm1}–${rr.Gm2} games</dd></dl></div><div class="record-meta"><span>Serving <strong>${names[r.server-1]}</strong></span><span>Won by <strong>${names[r.winner-1]}</strong></span></div>`;
    const dl=document.createElement('dl');dl.className='raw-fields';
    for(const[key,value]of Object.entries(rr)){const cell=document.createElement('div'),dt=document.createElement('dt'),dd=document.createElement('dd');dt.textContent=key;dd.textContent=value||'(empty)';cell.append(dt,dd);dl.append(cell);}
    $('#raw-record').replaceChildren(dl);
    $('#prev-point').disabled=sel[0].id===r.id;$('#next-point').disabled=sel.at(-1).id===r.id;
    updateHalo();
  }
  function highlight(){const ids=new Set(filterRows().map(r=>r.id));for(const[id,node]of nodes){const selected=ids.has(id);node.classList.toggle('is-muted',!selected);node.classList.toggle('is-selected',selected);node.dataset.selected=String(selected);}}
  function selectFilter(filter){
    if(motion)settle(motion.token);
    state.filter=filter;if(!filterRows().some(r=>r.id===state.point))state.point=filterRows()[0].id;
    $$('#filters button').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.filter===filter)));
    highlight();renderRecord();
  }
  function pinPoint(id){
    if(motion)settle(motion.token);
    if(!Number.isInteger(id)||id<1||id>422){$('#point-number').value=state.point;return;}
    if(!filterRows().some(r=>r.id===id)){state.filter='all';$$('#filters button').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.filter==='all')));highlight();}
    state.point=id;renderRecord();
  }
  function stepPoint(delta){const a=filterRows(),i=a.findIndex(r=>r.id===state.point);pinPoint(a[Math.max(0,Math.min(a.length-1,i+delta))].id);}
  function returnToPhoneFocalPoint(){if(innerWidth>760)return false;const evidence=state.chapter===2||state.chapter===3;const target=evidence?$('#evidence-stage'):$('#sequence');window.scrollTo({top:window.scrollY+target.getBoundingClientRect().top,behavior:'instant'});(evidence?$('#arrangement'):$('#chapter-title')).focus({preventScroll:true});return true;}
  $('#next').addEventListener('click',()=>{if(state.chapter===4){$('#inspection').scrollIntoView({block:'start',behavior:'instant'});$('#point-number').focus({preventScroll:true});}else {go(state.chapter+1);returnToPhoneFocalPoint();}});
  $('#back').addEventListener('click',()=>{go(state.chapter-1);if(!returnToPhoneFocalPoint()&&state.chapter===0)$('#next').focus({preventScroll:true});});
  $$('.chapter-track button').forEach(b=>b.addEventListener('click',()=>go(+b.dataset.chapter)));
  function pauseAll(){if(!motion)return;const held=motion.animations[0].currentTime;for(const a of motion.animations){a.pause();a.currentTime=held;}state.paused=true;updateStatus();}
  $('#pause').addEventListener('click',()=>{if(!motion)return;if(!state.paused)pauseAll();else{state.paused=false;for(const a of motion.animations)a.play();updateStatus();}});
  $('#replay').addEventListener('click',()=>{const target=state.chapter;go(Math.max(0,target-1),{instant:true});go(target);});
  $$('#filters button').forEach(b=>b.addEventListener('click',()=>selectFilter(b.dataset.filter)));
  $$('[data-point]').forEach(b=>b.addEventListener('click',()=>pinPoint(+b.dataset.point)));
  $('#restore').addEventListener('click',()=>selectFilter('all'));
  $('#point-number').addEventListener('change',e=>pinPoint(+e.target.value));
  $('#prev-point').addEventListener('click',()=>stepPoint(-1));$('#next-point').addEventListener('click',()=>stepPoint(1));
  $('#record-detail').setAttribute('tabindex','0');$('#record-detail').setAttribute('aria-label','Selected point details. Use left and right arrows to step through selected records.');
  $('#record-detail').addEventListener('keydown',e=>{if(e.key==='ArrowLeft'||e.key==='ArrowRight'){e.preventDefault();stepPoint(e.key==='ArrowRight'?1:-1);}if(e.key==='Escape')$('#point-number').focus();});
  $('#ledger').addEventListener('click',e=>{const node=e.target.closest('.point');if(node){pinPoint(+node.dataset.id);$('#inspection').scrollIntoView({block:'start',behavior:'instant'});}});
  let resizeTimer,mobileOrder=null;
  function orderForViewport(){const mobile=innerWidth<=760;if(mobile===mobileOrder)return;mobileOrder=mobile;const active=document.activeElement;for(const selector of ['#chapter-copy','#chapter-aside','.story-actions'])(mobile?$('#sequence'):$('.story')).append($(selector));if(active&&active!==document.body)active.focus({preventScroll:true});}
  const reflow=()=>{if(Math.abs($('.visual-wrap').clientWidth-width)<1)return;orderForViewport();const id=state.point;go(state.chapter,{instant:true});state.point=id;renderRecord();};
  window.addEventListener('resize',()=>{clearTimeout(resizeTimer);resizeTimer=setTimeout(reflow,80);});
  reduced.addEventListener('change',()=>{if(motion)settle(motion.token);});
  $('#motion-setting').addEventListener('click',()=>{state.reduceOverride=!state.reduceOverride;$('#motion-setting').setAttribute('aria-pressed',String(state.reduceOverride));$('#motion-setting').textContent=state.reduceOverride?'Motion reduced':'Reduce motion';document.body.classList.toggle('motion-reduced',state.reduceOverride);if(motion)settle(motion.token);});
  document.addEventListener('visibilitychange',()=>{if(document.hidden&&motion)pauseAll();});
  orderForViewport();go(0,{instant:true});selectFilter('all');
  // Read-only diagnostics for the disposable experiment; no test navigation API.
  window.marginsSnapshot=()=>({state:{...state},reducedMotion:reduceMotion(),width,height,records:rows.map(r=>({id:r.id,winner:r.winner,set:r.set,tb:r.tb})),groups:groups(state.chapter).map(g=>({name:g.name,ids:g.records.map(r=>r.id),...stats(g.records)})),selected:filterRows().map(r=>r.id),positions:[...readPositions()].map(([id,p])=>({id,...p})),animations:document.getAnimations().length});
})();
