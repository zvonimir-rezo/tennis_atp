/* Disposable US Open 2023 case. Explicit source IDs, no reusable case engine. */
(() => {
  'use strict';
  const $ = s => document.querySelector(s), $$ = s => [...document.querySelectorAll(s)];
  const raw = window.TACTICAL_DATA.records;
  const sv = new Set(window.TACTICAL_DATA.serveVolleyIds), drops = new Set(window.TACTICAL_DATA.dropIds);
  const rows = raw.map(r => ({id:+r.Pt, winner:+r.PtWinner, server:+r.Svr, raw:r, kind:sv.has(+r.Pt)?'sv':drops.has(+r.Pt)?'drop':'other'}));
  const game = rows.filter(r => r.id >= 143 && r.id <= 156);
  const reducedQuery = matchMedia('(prefers-reduced-motion: reduce)'), compactQuery=matchMedia('(max-height: 560px), (min-width: 761px) and (max-height: 650px)');
  let override=false, scope='all', pattern='all', selected=7, progress=0, dimensions, queued=false, phase='', scopeTested=false, pendingFocus=null, lastScroll=0, lastPaintProgress=NaN;
  const opened=new Set(), seen=new Set([150]);
  const reduced=()=>override||reducedQuery.matches;
  const staticCourt=()=>reduced()||compactQuery.matches;
  const clamp=(n,a=0,b=1)=>Math.max(a,Math.min(b,n));
  const smooth=n=>{n=clamp(n);return n*n*(3-2*n);};
  const mix=(a,b,t)=>a+(b-a)*t;
  const ns='http://www.w3.org/2000/svg';
  const linework='<rect x="65" y="45" width="720" height="330"/><path d="M65 87h720M65 333h720M280 87v246M570 87v246M280 210h290M425 45v330M61 210h8M781 210h8"/>';
  const slices=[];
  for(let i=0;i<3;i++){
    const slab=document.createElement('div');slab.className='court-slice';slab.style.left=(i*100/3)+'%';
    slab.innerHTML=`<div class="slab-back"></div><div class="slab-face"></div><div class="slab-side"></div><div class="slab-top"><svg class="court-lines" style="left:${-i*100}%" viewBox="0 0 850 420">${linework}</svg><div class="slab-paper"></div></div>`;
    $('#court').append(slab);slices.push({slab,paper:slab.querySelector('.slab-paper'),lines:slab.querySelector('.court-lines')});
  }
  const net=document.createElement('div');net.className='court-net';$('#court').append(net);
  const marks=new Map();
  for(const r of rows){
    const g=document.createElementNS(ns,'g');g.classList.add('point');if(r.winner===2)g.classList.add('lost-point');g.dataset.id=r.id;
    const c=document.createElementNS(ns,'circle');c.setAttribute('r','4');
    const seam=document.createElementNS(ns,'path');seam.setAttribute('d','M-2.5-2.5Q-1 0-2.5 2.5M2.5-2.5Q1 0 2.5 2.5');seam.setAttribute('class','point-seam');
    g.append(c,seam);$('#point-field').append(g);marks.set(r.id,g);
  }
  function activeRows(){return scope==='serve'?rows.filter(r=>r.server===1):rows;}
  function drawEvidence(){
    if(!dimensions)return;
    const {plotW,plotH,mobile}=dimensions, gap=mobile?9:24, colW=(plotW-2*gap)/3;
    const dense=mobile||plotH<360,radius=dense?2.5:5,targetPitch=dense?7.5:17;
    const selectedRows=activeRows(), visible=new Set(selectedRows.map(r=>r.id));
    for(const r of rows){const mark=marks.get(r.id);mark.style.display=visible.has(r.id)?'':'none';mark.classList.toggle('concealed',!opened.has(r.kind));}
    const groups=['sv','drop','other'].map((key,i)=>{const sample=selectedRows.filter(r=>r.kind===key);return {key,i,sample,won:sample.filter(r=>r.winner===1).length,isOpen:opened.has(key),button:$('[data-open="'+key+'"]')};});
    for(const {key,sample,won,isOpen,button} of groups){
      $('#count-'+key).innerHTML=isOpen?`${won}<span class="denominator">/${sample.length}</span>`:`${sample.length}`;
      $('#note-'+key).textContent=isOpen?'Djokovic won':'points';
      $('#action-'+key).textContent=isOpen?'Results open':'Reveal →';
      button.setAttribute('aria-expanded',String(isOpen));
      button.setAttribute('aria-label',(key==='sv'?'Serve and volley':key==='drop'?'Drop-shot points':'Other points')+(isOpen?`: ${won} of ${sample.length} won. Hide results.`:`: ${sample.length} points. Open the results.`));
      button.classList.toggle('is-open',isOpen);
    }
    // Header wrapping and result disclosure determine where marks can begin.
    // Read after the label writes, once per result/scope/resize, never while scrolling.
    const top=Math.ceil(Math.max(...groups.flatMap(({button,isOpen})=>[...button.children].filter(el=>!(isOpen&&el.classList.contains('group-action'))).map(el=>el.offsetTop+el.offsetHeight)))+12);
    for(const {key,i,sample,won,isOpen} of groups){
      if(!isOpen){
        const cols=Math.max(1,Math.floor((colW-(mobile?18:44))/(mobile?8:17))), pitch=mobile?8:17;
        const rowCount=Math.ceil(sample.length/cols), dy=Math.min(pitch,(plotH-top-12)/Math.max(1,rowCount-1));
        sample.forEach((r,j)=>marks.get(r.id).setAttribute('transform',`translate(${i*(colW+gap)+(mobile?9:22)+radius+(j%cols)*pitch} ${top+radius+Math.floor(j/cols)*dy}) scale(${radius/4})`));
        continue;
      }
      const padding=mobile?9:22, lane=(colW-padding*2-12)/2;
      const cols=Math.max(1,Math.floor((lane-2*radius)/targetPitch)+1);
      const maxRows=Math.ceil(Math.max(won,sample.length-won)/cols);
      const pitch=Math.min(targetPitch,(plotH-top-2*radius-8)/Math.max(1,maxRows-1));
      for(const winner of [1,2])sample.filter(r=>r.winner===winner).forEach((r,j)=>{
        const x=i*(colW+gap)+padding+radius+(winner-1)*(lane+12)+(j%cols)*pitch;
        const y=top+radius+Math.floor(j/cols)*pitch;
        marks.get(r.id).setAttribute('transform',`translate(${x} ${y}) scale(${radius/4})`);
      });
    }
    $('#point-field').setAttribute('viewBox',`0 ${top} ${plotW} ${plotH-top}`);
    $('#point-field').style.top=top+'px';$('#point-field').style.height=(plotH-top)+'px';
    $('#field-desc').textContent=['sv','drop','other'].map(key=>{const a=selectedRows.filter(r=>r.kind===key);return `${key==='sv'?'Serve and volley':key==='drop'?'Own drop-shot points':'Other points'}: ${opened.has(key)?'Djokovic won '+a.filter(r=>r.winner===1).length+' of '+a.length:a.length+' points, results unopened'}.`;}).join(' ')+' One equal ball is one recorded point. Positions are groups, not shot locations.';
    $('#scope-note').textContent=scope==='serve'?'52 service points · 58 return points removed.':'110 points · 58 return points included.';
    $('#scope-comparison').textContent=scopeTested&&opened.has('sv')&&opened.has('drop')?'Drop-shot points: 3/11 overall → 1/5 on serve. Serve & volley stays 11/11.':'';
    $('#pressure-link').hidden=!(opened.has('sv')&&opened.has('drop'));
    document.dispatchEvent(new CustomEvent('comparison-scope',{detail:scope}));
    updateStory();
    $$('.scope button').forEach(b=>{b.setAttribute('aria-pressed',String(b.dataset.scope===scope));b.hidden=b.dataset.scope===scope;});
    $('#scope-question').textContent=scope==='all'?'Could return points explain the gap?':'Removing returns widens the gap.';
  }
  const openingCopy='Come in behind the serve. Or play a drop shot.<br>Two ways forward. Did both work?';
  function updateStory(){
    const both=opened.has('sv')&&opened.has('drop');
    const dropResult=scope==='serve'?'One in five drop-shot points.':'Three in eleven drop-shot points.';
    $('#story-copy').innerHTML=phase==='transition'?'The same set.<br>Three groups of points.':phase==='split'?(both?'Eleven wins behind the serve.<br>'+dropResult:'Two ways to leave the baseline.<br>Open the results. Which one paid off?'):openingCopy;
    $('#stage').classList.toggle('comparison-open',both);
  }
  $$('[data-open]').forEach(b=>b.addEventListener('click',()=>{
    const key=b.dataset.open;
    if(opened.has(key))opened.delete(key);else opened.add(key);
    drawEvidence();
  }));
  const cachedStyle=new WeakMap();
  function style(el,key,value){let c=cachedStyle.get(el);if(!c){c={};cachedStyle.set(el,c);}if(c[key]!==value){c[key]=value;el.style[key]=value;}}
  function paint(){
    queued=false;if(!dimensions)return;
    const d=dimensions;lastScroll=scrollY;
    progress=staticCourt()?1:clamp((scrollY-d.top)/d.travel);
    if(progress===lastPaintProgress&&!pendingFocus)return;
    lastPaintProgress=progress;
    const flat=smooth((progress-.26)/.28),apart=smooth((progress-.1)/.28),show=smooth((progress-.51)/.12);
    const next=show>=.95?'split':progress>.36?'transition':'opening';
    if(next!==phase){phase=next;$('#stage').dataset.phase=phase;updateStory();$$('[data-chapter]').forEach(b=>{if((+b.dataset.chapter===1)===(phase==='split'))b.setAttribute('aria-current','step');else b.removeAttribute('aria-current');});}
    // Editorial type follows the same reversible scroll input as the court.
    const compact=smooth((progress-.08)/.36);
    style($('.story h1'),'transform',`translate3d(0,${mix(d.titleStart,d.titleEnd,compact)-d.titleStart}px,0) scale(${mix(1,d.titleScale,compact)})`);
    // Let the court carry the handoff; copy must not travel through its surface.
    const copyOut=1-smooth((progress-.08)/.08),copyIn=smooth((progress-.44)/.08),copyOpacity=Math.max(copyOut,copyIn);
    style($('#story-copy'),'transform',`translate3d(${progress<.3?0:d.copyX}px,${progress<.3?d.copyStart:d.copyEnd}px,0)`);
    style($('#story-copy'),'opacity',copyOpacity);
    $('#story-copy').setAttribute('aria-hidden',String(copyOpacity<.05));
    style($('#start'),'opacity',1-smooth((progress-.04)/.12));
    $('#start').hidden=progress>.2;
    const scale0=d.opening.scale;
    const sx=mix(scale0,d.plotW/850,flat),sy=mix(scale0,d.plotH/420,flat);
    const cx=mix(d.opening.cx,d.artLeft+d.plotW/2,flat),cy=mix(d.opening.cy,d.artTop+d.plotH/2,flat);
    style($('#camera'),'transform',`translate3d(${cx-425}px,${cy-210}px,0) scale3d(${sx},${sy},${mix(scale0,1,flat)})`);
    style($('#court'),'transform',`rotateX(${mix(57,0,flat)}deg) rotateZ(${mix(-25,0,flat)}deg)`);
    const gap=d.mobile?9:24, column=(d.plotW-2*gap)/3;
    slices.forEach(({slab,paper,lines},i)=>{
      const x=mix((i-1)*40*apart,i*(column+gap)/d.plotW*850-i*850/3,flat);
      style(slab,'transform',`translate3d(${x}px,0,${(i===1?22:3)*apart*(1-flat)}px) scale(${mix(1,column/d.plotW*3,flat)},1)`);
      style(paper,'opacity',flat);style(lines,'opacity',1-flat);
    });
    style(net,'opacity',1-smooth((progress-.12)/.17));style($('#floor-shadow'),'opacity',.24*(1-flat));
    style($('#opening-note'),'opacity',1-smooth((progress-.15)/.12));style($('#evidence'),'opacity',show);style($('#comparison'),'opacity',show);
    style($('#evidence'),'visibility',show<.3?'hidden':'visible');style($('#comparison'),'visibility',show<.3?'hidden':'visible');
    const hidden=show<.95;
    for(const el of [$('#evidence'),$('#comparison')]){el.inert=hidden;el.setAttribute('aria-hidden',String(hidden));}
    $('#stage-caption').textContent=show===1?'Equal court pieces name categories.':'An illustrated hard court. A real point record.';
    if(pendingFocus&&(!hidden||pendingFocus==='start')){const target=pendingFocus==='start'?$('#start'):$('[data-open=sv]');pendingFocus=null;target.focus({preventScroll:true});}
  }
  function requestPaint(){if(!queued){queued=true;requestAnimationFrame(paint);}}
  function openingCourt(box,w,h){
    const rz=-25*Math.PI/180,rx=57*Math.PI/180,vertices=[];
    // Bound the existing slab and the net at its actual editorial offsets.
    const corners=[];
    for(const x of [-425,425])for(const y of [-210,210])for(const z of [-17,0])corners.push({x,y,z});
    for(const y of [-165,165])for(const z of [0,48])corners.push({x:0,y,z});
    for(const {x,y,z} of corners){
      const px=x*Math.cos(rz)-y*Math.sin(rz),py=x*Math.sin(rz)+y*Math.cos(rz);
      vertices.push({x:px,y:py*Math.cos(rx)-z*Math.sin(rx),z:py*Math.sin(rx)+z*Math.cos(rx)});
    }
    let scale=Math.min(box.width/1100,box.height/600),cx=box.x+box.width/2,cy=box.y+box.height/2;
    for(let i=0;i<5;i++){
      const points=vertices.map(p=>{const f=1/(1-scale*p.z/1600);return {x:w/2+(cx+scale*p.x-w/2)*f,y:h/2+(cy+scale*p.y-h/2)*f};});
      const left=Math.min(...points.map(p=>p.x)),right=Math.max(...points.map(p=>p.x)),top=Math.min(...points.map(p=>p.y)),bottom=Math.max(...points.map(p=>p.y));
      scale*=Math.min(box.width/(right-left),box.height/(bottom-top));
      cx+=box.x+box.width/2-(left+right)/2;cy+=box.y+box.height/2-(top+bottom)/2;
    }
    return {scale,cx,cy};
  }
  function resize(){
    document.body.classList.toggle('compact-court',compactQuery.matches);
    const stage=$('#stage').getBoundingClientRect(),art=$('#evidence').getBoundingClientRect(),section=$('#sequence').getBoundingClientRect();
    const mobile=innerWidth<=760,title=$('.story h1'),titleFont=parseFloat(getComputedStyle(title).fontSize),titleStart=stage.height*(mobile?.16:.17),titleEnd=mobile?20:40,titleScale=(mobile?(innerHeight<740?36:48):(innerHeight<741?66:Math.min(96,innerWidth*.062)))/titleFont;
    dimensions={w:innerWidth,h:stage.height,mobile,sectionHeight:section.height,titleStart,titleEnd,titleScale,copyX:mobile?0:stage.width*.522,copyStart:titleStart+title.offsetHeight+(mobile?18:26),copyEnd:mobile?titleEnd+title.offsetHeight*titleScale+8:titleEnd+10,top:scrollY+section.top,travel:Math.max(1,section.height-stage.height),plotW:art.width,plotH:art.height,artLeft:art.left-stage.left,artTop:art.top-stage.top};
    const copyMeasure=$('#story-copy').cloneNode(false);copyMeasure.removeAttribute('id');copyMeasure.setAttribute('aria-hidden','true');copyMeasure.style.visibility='hidden';copyMeasure.style.transform='none';copyMeasure.innerHTML=openingCopy;$('.story').append(copyMeasure);
    const startTop=dimensions.copyStart+copyMeasure.offsetHeight+18,copyWidth=copyMeasure.offsetWidth;copyMeasure.remove();
    const note=$('#opening-note');note.hidden=false;
    note.hidden=mobile||startTop+68>note.getBoundingClientRect().top-stage.top;
    const footerTop=$('.stage-footer').getBoundingClientRect().top-stage.top;
    const objectLeft=Math.max(stage.width*.43,stage.width*.05+copyWidth+24);
    const box=mobile?{x:stage.width*.06,y:startTop+62,width:stage.width*.88,height:Math.max(40,footerTop-20-startTop-62)}:{x:objectLeft,y:stage.height*.24,width:stage.width*.95-objectLeft,height:footerTop-24-stage.height*.24};
    dimensions.opening=openingCourt(box,stage.width,stage.height);
    lastPaintProgress=NaN;
    $('#start').style.top=startTop+'px';
    drawEvidence();paint();
  }
  function go(chapter,behavior='instant'){pendingFocus=chapter?'sv':'start';window.scrollTo({top:dimensions.top+(chapter?1:0)*dimensions.travel,behavior});requestPaint();}
  $('#start').addEventListener('click',event=>go(1,!reduced()&&event.detail>0?'smooth':'instant'));$$('[data-chapter]').forEach(b=>b.addEventListener('click',()=>go(+b.dataset.chapter)));
  $$('[data-scope]').forEach(b=>b.addEventListener('click',()=>{scope=b.dataset.scope;scopeTested=true;drawEvidence();$('.scope button:not([hidden])').focus({preventScroll:true});}));
  document.addEventListener('comparison-scope-request',event=>{
    if(!['all','serve'].includes(event.detail))return;
    scope=event.detail;scopeTested=true;drawEvidence();
  });
  function preference(){
    const initialized=Boolean(dimensions),previousY=lastScroll,previousHeight=dimensions?.sectionHeight||0,previousEnd=(dimensions?.top||0)+previousHeight;
    const within=previousY<(dimensions?.top||0)+previousHeight;
    pendingFocus=null;
    document.body.classList.toggle('motion-reduced',reduced());$('#motion').textContent=reducedQuery.matches?'Motion reduced':override?'Full motion':'Reduce motion';$('#motion').disabled=reducedQuery.matches;$('#motion').setAttribute('aria-pressed',String(override));
    resize();
    if(!initialized)return;
    if(within)window.scrollTo({top:reduced()?dimensions.top:dimensions.top+dimensions.travel,behavior:'instant'});
    else window.scrollTo({top:previousY+dimensions.top+dimensions.sectionHeight-previousEnd,behavior:'instant'});
    requestPaint();
  }
  $('#motion').addEventListener('click',()=>{override=!override;preference();});reducedQuery.addEventListener('change',preference);compactQuery.addEventListener('change',preference);
  addEventListener('scroll',requestPaint,{passive:true});
  for(const type of ['wheel','touchstart'])addEventListener(type,()=>{pendingFocus=null;},{passive:true});
  addEventListener('keydown',event=>{if(event.key==='Escape'&&pendingFocus){pendingFocus=null;window.scrollTo({top:scrollY,behavior:'instant'});}});let resizeFrame;addEventListener('resize',()=>{cancelAnimationFrame(resizeFrame);resizeFrame=requestAnimationFrame(resize);});
  function type(r){return r.kind==='sv'?'Serve & volley':r.kind==='drop'?'Own drop-shot point':[146,148].includes(r.id)?'Double fault':'Other point';}
  const notes={143:'A Djokovic drop shot is part of this rally. Medvedev wins it.',144:'Djokovic wins the next point on a first-serve rally.',145:'An intended serve-and-volley first serve faults. The point continues on a second serve, without that approach code.',146:'A double fault brings Medvedev level at 30–30.',147:'Djokovic follows his serve forward and wins the point.',148:'Another double fault. The game returns to deuce.',149:'Medvedev wins the rally. He now has set point on the next point.',150:'Two backhand volleys. The second, directed down the middle, saves set point.',151:'Djokovic wins a second-serve rally and earns game point.',152:'Medvedev wins the rally. Back to deuce.',153:'A serve-and-volley play draws a missed return. Djokovic has game point again.',154:'Djokovic’s backhand drop shot goes into the net. Another game point goes.',155:'The approach is coded, but no volley follows: Medvedev’s forehand return misses wide.',156:'Medvedev misses the return. Djokovic holds for 6–6; the set goes to a tiebreak.'};
  function rawFields(holder,r){holder.replaceChildren();Object.entries(r.raw).forEach(([k,v])=>{const cell=document.createElement('div');if(['1st','2nd','Notes'].includes(k))cell.className='code-field';const dt=document.createElement('dt'),dd=document.createElement('dd');dt.textContent=k;dd.textContent=v||'(empty)';cell.append(dt,dd);holder.append(cell);});}
  const moments={
    150:{next:154,nextLabel:'And on game point? →'},
    154:{next:155,nextLabel:'What about his next serve? →'},
    155:{next:null,nextLabel:'Read the verdict →'}
  };
  function selectPoint(id){selected=game.findIndex(r=>r.id===id);seen.add(id);renderPoint();}
  const buttons=game.map((r,i)=>{
    const b=document.createElement('button');b.type='button';b.textContent=i+1;b.dataset.id=r.id;
    b.title=`${r.raw.Pts.replace('-','–')} · ${type(r)}`;
    b.setAttribute('aria-label',`Point ${i+1} of this game, source point ${r.id}. Before ${r.raw.Pts.replace('-','–')}. Inspect result`);
    b.addEventListener('click',()=>selectPoint(r.id));$('#point-strip').append(b);return b;
  });
  function renderPoint(){
    const r=game[selected],scores=r.raw.Pts.split('-'),moment=moments[r.id];
    // Other points carry their complete explanation inside the inspection frame.
    $('.game-explanation').hidden=!moment;
    $('#score-dj').textContent=scores[0];$('#score-med').textContent=scores[1];
    $('.scoreboard').classList.toggle('set-point',r.id===150);
    $('#score-status').textContent=r.id===150?'Set point Medvedev · before this point':'Before this point · Djokovic serving';
    $('#point-position').textContent=`Point ${selected+1} of 14 · source ${r.id}`;
    $('#point-type').textContent=type(r);
    $('#point-outcome').textContent=(r.id===150?'He comes in. He wins.':r.id===154?'The drop shot misses.':r.id===155?'No volley needed.':r.id===156?'A hold. A tiebreak.':`${r.winner===1?'Djokovic':'Medvedev'} wins.`);
    $('#point-description').textContent=notes[r.id];
    $('#point-status').textContent=`Source point ${r.id}. ${$('#point-outcome').textContent} ${notes[r.id]}`;
    $('#continue-moment').hidden=!moment;
    $('#continue-moment').textContent=moment?.nextLabel||'';
    $('#game-payoff').hidden=!(r.id===155);
    buttons.forEach((b,i)=>{
      b.setAttribute('aria-pressed',String(i===selected));b.tabIndex=i===selected?0:-1;
      b.classList.toggle('is-dim',pattern!=='all'&&game[i].kind!==pattern);
      if(seen.has(game[i].id))b.dataset.winner=game[i].winner;else delete b.dataset.winner;
    });
    $$('[data-moment]').forEach(b=>{b.setAttribute('aria-pressed',String(+b.dataset.moment===r.id));b.classList.toggle('was-seen',seen.has(+b.dataset.moment));});
    $$('.game-filter button').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.pattern===pattern)));
    $('#previous').disabled=selected===0;$('#next').disabled=selected===game.length-1;
    $('#game-pattern-note').textContent=pattern==='sv'?'Four points, four wins.':pattern==='drop'?'Two points, both lost.':'All fourteen points stay in context.';
    rawFields($('#raw-record'),r);
    window.pressureView?.select(r.id,{type:type(r),description:notes[r.id]});
  }
  $('#continue-moment').addEventListener('click',()=>{
    const next=moments[game[selected].id]?.next;
    if(next){selectPoint(next);$('#shot-view').scrollIntoView({block:'start',behavior:'instant'});$('#shot-view-title').focus({preventScroll:true});}
    else{$('.verdict').scrollIntoView({behavior:'instant'});$('#verdict-title').focus({preventScroll:true});}
  });
  $$('[data-moment]').forEach(b=>b.addEventListener('click',()=>selectPoint(+b.dataset.moment)));
  $('#previous').addEventListener('click',()=>selectPoint(game[Math.max(0,selected-1)].id));
  $('#next').addEventListener('click',()=>selectPoint(game[Math.min(13,selected+1)].id));
  $('#set-point').addEventListener('click',()=>selectPoint(150));
  $$('[data-pattern]').forEach(b=>b.addEventListener('click',()=>{pattern=b.dataset.pattern;renderPoint();}));
  $('#point-strip').addEventListener('keydown',e=>{
    if(!['ArrowRight','ArrowLeft','Home','End'].includes(e.key))return;
    e.preventDefault();
    const next=e.key==='Home'?0:e.key==='End'?13:clamp(selected+(e.key==='ArrowRight'?1:-1),0,13);
    selectPoint(game[next].id);buttons[selected].focus({preventScroll:true});
  });
  const momentButtons=$$('[data-moment]');
  $('.moments').addEventListener('keydown',event=>{
    if(!['ArrowRight','ArrowLeft','Home','End'].includes(event.key))return;
    event.preventDefault();const current=momentButtons.indexOf(document.activeElement);
    const index=event.key==='Home'?0:event.key==='End'?2:clamp(current+(event.key==='ArrowRight'?1:-1),0,2);
    selectPoint(+momentButtons[index].dataset.moment);momentButtons[index].focus({preventScroll:true});
  });
  // Anchor journeys place keyboard focus where the reader has arrived.
  const destinations={'#comparison-records':'#comparison-title','#game':'#game-title','#sources':'#sources-title'};
  document.addEventListener('click',event=>{
    const link=event.target.closest('a[href^="#"]'),heading=link&&destinations[link.hash];
    if(!heading)return;
    const target=$(link.hash);if(!target)return;
    event.preventDefault();
    if(link.matches('.comparison-intro a'))selectPoint(150);
    if(location.hash!==link.hash)history.pushState(null,'',link.hash);
    target.scrollIntoView({block:'start',behavior:'instant'});$(heading).focus({preventScroll:true});
  });
  renderPoint();if(reducedQuery.matches)preference();else resize();
  // Font substitution can change wrapping without a window resize.
  document.fonts.ready.then(()=>requestAnimationFrame(resize));
  // Read-only diagnostic snapshot for this disposable demo's browser checks.
  window.tacticalSnapshot=()=>({scope,scopeTested,pattern,progress,staticCourt:staticCourt(),opened:[...opened],seen:[...seen],reduced:reduced(),selectedPoint:game[selected].id,groups:['sv','drop','other'].map(kind=>{const a=activeRows().filter(r=>r.kind===kind);return {kind,ids:a.map(r=>r.id),won:a.filter(r=>r.winner===1).length};}),gameIds:game.map(r=>r.id),records:raw});
})();
